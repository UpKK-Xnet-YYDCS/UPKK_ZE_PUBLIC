import os
import requests
import sys
import json
from PIL import Image
from tqdm import tqdm  # 用于显示进度条

def validate_maps_file(file_path):
    """验证 maps.txt 文件的结构和内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = json.load(file)  # 直接加载 JSON 数据
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    errors = []
    for map_entry in content:
        map_name = map_entry.get("MapName")
        workshop_id = map_entry.get("WorkshopId")

        if not map_name:
            errors.append("Missing MapName in one of the entries.")
        if not workshop_id:
            errors.append(f"Missing WorkshopId for map {map_name or 'unknown'}.")

        # 检查 workshop_id 是否为有效数字
        if workshop_id and not workshop_id.isdigit():
            errors.append(f"Invalid WorkshopId '{workshop_id}' for map {map_name}.")

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
            data[f'publishedfileids[{j}]'] = workshop_id.strip()

        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
            all_details.extend(result['response']['publishedfiledetails'])
        else:
            print(f"Error fetching workshop details for batch starting at index {i}")

    return all_details

def extract_workshop_ids(file_path):
    """提取 maps.txt 文件中的 workshop_id 和 MapName"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = json.load(file)  # 直接加载 JSON 数据
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    workshop_ids = []
    workshop_to_mapname = {}
    for map_entry in content:
        map_name = map_entry.get("MapName", "").strip()
        workshop_id = map_entry.get("WorkshopId", "").strip()

        if workshop_id:
            workshop_ids.append(workshop_id)
            workshop_to_mapname[workshop_id] = map_name

    return workshop_ids, workshop_to_mapname

def download_preview_images(details, workshop_to_mapname):
    """根据 workshop_id 下载所有预览图并以 MapName 保存为 webp 格式"""
    preview_url_key = 'preview_url'
    download_dir = "map_previews_images"

    # 确保目录存在
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    total = len(details)
    for idx, detail in enumerate(tqdm(details, desc="Downloading previews", unit="file")):
        workshop_id = detail['publishedfileid']
        map_name = workshop_to_mapname.get(workshop_id, f"{workshop_id}")
        filename = f"{map_name}.webp"

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
        print("Usage: python DownloadPreviewImagesByMappingJson.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    # 验证文件结构和内容
    validate_maps_file(file_path)

    all_workshop_ids, workshop_to_mapname = extract_workshop_ids(file_path)

    # 显示 maps.txt 中找到的所有 workshop_id 的总数量
    print(f"maps.txt 中找到的所有 workshop_id 总数量: {len(all_workshop_ids)}")

    details = check_workshop_ids_in_batches(all_workshop_ids)

    # 下载预览图并转换为 webp 格式
    download_preview_images(details, workshop_to_mapname)

    # 显示 API 返回的 workshop_id 数量
    print(f"API 返回的 workshop_id 数量: {len(details)}")

if __name__ == "__main__":
    main()