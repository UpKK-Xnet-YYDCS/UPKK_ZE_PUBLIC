# 本地部署ollama 并利用 Qwen2.5:7B-Instruct模型 进行自动化翻译
# 将配置和路径修改为正确的本地ollama地址 运行此脚本.
# 如具有更好的GPU算力则可以使用更大的模型以达到更精确的效果
# ollama pull Qwen2.5:7B-Instruct
# sudo systemctl start ollama
# sudo apt install 
# sudo python3 
# sudo pip install tqdm requests argparse


import requests
import json
import os
import re
import time
import sys
import shutil
import argparse
from tqdm import tqdm
import concurrent.futures
import difflib

# 配置
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "qwen2.5:7b-instruct"
DIRECTORY = '/home/UPKK_ZE_PUBLIC-fe662eec4e53d65a1819cb8e7e7682d90eedb401/cs2/counterstrikesharp/configs/map-text'
HEADERS = {"Content-Type": "application/json"}

LANGUAGE_MAP = {
    "US": ("英文", "English"),
    "CN": ("简体中文", "Simplified Chinese"),
    "JP": ("日文", "Japanese"),
    "KR": ("韩文", "Korean"),
    "TW": ("繁体中文", "Traditional Chinese")
}

REST_SECONDS = 5
CONTINUOUS_WORK_SECONDS_BEFORE_REST = 900

MAX_PARALLEL_TASKS = 1  # 默认并行任务数，可通过命令行动态改

MAX_RETRIES = 3
TIMEOUT_SECONDS = 60

# Chinese number mapping for CN and TW
# 模型翻译出现中文数字则替换纠正.
chinese_to_arabic = {
    "零": "0",
    "一": "1",
    "二": "2",
    "三": "3",
    "四": "4",
    "五": "5",
    "六": "6",
    "七": "7",
    "八": "8",
    "九": "9",
    "十": "10"
}

# 去除特殊字符的函数，仅保留字母、数字、中文、日文、韩文字符
def sanitize_for_similarity(text):
    # 使用正则表达式移除所有非字母、数字、中文、日文、韩文的字符
    cleaned_text = re.sub(r'[^A-Za-z0-9\u4e00-\u9fff\u3040-\u30ff\u31f0-\u31ff\uFF00-\uFFEF\uAC00-\uD7AF]', '', text)
    return cleaned_text

# 计算相似度，首先清洗文本，移除特殊字符
def calculate_similarity(text1, text2):
    text1_cleaned = sanitize_for_similarity(text1)
    text2_cleaned = sanitize_for_similarity(text2)

    sequence_matcher = difflib.SequenceMatcher(None, text1_cleaned, text2_cleaned)
    return sequence_matcher.ratio()
    

# 修改原来的判断逻辑
def process_translation(text, lang_code, original_text, translated):
    # 计算原文与翻译后的相似度
    similarity = calculate_similarity(original_text, translated)
    print(f"相似度 {similarity:.2f} | 语言: {lang_code}")
    
    # 如果相似度超过95%，则不进行翻译
    if similarity >= 0.88:
        print(f"[跳过] {lang_code} 语言: 翻译与原文相似度高于95%，跳过翻译")
        return ""

    # 否则继续翻译处理
    return translated
    
# Function to replace Chinese numbers in CN and TW translations with Arabic numerals
def replace_chinese_numbers(text):
    # Regex to match Chinese numbers
    pattern = r"([一二三四五六七八九十])"
    
    # Replace Chinese numbers with Arabic numbers
    return re.sub(pattern, lambda match: chinese_to_arabic.get(match.group(1), match.group(1)), text)

# 工具函数
def should_skip(text):
    return bool(re.match(r'^[A-Za-z0-9\s\-\.\,\!\?\'\"\[\]\(\)\/\:\;]*$', text))

def is_english_text(text):
    return bool(re.match(r'^[A-Za-z0-9\s\-\.\,\!\?\'\"\[\]\(\)\/\:\;\*\`\~\@\#\$\%\^\&\_\+\=\|\>\<\{\}]*$', text))

def is_finalized_english_text(text):
    if not is_english_text(text):
        return False
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    uppercase_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    return uppercase_ratio >= 0.8

def sanitize_text(text):
    if not text:
        return ""
    text = re.sub(r'\\(?![ntr"\\/])', '', text)
    text = ''.join(c for c in text if c >= ' ' or c == '\n')
    return text.strip()

def is_valid_translation(text):
    if not text:
        return False
    cleaned_text = text.strip()
    if cleaned_text in ('', '```', '"""', '\'\'\'', '""', "''"):
        return False
    if len(cleaned_text) <= 5 and not re.search(r'[A-Za-z0-9\u4e00-\u9fff]', cleaned_text):
        return False
    return True

def extract_translation(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines:
        return ""
    return lines[-1]

def build_prompt(target_language, original_text):
    return (
        f"Act as a professional game text translator.\n"
        f"Translate the following game-related short text into {target_language}.\n"
        f"Return ONLY the translation. DO NOT add any explanation, introduction, quotation marks, or extra words.\n"
        f"Be concise, faithful to the original meaning, and adapt to the style of in-game texts.\n"
        f"Keep all numbers (e.g., 1, 2, 10, 30) exactly the same. Do NOT translate numbers into words.\n"
        f"Preserve all special symbols such as ***, >> <<, exactly as they appear.\n"
        f"Do NOT change the sentence structure, tone, or add any embellishment.\n\n"
        f"【绝对遵守以下规则】\n"
        f"1. 只翻译内容，不解释，不扩展，不引导。\n"
        f"2. 所有标点（如***、>> <<）必须原样保留，不可漏掉或改动。\n"
        f"3. 不要把数字翻译成其他语言或中文,请务必保持阿拉伯数字。\n"
        f"4. 翻译错误、多译均视为任务失败。\n\n"
        f"【开始翻译】\n"
        f"Text:\n{original_text}"
    )

def dynamic_rest(seconds):
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    for remaining in range(seconds, 0, -1):
        minutes = remaining // 60
        secs = remaining % 60
        message = f'休息中... 剩余 {minutes}分{secs}秒'
        sys.stdout.write('\r' + ' ' * (terminal_width - 1) + '\r')
        sys.stdout.write(message)
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\r' + ' ' * (terminal_width - 1) + '\r')
    sys.stdout.write('休息结束，继续处理...\n')
    sys.stdout.flush()

def translate_text(original_text, lang_code):
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
            translation = result.get('response', '')
            return sanitize_text(extract_translation(translation))
        except Exception as e:
            if attempt < MAX_RETRIES:
                print(f"\n[警告] 翻译失败，正在进行第 {attempt} 次重试...\n")
                time.sleep(2)
            else:
                print(f"\n[错误] 翻译失败，已达到最大重试次数，跳过该条目。")
                return None

# 修改原来的判断逻辑
def process_translation(text, lang_code, original_text, translated):
    # 计算原文与翻译后的相似度
    similarity = calculate_similarity(original_text, translated)
    print(f"相似度 {similarity:.2f} | 语言: {lang_code}")
    
    # 如果相似度超过95%，则不进行翻译
    if similarity >= 0.95:
        print(f"[跳过] {lang_code} 语言: 翻译与原文相似度高于95%，跳过翻译")
        return ""

    # 否则继续翻译处理
    return translated

# 调整以下代码部分来使用新的 `process_translation` 函数
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
        for idx, key in enumerate(keys, start=1):
            if not key or not isinstance(data[key].get('MultiLang'), dict):
                pbar.update(1)
                continue

            original_text = key.strip()
            value = data[key]['MultiLang']

            for lang_code in ['US', 'JP', 'CN', 'KR', 'TW']:
                if value.get(lang_code, "") == "":
                    translated = ""

                    if lang_code == 'US':
                        if is_finalized_english_text(original_text):
                            translated = sanitize_text(original_text)
                        else:
                            translated = translate_text(original_text, "US")
                    else:
                        translated = translate_text(original_text, lang_code)

                    # 跳过翻译结果与原文相似度超过95%的情况
                    if lang_code == 'US' and calculate_similarity(original_text, translated) >= 0.88:
                        continue
                    elif lang_code != 'US' and calculate_similarity(original_text, translated) >= 0.88:
                        continue

                    # 验证有效性并处理翻译
                    if translated and is_valid_translation(translated) and (lang_code == 'US' or len(translated) <= len(original_text) * 5):
                        # CN 和 TW 的特殊处理
                        if lang_code in ['CN', 'TW']:
                            translated = replace_chinese_numbers(translated)
                        
                        # 使用新的 `process_translation` 函数来判断是否跳过
                        final_translation = process_translation(text=original_text, lang_code=lang_code, original_text=original_text, translated=translated)
                        if final_translation:
                            value[lang_code] = final_translation
                            modified = True

                        pbar.set_postfix({
                            "原文": (original_text[:10] + '...') if len(original_text) > 10 else original_text,
                            "翻译": (translated[:10] + '...') if len(translated) > 10 else translated,
                            "语言": lang_code
                        })

            pbar.update(1)

    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存文件失败: {file_path}, 错误: {e}")

# 主程序
def main():
    global MAX_PARALLEL_TASKS
    parser = argparse.ArgumentParser(description="本地批量翻译或单文件翻译脚本 (使用 Ollama + Qwen2:7b)")
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="指定单个文件进行翻译处理（可选，若不指定则默认处理整个目录）"
    )
    parser.add_argument(
        "-p", "--parallel",
        type=int,
        help="并行处理文件数（可选，默认1个）"
    )
    args = parser.parse_args()

    if args.parallel:
        MAX_PARALLEL_TASKS = args.parallel

    print(f"使用模型: {MODEL} | API地址: {OLLAMA_URL}")
    print(f"并行任务数: {MAX_PARALLEL_TASKS} | 连续处理 {CONTINUOUS_WORK_SECONDS_BEFORE_REST // 60} 分钟后休息 {REST_SECONDS // 60} 分钟\n")

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

        start_time = time.time()
        last_rest_time = start_time

        with tqdm(total=total_files, desc="处理所有文件", ncols=100, unit="个", dynamic_ncols=True) as pbar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PARALLEL_TASKS) as executor:
                futures = [executor.submit(process_file, file_path) for file_path in file_list]

                for future in concurrent.futures.as_completed(futures):
                    pbar.update(1)

        print("\n\n=== 全部完成 ===")
        print(f"共处理文件: {total_files}")

if __name__ == "__main__":
    main()