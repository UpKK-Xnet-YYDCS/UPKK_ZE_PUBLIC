import requests
import sys
import re

def parse_keyvalue(content):
    """解析 KeyValue 格式的内容，并转换为字典"""
    pattern = re.compile(r'"([^"]+)"\s*"([^"]+)"')
    matches = pattern.findall(content)
    data = {}
    for match in matches:
        key, value = match
        data[key] = value
    return data

def validate_maps_file(file_path):
    """验证 maps.txt 文件的结构和内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    pattern = re.compile(r'"([^"]+)"\s*\{([^}]+)\}', re.DOTALL)
    matches = pattern.findall(content)

    errors = []
    for key, value in matches:
        data = parse_keyvalue(value)
        workshop_id = data.get("workshop_id")
        enabled = data.get("enabled", "1")
        filename = data.get("filename")

        if not workshop_id:
            errors.append(f"Missing workshop_id in map {key}")
        if not filename:
            errors.append(f"Missing filename in map {key}")

        # Additional checks for valid values
        if workshop_id and not re.match(r"^\d+$", workshop_id):
            errors.append(f"Invalid workshop_id '{workshop_id}' in map {key}")
        if enabled and enabled not in ["0", "1"]:
            errors.append(f"Invalid enabled value '{enabled}' in map {key}")

    if errors:
        print("Validation errors found:")
        for error in errors:
            print(error)
        sys.exit(1)
    else:
        print("No validation errors found. File is valid.")

def check_workshop_ids_in_batches(workshop_ids, batch_size=100):
    """批量检查 workshop_id 的有效性"""
    url = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    all_details = []

    for i in range(0, len(workshop_ids), batch_size):
        batch = workshop_ids[i:i + batch_size]
        data = {'itemcount': len(batch)}
        for j, workshop_id in enumerate(batch):
            data[f'publishedfileids[{j}]'] = workshop_id.strip()  # 去除前后空格

        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
            all_details.extend(result['response']['publishedfiledetails'])
        else:
            print(f"Error fetching workshop details for batch starting at index {i}")

    return all_details

def recheck_unavailable_id(workshop_id):
    """重新检查不可用的 workshop_id"""
    url = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    data = {'itemcount': 1, 'publishedfileids[0]': workshop_id.strip()}  # 去除前后空格

    response = requests.post(url, data=data)
    if response.status_code == 200:
        result = response.json()
        if 'publishedfiledetails' in result['response']:
            return result['response']['publishedfiledetails'][0]
    return None

def check_steam_community_page(workshop_id):
    """检查 Steam 社区页面是否包含 SubscribeItemOptionAdd"""
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={workshop_id.strip()}"  # 去除前后空格
    response = requests.get(url)
    if response.status_code == 200:
        return "SubscribeItemOptionAdd" in response.text
    elif response.status_code == 404:
        return False  # 页面不存在，标记为不可用
    return None  # 状态码不是 200 或 404，不确定是否可用

def update_maps_file(file_path, unavailable_ids):
    """更新 maps.txt 文件，将不可用的 workshop_id 的 enabled 设置为 0"""
    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            content = file.read()
            for workshop_id in unavailable_ids:
                pattern = re.compile(r'("workshop_id"\s*"\s*' + workshop_id + r'"\s*.*?"enabled"\s*")1(\s*")', re.IGNORECASE | re.DOTALL)
                new_content = pattern.sub(r'\g<1>0\2', content)
                if new_content != content:
                    print(f"Updated workshop_id {workshop_id} to enabled 0")
                content = new_content

            # 将修改后的内容写回文件
            file.seek(0)
            file.write(content)
            file.truncate()
    except Exception as e:
        print(f"Error updating file: {e}")
        sys.exit(1)

def extract_workshop_ids(file_path):
    """提取 maps.txt 文件中的 workshop_id 和 filename"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    pattern = re.compile(r'"([^"]+)"\s*\{([^}]+)\}', re.DOTALL)
    matches = pattern.findall(content)

    workshop_ids = []
    workshop_to_filename = {}
    for key, value in matches:
        data = parse_keyvalue(value)
        workshop_id = data.get("workshop_id", "").strip()
        filename = data.get("filename", "").strip()
        enabled = data.get("enabled", "1").strip()  # 默认值为 "1"
        if workshop_id and enabled == "1":
            workshop_ids.append(workshop_id)
            workshop_to_filename[workshop_id] = filename

    return workshop_ids, workshop_to_filename, matches

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_workshop_ids.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    # 验证文件结构和内容
    validate_maps_file(file_path)

    all_workshop_ids, workshop_to_filename, matches = extract_workshop_ids(file_path)

    # 显示 maps.txt 中找到的所有 workshop_id 的总数量
    print(f"maps.txt 中找到的所有 workshop_id 总数量: {len(all_workshop_ids)}")

    details = check_workshop_ids_in_batches(all_workshop_ids)

    # 显示 API 返回的 workshop_id 数量
    print(f"API 返回的 workshop_id 数量: {len(details)}")

    unavailable_ids = []
    available_ids = []
    for detail in details:
        workshop_id = detail['publishedfileid']
        name = detail.get('title', 'Unknown Title')
        filename = workshop_to_filename.get(workshop_id, "Unknown Filename")
        print(f"Checking {workshop_id} ({name}) with filename {filename}")
        if detail['result'] == 1:
            available_ids.append(f"{workshop_id} ({name})")
        else:
            unavailable_ids.append((workshop_id, filename))

    # 对状态不是1的进行再次确认
    if unavailable_ids:
        confirmed_unavailable_ids = []
        for workshop_id, filename in unavailable_ids:
            detail = recheck_unavailable_id(workshop_id)
            if detail and detail['result'] == 1:
                available_ids.append(f"{detail['publishedfileid']} ({detail.get('title', 'Unknown Title')})")
            else:
                # 通过 Steam 社区页面进行最终确认
                check_result = check_steam_community_page(workshop_id)
                if check_result is False:
                    confirmed_unavailable_ids.append((workshop_id, filename))

        if confirmed_unavailable_ids:
            update_maps_file(file_path, [workshop_id for workshop_id, _ in confirmed_unavailable_ids])
            print('::set-output name=result::failure')
            with open("unavailable_ids.txt", "w") as f:
                for workshop_id, filename in confirmed_unavailable_ids:
                    f.write(f"{workshop_id} (filename: {filename})\n")
            print("不可用 IDs 汇总:")
            for workshop_id, filename in confirmed_unavailable_ids:
                print(f"\033[91m{workshop_id} (filename: {filename})\033[0m")
        else:
            print(f"\033[92m可用 IDs: {', '.join(available_ids)}\033[0m")
            print('::set-output name=result::success')
    else:
        print(f"\033[92m可用 IDs: {', '.join(available_ids)}\033[0m")
        print('::set-output name=result::success')

    # 输出所有 enabled 为 0 的地图条目
    print("\n以下是所有 enabled 为 0 的地图条目:")
    for key, value in matches:
        data = parse_keyvalue(value)
        workshop_id = data.get("workshop_id")
        enabled = data.get("enabled", "1")
        filename = data.get("filename")
        if enabled == "0":
            print(f"workshop_id: {workshop_id}, filename: {filename}")

    # 输出最后找到的内容区块
    print("\n最后找到的内容区块:")
    if workshop_to_filename:
        last_key = next(reversed(workshop_to_filename))
        print(f'workshop_id: {last_key}, filename: {workshop_to_filename[last_key]}')
    
    if unavailable_ids and confirmed_unavailable_ids:
        sys.exit(1)  # 确保脚本以非零状态码退出

if __name__ == "__main__":
    main()