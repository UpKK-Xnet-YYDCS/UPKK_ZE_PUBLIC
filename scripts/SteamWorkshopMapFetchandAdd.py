import requests
import json
import time
import os
import subprocess
import argparse

# 配置
STEAM_API_KEY = os.getenv("STEAM_API_KEY")  # 从环境变量加载 API 密钥
BASE_URL = "https://api.steampowered.com"
DEFAULT_OUTPUT_FILE = "workshop_maps.json"
DEFAULT_APPID = 730  # 默认 CS:GO/CS2 AppID
DEFAULT_WHITELIST_FILE = "scripts/workshop_white_steam64.txt"  # 默认白名单文件
DEFAULT_BLACKLIST_FILE = "scripts/workshop_black_steam64.txt"  # 默认黑名单文件
DEFAULT_ITEM_BLACKLIST_FILE = "scripts/workshop_item_black_lists.txt"  # 工坊单个项目黑名单文件


def load_whitelist(file_path):
    """从文件加载白名单列表"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            whitelist = {line.strip() for line in f if line.strip()}  # 使用集合避免重复
        return whitelist
    except FileNotFoundError:
        print(f"错误：白名单文件 {file_path} 未找到")
        return set()
    except Exception as e:
        print(f"读取白名单文件时出错: {e}")
        return set()

def load_blacklist(file_path):
    """从文件加载黑名单列表"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            blacklist = {line.strip() for line in f if line.strip()}  # 使用集合避免重复
        return blacklist
    except FileNotFoundError:
        print(f"错误：黑名单文件 {file_path} 未找到")
        return set()
    except Exception as e:
        print(f"读取黑名单文件时出错: {e}")
        return set()


def load_item_blacklist(file_path):
    """从文件加载项目黑名单列表"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            item_blacklist = {line.strip() for line in f if line.strip()}  # 使用集合避免重复
        return item_blacklist
    except FileNotFoundError:
        print(f"错误：项目黑名单文件 {file_path} 未找到")
        return set()
    except Exception as e:
        print(f"读取项目黑名单文件时出错: {e}")
        return set()



def get_workshop_maps(api_key, appid=730, search_prefix="ze_", whitelist=None, blacklist=None, itemblacklist=None, numperpage=200, page_count=1):
    """获取用户上传的所有创意工坊内容（地图和合集），并过滤不在白名单中的作者和黑名单中的作者"""
    url = f"{BASE_URL}/IPublishedFileService/QueryFiles/v1/"
    items = []

    for page in range(1, page_count + 1):
        params = {
            "key": api_key,
            "query_type": 1,  # 排序依据：按发布时间排序
            "appid": appid,
            "numperpage": numperpage,  # 每页最大数量，动态传入
            "return_details": True,
            "search_text": search_prefix,  # 使用参数作为搜索文本
            "return_tags": True,
            "return_kv_tags": True,
            "return_previews": True,
            "return_children": True,
            "filetype": 0,
            "page": page  # 分页参数
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # 检查是否有数据
            if not data.get("response") or not data["response"].get("publishedfiledetails"):
                break  # 如果没有数据了，停止分页请求

            # 提取内容信息
            for item in data["response"]["publishedfiledetails"]:
                if item.get("result") != 1:  # 1 表示成功
                    continue


                # 检查是否有CS2 标签 以防止CSGO地图
                tags = item.get("tags", [])
                if not any(tag.get("tag", "").lower() == "cs2" for tag in tags):
                    print(f"忽略项目 {item_id}，因为它没有 CS2 标签")
                    continue

               # 如果项目 ID 在黑名单里，跳过此项目
                item_id = str(item.get("publishedfileid"))
                if itemblacklist and item_id in itemblacklist:
                    print(f"忽略项目 {item_id}，因为它在单个项目黑名单中")
                    continue

                # 如果创作者在黑名单里，跳过此项目
                creator = str(item.get("creator"))
                if blacklist and creator in blacklist:
                    print(f"忽略创作者 {creator}，因为他们在黑名单中 地图ID是{item_id} ")
                    continue

                # 如果创作者不在白名单里，且白名单不为空，则跳过此项目
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
        except requests.RequestException as e:
            print(f"抓取创意工坊内容时出错: {e}")
            break

    # 按创建时间排序（最新优先）
    items.sort(key=lambda x: x.get("time_created", "0"), reverse=True)

    return items

def main():
    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(description="抓取 Steam 创意工坊内容")
    parser.add_argument(
        "--map_file_path", 
        help="MapChooser 配置文件路径 (cs2/counterstrikesharp/configs/plugins/MapChooser/maps.txt)",
        required=True  # 强制要求传入此参数
    )
    parser.add_argument(
        "--whitelist_file", 
        help="白名单文件路径 (例如 scripts/workshop_white_steam64.txt)",
        default=DEFAULT_WHITELIST_FILE  # 如果没有传入则使用默认值
    )
    parser.add_argument(
        "--blacklist_file", 
        help="黑名单文件路径 (例如 scripts/workshop_black_steam64.txt)",
        default=DEFAULT_BLACKLIST_FILE  # 如果没有传入则使用默认值
    )
    parser.add_argument(
        "--blacklist_item_file", 
        help="黑名单文件路径 (例如 scripts/workshop_item_black_lists.txt)",
        default=DEFAULT_ITEM_BLACKLIST_FILE  # 如果没有传入则使用默认值
    )

    parser.add_argument(
        "--search_prefix", 
        help="搜索前缀，默认为 'ze_'",
        default="ze_"  # 默认前缀
    )
    parser.add_argument(
        "--numperpage", 
        type=int,
        help="每页的最大数量，默认为 200",
        default=200  # 默认每页 200 个项目
    )
    parser.add_argument(
        "--page_count", 
        type=int,
        help="获取的总页数，默认为 1",
        default=1  # 默认获取 1 页
    )

    args = parser.parse_args()

    # 检查路径参数
    if not args.map_file_path:
        print("错误：必须传入 MapChooser的 maps 配置文件路径参数。")
        return

    print(f"开始抓取创意工坊内容...")
    print(f"使用输出文件: {DEFAULT_OUTPUT_FILE}，AppID: {DEFAULT_APPID}")

    if not STEAM_API_KEY:
        print("错误：未设置 STEAM_API_KEY 环境变量。请使用 'export STEAM_API_KEY=your_key' 设置, Windows系统 使用 set")
        return

    # 加载白名单和黑名单
    whitelist = load_whitelist(args.whitelist_file)
    blacklist = load_blacklist(args.blacklist_file)
    itemblacklist = load_item_blacklist(args.blacklist_item_file)

    if not whitelist:
        print(f"白名单文件 {args.whitelist_file} 为空或加载失败，将不过滤创作者。")
    
    if not blacklist:
        print(f"黑名单文件 {args.blacklist_file} 为空或加载失败，将不过滤创作者。")

    if not itemblacklist:
        print(f"工坊内容单个黑名单文件 {args.blacklist_item_file} 为空或加载失败,将不过过滤单个文件id。")

    # 获取创意工坊内容
    items = get_workshop_maps(
        STEAM_API_KEY, 
        DEFAULT_APPID, 
        search_prefix=args.search_prefix, 
        whitelist=whitelist, 
        blacklist=blacklist,
        itemblacklist=itemblacklist,
        numperpage=args.numperpage,  # 每页最大数量
        page_count=args.page_count  # 获取的页数
    )

    if not items:
        print(f"未找到创意工坊内容")
    else:
        print(f"找到 {len(items)} 个创意工坊项目")
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
            # 传递 id 和 title 到 add_map.py 脚本
            try:
                subprocess.run(["python3", "scripts/add_map.py", args.map_file_path, item["title"], str(item["id"])], check=True)
            except subprocess.CalledProcessError as e:
                print(f"运行 add_map.py 脚本时出错 (地图 {item['title']} ID: {item['id']}): {e}")

if __name__ == "__main__":
    main()
