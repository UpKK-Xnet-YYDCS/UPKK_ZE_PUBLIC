import requests
import sys

def check_workshop_id(workshop_id):
    url = f"https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    data = {
        'itemcount': 1,
        'publishedfileids[0]': workshop_id
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        result = response.json()
        if result['response']['publishedfiledetails'][0]['result'] == 1:
            return True
    return False

def main():
    # 获取新增的内容
    added_lines = sys.stdin.read().splitlines()

    unavailable_ids = []
    available_ids = []
    for line in added_lines:
        if 'workshop_id' in line:
            workshop_id = line.split('"')[3]
            if check_workshop_id(workshop_id):
                available_ids.append(workshop_id)
            else:
                unavailable_ids.append(workshop_id)

    if unavailable_ids:
        print(f"\033[91mUnavailable IDs: {', '.join(unavailable_ids)}\033[0m")
        print('::set-output name=result::failure')
    else:
        print(f"\033[92mAvailable IDs: {', '.join(available_ids)}\033[0m")
        print('::set-output name=result::success')

if __name__ == "__main__":
    main()