# -*- coding: utf-8 -*-
"""
Game Localization Auto-Translator
Dify Workflow API Edition — Python 3.13+

Dify 后台需创建一个「Workflow」应用，工作流包含：
  开始节点（4 个输入变量）→ LLM 节点（翻译 prompt）→ 结束节点
"""

import argparse
import concurrent.futures
import json
import logging
import os
import re
import sys
import time
from pathlib import Path

import requests
from tqdm import tqdm

# ==================== Configuration ====================

DIFY_BASE_URL = os.getenv("DIFY_API_URL", "http://192.168.50.152/v1")
DIFY_API_KEY  = os.getenv("DIFY_API_KEY", "app-ntP1IznP1iaEnnZU2HBrMHJs")

STREAM_FIRST_TOKEN_TIMEOUT = int(os.getenv("STREAM_FIRST_TOKEN_TIMEOUT", "120"))   # 首 token 最大等待秒数
STREAM_TOTAL_TIMEOUT       = int(os.getenv("STREAM_TOTAL_TIMEOUT", "600"))          # 流式接收总超时

DIRECTORY = Path(os.getenv("TRANSLATE_DIR", os.getcwd()))

LANGUAGE_MAP: dict[str, tuple[str, str]] = {
    "CN": ("简体中文", "Simplified Chinese"),
    "TW": ("繁体中文", "Traditional Chinese"),
    "JP": ("日文",     "Japanese"),
    "KR": ("韩文",     "Korean"),
    "US": ("英文",     "English"),
}

MAX_RETRIES     = 4
RETRY_DELAY     = 4
CHUNK_SIZE      = 8
REQUEST_TIMEOUT = (10, 600)

# ── 🆕 单文件超时 & 重试配置 ─────────────────────────────────────────────────

FILE_TIMEOUT     = int(os.getenv("FILE_TIMEOUT", "1800"))      # 单文件最大处理时间（秒），默认 30min
FILE_MAX_RETRIES = int(os.getenv("FILE_MAX_RETRIES", "2"))    # 单文件最大重试次数，默认 2
FILE_RETRY_DELAY = int(os.getenv("FILE_RETRY_DELAY", "5"))    # 文件重试间隔基数（秒），默认 5

# =======================================================

log = logging.getLogger("dify_translator")
_token_bar: tqdm | None = None


def _get_headers() -> dict:
    return {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {DIFY_API_KEY}",
    }


# ── 🔧 FIX: 让 logging 通过 tqdm.write() 输出，避免和进度条互相覆盖 ─────────

class TqdmLoggingHandler(logging.Handler):
    """日志 handler: 通过 tqdm.write() 输出，确保不被进度条覆盖。"""
    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            tqdm.write(msg, file=sys.stdout)
        except Exception:
            self.handleError(record)


def setup_logging(verbose: bool = False) -> None:
    root = logging.getLogger()
    level = logging.DEBUG if verbose else logging.INFO
    root.setLevel(level)
    root.handlers.clear()

    handler = TqdmLoggingHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s │ %(levelname)-7s │ %(message)s",
        datefmt="%H:%M:%S",
    ))
    root.addHandler(handler)
    log.setLevel(level)


# ── Text classification ──────────────────────────────────────────────────────

_PUNCT_ONLY  = re.compile(r'^[\s\W\d_]+$')
_HAS_LATIN   = re.compile(r'[a-zA-Z]')
_HAS_CJK     = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')
_HAS_KANA    = re.compile(r'[\u3040-\u30ff\u31f0-\u31ff]')
_HAS_HANGUL  = re.compile(r'[\uac00-\ud7af]')
_PLACEHOLDER = re.compile(r'^\{[^}]+\}$|^<[^>]+>$|^%[sd%]$')


def _source_language(text: str) -> str | None:
    if _HAS_KANA.search(text):   return "JP"
    if _HAS_HANGUL.search(text): return "KR"
    if _HAS_CJK.search(text):    return "CN"
    if _HAS_LATIN.search(text):  return "US"
    return None


def need_translate(text: str, lang_code: str) -> bool:
    s = text.strip()
    if not s:                 return False
    if _PUNCT_ONLY.match(s):  return False
    if _PLACEHOLDER.match(s): return False
    src = _source_language(s)
    if src == lang_code:      return False
    if lang_code in ("TW", "CN") and src in ("TW", "CN"):
        return lang_code != src
    return True


# ── Build Dify Workflow inputs ───────────────────────────────────────────────

def _build_dify_inputs(items: list[dict], lang_en: str) -> dict[str, str]:
    source_lines    = "\n".join(f"{i+1}. {t['text']}" for i, t in enumerate(items))
    expected_format = ", ".join(f'"{i+1}": "..."' for i in range(len(items)))
    return {
        "target_language": lang_en,
        "item_count":      str(len(items)),
        "source_lines":    source_lines,
        "expected_format":  f"{{{expected_format}}}",
    }


# ── JSON extraction ──────────────────────────────────────────────────────────

def _extract_json_object(raw: str) -> dict:
    """Strip noise and robustly extract the first valid JSON object."""
    raw = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()

    if m := re.search(r'```(?:json)?\s*([\s\S]+?)```', raw):
        raw = m.group(1).strip()

    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    start = raw.find('{')
    if start != -1:
        depth, in_str, escape = 0, False, False
        for idx, ch in enumerate(raw[start:], start):
            if escape:
                escape = False
                continue
            if ch == '\\' and in_str:
                escape = True
                continue
            if ch == '"':
                in_str = not in_str
                continue
            if not in_str:
                if   ch == '{': depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        try:
                            parsed = json.loads(raw[start:idx + 1])
                            if isinstance(parsed, dict):
                                return parsed
                        except json.JSONDecodeError:
                            break

    raise ValueError(f"Cannot extract JSON object from model output:\n{raw[:800]}")


# ── SSE text extraction (兼容多种 Dify 版本) ─────────────────────────────────

def _extract_text_from_chunk(event_data: dict) -> str:
    """兼容多种 text_chunk 格式."""
    data_field = event_data.get("data")
    if isinstance(data_field, dict):
        text = data_field.get("text", "")
        if text:
            return text
    text = event_data.get("text", "")
    if text:
        return text
    text = event_data.get("answer", "")
    if text:
        return text
    if isinstance(data_field, str) and data_field:
        return data_field
    return ""


def _extract_text_from_outputs(event_data: dict) -> str:
    """从 node_finished / workflow_finished 提取完整输出."""
    data_field = event_data.get("data", {})
    if isinstance(data_field, dict):
        outputs = data_field.get("outputs", {})
        if isinstance(outputs, dict):
            for key in ("text", "result", "output", "answer"):
                val = outputs.get(key, "")
                if val and isinstance(val, str):
                    return val
            if len(outputs) == 1:
                val = next(iter(outputs.values()))
                if isinstance(val, str):
                    return val
        text = data_field.get("text", "")
        if text:
            return text

    outputs = event_data.get("outputs", {})
    if isinstance(outputs, dict):
        for key in ("text", "result", "output", "answer"):
            val = outputs.get(key, "")
            if val and isinstance(val, str):
                return val
    return ""


# ── Dify Workflow API calling ────────────────────────────────────────────────

def _call_dify_workflow_streaming(
    inputs: dict, lang_label: str, chunk_desc: str,
) -> str:
    url     = f"{DIFY_BASE_URL}/workflows/run"
    payload = {
        "inputs":        inputs,
        "response_mode": "streaming",
        "user":          "game-translator",
    }

    parts: list[str] = []
    count = 0
    start = time.monotonic()
    fallback_text: str = ""
    got_first_token = False                          # 🆕

    if _token_bar is not None:
        _token_bar.set_description_str(f"[{lang_label}] ⏳ 连接中...")
        _token_bar.refresh()

    with requests.post(
        url, json=payload, headers=_get_headers(),
        stream=True, timeout=REQUEST_TIMEOUT,
    ) as resp:
        resp.raise_for_status()
        if _token_bar is not None:
            _token_bar.set_description_str(f"[{lang_label}] ⚡ 等待首 token...")
            _token_bar.refresh()

        # ── 🆕 用 resp.raw 替代 iter_lines，实现行级超时 ────────────
        # 设置 socket 级别的超时，让 readline 可以被打断
        raw_socket = resp.raw._fp
        if hasattr(raw_socket, 'settimeout'):
            raw_socket.settimeout(STREAM_FIRST_TOKEN_TIMEOUT)

        for raw_line in resp.iter_lines():
            now = time.monotonic()

            # ── 🆕 流式总超时检查 ────────────────────────────────────
            if now - start > STREAM_TOTAL_TIMEOUT:
                log.warning(
                    f"[{lang_label}] ⏰ 流式总超时 ({STREAM_TOTAL_TIMEOUT}s)，"
                    f"已收到 {count} tokens，强制结束"
                )
                break

            # ── 🆕 首 token 超时检查 ─────────────────────────────────
            if not got_first_token and (now - start > STREAM_FIRST_TOKEN_TIMEOUT):
                raise TimeoutError(
                    f"[{lang_label}] 等待首 token 超时 "
                    f"({STREAM_FIRST_TOKEN_TIMEOUT}s)，中断请求"
                )

            if not raw_line:
                continue

            line = raw_line.decode("utf-8")
            if not line.startswith("data: "):
                continue

            try:
                event_data = json.loads(line[6:])
            except json.JSONDecodeError:
                log.debug(f"[{lang_label}] SSE parse failed: {line[:200]}")
                continue

            event = event_data.get("event", "")

            log.debug(
                f"[{lang_label}] SSE event={event} "
                f"keys={list(event_data.keys())} "
                f"data={json.dumps(event_data, ensure_ascii=False)[:400]}"
            )

            if event == "text_chunk":
                text_piece = _extract_text_from_chunk(event_data)
                if text_piece:
                    parts.append(text_piece)
                    count += 1

                    # ── 🆕 首 token 到达 → 切换为正常 read timeout ───
                    if not got_first_token:
                        got_first_token = True
                        if hasattr(raw_socket, 'settimeout'):
                            raw_socket.settimeout(REQUEST_TIMEOUT[1])
                        log.debug(
                            f"[{lang_label}] ✓ 首 token 到达 "
                            f"({now - start:.1f}s)"
                        )

            elif event == "node_finished":
                text = _extract_text_from_outputs(event_data)
                if text:
                    fallback_text = text
                    log.debug(f"[{lang_label}] node_finished fallback ({len(text)} chars)")

            elif event == "workflow_finished":
                if not parts:
                    text = _extract_text_from_outputs(event_data)
                    if text:
                        fallback_text = text
                break

            elif event == "error":
                msg  = event_data.get("message", "")
                code = event_data.get("code", "")
                raise RuntimeError(f"Dify Workflow error [{code}]: {msg}")

            # 更新 tqdm postfix
            if _token_bar is not None and count > 0 and (count == 1 or count % 5 == 0):
                elapsed = time.monotonic() - start
                speed   = count / elapsed if elapsed else 0
                _token_bar.set_description_str(f"[{lang_label}] {chunk_desc}")
                _token_bar.set_postfix_str(
                    f"{count} tok │ {speed:.1f} t/s │ {elapsed:.1f}s",
                    refresh=True,
                )

    elapsed = time.monotonic() - start
    speed   = count / elapsed if elapsed else 0
    collected = "".join(parts)

    # 兜底: 如果流式拼接为空或明显不完整
    if not collected.strip() or (collected.count('"') < 4 and fallback_text):
        log.info(
            f"[{lang_label}] ⚠ text_chunk 拼接不完整 "
            f"({len(collected)} chars), 使用 node_finished 兜底 "
            f"({len(fallback_text)} chars)"
        )
        collected = fallback_text

    # 更新最终进度
    if _token_bar is not None:
        _token_bar.set_description_str(f"[{lang_label}] {chunk_desc}")
        _token_bar.set_postfix_str(
            f"✓ {count} tok │ {speed:.1f} t/s │ {elapsed:.1f}s",
            refresh=True,
        )

    log.info(
        f"[{lang_label}] 📝 Dify 原始输出 ({len(collected)} chars): "
        f"{collected[:400]}{'...' if len(collected) > 400 else ''}"
    )

    return collected


def _call_dify_workflow_blocking(
    inputs: dict, lang_label: str, chunk_desc: str,
) -> str:
    url     = f"{DIFY_BASE_URL}/workflows/run"
    payload = {
        "inputs":        inputs,
        "response_mode": "blocking",
        "user":          "game-translator",
    }

    if _token_bar is not None:
        _token_bar.set_description_str(f"[{lang_label}] ⏳ blocking...")
        _token_bar.refresh()

    start = time.monotonic()
    resp  = requests.post(
        url, json=payload, headers=_get_headers(),
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    result = resp.json()

    elapsed = time.monotonic() - start

    log.debug(
        f"[{lang_label}] blocking response: "
        f"{json.dumps(result, ensure_ascii=False)[:500]}"
    )

    text = _extract_text_from_outputs(result)
    if not text:
        text = _extract_text_from_outputs({"data": result})

    if _token_bar is not None:
        _token_bar.set_description_str(f"[{lang_label}] {chunk_desc}")
        _token_bar.set_postfix_str(f"✓ blocking │ {elapsed:.1f}s", refresh=True)

    log.info(
        f"[{lang_label}] 📝 Dify 原始输出 ({len(text)} chars): "
        f"{text[:400]}{'...' if len(text) > 400 else ''}"
    )

    return text


# ── Translation core ─────────────────────────────────────────────────────────

def _translate_chunk(
    tasks: list[dict],
    lang_code: str,
    data: dict,
    chunk_desc: str = "",
    use_streaming: bool = True,
) -> int:
    _, lang_en = LANGUAGE_MAP[lang_code]
    lang_label = LANGUAGE_MAP[lang_code][0]
    inputs     = _build_dify_inputs(tasks, lang_en)

    last_exc: Exception = RuntimeError("No attempts made")
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if use_streaming:
                raw = _call_dify_workflow_streaming(inputs, lang_label, chunk_desc)
            else:
                raw = _call_dify_workflow_blocking(inputs, lang_label, chunk_desc)

            if not raw.strip():
                raise ValueError("Dify returned empty output")

            result = _extract_json_object(raw)

            log.info(
                f"[{lang_label}] 📦 解析到 keys: {sorted(result.keys())} "
                f"(期望: {[str(i+1) for i in range(len(tasks))]})"
            )

            expected_keys = {str(i + 1) for i in range(len(tasks))}
            got_keys      = set(result.keys()) & expected_keys
            missing_ratio = 1 - len(got_keys) / len(expected_keys)

            if missing_ratio > 0.5 and attempt < MAX_RETRIES:
                log.warning(
                    f"[{lang_label}] 返回 key 严重缺失 "
                    f"({len(got_keys)}/{len(expected_keys)}), 重试..."
                )
                raise ValueError(
                    f"Only {len(got_keys)}/{len(expected_keys)} keys returned"
                )

            written = 0
            missing_tasks: list[dict] = []
            for i, task in enumerate(tasks):
                translation = result.get(str(i + 1), "").strip()
                if translation:
                    data[task["id"]]["MultiLang"][lang_code] = translation
                    written += 1
                    if _token_bar is not None:
                        _token_bar.update(1)
                else:
                    log.warning(
                        f'[{lang_label}] missing key "{i+1}" '
                        f'for: "{task["text"][:50]}"'
                    )
                    missing_tasks.append(task)

            # 逐条补翻缺失的 key
            if missing_tasks and written > 0:
                log.info(f"[{lang_label}] 🔄 补翻 {len(missing_tasks)} 条缺失...")
                for mt in missing_tasks:
                    try:
                        single_inputs = _build_dify_inputs([mt], lang_en)
                        if use_streaming:
                            single_raw = _call_dify_workflow_streaming(
                                single_inputs, lang_label, f"{lang_label} 补翻",
                            )
                        else:
                            single_raw = _call_dify_workflow_blocking(
                                single_inputs, lang_label, f"{lang_label} 补翻",
                            )
                        single_result = _extract_json_object(single_raw)
                        translation   = single_result.get("1", "").strip()
                        if translation:
                            data[mt["id"]]["MultiLang"][lang_code] = translation
                            written += 1
                            if _token_bar is not None:
                                _token_bar.update(1)
                            log.info(
                                f'[{lang_label}] ✓ 补翻: '
                                f'"{mt["text"][:30]}" → "{translation[:30]}"'
                            )
                        else:
                            log.warning(
                                f'[{lang_label}] ✗ 补翻失败: "{mt["text"][:50]}"'
                            )
                    except Exception as exc:
                        log.warning(
                            f'[{lang_label}] ✗ 补翻异常: "{mt["text"][:50]}" — {exc}'
                        )

            log.info(f"[{lang_label}] chunk 完成: {written}/{len(tasks)}")
            return written

        except (TimeoutError, Exception) as exc:
            last_exc = exc
            is_timeout = isinstance(exc, TimeoutError)
            log.warning(
                f"[{lang_label}] attempt {attempt}/{MAX_RETRIES} "
                f"{'⏰ 超时' if is_timeout else '失败'}: {exc}"
            )
            if attempt < MAX_RETRIES:
                delay = RETRY_DELAY * (attempt * 2 if is_timeout else attempt)
                log.info(f"[{lang_label}] ⏳ {delay}s 后重试...")
                time.sleep(delay)

    raise RuntimeError(
        f"[{lang_label}] all {MAX_RETRIES} retries exhausted"
    ) from last_exc


def translate_language(
    data: dict,
    lang_code: str,
    force: bool = False,
    token_bar: tqdm | None = None,
    use_streaming: bool = True,
) -> tuple[dict, int]:
    global _token_bar
    _token_bar = token_bar

    lang_label = LANGUAGE_MAP[lang_code][0]

    tasks = [
        {"id": key, "text": key.strip()}
        for key, value in data.items()
        if isinstance(value.get("MultiLang"), dict)
        and (force or not value["MultiLang"].get(lang_code))
        and need_translate(key.strip(), lang_code)
    ]

    if not tasks:
        log.info(f"[{lang_label}] nothing to translate — skipping")
        return data, 0

    n_chunks = (len(tasks) + CHUNK_SIZE - 1) // CHUNK_SIZE
    log.info(
        f"[{lang_label}] {len(tasks)} strings │ "
        f"{n_chunks} chunk(s) │ "
        f"{'forced' if force else 'new only'}"
    )

    if token_bar is not None:
        token_bar.total = (token_bar.total or 0) + len(tasks)
        token_bar.refresh()

    total  = 0
    chunks = [tasks[i:i + CHUNK_SIZE] for i in range(0, len(tasks), CHUNK_SIZE)]
    for idx, chunk in enumerate(chunks, 1):
        desc = f"{lang_label} chunk {idx}/{n_chunks}"
        if n_chunks > 1:
            log.info(f"[{lang_label}] chunk {idx}/{n_chunks} ({len(chunk)} items)")
        try:
            total += _translate_chunk(
                chunk, lang_code, data,
                chunk_desc=desc, use_streaming=use_streaming,
            )
        except RuntimeError as exc:
            log.error(str(exc))

    log.info(f"[{lang_label}] ✔ 共写入 {total} 条")
    return data, total


# ── File I/O ─────────────────────────────────────────────────────────────────

def _load_jsonc(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'(?<![:/])//[^\n]*', '', text)
    return json.loads(text)


def _save_json(path: Path, data: dict) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)


# ── 🆕 单文件处理内核（供超时包装调用）──────────────────────────────────────

def _process_file_inner(
    filepath: Path,
    langs: list[str],
    force: bool,
    file_bar: tqdm | None,
    token_bar: tqdm | None,
    use_streaming: bool,
) -> str:
    """
    单文件翻译核心逻辑。

    返回值:
        "ok"      — 正常完成且有写入
        "skipped" — 文件无需翻译内容
        其他字符串 — 读取或处理失败的错误描述
    """
    if file_bar is not None:
        file_bar.set_description_str(f"📄 {filepath.name[:40]}")
        file_bar.set_postfix_str(f"{len(langs)} lang(s)", refresh=True)
    log.info(f"▶ {filepath.name}  ({len(langs)} lang(s){', forced' if force else ''})")

    try:
        data = _load_jsonc(filepath)
    except Exception as exc:
        log.error(f"failed to read {filepath.name}: {exc}")
        return f"read error: {exc}"

    total = 0
    for lang_code in langs:
        if file_bar is not None:
            file_bar.set_postfix_str(
                f"{LANGUAGE_MAP[lang_code][0]} | written={total}", refresh=True
            )
        data, written = translate_language(
            data, lang_code, force=force,
            token_bar=token_bar, use_streaming=use_streaming,
        )
        total += written
        if written:
            _save_json(filepath, data)

    if total:
        log.info(f"✔ saved {filepath.name}  ({total} translations)")
    else:
        log.info(f"— no changes: {filepath.name}")

    return "ok" if total else "skipped"


# ── 🆕 带超时 & 重试的文件处理入口 ──────────────────────────────────────────

def process_file(
    filepath: Path,
    langs_to_translate: list[str] | None = None,
    force: bool = False,
    file_bar:  tqdm | None = None,
    token_bar: tqdm | None = None,
    use_streaming: bool = True,
    file_timeout: int = FILE_TIMEOUT,
    file_max_retries: int = FILE_MAX_RETRIES,
    file_retry_delay: int = FILE_RETRY_DELAY,
) -> str:
    """
    处理单个文件（含超时保护 & 重试）。

    返回值:
        "ok"      — 成功完成
        "skipped" — 无需翻译
        "failed"  — 全部重试耗尽后失败
    """
    langs = list(LANGUAGE_MAP.keys()) if langs_to_translate is None else langs_to_translate
    result = "failed"

    for attempt in range(1, file_max_retries + 1):
        try:
            # 使用线程池 + timeout 实现单文件超时保护
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    _process_file_inner,
                    filepath, langs, force,
                    file_bar, token_bar, use_streaming,
                )
                result = future.result(timeout=file_timeout)

            # 正常完成（"ok" 或 "skipped"），跳出重试循环
            if file_bar is not None:
                if result == "ok":
                    file_bar.set_postfix_str("✔ done", refresh=True)
                elif result == "skipped":
                    file_bar.set_postfix_str("— skipped", refresh=True)
                else:
                    file_bar.set_postfix_str(f"⚠ {result[:30]}", refresh=True)
                file_bar.update(1)
            return result

        except concurrent.futures.TimeoutError:
            log.warning(
                f"⏰ {filepath.name} 超时 ({file_timeout}s) — "
                f"第 {attempt}/{file_max_retries} 次尝试"
            )
            if attempt < file_max_retries:
                delay = file_retry_delay * attempt
                log.info(f"   ⏳ {delay}s 后重试 {filepath.name} ...")
                time.sleep(delay)
            result = "failed"

        except Exception as exc:
            log.error(
                f"❌ {filepath.name} 处理失败 (第 {attempt}/{file_max_retries} 次): {exc}"
            )
            if attempt < file_max_retries:
                delay = file_retry_delay * attempt
                log.info(f"   ⏳ {delay}s 后重试 {filepath.name} ...")
                time.sleep(delay)
            result = "failed"

    # 全部重试耗尽
    log.error(f"❌ {filepath.name} — 共 {file_max_retries} 次尝试均失败，跳过此文件")
    if file_bar is not None:
        file_bar.set_postfix_str("❌ failed", refresh=True)
        file_bar.update(1)
    return "failed"


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Game Localization Auto-Translator (Dify Workflow API, Python 3.13+)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python translate_dify.py                     # all files, new strings only
  python translate_dify.py -f file.json        # single file
  python translate_dify.py -r                  # force re-translate ALL
  python translate_dify.py -r JP KR            # force re-translate JP + KR
  python translate_dify.py -l US JP            # only US and JP (no force)
  python translate_dify.py -p 3                # 3 files in parallel
  python translate_dify.py --blocking          # blocking mode
  python translate_dify.py --file-timeout 300  # 5 min per-file timeout
  python translate_dify.py --file-retries 3    # retry each file up to 3 times
  python translate_dify.py -v                  # verbose / debug

environment variables:
  DIFY_API_URL      Dify API base URL   (default: http://192.168.50.152/v1)
  DIFY_API_KEY      Dify application API key (required)
  TRANSLATE_DIR     Directory containing JSON files (default: cwd)
  FILE_TIMEOUT      Per-file timeout in seconds (default: 600)
  FILE_MAX_RETRIES  Per-file max retries (default: 2)
  FILE_RETRY_DELAY  Delay base between file retries in seconds (default: 5)
""",
    )
    parser.add_argument("-f", "--file",     type=Path)
    parser.add_argument("-p", "--parallel", type=int, default=1, metavar="N")
    parser.add_argument("-r", "--retranslate", nargs="*", metavar="LANG")
    parser.add_argument("-l", "--langs", nargs="+", metavar="LANG",
                        choices=list(LANGUAGE_MAP.keys()))
    parser.add_argument("--blocking", action="store_true",
                        help="Use blocking mode instead of streaming.")
    parser.add_argument("--file-timeout", type=int, default=FILE_TIMEOUT,
                        metavar="SEC",
                        help=f"Per-file timeout in seconds (default: {FILE_TIMEOUT})")
    parser.add_argument("--file-retries", type=int, default=FILE_MAX_RETRIES,
                        metavar="N",
                        help=f"Max retries per file on failure (default: {FILE_MAX_RETRIES})")
    parser.add_argument("-v", "--verbose", action="store_true")

    parser.add_argument("--first-token-timeout", type=int,
                        default=STREAM_FIRST_TOKEN_TIMEOUT, metavar="SEC",
                        help=f"首 token 超时秒数 (default: {STREAM_FIRST_TOKEN_TIMEOUT})")
    parser.add_argument("--stream-timeout", type=int,
                        default=STREAM_TOTAL_TIMEOUT, metavar="SEC",
                        help=f"流式接收总超时秒数 (default: {STREAM_TOTAL_TIMEOUT})")


    args = parser.parse_args()

    # 只初始化一次
    setup_logging(verbose=args.verbose)

    if not DIFY_API_KEY:
        log.error(
            "❌ 请设置环境变量 DIFY_API_KEY\n"
            "   export DIFY_API_KEY='app-your-actual-key'"
        )
        sys.exit(1)

    use_streaming = not args.blocking
    langs_to_translate: list[str] | None = args.langs
    force = False

    if args.retranslate is not None:
        force = True
        if args.retranslate:
            codes   = [c.upper() for c in args.retranslate]
            invalid = [c for c in codes if c not in LANGUAGE_MAP]
            if invalid:
                parser.error(
                    f"unknown lang code(s): {', '.join(invalid)} — "
                    f"valid: {', '.join(LANGUAGE_MAP)}"
                )
            langs_to_translate = (
                codes if langs_to_translate is None
                else [c for c in langs_to_translate if c in codes]
            )

    log.info(f"🔗 Dify API: {DIFY_BASE_URL}/workflows/run")
    log.info(f"📡 Mode: {'streaming' if use_streaming else 'blocking'}")
    log.info(f"⏰ File timeout: {args.file_timeout}s │ retries: {args.file_retries}")
    log.info(f"🔊 Verbose: {args.verbose}")

    # ── 🆕 统计计数 ─────────────────────────────────────────────────────────
    stats = {"ok": 0, "skipped": 0, "failed": 0}

    if args.file:
        if not args.file.exists():
            parser.error(f"file not found: {args.file}")
        with tqdm(
            total=0, desc="tokens", unit="str", ncols=100,
            bar_format="{desc} │ {postfix}", position=0,
        ) as tok_bar:
            result = process_file(
                args.file,
                langs_to_translate=langs_to_translate,
                force=force,
                token_bar=tok_bar,
                use_streaming=use_streaming,
                file_timeout=args.file_timeout,
                file_max_retries=args.file_retries,
                file_retry_delay=FILE_RETRY_DELAY,
            )
            stats[result] = stats.get(result, 0) + 1
    else:
        files = sorted(DIRECTORY.glob("*.json")) + sorted(DIRECTORY.glob("*.jsonc"))
        if not files:
            log.warning(f"no .json/.jsonc files found in {DIRECTORY}")
            return
        log.info(f"found {len(files)} file(s) in {DIRECTORY}")

        with (
            tqdm(
                total=len(files), desc="files  ", unit="file", ncols=100,
                position=0, leave=True,
            ) as file_bar,
            tqdm(
                total=0, desc="tokens ", unit="str", ncols=100,
                position=1, leave=True,
                bar_format="{desc} │ {postfix}",
            ) as token_bar,
        ):
            def _process(fp: Path) -> str:
                return process_file(
                    fp,
                    langs_to_translate=langs_to_translate,
                    force=force,
                    file_bar=file_bar,
                    token_bar=token_bar,
                    use_streaming=use_streaming,
                    file_timeout=args.file_timeout,
                    file_max_retries=args.file_retries,
                    file_retry_delay=FILE_RETRY_DELAY,
                )

            if args.parallel > 1:
                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=args.parallel
                ) as pool:
                    results = list(pool.map(_process, files))
            else:
                results = [_process(fp) for fp in files]

            for r in results:
                stats[r] = stats.get(r, 0) + 1

    # ── 🆕 最终汇总 ─────────────────────────────────────────────────────────
    print(
        f"\n✅ all done! "
        f"({stats.get('ok', 0)} succeeded, "
        f"{stats.get('failed', 0)} failed, "
        f"{stats.get('skipped', 0)} skipped)"
    )


if __name__ == "__main__":
    main()