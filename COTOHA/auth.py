import json

import requests


def get_access_token():
    with open('./COTOHA/client.json', 'r', encoding='utf-8') as rf:
        headers_data = json.load(rf)
        url = headers_data['url']
        headers_data.pop('url')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, json=headers_data, headers=headers)
        response_json = response.json()
        with open('./COTOHA/access.json', 'w', encoding='utf-8') as wf:
            json.dump(response_json, wf, indent=4)


if __name__ == "__main__":
    get_access_token()
