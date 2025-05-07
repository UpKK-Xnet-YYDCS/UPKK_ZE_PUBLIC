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

# 配置
OLLAMA_URL = "http://192.168.50.5:11434/api/generate"  # 本地 Ollama 地址
MODEL = "gemma3:4b"
DIRECTORY = os.getcwd()  # 默认设置为当前目录
HEADERS = {"Content-Type": "application/json"}

LANGUAGE_MAP = {
    "US": ("英文", "English"),
    "CN": ("简体中文", "Simplified Chinese"),
    "JP": ("日文", "Japanese"),
    "KR": ("韩文", "Korean"),
    "TW": ("繁体中文", "Traditional Chinese")
}

MAX_RETRIES = 5
TIMEOUT_SECONDS = 60
SIMILARITY_THRESHOLD = 0.88
LOG_FILE = 'translation_log.txt'  # 日志文件路径

# 设置日志
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# 检测文本是否为正确的语言
def is_correct_language(text, lang):
    language_patterns = {
        "CN": r'[\u4e00-\u9fff]',  # 简体中文
        "JP": r'[\u3040-\u30ff\u31f0-\u31ff\u4e00-\u9fff]',  # 日语
        "KR": r'[\uac00-\ud7af]',  # 韩语
        "TW": r'[\u4e00-\u9fff]',  # 繁体中文
        "US": r'[a-zA-Z]'  # 英语
    }
    pattern = language_patterns.get(lang, "")
    if not pattern:
        logging.warning(f"[Warning] 未知的目标语言: {lang}")
        return False

    match = bool(re.search(pattern, text))
    if not match:
        logging.debug(f"[Language Mismatch] 文本: {text} 不符合目标语言: {lang}")
    return match

# 判断原文是否仅包含符号或数字
def is_text_symbol_or_number(text):
    return bool(re.match(r'^[\W\d_]+$', text.strip()))

# 判断原文是否是英语
def is_english(text):
    # 判断是否只包含英文字母、数字和空格
    return bool(re.match(r'^[a-zA-Z0-9\s\*\_\-\!\@\#\$\%\^\&\(\)\[\]\{\}\,\.\?\:\;\"\'\<\>\\\/\|\+\=]*$', text.strip()))

# 构建翻译提示的函数
def build_prompt(target_language, original_text):
    original_text = re.sub(r"【.*?】", "", original_text)  # 去除特殊标记
    prompt = (
        f"Translate the following game text into {target_language}.\n"
        f"Rules:\n"
        f"1. If the source text is already in {target_language}, return it as is, without modification.\n"
        f"2. If the source text is NOT in {target_language}, translate it accurately.\n"
        f"3. Do NOT copy the source text as the translation unless it is already valid in {target_language}.\n"
        f"4. Preserve all special symbols (e.g., ***, >> <<) and numbers exactly as they appear.\n"
        f"5. Do not translate numbers into their corresponding words in the target language.\n"
        f"6. Maintain the style and tone of in-game text.\n\n"
        f"Text:\n{original_text}\n"
        f"Output the translation in JSON format (e.g., {{\"text\": \"<translation>\"}})."
    )
    return prompt

# 清理文本（移除不需要的字符）
def sanitize_text(text):
    if not text:
        return ""
    text = re.sub(r'\\(?![ntr"\\/])', '', text)
    text = ''.join(c for c in text if c >= ' ' or c == '\n')
    return text.strip()

# 计算文本相似度
def calculate_similarity(text1, text2):
    text1_cleaned = re.sub(r'[^A-Za-z0-9\u4e00-\u9fff\u3040-\u30ff\u31f0-\u31ff\uFF00-\uFFEF\uAC00-\uD7AF]', '', text1)
    text2_cleaned = re.sub(r'[^A-Za-z0-9\u4e00-\u9fff\u3040-\u30ff\u31f0-\u31ff\uFF00-\uFFEF\uAC00-\uD7AF]', '', text2)
    sequence_matcher = SequenceMatcher(None, text1_cleaned, text2_cleaned)
    return sequence_matcher.ratio()

# 翻译文本
def translate_text(original_text, lang_code, filename):
    if is_text_symbol_or_number(original_text):
        logging.info(f"[Skip]: 文件: {filename} | 原文: {original_text} | 目标语言: {LANGUAGE_MAP[lang_code][0]} | 理由: 仅包含符号或数字")
        return None

    if lang_code == "US" and is_english(original_text):
        logging.info(f"[Skip]: 文件: {filename} | 原文: {original_text} | 目标语言: {LANGUAGE_MAP[lang_code][0]} | 理由: 原文为英语，无需翻译")
        return None

    _, lang_en_name = LANGUAGE_MAP[lang_code]
    prompt = build_prompt(lang_en_name, original_text)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            payload = {"model": MODEL, "prompt": prompt, "stream": False}
            response = requests.post(OLLAMA_URL, headers=HEADERS, json=payload, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            result = response.json()
            translation = result.get('response', '').strip()

            if is_correct_language(translation, lang_code):
                logging.info(f"[OK][{filename}] 原文: {original_text} -> 翻译: {translation} | 目标语言: {LANGUAGE_MAP[lang_code][0]}")
                return sanitize_text(translation)
            else:
                logging.error(f"[Fail][{filename}] 原文: {original_text} | 翻译: {translation} | 目标语言: {LANGUAGE_MAP[lang_code][0]}")
        except Exception as e:
            logging.error(f"[Error][{filename}] 原文: {original_text} | 错误: {e} | 目标语言: {LANGUAGE_MAP[lang_code][0]}")
            if attempt < MAX_RETRIES:
                time.sleep(2)
    return None

# 处理文件
def process_file(file_path):
    filename = os.path.basename(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"打开文件失败: {file_path}, 错误: {e}")
        return

    keys = list(data.keys())
    modified = False

    with tqdm(total=len(keys), desc=f"[文件] {filename}", ncols=100, unit="条", leave=False) as pbar:
        for key in keys:
            if not key or not isinstance(data[key].get('MultiLang'), dict):
                pbar.update(1)
                continue

            original_text = key.strip()
            value = data[key]['MultiLang']

            for lang_code in LANGUAGE_MAP.keys():
                if lang_code == "US" and is_english(original_text):
                    logging.info(f"[Skip]: 文件: {filename} | 原文: {original_text} | 原语言: 英文 | 目标语言: {LANGUAGE_MAP[lang_code][0]} | 理由: 原文为英语，无需翻译")
                    continue

                if not value.get(lang_code):
                    translated = translate_text(original_text, lang_code, filename)
                    if translated and calculate_similarity(original_text, translated) < SIMILARITY_THRESHOLD:
                        value[lang_code] = translated
                        modified = True
            pbar.update(1)

    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"保存文件失败: {file_path}, 错误: {e}")

# 主程序
def main():
    parser = argparse.ArgumentParser(description="本地批量翻译脚本 (使用 Ollama + Qwen2.5:7B-Instruct)")
    parser.add_argument("-f", "--file", type=str, help="指定单个文件进行翻译处理")
    parser.add_argument("-p", "--parallel", type=int, default=1, help="并行处理文件数")
    args = parser.parse_args()

    if args.file:
        process_file(args.file)
    else:
        files = [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY) if f.endswith('.jsonc')]
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
            list(tqdm(executor.map(process_file, files), total=len(files), desc="处理所有文件"))

if __name__ == "__main__":
    main()