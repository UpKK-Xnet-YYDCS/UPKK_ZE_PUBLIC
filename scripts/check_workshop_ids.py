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

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_workshop_ids.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Regex to find workshop_id and filename pairs
    pattern = re.compile(r'"workshop_id"\s*"\s*(\d+)"\s*.*?"filename"\s*"\s*([^"]+)"', re.DOTALL)
    matches = pattern.findall(content)

    if not matches:
        print("No workshop IDs found in the file.")
        print('::set-output name=result::failure')
        sys.exit(1)

    workshop_ids = [match[0] for match in matches]
    file_map = {match[0]: match[1] for match in matches}

    details = check_workshop_ids(workshop_ids)
    unavailable_ids = []
    available_ids = []
    for detail in details:
        workshop_id = detail['publishedfileid']
        name = detail.get('title', 'Unknown Title')
        filename = file_map[workshop_id]
        if detail['result'] == 1:
            available_ids.append(f"{workshop_id} ({name}) with filename: {filename}")
        else:
            unavailable_ids.append(f"{workshop_id} ({name}) with filename: {filename}")

    if unavailable_ids:
        print(f"\033[91mUnavailable IDs: {', '.join(unavailable_ids)}\033[0m")
        print('::set-output name=result::failure')
        sys.exit(1)  # Ensure the script exits with a non-zero status code
    else:
        print(f"\033[92mAvailable IDs: {', '.join(available_ids)}\033[0m")
        print('::set-output name=result::success')

if __name__ == "__main__":
    main()