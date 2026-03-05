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
DIFY_API_KEY  = os.getenv("DIFY_API_KEY", "app-WPimuuDqClQpOXF9wqgSOSC1")

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

# =======================================================

log = logging.getLogger("dify_translator")
_token_bar: tqdm | None = None


def _get_headers() -> dict:
    return {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {DIFY_API_KEY}",
    }


# 🔧 FIX: setup_logging 改为强制覆盖，确保 -v 生效
def setup_logging(verbose: bool = False) -> None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG if verbose else logging.INFO)
    # 清除已有 handler，避免 basicConfig 被忽略
    root.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s │ %(levelname)-7s │ %(message)s",
        datefmt="%H:%M:%S",
    ))
    root.addHandler(handler)
    log.setLevel(logging.DEBUG if verbose else logging.INFO)


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


# ── JSON extraction (加强版) ─────────────────────────────────────────────────

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


# ── 从 SSE text_chunk 提取文本（兼容多种 Dify 版本格式）─────────────────────

def _extract_text_from_chunk(event_data: dict) -> str:
    # 格式A: {"event":"text_chunk","data":{"text":"..."}}
    data_field = event_data.get("data")
    if isinstance(data_field, dict):
        text = data_field.get("text", "")
        if text:
            return text
    # 格式B: 顶层 text
    text = event_data.get("text", "")
    if text:
        return text
    # 格式C: 顶层 answer
    text = event_data.get("answer", "")
    if text:
        return text
    # 格式D: data 就是字符串
    if isinstance(data_field, str) and data_field:
        return data_field
    return ""


# ── 从 node_finished / workflow_finished 提取完整输出 ─────────────────────────

def _extract_text_from_outputs(event_data: dict) -> str:
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

    def _status(msg: str) -> None:
        if _token_bar is not None:
            _token_bar.set_description_str(f"[{lang_label}] {msg}")
            _token_bar.refresh()
        else:
            print(f"\r  [{lang_label}] {msg}    ", end="", flush=True)

    _status("⏳ 连接 Dify Workflow...")

    with requests.post(
        url, json=payload, headers=_get_headers(),
        stream=True, timeout=REQUEST_TIMEOUT,
    ) as resp:
        resp.raise_for_status()
        _status("⚡ 等待首个 token...")

        for raw_line in resp.iter_lines():
            if not raw_line:
                continue

            line = raw_line.decode("utf-8")
            if not line.startswith("data: "):
                continue

            try:
                event_data = json.loads(line[6:])
            except json.JSONDecodeError:
                log.debug(f"  [{lang_label}] SSE parse failed: {line[:200]}")
                continue

            event = event_data.get("event", "")

            log.debug(
                f"  [{lang_label}] SSE event={event} "
                f"keys={list(event_data.keys())} "
                f"preview={json.dumps(event_data, ensure_ascii=False)[:300]}"
            )

            if event == "text_chunk":
                text_piece = _extract_text_from_chunk(event_data)
                if text_piece:
                    parts.append(text_piece)
                    count += 1

            elif event == "node_finished":
                text = _extract_text_from_outputs(event_data)
                if text:
                    fallback_text = text
                    log.debug(
                        f"  [{lang_label}] node_finished fallback "
                        f"({len(text)} chars)"
                    )

            elif event == "workflow_finished":
                if not parts:
                    text = _extract_text_from_outputs(event_data)
                    if text:
                        fallback_text = text
                break

            elif event == "error":
                msg = event_data.get("message", "")
                code = event_data.get("code", "")
                raise RuntimeError(f"Dify Workflow error [{code}]: {msg}")

            if count > 0 and (count == 1 or count % 5 == 0):
                elapsed = time.monotonic() - start
                speed   = count / elapsed if elapsed else 0
                if _token_bar is not None:
                    _token_bar.set_description_str(f"[{lang_label}] {chunk_desc}")
                    _token_bar.set_postfix_str(
                        f"{count} tok │ {speed:.1f} t/s │ {elapsed:.1f}s",
                        refresh=True,
                    )
                else:
                    spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
                    sc = spinner[(count // 5) % len(spinner)]
                    print(
                        f"\r  [{lang_label}] {sc} {count} tok │ "
                        f"{speed:.1f} t/s │ {elapsed:.1f}s  ",
                        end="", flush=True,
                    )

    elapsed = time.monotonic() - start
    speed   = count / elapsed if elapsed else 0

    collected = "".join(parts)

    # 🔧 FIX: 如果流式拼接为空或不完整��使用 fallback
    if not collected.strip() or (collected.count('"') < 4 and fallback_text):
        log.info(
            f"  [{lang_label}] ⚠ text_chunk 拼接不完整 "
            f"({len(collected)} chars), 使用 node_finished 兜底 "
            f"({len(fallback_text)} chars)"
        )
        collected = fallback_text

    final = f"✓ {count} tok │ {speed:.1f} t/s │ {elapsed:.1f}s"
    if _token_bar is not None:
        _token_bar.set_description_str(f"[{lang_label}] {chunk_desc}")
        _token_bar.set_postfix_str(final, refresh=True)
    else:
        print(f"\r  [{lang_label}] {final}          ")

    # 🔧 FIX: 关键日志提升到 INFO 级别，不用 -v 也能看到
    log.info(
        f"  [{lang_label}] 📝 Dify 原始输出 ({len(collected)} chars): "
        f"{collected[:300]}{'...' if len(collected) > 300 else ''}"
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

    def _status(msg: str) -> None:
        if _token_bar is not None:
            _token_bar.set_description_str(f"[{lang_label}] {msg}")
            _token_bar.refresh()
        else:
            print(f"\r  [{lang_label}] {msg}    ", end="", flush=True)

    _status("⏳ 连接 Dify Workflow (blocking)...")
    start = time.monotonic()

    resp = requests.post(
        url, json=payload, headers=_get_headers(),
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    result = resp.json()

    elapsed = time.monotonic() - start
    _status(f"✓ blocking 完成 │ {elapsed:.1f}s")

    log.debug(
        f"  [{lang_label}] blocking response: "
        f"{json.dumps(result, ensure_ascii=False)[:500]}"
    )

    text = _extract_text_from_outputs(result)
    if not text:
        text = _extract_text_from_outputs({"data": result})

    log.info(
        f"  [{lang_label}] 📝 Dify 原始输出 ({len(text)} chars): "
        f"{text[:300]}{'...' if len(text) > 300 else ''}"
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

            # 🔧 FIX: 打印解析后的 JSON key 列表，方便诊断
            log.info(
                f"  [{lang_label}] 📦 解析 JSON keys: {sorted(result.keys())} "
                f"(期望: {[str(i+1) for i in range(len(tasks))]})"
            )

            # 检查返回完整性，严重缺失��重试
            expected_keys = {str(i + 1) for i in range(len(tasks))}
            got_keys      = set(result.keys()) & expected_keys
            missing_ratio = 1 - len(got_keys) / len(expected_keys)

            if missing_ratio > 0.5 and attempt < MAX_RETRIES:
                log.warning(
                    f"  [{lang_label}] 返回 key 严重缺失 "
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
                        f'  [{lang_label}] missing key "{i+1}" '
                        f'for: "{task["text"][:50]}"'
                    )
                    missing_tasks.append(task)

            # 🔧 FIX: 对缺失的 key 逐条补翻（单条发送，成功率更高）
            if missing_tasks and written > 0:
                log.info(
                    f"  [{lang_label}] 🔄 补翻 {len(missing_tasks)} 条缺失..."
                )
                for mt in missing_tasks:
                    try:
                        single_inputs = _build_dify_inputs([mt], lang_en)
                        if use_streaming:
                            single_raw = _call_dify_workflow_streaming(
                                single_inputs, lang_label,
                                f"{lang_label} 补翻",
                            )
                        else:
                            single_raw = _call_dify_workflow_blocking(
                                single_inputs, lang_label,
                                f"{lang_label} 补翻",
                            )
                        single_result = _extract_json_object(single_raw)
                        translation = single_result.get("1", "").strip()
                        if translation:
                            data[mt["id"]]["MultiLang"][lang_code] = translation
                            written += 1
                            if _token_bar is not None:
                                _token_bar.update(1)
                            log.info(
                                f'  [{lang_label}] ✓ 补翻成功: '
                                f'"{mt["text"][:30]}" → "{translation[:30]}"'
                            )
                        else:
                            log.warning(
                                f'  [{lang_label}] ✗ 补翻仍失败: '
                                f'"{mt["text"][:50]}"'
                            )
                    except Exception as exc:
                        log.warning(
                            f'  [{lang_label}] ✗ 补翻异常: '
                            f'"{mt["text"][:50]}" — {exc}'
                        )

            log.debug(f"[{lang_label}] chunk done: {written}/{len(tasks)}")
            return written

        except Exception as exc:
            last_exc = exc
            log.warning(
                f"  [{lang_label}] attempt {attempt}/{MAX_RETRIES} failed: {exc}"
            )
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt)

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
        log.info(f"  [{lang_label}] nothing to translate — skipping")
        return data, 0

    n_chunks = (len(tasks) + CHUNK_SIZE - 1) // CHUNK_SIZE
    log.info(
        f"  [{lang_label}] {len(tasks)} strings │ "
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
            log.info(f"  [{lang_label}] chunk {idx}/{n_chunks} ({len(chunk)} items)")
        try:
            total += _translate_chunk(
                chunk, lang_code, data,
                chunk_desc=desc, use_streaming=use_streaming,
            )
        except RuntimeError as exc:
            log.error(str(exc))

    log.info(f"  [{lang_label}] ✔ {total} written")
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


def process_file(
    filepath: Path,
    langs_to_translate: list[str] | None = None,
    force: bool = False,
    file_bar:  tqdm | None = None,
    token_bar: tqdm | None = None,
    use_streaming: bool = True,
) -> None:
    langs = list(LANGUAGE_MAP.keys()) if langs_to_translate is None else langs_to_translate

    if file_bar is not None:
        file_bar.set_description_str(f"📄 {filepath.name[:40]}")
        file_bar.set_postfix_str(f"{len(langs)} lang(s)", refresh=True)
    log.info(f"▶ {filepath.name}  ({len(langs)} lang(s){', forced' if force else ''})")

    try:
        data = _load_jsonc(filepath)
    except Exception as exc:
        log.error(f"  failed to read {filepath.name}: {exc}")
        if file_bar is not None:
            file_bar.update(1)
        return

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

    if file_bar is not None:
        file_bar.set_postfix_str(f"✔ {total} written", refresh=True)
        file_bar.update(1)

    if total:
        log.info(f"✔ saved {filepath.name}  ({total} translations written)")
    else:
        log.info(f"— no changes: {filepath.name}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    # 🔧 FIX: 先不初始化 logging，等解析完参数再初始化
    parser = argparse.ArgumentParser(
        description="Game Localization Auto-Translator (Dify Workflow API, Python 3.13+)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python translate_dify.py                     # all files, new strings only
  python translate_dify.py -f file.json        # single file
  python translate_dify.py -r                  # force re-translate ALL languages
  python translate_dify.py -r JP KR            # force re-translate JP and KR only
  python translate_dify.py -l US JP            # only process US and JP (no force)
  python translate_dify.py -p 3                # 3 files in parallel
  python translate_dify.py --blocking          # use blocking mode instead of streaming
  python translate_dify.py -v                  # verbose / debug (查看 SSE 原始结构)

environment variables:
  DIFY_API_URL    Dify API base URL (default: https://api.dify.ai/v1)
  DIFY_API_KEY    Dify application API key (required)
  TRANSLATE_DIR   Directory containing JSON files (default: cwd)
""",
    )
    parser.add_argument("-f", "--file",     type=Path)
    parser.add_argument("-p", "--parallel", type=int, default=1, metavar="N")
    parser.add_argument("-r", "--retranslate", nargs="*", metavar="LANG")
    parser.add_argument("-l", "--langs", nargs="+", metavar="LANG",
                        choices=list(LANGUAGE_MAP.keys()))
    parser.add_argument("--blocking", action="store_true",
                        help="Use blocking mode instead of streaming.")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    # 🔧 FIX: 只初始化一次 logging，根据 -v 决定级别
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
    log.info(f"🔊 Verbose: {args.verbose}")

    if args.file:
        if not args.file.exists():
            parser.error(f"file not found: {args.file}")
        with tqdm(
            total=0, desc="tokens", unit="str", ncols=100,
            bar_format="{desc} │ {postfix}", position=0,
        ) as tok_bar:
            process_file(
                args.file,
                langs_to_translate=langs_to_translate,
                force=force,
                token_bar=tok_bar,
                use_streaming=use_streaming,
            )
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
            def _process(fp: Path) -> None:
                process_file(
                    fp,
                    langs_to_translate=langs_to_translate,
                    force=force,
                    file_bar=file_bar,
                    token_bar=token_bar,
                    use_streaming=use_streaming,
                )

            if args.parallel > 1:
                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=args.parallel
                ) as pool:
                    list(pool.map(_process, files))
            else:
                for fp in files:
                    _process(fp)

    print("\n✅ all done!")


if __name__ == "__main__":
    main()