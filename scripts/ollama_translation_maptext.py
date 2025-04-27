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
import shutil
import argparse
from tqdm import tqdm

# 配置
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
#MODEL = "qwen2:7b-instruct"
MODEL = "qwen2:7b"
DIRECTORY = '/home/MapText'
HEADERS = {"Content-Type": "application/json"}

LANGUAGE_MAP = {
    "US": ("英文", "English"),
    "CN": ("简体中文", "Simplified Chinese"),
    "JP": ("日文", "Japanese"),
    "KR": ("韩文", "Korean"),
    "TW": ("繁体中文", "Traditional Chinese")
}

# 休息配置
REST_SECONDS = 180
CONTINUOUS_WORK_SECONDS_BEFORE_REST = 900

# 翻译相关配置
MAX_RETRIES = 3
TIMEOUT_SECONDS = 60

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
        f"3. 数字必须精准，不能修改数字表达。\n"
        f"4. 句子风格必须与原文一致\n"
        f"5. 翻译错误、多译均视为任务失败。\n\n"
        f"【开始翻译】\n"
        f"Text:\n{original_text}"
    )


# 动态进度条+ETA
def print_progress(current, total, start_time, prefix="进度", source_text=None, target_lang=None, translated_text=None, filename=None):
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    bar_length = min(terminal_width - 50, 60)
    filled_length = int(bar_length * current // total)
    bar = '■' * filled_length + '□' * (bar_length - filled_length)
    percent = f"{(current / total) * 100:.1f}%"
    filename_info = f' [{filename}]' if filename else ''

    elapsed_time = time.time() - start_time
    avg_time_per_item = elapsed_time / current if current else 0
    eta_seconds = int(avg_time_per_item * (total - current))
    eta_minutes = eta_seconds // 60
    eta_seconds %= 60
    eta_display = f'ETA: {eta_minutes}m{eta_seconds}s'

    # 改为标准清空
    sys.stdout.write('\r')
    sys.stdout.write(' ' * terminal_width)
    sys.stdout.write('\r')

    progress_bar = f'{prefix}{filename_info}: [{bar}] {percent} ({current}/{total}) {eta_display}'
    sys.stdout.write(progress_bar)

    if source_text and target_lang and translated_text:
        source_text = (source_text[:20] + '...') if len(source_text) > 20 else source_text
        translated_text = (translated_text[:20] + '...') if len(translated_text) > 20 else translated_text
        extra_info = f'\n "{source_text}" ➔ ({target_lang}) "{translated_text}"'
        sys.stdout.write(extra_info)

    sys.stdout.flush()


# 动态休息倒计时（分钟+秒）
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

# 翻译文本（带重试提示）
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

# 处理单个文件
def process_file(file_path):
    filename = os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    keys = list(data.keys())
    total_keys = len(keys)
    modified = False

    # tqdm进度条（处理每个 key）
    with tqdm(total=total_keys, desc=f"[文件] {filename}", ncols=100, unit="条", dynamic_ncols=True) as pbar:
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

                    if translated and is_valid_translation(translated) and (lang_code == 'US' or len(translated) <= len(original_text) * 5):
                        value[lang_code] = translated
                        modified = True

                        # 更新进度条后缀
                        pbar.set_postfix({
                            "原文": (original_text[:10] + '...') if len(original_text) > 10 else original_text,
                            "翻译": (translated[:10] + '...') if len(translated) > 10 else translated,
                            "语言": lang_code
                        })

            pbar.update(1)  # 每处理一个 key，进度加一

    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"\n保存文件失败: {file_path} 错误: {e}")

# 主程序
def main():
    parser = argparse.ArgumentParser(description="本地批量翻译或单文件翻译脚本 (使用 Ollama + Qwen2:7b)")
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="指定单个文件进行翻译处理（可选，若不指定则默认处理整个目录）"
    )
    args = parser.parse_args()

    print(f"使用模型: {MODEL} | API地址: {OLLAMA_URL}\n")
    print(f"设置: 连续处理 {CONTINUOUS_WORK_SECONDS_BEFORE_REST // 60} 分钟后休息 {REST_SECONDS // 60} 分钟\n")

    if args.file:
        file_path = args.file
        if not os.path.isfile(file_path):
            print(f"错误: 文件不存在 -> {file_path}")
            return
        print(f"\n处理单个文件: {file_path}\n")
        process_file(file_path)
    else:
        file_list = sorted(
            [f for f in os.listdir(DIRECTORY) if f.endswith('.jsonc')],
            key=lambda x: os.path.getsize(os.path.join(DIRECTORY, x))
        )
        total_files = len(file_list)

        start_time = time.time()
        last_rest_time = start_time

        with tqdm(total=total_files, desc="处理所有文件", ncols=100, unit="个", dynamic_ncols=True) as pbar:
            for idx, filename in enumerate(file_list, start=1):
                file_path = os.path.join(DIRECTORY, filename)
                process_file(file_path)
                pbar.update(1)

                now = time.time()
                elapsed_since_last_rest = now - last_rest_time

                if CONTINUOUS_WORK_SECONDS_BEFORE_REST > 0 and REST_SECONDS > 0:
                    if elapsed_since_last_rest >= CONTINUOUS_WORK_SECONDS_BEFORE_REST and idx != total_files:
                        print(f"\n连续处理了 {elapsed_since_last_rest/60:.1f} 分钟，需要休息 {REST_SECONDS // 60} 分钟...")
                        dynamic_rest(REST_SECONDS)
                        last_rest_time = time.time()

        print("\n\n=== 全部完成 ===")
        print(f"共处理文件: {total_files}")


if __name__ == "__main__":
    main()
