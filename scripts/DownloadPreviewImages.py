import os
import requests
import sys
import re
from PIL import Image
from tqdm import tqdm  # 用于显示进度条

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

def download_preview_images(details, workshop_to_filename):
    """根据 workshop_id 下载所有预览图并以 filename 保存为 webp 格式"""
    preview_url_key = 'preview_url'  # API 返回的 key，用于获取预览图 URL
    download_dir = "previews"  # 保存预览图的目录

    # 确保目录存在
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    total = len(details)
    for idx, detail in enumerate(tqdm(details, desc="Downloading previews", unit="file")):
        workshop_id = detail['publishedfileid']
        filename = workshop_to_filename.get(workshop_id, f"{workshop_id}.webp")
        
        # 添加检查，确保文件名以 .webp 结尾
        if not filename.endswith(".webp"):
            filename += ".webp"
        
        webp_path = os.path.join(download_dir, filename)
        if os.path.exists(webp_path):
            print(f"[{idx + 1}/{total}] File {filename} already exists. Skipping...")
            continue

        preview_url = detail.get(preview_url_key)

        if preview_url:
            try:
                response = requests.get(preview_url, stream=True)
                if response.status_code == 200:
                    temp_jpg_path = os.path.join(download_dir, f"{workshop_id}.jpg")
                    with open(temp_jpg_path, 'wb') as image_file:
                        for chunk in response.iter_content(1024):
                            image_file.write(chunk)
                    
                    # 转换为 webp 格式
                    with Image.open(temp_jpg_path) as img:
                        img.save(webp_path, 'webp', quality=70)
                    os.remove(temp_jpg_path)  # 删除临时的 jpg 文件
                    print(f"[{idx + 1}/{total}] Downloaded and converted preview for {workshop_id} as {filename}")
                else:
                    print(f"[{idx + 1}/{total}] Failed to download preview for {workshop_id}: HTTP {response.status_code}")
            except Exception as e:
                print(f"[{idx + 1}/{total}] Error downloading or converting preview for {workshop_id}: {e}")
        else:
            print(f"[{idx + 1}/{total}] No preview URL found for {workshop_id}")
        print(f"Remaining: {total - idx - 1}")

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

    # 下载预览图并转换为 webp 格式
    download_preview_images(details, workshop_to_filename)

    # 显示 API 返回的 workshop_id 数量
    print(f"API 返回的 workshop_id 数量: {len(details)}")

if __name__ == "__main__":
    main()