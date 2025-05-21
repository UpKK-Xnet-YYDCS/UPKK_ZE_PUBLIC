import requests
import json
import time
import os
import logging

# 配置
STEAM_API_KEY = os.getenv("STEAM_API_KEY")  # 从环境变量加载 API 密钥
BASE_URL = "https://api.steampowered.com"
DEFAULT_OUTPUT_FILE = "workshop_maps.json"
DEFAULT_APPID = 730  # 默认 CS:GO/CS2 AppID
STEAM_ID = "76561198012345678"  # 直接指定 SteamID64
WHITELIST_FILE = "workshop_white_steam64.txt"  # 白名单文件

# 设置日志
logging.basicConfig(filename="workshop_errors.log", level=logging.DEBUG, 
                   format="%(asctime)s - %(levelname)s - %(message)s")

def load_whitelist(file_path):
    """从文件加载白名单列表"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            whitelist = {line.strip() for line in f if line.strip()}  # 使用集合避免重复
        logging.info(f"从 {file_path} 加载了 {len(whitelist)} 个白名单 SteamID")
        return whitelist
    except FileNotFoundError:
        logging.error(f"白名单文件 {file_path} 未找到")
        print(f"错误：白名单文件 {file_path} 未找到")
        return set()
    except Exception as e:
        logging.error(f"读取白名单文件 {file_path} 时出错: {e}")
        print(f"读取白名单文件时出错: {e}")
        return set()

def get_workshop_maps(steam_id, api_key, appid=730, search_prefix="ze_", whitelist=None):
    """获取用户上传的所有创意工坊内容（地图和合集），并过滤不在白名单中的作者"""
    url = f"{BASE_URL}/IPublishedFileService/QueryFiles/v1/"
    params = {
        "key": api_key,
        "query_type": 1,  #排序依据：按发布时间排序
        "appid": appid,
        "numperpage": 100,  # 每页最大数量
        "return_details": True,
        "search_text": search_prefix,  # 使用参数作为搜索文本
        "return_tags": True,
        "return_kv_tags": True,
        "return_previews": True,
        "return_children": True,
        "filetype": 0
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # 检查是否有数据
        if not data.get("response") or not data["response"].get("publishedfiledetails"):
            logging.info(f"SteamID {steam_id}: 未找到创意工坊内容")
            return []

        # 提取内容信息
        items = []
        for item in data["response"]["publishedfiledetails"]:
            if item.get("result") != 1:  # 1 表示成功
                continue

            # 如果创作者不在白名单里，跳过此项目
            creator = str(item.get("creator"))
            if whitelist and creator not in whitelist:
                continue

            # 处理时间戳
            time_created = item.get("time_created", 0)
            time_updated = item.get("time_updated", 0)

            # 如果标题不以指定的前缀开头，跳过该项目
            if not item.get("title", "").startswith(search_prefix):
                continue

            items.append({
                "title": item.get("title", "未命名"),
                "description": item.get("description", ""),
                "file_type": item.get("file_type", 0),  # 0=地图, 2=合集
                "id": item["publishedfileid"],
                "creator": item["creator"],
                "file_size": item["file_size"],
                "url": f"https://steamcommunity.com/sharedfiles/filedetails/?id={item['publishedfileid']}",
                "time_created": time.strftime("%Y-%m-%d", time.localtime(time_created)) if time_created else "未知",
                "time_updated": time.strftime("%Y-%m-%d", time.localtime(time_updated)) if time_updated else "未知",
                "views": item.get("views", 0),
                "subscriptions": item.get("subscriptions", 0),
                "favorited": item.get("favorited", 0)
            })

        # 按创建时间排序（最新优先）
        items.sort(key=lambda x: x.get("time_created", "0"), reverse=True)

        return items

    except requests.RequestException as e:
        logging.error(f"SteamID {steam_id}: 抓取创意工坊内容时出错: {e}")
        print(f"SteamID {steam_id}: 抓取创意工坊内容时出错: {e}")
        return []

def main():
    print(f"开始抓取创意工坊内容...")
    print(f"使用输出文件: {DEFAULT_OUTPUT_FILE}，AppID: {DEFAULT_APPID}，SteamID: {STEAM_ID}")

    if not STEAM_API_KEY:
        print("错误：未设置 STEAM_API_KEY 环境变量。请使用 'export STEAM_API_KEY=your_key' 设置。")
        return

    # 加载白名单
    whitelist = load_whitelist(WHITELIST_FILE)
    if not whitelist:
        print("白名单为空，程序退出")
        return

    steam_id = STEAM_ID
    print(f"处理 SteamID: {steam_id}")

    items = get_workshop_maps(steam_id, STEAM_API_KEY, DEFAULT_APPID, whitelist=whitelist)

    if not items:
        print(f"SteamID {steam_id}: 未找到创意工坊内容")
    else:
        print(f"SteamID {steam_id}: 找到 {len(items)} 个创意工坊项目")
        for item in items:
            print(f"  - 类型: {'合集' if item['file_type'] == 2 else '地图'}")
            print(f"    标题: {item['title']}")
            print(f"    URL: {item['url']}")
            print(f"    文件ID: {item['id']}")
            print(f"    创建时间: {item['time_created']}")
            print(f"    更新时间: {item['time_updated']}")
            print(f"    作者: {item['creator']}")
            print(f"    文件大小: {item['file_size']}")
            print("    " + "-"*40)

    # 保存结果，移除 SteamID
    results = {
        "items": items
    }

    # 保存结果
    if results:
        try:
            with open(DEFAULT_OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n结果已保存到 {DEFAULT_OUTPUT_FILE}")
        except Exception as e:
            print(f"保存结果时出错: {e}")

if __name__ == "__main__":
    main()
