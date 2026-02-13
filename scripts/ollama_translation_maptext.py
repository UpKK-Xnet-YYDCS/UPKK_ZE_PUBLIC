# -*- coding: utf-8 -*-
import json
import os
import re
import time
import requests
import argparse
import concurrent.futures
from tqdm import tqdm
import logging

# ==================== 配置区 ====================
OLLAMA_URL = "http://192.168.50.7:11434/api/generate"
MODEL = "glm-4.7-flash:latest"   # 可能现阶段更好的选择?
DIRECTORY = os.getcwd()
HEADERS = {"Content-Type": "application/json"}

LANGUAGE_MAP = {
    "CN": ("简体中文", "Simplified Chinese"),
    "TW": ("繁体中文", "Traditional Chinese"),
    "JP": ("日文", "Japanese"),
    "KR": ("韩文", "Korean"),
    "US": ("英文", "English"),
}

MAX_RETRIES = 4
TIMEOUT_SECONDS = 300                     # 批量翻译一次可能很长
SIMILARITY_THRESHOLD = 0.88
# ================================================

def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s | %(message)s',
                        handlers=[logging.StreamHandler()])

# 语言快速检测
def need_translate(text, lang_code):
    if not text or len(text.strip()) == 0:
        return False
    if re.match(r'^[\s\W\d_]+$', text.strip()):    # 纯符号数字
        return False
    if lang_code == "US" and re.search(r'[a-zA-Z]', text):
        return False
    if lang_code in ["CN", "TW"] and re.search(r'[\u4e00-\u9fff]', text):
        return False
    if lang_code == "JP" and re.search(r'[\u3040-\u30ff\u31f0-\u31ff]', text):
        return False
    if lang_code == "KR" and re.search(r'[\uac00-\ud7af]', text):
        return False
    return True

# 核心：批量翻译整个文件（Qwen3-30B 专属超级 Prompt）
# 把原来的 batch_translate_file 替换成下面这个终极流式版

def batch_translate_file(data: dict, lang_code: str, force_retranslate=False) -> dict:
    _, lang_en = LANGUAGE_MAP[lang_code]

    tasks = []
    for key, value in data.items():
        text = key.strip()
        ml = value.get("MultiLang", {})
        if not isinstance(ml, dict):
            continue
        if not force_retranslate and ml.get(lang_code):
            continue
        if not need_translate(text, lang_code):
            continue
        tasks.append({"id": key, "text": text})

    if not tasks:
        return data

    force_hint = "\n【强制重译模式】：即使原文已有翻译，也请重新给出最优翻译版本。\n" if force_retranslate else ""
    
    prompt = f"""你是一名专业的游戏本地化翻译专家，正在将游戏文本翻译成【{lang_en}】。
{force_hint}要求：
1. 保持角色一贯的口癖、语气、语尾完全统一
2. 专有名词、占位符、数字、特殊符号绝对不翻译、不改动
3. 保留所有换行\n和格式
4. 整份文件风格、用词必须高度一致

请翻译以下所有文本（保持顺序）：

"""
    for i, t in enumerate(tasks, 1):
        prompt += f"{i:3d}. {t['text']}\n"

    prompt += f"""
直接输出一个合法的 JSON 数组，不要任何解释、代码块、额外文字。
格式示例：
[
  {{"id": "原文1", "translation": "翻译后文本1"}}
]
开始输出："""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.3,
            "top_p": 0.95,
            "repeat_penalty": 1.02,
            "num_ctx": 32768,
            "num_predict": 8192
        }
    }

    received = ""
    tokens_count = 0
    start_time = time.time()
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]  # 美观转圈动画
    spinner_idx = 0

    for attempt in range(MAX_RETRIES):
        try:
            with requests.post(OLLAMA_URL, json=payload, headers=HEADERS,
                             stream=True, timeout=(10, 600)) as r:
                r.raise_for_status()

                # 初始状态栏
                print(f"  → [{LANGUAGE_MAP[lang_code][0]}] 正在翻译 {len(tasks)} 条 ", end="", flush=True)

                for line in r.iter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        if chunk.get("done", False):
                            break

                        token = chunk.get("response", "")
                        received += token
                        tokens_count += 1

                        # 每 8 个 token 刷新一次显示（不刷屏但足够流畅）
                        if tokens_count % 8 == 0 or chunk.get("done"):
                            elapsed = time.time() - start_time
                            speed = tokens_count / elapsed if elapsed > 0 else 0
                            spinner_char = spinner[spinner_idx % len(spinner)]
                            spinner_idx += 1

                            print(f"\r  → [{LANGUAGE_MAP[lang_code][0]}] {spinner_char} 正在翻译… "
                                  f"{tokens_count} tokens | {speed:.1f} t/s | {len(tasks)} 条任务", 
                                  end="", flush=True)

                    except json.JSONDecodeError:
                        continue

                # 结束时清一行再打印最终结果
                elapsed = time.time() - start_time
                speed = tokens_count / elapsed if elapsed > 0 else 0
                print(f"\r  → [{LANGUAGE_MAP[lang_code][0]}] ✓ 翻译完成！ "
                      f"{tokens_count} tokens | 平均 {speed:.1f} t/s | 耗时 {elapsed:.1f}s          ")

            # 提取 JSON
            import re
            json_match = re.search(r'\[\s*\{.*\}\s*\]', received, re.DOTALL)
            if not json_match:
                raise ValueError("未检测到完整 JSON 数组")

            result = json.loads(json_match.group(0))

            # 写回
            modified = False
            for item in result:
                orig_id = item.get("id")
                trans = str(item.get("translation", "")).strip()
                if not trans or not orig_id:
                    continue
                clean_o = re.sub(r'[^\w\u4e00-\u9fff]', '', orig_id)
                clean_t = re.sub(r'[^\w\u4e00-\u9fff]', '', trans)
                if clean_o and clean_t:
                    jaccard = len(set(clean_t) & set(clean_o)) / len(set(clean_t) | set(clean_o))
                    if jaccard > 0.9:
                        continue
                if orig_id in data and isinstance(data[orig_id].get("MultiLang"), dict):
                    data[orig_id]["MultiLang"][lang_code] = trans
                    modified = True

            if modified:
                logging.info(f"  → [{LANGUAGE_MAP[lang_code][0]}] 成功写入 {len(result)} 条翻译")
            return data

        except Exception as e:
            print(f"\n  → [{LANGUAGE_MAP[lang_code][0]}] ✗ 第 {attempt+1} 次失败: {e}")
            time.sleep(4)
            received = ""
            tokens_count = 0
            start_time = time.time()

    logging.error(f"  → [{LANGUAGE_MAP[lang_code][0]}] 全部重试失败，跳过此语言")
    return data


# 处理单个文件（支持 .json 和 .jsonc）
# ==================== 主函数 + process_file 大改造（重点在这里） ====================
def process_file(filepath, retranslate_langs=None):
    """
    retranslate_langs: None → 全部强制重译
                       []    → 不强制重译任何语言（只补缺）
                       ["JP", "KR"] → 只强制重译日文和韩文
    """
    if retranslate_langs is None:
        # 完全强制重译全部语言（原 -r 行为）
        force_all = True
        specific_langs = set(LANGUAGE_MAP.keys())
    else:
        force_all = False
        specific_langs = set(retranslate_langs) if retranslate_langs else set()

    filename = os.path.basename(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        content = re.sub(r'//.*?$|/\*.*?\*/', '', content, flags=re.MULTILINE|re.DOTALL)
        data = json.loads(content)
    except Exception as e:
        logging.error(f"读取失败 {filename}: {e}")
        return

    mode_str = ""
    if force_all:
        mode_str = " [强制重译全部语言]"
    elif specific_langs:
        names = [LANGUAGE_MAP[c][0] for c in specific_langs if c in LANGUAGE_MAP]
        mode_str = f" [强制重译：{'、'.join(names)}]"

    logging.info(f"正在处理: {filename} （共 {len(data)} 条）{mode_str}")
    modified = False

    for lang_code in LANGUAGE_MAP.keys():
        # 决定本次是否强制重译
        force_this_lang = force_all or (lang_code in specific_langs)

        old_data = json.dumps(data, ensure_ascii=False)
        data = batch_translate_file(data, lang_code, force_retranslate=force_this_lang)
        if json.dumps(data, ensure_ascii=False) != old_data:
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
        logging.info(f"已保存: {filename}")
    else:
        logging.info(f"无需更新: {filename}")



# 主函数
# 主函数部分修改如下（完整替换原 main() 即可）

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Qwen3-30B 全文件上下文批量游戏翻译神器")
    parser.add_argument("-f", "--file", type=str, help="单个文件路径")
    parser.add_argument("-p", "--parallel", type=int, default=2, help="并行文件数（建议 1-3）")
    
    # 重磅升级：-r 现在支持指定语言！
    parser.add_argument("-r", "--retranslate", nargs="*", 
                        help="强制重新翻译指定语言（例如：-r JP KR TW US），不写参数表示全部强制重译，留空则只补缺")

    args = parser.parse_args()

    # 智能解析 -r 参数
    if args.retranslate is None:
        # 没写 -r → 只补缺
        retranslate_langs = []
    elif len(args.retranslate) == 0:
        # 写了 -r 但没给参数 → 全部强制重译（兼容老版本行为）
        retranslate_langs = None
    else:
        # 写了 -r JP KR → 只重译这些
        retranslate_langs = [code.strip().upper() for code in args.retranslate]

    # 校验语言代码
    if retranslate_langs:
        valid = set(LANGUAGE_MAP.keys())
        invalid = set(retranslate_langs) - valid if retranslate_langs else set()
        if invalid:
            print(f"错误：不支持的语言代码 → {', '.join(invalid)}")
            print(f"可选语言：{', '.join(valid)}")
            return

    if args.file:
        process_file(args.file, retranslate_langs)
    else:
        files = [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY)
                 if f.endswith(('.json', '.jsonc'))]
        files.sort()

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as exe:
            list(tqdm(
                exe.map(lambda f: process_file(f, retranslate_langs), files),
                total=len(files), desc="总进度", ncols=100
            ))

    print("\n全部完成！")
    

if __name__ == "__main__":
    main()
