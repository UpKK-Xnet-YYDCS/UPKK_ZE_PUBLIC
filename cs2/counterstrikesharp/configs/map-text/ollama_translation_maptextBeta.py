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
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "qwen3:8b"  # 修改为千问3模型
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
TIMEOUT_SECONDS = 120  # 增加超时时间以适配千问3
SIMILARITY_THRESHOLD = 0.88
LOG_FILE = 'translation_log.txt'  # 日志文件路径

# 设置日志
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# 检测文本是否为正确的语言
def is_correct_language(text, lang):
    if lang == "CN":
        return bool(re.search(r'[\u4e00-\u9fff]', text))  # 简体中文
    elif lang == "JP":
        return bool(re.search(r'[\u3040-\u30ff\u31f0-\u31ff\u4e00-\u9fff]', text))  # 日文
    elif lang == "KR":
        return bool(re.search(r'[\uac00-\ud7af]', text))  # 韩文
    elif lang == "TW":
        return bool(re.search(r'[\u4e00-\u9fff]', text))  # 繁体中文
    elif lang == "US":
        return bool(re.search(r'[a-zA-Z]', text))  # 英文
    return False

# 用于翻译的函数
def translate_text(original_text, lang_code, filename):
    # 跳过仅包含符号和数字的原文
    if is_text_symbol_or_number(original_text):
        message = f"[Skip]: 文件: {filename} | 原文: {original_text} | 原语言: {LANGUAGE_MAP[lang_code][0]} | 目标语言: {lang_code} | 理由: 仅包含符号或数字"
        logging.info(message)
        print(message)  # 控制台输出
        return None

    _, lang_en_name = LANGUAGE_MAP[lang_code]
    prompt = build_prompt(lang_en_name, original_text)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            payload = {
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(OLLAMA_URL, headers=HEADERS, json=payload, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            result = response.json()
            translation = result.get('response', '').strip()

            # 如果翻译成功且语言匹配，返回翻译结果
            if is_correct_language(translation, lang_code):
                message = f"[OK][{filename}] [{original_text}] 目标语言: {lang_en_name} - 内容: {translation}"
                logging.info(message)
                print(message)  # 控制台输出
                return sanitize_text(translation)
            else:
                # 如果翻译失败，记录实际翻译结果内容
                message = f"[失败] 文件: {filename} | [{original_text}] 目标语言: {lang_en_name} 内容: 翻译返回结果: {translation}"
                logging.error(message)
                print(f"[失败] {message}")
                time.sleep(2)
        except Exception as e:
            message = f"(翻译失败 文件: {filename} | [{original_text}]) 目标语言: {lang_en_name} 内容: 错误 - {e}"
            logging.error(message)
            print(f"[错误] 翻译失败: {e}, 第{attempt}次重试...")
            if attempt < MAX_RETRIES:
                time.sleep(2)
            else:
                print(f"[错误] 达到最大重试次数，跳过该条目。")
                return None
    return None

# 判断原文是否仅包含符号或数字
def is_text_symbol_or_number(text):
    # 判断是否仅包含符号、数字或空白
    return bool(re.match(r'^[\W\d_]+$', text.strip()))  # \W 匹配非字母数字符号，\d 匹配数字，_ 匹配下划线

# 构建翻译提示的函数（优化为千问3）
def build_prompt(target_language, original_text):
    # 清除翻译指令等非翻译内容
    original_text = re.sub(r"【.*?】", "", original_text)  # 去除【开始翻译】等标记
    prompt = (
        f"Translate the following game-related text into {target_language}. "
        f"Return only the translation, preserving numbers and special symbols exactly as they appear. "
        f"Be concise and faithful to the original meaning, adapting to in-game text style. "
        f"Text: {original_text}"
    )
    return prompt

# 清理文本（移除不需要的字符）
def sanitize_text(text):
    if not text:
        return ""
    text = re.sub(r'\\(?![ntr"\\/])', '', text)
    text = ''.join(c for c in text if c >= ' ' or c == '\n')
    return text.strip()

# 将处理过的翻译文本与原文本进行相似度对比，并决定是否跳过翻译
def calculate_similarity(text1, text2):
    text1_cleaned = re.sub(r'[^A-Za-z0-9\u4e00-\u9fff\u3040-\u30ff\u31f0-\u31ff\uFF00-\uFFEF\uAC00-\uD7AF]', '', text1)
    text2_cleaned = re.sub(r'[^A-Za-z0-9\u4e00-\u9fff\u3040-\u30ff\u31f0-\u31ff\uFF00-\uFFEF\uAC00-\uD7AF]', '', text2)
    sequence_matcher = SequenceMatcher(None, text1_cleaned, text2_cleaned)
    return sequence_matcher.ratio()

# 处理文件并尝试翻译
def process_file(file_path):
    filename = os.path.basename(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"打开文件失败: {file_path}, 错误: {e}")
        return

    keys = list(data.keys())
    total_keys = len(keys)
    modified = False

    with tqdm(total=total_keys, desc=f"[文件] {filename}", ncols=100, unit="条", dynamic_ncols=True, leave=False) as pbar:
        for key in keys:
            if not key or not isinstance(data[key].get('MultiLang'), dict):
                pbar.update(1)
                continue

            original_text = key.strip()
            value = data[key]['MultiLang']

            for lang_code in LANGUAGE_MAP.keys():
                # 如果原文是英语，则跳过 US 语言的翻译
                if lang_code == "US" and is_english(original_text):
                    message = f"[Skip]: 文件: {filename} | 原文: {original_text} | 原语言: 英文 | 目标语言: US | 理由: 原文为英语"
                    logging.info(message)
                    print(message)  # 控制台输出
                    continue

                if value.get(lang_code, "") == "":
                    translated = translate_text(original_text, lang_code, filename)

                    # 跳过翻译结果与原文相似度超过阈值的情况
                    if translated and calculate_similarity(original_text, translated) >= SIMILARITY_THRESHOLD:
                        continue

                    # 验证有效性并处理翻译
                    if translated:
                        value[lang_code] = translated
                        modified = True

            pbar.update(1)

    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存文件失败: {file_path}, 错误: {e}")

# 判断原文是否是英语
def is_english(text):
    return bool(re.match(r'^[a-zA-Z0-9\s]*$', text))

# 主程序
def main():
    parser = argparse.ArgumentParser(description="本地批量翻译或单文件翻译脚本 (使用 Ollama + Qwen3:7b-instruct) ")
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="指定单个文件进行翻译处理（可选，若不指定则默认处理整个目录）"
    )
    parser.add_argument(
        "-p", "--parallel",
        type=int,
        default=1,
        help="并行处理文件数（可选，默认1个）"
    )
    args = parser.parse_args()

    print(f"使用模型: {MODEL} | API地址: {OLLAMA_URL}")

    if args.file:
        file_path = args.file
        if not os.path.isfile(file_path):
            print(f"错误: 文件不存在 -> {file_path}")
            return
        print(f"处理单个文件: {file_path}")
        process_file(file_path)
    else:
        file_list = sorted(
            [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY) if f.endswith('.jsonc')],
            key=lambda x: os.path.getsize(x)
        )
        total_files = len(file_list)

        with tqdm(total=total_files, desc="处理所有文件", ncols=100, unit="个", dynamic_ncols=True) as pbar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
                futures = [executor.submit(process_file, file_path) for file_path in file_list]

                for future in concurrent.futures.as_completed(futures):
                    pbar.update(1)

        print("\n\n=== 全部完成 ===")

if __name__ == "__main__":
    main()