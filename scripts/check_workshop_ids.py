import requests
import sys
import re

def check_workshop_ids(workshop_ids):
    url = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    data = {
        'itemcount': len(workshop_ids),
    }
    for i, workshop_id in enumerate(workshop_ids):
        data[f'publishedfileids[{i}]'] = workshop_id

    response = requests.post(url, data=data)
    if response.status_code == 200:
        result = response.json()
        return result['response']['publishedfiledetails']
    return []

def update_maps_file(file_path, unavailable_ids):
    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            content = file.read()

            for workshop_id in unavailable_ids:
                # 使用正则表达式查找并替换 enabled 字段
                pattern = re.compile(r'("workshop_id"\s*"\s*' + workshop_id + r'"\s*.*?"enabled"\s*")1(\s*")', re.DOTALL)
                content = pattern.sub(r'\g<1>0\2', content)

            # 将修改后的内容写回文件
            file.seek(0)
            file.write(content)
            file.truncate()
    except Exception as e:
        print(f"Error updating file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("用法: python check_workshop_ids.py <文件路径>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        sys.exit(1)

    # 正则表达式查找 workshop_id 和相关字段
    pattern = re.compile(r'"workshop_id"\s*"\s*(\d+)"\s*.*?"filename"\s*"\s*([^"]+)"\s*.*?"enabled"\s*"\s*(\d)"', re.DOTALL)
    matches = pattern.findall(content)

    if not matches:
        print("文件中未找到任何 workshop IDs。")
        print('::set-output name=result::failure')
        sys.exit(1)

    workshop_ids = [match[0] for match in matches]
    file_map = {match[0]: match[1] for match in matches}
    enabled_map = {match[0]: match[2] for match in matches}

    details = check_workshop_ids(workshop_ids)
    unavailable_ids = []
    available_ids = []
    for detail in details:
        workshop_id = detail['publishedfileid']
        name = detail.get('title', 'Unknown Title')
        filename = file_map[workshop_id]
        enabled = enabled_map[workshop_id]
        if detail['result'] == 1:
            available_ids.append(f"{workshop_id} ({name}) 文件名: {filename}")
        else:
            if enabled == '1':  # 仅考虑 enabled 字段为 '1' 的 workshop_ids
                unavailable_ids.append(workshop_id)
                print(f"\033[91m不可用 ID: {workshop_id} ({name}) 文件名: {filename}\033[0m")

    if unavailable_ids:
        update_maps_file(file_path, unavailable_ids)
        print('::set-output name=result::failure')
        sys.exit(1)  # 确保脚本以非零状态码退出
    else:
        print(f"\033[92m可用 IDs: {', '.join(available_ids)}\033[0m")
        print('::set-output name=result::success')

if __name__ == "__main__":
    main()