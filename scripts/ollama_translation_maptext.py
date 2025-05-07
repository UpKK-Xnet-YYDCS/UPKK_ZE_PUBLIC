# 本地部署ollama 并利用 google gemma3 模型 进行自动化翻译
# 此脚本目前不会对现有翻译进行覆盖
# 将配置和路径修改为正确的本地ollama地址 运行此脚本.
# 如具有更好的GPU算力则可以使用更大的模型以达到更精确的效果
# ollama pull Qwen2.5:7B-Instruct
# ollama pull gemma3:4b
# sudo systemctl start ollama
# sudo apt install python3
# sudo pip install tqdm requests argparse
# 注 基于AI推理翻译每次运行结果可能都会不同 同时可能会犯错以及不正确的翻译.

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
SHOW_LOGS = False  # 是否显示日志
DISABLE_FILE_LOG = True  # 是否禁用文件日志

# 设置日志
def setup_logging(show_logs, disable_file_log):
    # 清除所有已有的日志处理器
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging_handlers = []
    if show_logs:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logging_handlers.append(console_handler)
    if not disable_file_log:
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")  # 指定 UTF-8 编码
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logging_handlers.append(file_handler)

    logging.basicConfig(level=logging.INFO, handlers=logging_handlers)

# 检测文本是否为正确的语言
def is_correct_language(text, lang):
    language_patterns = {
        "CN": r'[\u4e00-\u9fff]',  # 简体中文
        "JP": r'[\u3040-\u30ff\u31f0-\u31ff\u4e00-\u9fff]',  # 日语
        "KR": r'[\uac00-\ud7af]',  # 韩语
        "TW": r'[\u4e00-\u9fff]',  # 繁体中文
        "US": r'[a-zA-Z]'  # 英语
    }
    return bool(re.search(language_patterns.get(lang, ""), text))

# 判断原文是否仅包含符号或数字
def is_text_symbol_or_number(text):
    return bool(re.match(r'^[\W\d_]+$', text.strip()))

# 判断原文是否是英语
def is_english(text):
    return bool(re.match(r'^[a-zA-Z0-9\s\*\_\-\!\@\#\$\%\^\&\(\)\[\]\{\}\,\.\?\:\;\"\'\<\>\\\/\|\+\=]*$', text.strip()))

# 构建翻译提示的函数
def build_prompt(target_language, original_text):
    original_text = re.sub(r"【.*?】", "", original_text)  # 去除特殊标记
    return (
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

# 清理文本（移除不需要的字符）
def sanitize_text(text):
    if not text:
        return ""
    text = re.sub(r'\\(?![ntr"\\/])', '', text)
    return ''.join(c for c in text if c >= ' ' or c == '\n').strip()

# 计算文本相似度
def calculate_similarity(text1, text2):
    text1_cleaned = re.sub(r'[^A-Za-z0-9\u4e00-\u9fff\u3040-\u30ff\u31f0-\u31ff\uFF00-\uFFEF\uAC00-\uD7AF]', '', text1)
    text2_cleaned = re.sub(r'[^A-Za-z0-9\u4e00-\u9fff\u3040-\u30ff\u31f0-\u31ff\uFF00-\uFFEF\uAC00-\uD7AF]', '', text2)
    sequence_matcher = SequenceMatcher(None, text1_cleaned, text2_cleaned)
    return sequence_matcher.ratio()

# 翻译文本
def translate_text(original_text, lang_code):
    if is_text_symbol_or_number(original_text):
        return None

    if lang_code == "US" and is_english(original_text):
        return None

    _, lang_en_name = LANGUAGE_MAP[lang_code]
    prompt = build_prompt(lang_en_name, original_text)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            payload = {"model": MODEL, "prompt": prompt, "stream": False}
            response = requests.post(OLLAMA_URL, headers=HEADERS, json=payload, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            result = response.json()
            raw_translation = result.get('response', '').strip()

            try:
                raw_translation = re.sub(r'^```json|```$', '', raw_translation.strip(), flags=re.MULTILINE).strip()
                translation_json = json.loads(raw_translation)
                translation = translation_json.get("text", "").strip()
            except json.JSONDecodeError:
                translation = raw_translation
                print(f"[ERROR]: | 原文: {original_text} | 目标语言: {LANGUAGE_MAP[lang_code][0]} | 理由: 返回了非标准的JSON")

            if is_correct_language(translation, lang_code):
                return sanitize_text(translation)
        except Exception:
            time.sleep(2)
    return None

# 处理文件
def process_file(file_path):
    filename = os.path.basename(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"文件打开失败: {filename}, 错误: {e}")
        return False

    keys = list(data.keys())
    modified = False

    with tqdm(total=len(keys), desc=f"[文件] {filename}", ncols=100, unit="条", leave=False) as pbar:
        for key in keys:
            if not key or not isinstance(data[key].get('MultiLang'), dict):
                pbar.update(1)
                continue

            original_text = key.strip()
            value = data[key]['MultiLang']

            # 动态更新进度条的描述信息，仅显示当前原文片段
            pbar.set_description(f"[文件] {filename} | 正在翻译: {original_text[:30]} ...")

            for lang_code in LANGUAGE_MAP.keys():
                if lang_code == "US" and is_english(original_text):
                    continue

                if not value.get(lang_code):
                    # 翻译文本
                    translated = translate_text(original_text, lang_code)
                    if translated and calculate_similarity(original_text, translated) < SIMILARITY_THRESHOLD:
                        value[lang_code] = translated
                        modified = True

            pbar.update(1)

    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"文件保存失败: {filename}, 错误: {e}")

    return True

# 主程序
def main():
    parser = argparse.ArgumentParser(description="本地批量翻译脚本 (使用 Ollama + Gemma3)")
    parser.add_argument("-f", "--file", type=str, help="指定单个文件进行翻译处理")
    parser.add_argument("-p", "--parallel", type=int, default=1, help="并行处理文件数")
    args = parser.parse_args()

    setup_logging(SHOW_LOGS, DISABLE_FILE_LOG)

    if args.file:
        process_file(args.file)
    else:
        files = [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY) if f.endswith('.jsonc')]
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
            list(tqdm(executor.map(process_file, files), total=len(files), desc="Processing all files"))

if __name__ == "__main__":
    main()