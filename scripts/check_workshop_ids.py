import requests
import json

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
    with open('cs2/counterstrikesharp/configs/plugins/MapChooser/maps.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    unavailable_ids = []
    for line in lines:
        if 'workshop_id' in line:
            workshop_id = line.split('"')[3]
            if not check_workshop_id(workshop_id):
                unavailable_ids.append(workshop_id)

    if unavailable_ids:
        with open('cs2/counterstrikesharp/configs/plugins/MapChooser/maps.txt', 'w', encoding='utf-8') as file:
            for line in lines:
                if any(workshop_id in line for workshop_id in unavailable_ids):
                    line = line.replace('"enabled"		"1"', '"enabled"		"0"')
                file.write(line)
        print('::set-output name=result::failure')
    else:
        print('::set-output name=result::success')

if __name__ == "__main__":
    main()
