import re
import sys
import requests

def parse_keyvalue(content):
    """解析 KeyValue 格式的内容，并转换为字典"""
    pattern = re.compile(r'"([^"]+)"\s*"([^"]+)"')
    matches = pattern.findall(content)
    data = {}
    for match in matches:
        key, value = match
        data[key] = value
    return data

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

def check_workshops_in_collections(collection_ids, workshop_ids, batch_size=50):
    """批量检查合集中的 workshop_id"""
    url = "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    results_in = []
    results_not_in = []

    for collection_id in collection_ids:
        for i in range(0, len(workshop_ids), batch_size):
            batch = workshop_ids[i:i + batch_size]
            data = {
                'collectioncount': 1,
                'publishedfileids[0]': collection_id
            }
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                result = response.json()
                if 'collectiondetails' in result['response']:
                    collection_details = result['response']['collectiondetails'][0]
                    if collection_details['result'] == 1:
                        found_ids = [item['publishedfileid'] for item in collection_details['children']]
                        for workshop_id in batch:
                            if workshop_id in found_ids:
                                results_in.append(workshop_id)
                            else:
                                results_not_in.append(workshop_id)
            else:
                print(f"Error fetching collection details for collection ID {collection_id}: {response.status_code}")

    return results_in, results_not_in

def main():
    if len(sys.argv) < 3:
        print("Usage: python check_workshop_in_collection.py <file_path> <collection_id1> <collection_id2> ... <collection_idN>")
        sys.exit(1)

    file_path = sys.argv[1]
    collection_ids = sys.argv[2:]

    # 提取 workshop_id
    print(f"Extracting workshop IDs from {file_path}...")
    workshop_ids, workshop_to_filename, _ = extract_workshop_ids(file_path)
    print(f"Found {len(workshop_ids)} workshop IDs.")

    # 批量检查合集
    print(f"Checking if workshop IDs are in the specified collections...")
    results_in, results_not_in = check_workshops_in_collections(collection_ids, workshop_ids)

    # 输出总结
    print("\nSummary:")
    print(f"Workshop IDs in the collections: {', '.join(results_in)}")
    print(f"Workshop IDs NOT in the collections: {', '.join(results_not_in)}")

    if results_not_in:
        print('::set-output name=result::failure')
    else:
        print('::set-output name=result::success')

if __name__ == "__main__":
    main()
    