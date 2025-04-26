# 本地部署ollama 并利用 qwen2:7b模型 进行自动化翻译
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

MAX_RETRIES = 3
TIMEOUT_SECONDS = 60

# 判断是否可以直接跳过（纯数字/符号/简单英文）
def should_skip(text):
    return bool(re.match(r'^[A-Za-z0-9\s\-\.\,\!\?\'\"\[\]\(\)\/\:\;]*$', text))

# 清理非法转义字符
def clean_text(text):
    text = re.sub(r'\\(?!u[0-9a-fA-F]{4})', '', text)
    text = re.sub(r'[^\w\s\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af.,!?()\[\]{}:;\"\'\/-]', '', text)
    return text.strip()

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
        f"Be concise, faithful to the original meaning, and adapt to the style of in-game texts.\n\n"
        f"Text:\n{original_text}"
    )

# 翻译函数
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
            return clean_text(extract_translation(translation))
        except Exception:
            if attempt < MAX_RETRIES:
                time.sleep(2)
            else:
                return None

# 进度条
def print_progress(current, total, prefix="进度"):
    bar_length = 40
    filled_length = int(bar_length * current // total)
    bar = '■' * filled_length + '□' * (bar_length - filled_length)
    percent = f"{(current / total) * 100:.1f}%"
    sys.stdout.write(f'\r{prefix}: [{bar}] {percent} ({current}/{total})')
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

        # ➡️ 新增：如果是简单英文/数字/符号，直接跳过
        if should_skip(original_text):
            print_progress(idx, total_keys, prefix="条目进度 (已跳过)")
            continue

        if value := data[key]['MultiLang']:
            # 处理英文 US
            if value.get('US', "") == "":
                translation = translate_text(original_text, "US")
                if translation:
                    value['US'] = translation
                    modified = True

            # 处理其他语言
            for lang_code in ['JP', 'CN', 'KR', 'TW']:
                if value.get(lang_code, "") == "":
                    translation = translate_text(original_text, lang_code)
                    if translation and len(translation) <= len(original_text) * 2:
                        value[lang_code] = translation
                        modified = True

        print_progress(idx, total_keys, prefix="条目进度")

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# 主程序
def main():
    print(f"使用模型: {MODEL} | API地址: {OLLAMA_URL}\n")

    file_list = [f for f in os.listdir(DIRECTORY) if f.endswith('.jsonc')]
    total_files = len(file_list)

    for idx, filename in enumerate(file_list, start=1):
        print(f"\n\n处理文件 ({idx}/{total_files}): {filename}")
        file_path = os.path.join(DIRECTORY, filename)
        process_file(file_path)
        print_progress(idx, total_files, prefix="文件进度")

    print("\n\n=== 全部完成 ===")
    print(f"共处理文件: {total_files}")

if __name__ == "__main__":
    main()
