import datetime
import json
import pprint

import requests


def check_token():
    """
    アクセストークンの有効期限を確認する.

    Returns:
        bool: 有効期限内ならばTrue,そうでなければFalse.
    """
    now_datetime = datetime.datetime.now()
    now_time = now_datetime.timestamp()
    with open('./COTOHA/access.json', mode='r', encoding='utf-8') as rf:
        access_json = json.load(rf)
        limit_time = float(access_json['limit_time'])
        if now_time < limit_time:
            return True
        else:
            return False


def get_access_token():
    """
    client.json(認証情報)を読み込みアクセストークンを取得する.
    取得したアクセストークンを有効期限と共にaccess.jsonへ書き込む.
    """
    with open('./COTOHA/client.json', mode='r', encoding='utf-8') as rf:
        headers_data = json.load(rf)
        # Access Token Publish URL取得
        url = headers_data.pop('url')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, json=headers_data, headers=headers)
        response_json = response.json()
        # 有効期限取得(ミリ秒なので下三桁切り捨て)
        issued_at = float(response_json['issued_at'][:-3])
        access_token = response_json['access_token']
    with open('./COTOHA/access.json', mode='r', encoding='utf-8') as rf:
        access_json = json.load(rf)
        # 有効期限は1日(86400ミリ秒)なのでそれを加算して記録
        access_json['limit_time'] = issued_at+86400
        access_json['Authorization'] = 'Bearer '+access_token
    with open('./COTOHA/access.json', mode='w', encoding='utf-8') as wf:
        json.dump(access_json, fp=wf, indent=4)


def get_requests_headers():
    """
    API使用時のリクエストヘッダーを取得する.

    Returns:
        dict: リクエストヘッダー.
    """
    with open('./COTOHA/access.json', mode='r', encoding='utf-8') as rf:
        requests_headers = json.load(rf)
        # limit_timeは必要ないため削除
        del requests_headers['limit_time']
        return requests_headers


def get_parse_response(sentence: str, sentence_type='default', dic_type=[]):
    """
    Args:
        sentence (str): 構文解析対象
        sentence_type (str, optional):
            'default' or 'kuzure'. Defaults to 'default'.
        dic_type (list, optional):
            使用する専門用語辞書を指定. for Enterpriseのみ. Defaults to [].

    Returns:
        dict: 構文解析の結果(レスポンス).
    """
    requests_headers = get_requests_headers()
    url = requests_headers.pop('base_url')+'nlp/v1/parse'
    requests_body = {'sentence': sentence,
                     'type': sentence_type, 'dic_type': dic_type}
    parse_response = requests.post(
        url=url, json=requests_body, headers=requests_headers)
    return parse_response.json()


if __name__ == "__main__":
    # アクセストークンの有効期限の確認
    if not(check_token()):
        get_access_token()
        print('Update Access Token')

    # 構文解析について
    parse_response = get_parse_response('犬は歩く。')
    pprint.pprint(parse_response)
