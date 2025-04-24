import json
import os

# 支持的语言列表
languages = ["US", "JP", "CN", "KR", "TW"]

def convert_to_new_format(old_data):
    new_data = {}
    for key, value in old_data.items():
        translation = value.get("translation", "").strip()
        multilanguage = {lang: (translation if lang == "CN" and translation else "") for lang in languages}
        new_data[key] = {
            "translation": translation,
            "MultiLang": multilanguage
        }
    return new_data

# 遍历当前目录下所有 .jsonc 文件
for filename in os.listdir("."):
    if filename.endswith(".jsonc"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                old_data = json.load(f)

            new_data = convert_to_new_format(old_data)

            # 直接覆盖原文件
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)

            print(f"✅ 已覆盖: {filename}")
        except Exception as e:
            print(f"❌ 处理失败: {filename}，错误: {e}")
