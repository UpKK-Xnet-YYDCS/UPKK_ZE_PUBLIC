# 本地部署ollama 并利用 qwen2:7b模型 进行自动化翻译
# ollama pull qwen2:7b
# 将配置和路径修改为正确的本地ollama地址 运行此脚本. 
# 如具有更好的GPU算力则可以使用更大的模型以达到更精确的效果

import requests
import json
import os
import re
import time
import sys

# 配置
OLLAMA_URL = "http://192.168.50.146:11434/api/generate"
MODEL = "qwen2:7b"
DIRECTORY = 'C:/Users/Administrator/Documents/GitHub/UPKK_ZE_PUBLIC/cs2/counterstrikesharp/configs/map-text/'
HEADERS = {"Content-Type": "application/json"}

LANGUAGE_MAP = {
    "US": ("英文", "English"),
    "CN": ("简体中文", "Simplified Chinese"),
    "JP": ("日文", "Japanese"),
    "KR": ("韩文", "Korean"),
    "TW": ("繁体中文", "Traditional Chinese")
}

# 休息配置
REST_SECONDS = 180         # 每次休息时间（秒）
CONTINUOUS_WORK_SECONDS_BEFORE_REST = 900  # 连续工作超过多少秒后休息（900秒=15分钟）

# 翻译相关配置
MAX_RETRIES = 3
TIMEOUT_SECONDS = 60

# 判断是否是简单英文/符号
def should_skip(text):
    return bool(re.match(r'^[A-Za-z0-9\s\-\.\,\!\?\'\"\[\]\(\)\/\:\;]*$', text))

# 判断是不是英文组成
def is_english_text(text):
    return bool(re.match(r'^[A-Za-z0-9\s\-\.\,\!\?\'\"\[\]\(\)\/\:\;\*\`\~\@\#\$\%\^\&\_\+\=\|\>\<\{\}]*$', text))

# 判断是不是成型的英文（大写比例高）
def is_finalized_english_text(text):
    if not is_english_text(text):
        return False
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    uppercase_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    return uppercase_ratio >= 0.8  # 大写比例超过80%，认为是成型英文

# 清理非法字符
def sanitize_text(text):
    if not text:
        return ""
    text = re.sub(r'\\(?![ntr"\\/])', '', text)
    text = ''.join(c for c in text if c >= ' ' or c == '\n')
    return text.strip()

# 判断翻译是否有效
def is_valid_translation(text):
    if not text:
        return False
    cleaned_text = text.strip()
    if cleaned_text in ('', '```', '"""', '\'\'\'', '""', "''"):
        return False
    if len(cleaned_text) <= 5 and not re.search(r'[A-Za-z0-9\u4e00-\u9fff]', cleaned_text):
        return False
    return True

# 提取最后一行翻译
def extract_translation(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines:
        return ""
    return lines[-1]

# 生成翻译prompt
def build_prompt(target_language, original_text):
    return (
        f"Act as a professional game text translator.\n"
        f"Translate the following game-related short text into {target_language}.\n"
        f"Return ONLY the translation. DO NOT add any explanation, introduction, quotes, or extra text.\n"
        f"Be concise, faithful to the original meaning, and adapt to the style of in-game texts.\n"
        f"Keep all numbers (e.g., 1, 2, 10, 30) exactly the same, do not translate numbers into words.\n\n"
        f"Text:\n{original_text}"
    )

# 替换文本中的数字为占位符
def replace_numbers_with_placeholder(text):
    numbers = re.findall(r'\d+(\.\d+)?', text)
    placeholder_text = re.sub(r'\d+(\.\d+)?', '[NUMBER]', text)
    return placeholder_text, numbers

# 把翻译后的占位符还原成原本的数字
def restore_numbers_from_placeholder(text, numbers):
    for number in numbers:
        text = text.replace('[NUMBER]', number, 1)
    return text


# 调用ollama翻译
def translate_text(original_text, lang_code):
    _, lang_en_name = LANGUAGE_MAP[lang_code]
    
    # 替换数字为占位符
    text_with_placeholder, original_numbers = replace_numbers_with_placeholder(original_text)
    prompt = build_prompt(lang_en_name, text_with_placeholder)

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
            translation = sanitize_text(extract_translation(translation))
            
            # 翻译回来后还原数字
            if original_numbers:
                translation = restore_numbers_from_placeholder(translation, original_numbers)

            return translation
        except Exception:
            if attempt < MAX_RETRIES:
                time.sleep(2)
            else:
                return None

# 打印进度条，并实时展示处理的内容
def print_progress(current, total, prefix="进度", source_text=None, target_lang=None, translated_text=None):
    bar_length = 40
    filled_length = int(bar_length * current // total)
    bar = '■' * filled_length + '□' * (bar_length - filled_length)
    percent = f"{(current / total) * 100:.1f}%"
    progress_bar = f'{prefix}: [{bar}] {percent} ({current}/{total})'

    if source_text and target_lang and translated_text:
        source_text = (source_text[:30] + '...') if len(source_text) > 30 else source_text
        translated_text = (translated_text[:30] + '...') if len(translated_text) > 30 else translated_text
        extra_info = f'  "{source_text}" ➔ ({target_lang}) "{translated_text}"'
        sys.stdout.write(f'\r{progress_bar}{extra_info}')
    else:
        sys.stdout.write(f'\r{progress_bar}')
    sys.stdout.flush()

# 处理单个文件
def process_file(file_path):
    filename = os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    keys = list(data.keys())
    total_keys = len(keys)
    modified = False

    for idx, key in enumerate(keys, start=1):
        if not key or not isinstance(data[key].get('MultiLang'), dict):
            continue

        original_text = key.strip()
        value = data[key]['MultiLang']

        # 处理每个语言
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

                if translated and is_valid_translation(translated) and (lang_code == 'US' or len(translated) <= len(original_text) * 5):
                    value[lang_code] = translated
                    modified = True
                    lang_name = LANGUAGE_MAP[lang_code][0]
                    print_progress(idx, total_keys, prefix="条目进度", source_text=original_text, target_lang=lang_name, translated_text=translated)
                else:
                    # 翻译无效，不写入，保持空
                    pass

    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"\n保存文件失败: {file_path} 错误: {e}")

# 主程序
def main():
    print(f"使用模型: {MODEL} | API地址: {OLLAMA_URL}\n")
    print(f"设置: 连续处理 {CONTINUOUS_WORK_SECONDS_BEFORE_REST // 60} 分钟后休息 {REST_SECONDS // 60} 分钟\n")

    file_list = [f for f in os.listdir(DIRECTORY) if f.endswith('.jsonc')]
    total_files = len(file_list)

    start_time = time.time()
    last_rest_time = start_time

    for idx, filename in enumerate(file_list, start=1):
        print(f"\n\n处理文件 ({idx}/{total_files}): {filename}")
        file_path = os.path.join(DIRECTORY, filename)
        process_file(file_path)

        now = time.time()
        elapsed_since_last_rest = now - last_rest_time

        if CONTINUOUS_WORK_SECONDS_BEFORE_REST > 0 and REST_SECONDS > 0:
            if elapsed_since_last_rest >= CONTINUOUS_WORK_SECONDS_BEFORE_REST and idx != total_files:
                print(f"\n连续处理了 {elapsed_since_last_rest/60:.1f} 分钟，休息 {REST_SECONDS // 60} 分钟...")
                time.sleep(REST_SECONDS)
                last_rest_time = time.time()

    print("\n\n=== 全部完成 ===")
    print(f"共处理文件: {total_files}")

if __name__ == "__main__":
    main()
