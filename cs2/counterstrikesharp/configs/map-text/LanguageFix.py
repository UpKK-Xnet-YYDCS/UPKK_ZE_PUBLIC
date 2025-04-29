import json
import os
import re
# 清除非正确语言
# 支持的语言列表
languages = ["US", "JP", "CN", "KR", "TW"]

# 检查文本是否包含中文字符
def contains_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))  # 中文字符

# 检查文本是否包含日文字符（平假名、片假名、汉字）
def contains_japanese(text):
    return bool(re.search(r'[\u3040-\u30ff\u31f0-\u31ff\u4e00-\u9fff]', text))  # 平假名、片假名、汉字

# 检查文本是否包含韩文字符
def contains_korean(text):
    return bool(re.search(r'[\uac00-\ud7af]', text))  # 韩文字符

# 检测 MultiLang 中的字段是否包含目标语言的字符
def is_correct_language(text, lang):
    if lang == "CN":
        return contains_chinese(text)
    elif lang == "JP":
        return contains_japanese(text)
    elif lang == "KR":
        return contains_korean(text)
    elif lang == "TW":
        return contains_chinese(text)  # 繁体中文使用与简体中文相同的字符集
    elif lang == "US":
        return bool(re.search(r'[a-zA-Z]', text))  # 英语包含拉丁字母
    return False

# 转换为新格式
def convert_to_new_format(old_data):
    new_data = {}
    for key, value in old_data.items():
        # 准备 MultiLang，对于不匹配的语言设置为空字符串
        multilanguage = {}

        # 遍历 MultiLang 中的每个语言字段
        for lang in languages:
            language_value = value.get("MultiLang", {}).get(lang, "").strip()
            
            # 如果语言字段包含目标语言的字符，则保留该字段内容
            if is_correct_language(language_value, lang):
                multilanguage[lang] = language_value
            else:
                multilanguage[lang] = ""  # 如果不匹配，设置为空字符串

        new_data[key] = {
            "translation": value.get("translation", "").strip(),  # 保留原始 translation 内容
            "MultiLang": multilanguage
        }
    return new_data

# 遍历当前目录下所有 .jsonc 文件
for filename in os.listdir("."):
    if filename.endswith(".jsonc"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                old_data = json.load(f)

            # 转换为新格式
            new_data = convert_to_new_format(old_data)

            # 直接覆盖原文件
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)

            print(f"✅ 已覆盖: {filename}")
        except Exception as e:
            print(f"❌ 处理失败: {filename}，错误: {e}")
