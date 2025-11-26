#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import time
import requests
import argparse
import concurrent.futures
from tqdm import tqdm
from difflib import SequenceMatcher
import logging
import sys

# ==================== 配置区 ====================
OLLAMA_URL = "http://192.168.50.7:11434/api/generate"  # 修改为你的本地地址
MODEL = "gemma3:27b-it-qat"  # 强烈推荐！JSON 纪律性极强
DIRECTORY = os.getcwd()
HEADERS = {"Content-Type": "application/json"}

LANGUAGE_MAP = {
    "US": ("英文", "English"),
    "CN": ("简体中文", "Simplified Chinese"),
    "JP": ("日文", "Japanese"),
    "KR": ("韩文", "Korean"),
    "TW": ("繁体中文", "Traditional Chinese")
}

MAX_RETRIES = 6
TIMEOUT_SECONDS = 120
SIMILARITY_THRESHOLD = 0.88
SHOW_LOGS = False
DISABLE_FILE_LOG = True
LOG_FILE = 'translation_log.txt'
# ================================================

def setup_logging():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    handlers = []
    if SHOW_LOGS:
        handlers.append(logging.StreamHandler(sys.stdout))
    if not DISABLE_FILE_LOG:
        handlers.append(logging.FileHandler(LOG_FILE, encoding='utf-8'))
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=handlers
    )

# 语言检测正则
LANG_PATTERNS = {
    "CN": re.compile(r'[\u4e00-\u9fff]'),
    "TW": re.compile(r'[\u4e00-\u9fff]'),
    "JP": re.compile(r'[\u3040-\u30ff\u31f0-\u31ff\u4e00-\u9fff]'),
    "KR": re.compile(r'[\uac00-\ud7af]'),
    "US": re.compile(r'[a-zA-Z]'),
}

def is_pure_punctuation_or_number(text):
    return bool(re.match(r'^[\W\d_]+$', text.strip()))

def is_mostly_target_language(text, lang_code):
    if len(text) < 3:
2:
        return False
    pattern = LANG_PATTERNS.get(lang_code)
    if not pattern:
        return False
    return bool(pattern.search(text))

def build_prompt(target_lang_en_name, text):
    # 清除可能干扰模型的标记
    clean_text = re.sub(r"【.*?】", "", text.strip())

    return f"""You are a professional game translator. Translate the following text into {target_lang_en_name}.

Rules:
- Only translate if the text is NOT already in {target_lang_en_name}.
- If it is already in {target_lang_en_name}, return it unchanged.
- Never translate numbers, codes, or special symbols like ***, >>, <<, {{}}, etc.
- Preserve all formatting and punctuation exactly.
- Respond ONLY with valid JSON in this exact format:

{{"text": "your translation here"}}

Text to translate:
{clean_text}

Output strictly in JSON format:"""

# 最强 JSON 提取 + 修复函数（三保险）
def extract_json_from_response(raw: str):
    raw = raw.strip()

    # 1. 去除代码块
    raw = re.sub(r'^```json\s*|```$', '', raw, flags=re.MULTILINE).strip()

    # 2. 尝试直接解析
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "text" in data:
            return data["text"].strip()
    except:
        pass

    # 3. 查找第一个 { ... } 或 [{"text": ...}]
    json_match = re.search(r'(\{(?:[^{}]|(?1))*\})', raw)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            if isinstance(data, dict) and "text" in data:
                return data["text"].strip()
        except:
            pass

    # 4. 极致 fallback：尝试用正则提取 "text": "..." 的内容
    text_match = re.search(r'"text"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"', raw)
    if text_match:
        escaped = text_match.group(1)
        # 手动处理常见转义
        escaped = escaped.replace('\\"', '"').replace('\\n', '\n').replace('\\/', '/')
        return escaped

    return None

def translate_text(original_text: str, lang_code: str) -> str | None:
    if is_pure_punctuation_or_number(original_text):
        return None

    # 如果已经是目标语言，直接跳过
    if is_mostly_target_language(original_text, lang_code):
        return None

    _, lang_en = LANGUAGE_MAP[lang_code]
    prompt = build_prompt(lang_en, original_text)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            payload = {
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",                    # 强制 JSON 模式（关键！）
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "top_k": 40
                }
            }

            resp = requests.post(OLLAMA_URL, json=payload, headers=HEADERS, timeout=TIMEOUT_SECONDS)
            resp.raise_for_status()
            result = resp.json()
            raw = result.get("response", "").strip()

            if not raw:
                logging.warning(f"空响应 | 原文: {original_text[:50]}")
                time.sleep(2)
                continue

            translation = extract_json_from_response(raw)

            if translation is None:
                logging.warning(f"第{attempt}次提取JSON失败 | 原文: {original_text[:50]}\n响应: {raw[:300]}")
                if attempt < MAX_RETRIES:
                    time.sleep(3)
                continue

            # 最终检查：是否误翻（相似度过高）
            if calculate_similarity(original_text, translation) >= SIMILARITY_THRESHOLD:
                return None

            # 目标语言检测
            if not is_mostly_target_language(translation, lang_code):
                logging.info(f"翻译非目标语言，丢弃 | 原文: {original_text[:30]} → {translation[:30]}")
                if attempt < MAX_RETRIES:
                    time.sleep(2)
                    continue

            return translation.strip()

        except Exception as e:
            logging.error(f"请求异常 (尝试 {attempt}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES:
                time.sleep(4)

    return None

def calculate_similarity(a: str, b: str) -> float:
    a = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', '', a.lower())
    b = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', '', b.lower())
    return SequenceMatcher(None, a, b).ratio()

def process_file(file_path: str) -> bool:
    filename = os.path.basename(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"读取失败 {filename}: {e}")
        return False

    keys = list(data.keys())
    modified = False

    with tqdm(total=len(keys), desc=f"处理 {filename}", leave=False, ncols=120) as pbar:
        for key in keys:
            original = key.strip() if isinstance(key, str) else ""
            if not original or not isinstance(data[key].get("MultiLang"), dict):
                pbar.update(1)
                continue

            pbar.set_description(f"{filename[:20]} | {original[:40]}")

            for lang_code in LANGUAGE_MAP.keys():
                if lang_code in data[key]["MultiLang"] and data[key]["MultiLang"][lang_code]:
                    continue

                translated = translate_text(original, lang_code)
                if translated and calculate_similarity(original, translated) < SIMILARITY_THRESHOLD:
                    data[key]["MultiLang"][lang_code] = translated
                    modified = True
                    pbar.set_postfix_str(f"✓ {LANGUAGE_MAP[lang_code][0]}")

            pbar.update(1)

    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info(f"已保存: {filename}")
        except Exception as e:
            logging.error(f"保存失败 {filename}: {e}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Ollama 本地游戏多语言翻译工具（强制JSON版）")
    parser.add_argument("-f", "--file", type=str, help="单个文件")
    parser.add_argument("-p", "--parallel", type=int, default=2, help="并行文件数（建议2-4）")
    args = parser.parse_args()

    setup_logging()

    print(f"使用模型: {MODEL}")
    print(f"目标目录: {DIRECTORY}\n")

    if args.file:
        process_file(args.file)
    else:
        files = [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY) if f.endswith(('.json', '.jsonc'))]
        if not files:
            print("未找到 .json 或 .jsonc 文件")
            return

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
            list(tqdm(executor.map(process_file, files), total=len(files), desc="总进度"))

    print("\n所有文件处理完成！")

if __name__ == "__main__":
    main()