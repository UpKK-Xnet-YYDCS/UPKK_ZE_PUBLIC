# -*- coding: utf-8 -*-
"""
Game Localization Auto-Translator
Ollama / Qwen — Python 3.13+
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
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://192.168.50.7:11434/api/generate")
MODEL      = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")
DIRECTORY  = Path(os.getenv("TRANSLATE_DIR", os.getcwd()))
HEADERS    = {"Content-Type": "application/json"}

LANGUAGE_MAP: dict[str, tuple[str, str]] = {
    "CN": ("简体中文", "Simplified Chinese"),
    "TW": ("繁体中文", "Traditional Chinese"),
    "JP": ("日文",     "Japanese"),
    "KR": ("韩文",     "Korean"),
    "US": ("英文",     "English"),
}

MAX_RETRIES     = 4
RETRY_DELAY     = 4         # base seconds between retries (multiplied by attempt)
CHUNK_SIZE      = 8         # items per LLM request (tuned for 4096 ctx)
REQUEST_TIMEOUT = (10, 600) # (connect, read) seconds

OLLAMA_OPTIONS: dict = {
    "temperature":    0.05,
    "top_p":          0.90,
    "repeat_penalty": 1.05,
    "num_ctx":        4096,
    "num_predict":    2048,
}
# =======================================================

log = logging.getLogger(__name__)

# 全局进度条引用（供嵌套函数写入 postfix）
_token_bar: tqdm | None = None


def setup_logging(verbose: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s │ %(levelname)-7s │ %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


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


# ── Prompt & parsing ─────────────────────────────────────────────────────────

def _build_prompt(items: list[dict], lang_en: str) -> str:
    lines    = "\n".join(f'{i+1}. {t["text"]}' for i, t in enumerate(items))
    expected = ", ".join(f'"{i+1}": "..."' for i in range(len(items)))
    return f"""/no_think
You are a professional game localization translator. Translate the strings below into {lang_en}.

STRICT RULES:
1. Output ONLY a single valid JSON object. No markdown, no code fences, no comments, no explanation.
2. Keys are the line numbers as strings ("1", "2", ...). Values are the translated strings.
3. Preserve ALL placeholders, escape sequences (\\n, %s, %d, {{0}}, <tag>), symbols, and numbers exactly.
4. Keep consistent character voice, tone, and terminology throughout.
5. Every key must be present. If a string cannot be translated, copy the original.

SOURCE STRINGS ({len(items)} total):
{lines}

REQUIRED OUTPUT FORMAT:
{{{expected}}}

Output the JSON object now:"""


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

    raise ValueError(f"Cannot extract JSON object from model output:\n{raw[:600]}")


# ── Ollama streaming ─────────────────────────────────────────────────────────

def _stream_request(payload: dict, lang_label: str, chunk_desc: str) -> str:
    parts: list[str] = []
    count = 0
    start = time.monotonic()

    def _status(msg: str) -> None:
        if _token_bar is not None:
            _token_bar.set_description_str(f"[{lang_label}] {msg}")
            _token_bar.refresh()
        else:
            print(f"\r  [{lang_label}] {msg}    ", end="", flush=True)

    _status("⏳ 连接中...")

    with requests.post(
        OLLAMA_URL, json=payload, headers=HEADERS,
        stream=True, timeout=REQUEST_TIMEOUT,
    ) as resp:
        resp.raise_for_status()
        _status("⚡ 等待首个 token...")

        for raw_line in resp.iter_lines():
            if not raw_line:
                continue
            chunk = json.loads(raw_line.decode("utf-8"))
            if chunk.get("done"):
                break

            parts.append(chunk.get("response", ""))
            count += 1

            if count == 1 or count % 5 == 0:
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
                        f"\r  [{lang_label}] {sc} {count} tok │ {speed:.1f} t/s │ {elapsed:.1f}s  ",
                        end="", flush=True,
                    )

    elapsed = time.monotonic() - start
    speed   = count / elapsed if elapsed else 0
    final   = f"✓ {count} tok │ {speed:.1f} t/s │ {elapsed:.1f}s"
    if _token_bar is not None:
        _token_bar.set_description_str(f"[{lang_label}] {chunk_desc}")
        _token_bar.set_postfix_str(final, refresh=True)
    else:
        print(f"\r  [{lang_label}] {final}          ")

    return "".join(parts)


# ── Translation core ─────────────────────────────────────────────────────────

def _translate_chunk(
    tasks: list[dict],
    lang_code: str,
    data: dict,
    chunk_desc: str = "",
) -> int:
    _, lang_en = LANGUAGE_MAP[lang_code]
    lang_label = LANGUAGE_MAP[lang_code][0]
    payload = {
        "model":   MODEL,
        "prompt":  _build_prompt(tasks, lang_en),
        "stream":  True,
        "think":   False,
        "format":  "json",
        "options": OLLAMA_OPTIONS,
    }

    last_exc: Exception = RuntimeError("No attempts made")
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw     = _stream_request(payload, lang_label, chunk_desc)
            result  = _extract_json_object(raw)
            written = 0
            for i, task in enumerate(tasks):
                translation = result.get(str(i + 1), "").strip()
                if translation:
                    data[task["id"]]["MultiLang"][lang_code] = translation
                    written += 1
                    if _token_bar is not None:
                        _token_bar.update(1)
                else:
                    log.warning(f"  [{lang_label}] missing key \"{i+1}\" in response")
            log.debug(f"[{lang_label}] chunk done: {written}/{len(tasks)}")
            return written
        except Exception as exc:
            last_exc = exc
            log.warning(f"  [{lang_label}] attempt {attempt}/{MAX_RETRIES} failed: {exc}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt)

    raise RuntimeError(f"[{lang_label}] all {MAX_RETRIES} retries exhausted") from last_exc


def translate_language(
    data: dict,
    lang_code: str,
    force: bool = False,
    token_bar: tqdm | None = None,
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
            total += _translate_chunk(chunk, lang_code, data, chunk_desc=desc)
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
            data, lang_code, force=force, token_bar=token_bar
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
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Game Localization Auto-Translator (Ollama / Qwen, Python 3.13+)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python translate.py                  # all files, new strings only
  python translate.py -f file.json     # single file
  python translate.py -r               # force re-translate ALL languages
  python translate.py -r JP KR         # force re-translate JP and KR only
  python translate.py -l US JP         # only process US and JP (no force)
  python translate.py -p 3             # 3 files in parallel
  python translate.py -v               # verbose / debug output
""",
    )
    parser.add_argument("-f", "--file",        type=Path, help="Single file to translate.")
    parser.add_argument("-p", "--parallel",    type=int,  default=1, metavar="N",
                        help="Files to process in parallel (default: 1).")
    parser.add_argument("-r", "--retranslate", nargs="*", metavar="LANG",
                        help="Force re-translate. No args=all; with args=specific codes.")
    parser.add_argument("-l", "--langs",       nargs="+", metavar="LANG",
                        choices=list(LANGUAGE_MAP.keys()),
                        help="Limit to specific language codes (default: all).")
    parser.add_argument("-v", "--verbose",     action="store_true")
    args = parser.parse_args()

    if args.verbose:
        setup_logging(verbose=True)

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

    if args.file:
        if not args.file.exists():
            parser.error(f"file not found: {args.file}")
        with tqdm(
            total=0, desc="tokens", unit="str", ncols=100,
            bar_format="{desc} │ {postfix}",
            position=0,
        ) as tok_bar:
            process_file(
                args.file,
                langs_to_translate=langs_to_translate,
                force=force,
                token_bar=tok_bar,
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
                )

            if args.parallel > 1:
                with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as pool:
                    list(pool.map(_process, files))
            else:
                for fp in files:
                    _process(fp)

    print("\n✅ all done!")


if __name__ == "__main__":
    main()