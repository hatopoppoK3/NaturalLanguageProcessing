import datetime
import json
import pprint

import requests


def check_token() -> bool:
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


def get_access_token() -> None:
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


def get_requests_headers() -> dict:
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


def get_parse(sentence: str, sentence_class='default', dic_type=[]) -> dict:
    """
    構文解析を行う.

    Args:
        sentence (str): 構文解析対象
        sentence_class (str, optional):
            'default' or 'kuzure'. Defaults to 'default'.
        dic_type (list, optional):
            使用する専門用語辞書を指定. for Enterpriseのみ. Defaults to [].

    Returns:
        dict: 構文解析結果(レスポンス).
    """
    requests_headers = get_requests_headers()
    url = requests_headers.pop('base_url')+'nlp/v1/parse'
    requests_body = {'sentence': sentence,
                     'type': sentence_class, 'dic_type': dic_type}
    parse = requests.post(
        url=url, json=requests_body, headers=requests_headers)
    return parse.json()


def get_ne(sentence: str, sentence_class='default', dic_type=[]) -> dict:
    """
    固有表現抽出を行う.

    Args:
        sentence (str): 固有表現抽出対象
        sentence_class (str, optional):
            'default' or 'kuzure'. Defaults to 'default'.
        dic_type (list, optional):
            使用する専門用語辞書を指定. for Enterpriseのみ. Defaults to [].

    Returns:
        dict: 固有表現抽出結果(レスポンス).
    """
    requests_headers = get_requests_headers()
    url = requests_headers.pop('base_url')+'nlp/v1/ne'
    requests_body = {'sentence': sentence,
                     'type': sentence_class, 'dic_type': dic_type}
    ne = requests.post(
        url=url, json=requests_body, headers=requests_headers)
    return ne.json()


def get_coreference(document: str, document_class='default',
                    do_segment=False) -> dict:
    """
    照応解析を行う.

    Args:
        document (str): 照応解析対象
        document_class (str, optional):
            'default' or 'kuzure'. Defaults to 'default'.
        do_segment (bool, optional):
            文区切りを行うかどうか. Defaults to False.

    Returns:
        dict: 照応解析結果(レスポンス).
    """
    requests_headers = get_requests_headers()
    url = requests_headers.pop('base_url')+'nlp/v1/coreference'
    requests_body = {'document': document,
                     'type': document_class, 'do_segment': do_segment}
    coreference = requests.post(
        url=url, json=requests_body, headers=requests_headers)
    return coreference.json()


def get_keyword(document: str, document_class='default',
                do_segment=False, max_keyword_num=5, dic_type=[]) -> dict:
    """
    キーワード抽出を行う.

    Args:
        document (str): キーワード抽出対象.
        document_class (str, optional):
            'default' or 'kuzure'. Defaults to 'default'.
        do_segment (bool, optional):
            文区切りを行うかどうか. Defaults to False.
        max_keyword_num (int, optional):
            抽出するキーワード上限個数. Defaults to 5.
        dic_type (list, optional):
            使用する専門用語辞書を指定. for Enterpriseのみ. Defaults to [].

    Returns:
        dict: キーワード抽出結果(レスポンス)
    """
    requests_headers = get_requests_headers()
    url = requests_headers.pop('base_url')+'nlp/v1/keyword'
    requests_body = {'document': document, 'type': document_class,
                     'do_segment': do_segment,
                     'max_keyword_num': max_keyword_num,
                     'dic_type': dic_type}
    keyword = requests.post(
        url=url, json=requests_body, headers=requests_headers)
    return keyword.json()


def get_similarity(s1: str, s2: str, sentence_class='default',
                   dic_type=[]) -> dict:
    """
    類似度算出を行う。

    Args:
        s1 (str): 類似度算出対象テキスト1.
        s2 (str): 類似度算出対象テキスト2.
        sentence_class (str, optional):
            'default' or 'kuzure'. Defaults to 'default'.
        dic_type (list, optional):
            使用する専門用語辞書を指定. for Enterpriseのみ. Defaults to [].

    Returns:
        dict: 類似度算出結果(レスポンス)
    """
    requests_headers = get_requests_headers()
    url = requests_headers.pop('base_url')+'nlp/v1/similarity'
    requests_body = {'s1': s1, 's2': s2, 'type': sentence_class,
                     'dic_type': dic_type}
    similarity = requests.post(
        url=url, json=requests_body, headers=requests_headers)
    return similarity.json()


def get_sentence_type(sentence: str, sentence_class='default') -> dict:
    """
    文タイプ判定を行う。

    Args:
        sentence (str): 文タイプ判定対象テキスト.
        sentence_class (str, optional):
            'default' or 'kuzure'. Defaults to 'default'.

    Returns:
        dict: 文タイプ判定結果(レスポンス)
    """
    requests_headers = get_requests_headers()
    url = requests_headers.pop('base_url')+'nlp/v1/sentence_type'
    requests_body = {'sentence': sentence, 'type': sentence_class}
    sentence_type = requests.post(
        url=url, json=requests_body, headers=requests_headers)
    return sentence_type.json()


def get_user_attribute(document: str, sentence_class='default',
                       do_segment=False) -> dict:
    """
    ユーザ属性推定を行う.

    Args:
        document (str): ユーザ属性推定対象.
        sentence_class (str, optional):
            'default' or 'kuzure'. Defaults to 'default'.
        do_segment (bool, optional):
            文区切りを行うかどうか. Defaults to False.

    Returns:
        dict: ユーザ属性推定結果(レスポンス)
    """
    requests_headers = get_requests_headers()
    url = requests_headers.pop('base_url')+'nlp/beta/user_attribute'
    requests_body = {'document': document,
                     'type': sentence_class, 'do_segment': do_segment}
    user_attribute = requests.post(
        url=url, json=requests_body, headers=requests_headers)
    return user_attribute.json()


def get_remove_filler(text: str, do_segment=False) -> dict:
    """
    言い淀み除去を行う.

    Args:
        text (str): 言い淀み除去対象.
        do_segment (bool, optional):
            文区切りを行うかどうか. Defaults to False.

    Returns:
        dict: 言い淀み除去結果(レスポンス)
    """
    requests_headers = get_requests_headers()
    url = requests_headers.pop('base_url')+'nlp/beta/remove_filler'
    requests_body = {'text': text, 'do_segment': do_segment}
    remove_filler = requests.post(
        url=url, json=requests_body, headers=requests_headers)
    return remove_filler.json()


def get_detect_misrecognition(sentence: str) -> dict:
    """
    音声認識誤り検知を行う.

    Args:
        sentence (str): 音声認識誤り検知対象.

    Returns:
        dict: 音声認識誤り検知結果(レスポンス)
    """
    requests_headers = get_requests_headers()
    url = requests_headers.pop('base_url')+'nlp/beta/detect_misrecognition'
    requests_body = {'sentence': sentence}
    detect_misrecognition = requests.post(
        url=url, json=requests_body, headers=requests_headers)
    return detect_misrecognition.json()


def get_sentiment(sentence: str) -> dict:
    """
    感情分析を行う.

    Args:
        sentence (str): 感情分析対象.

    Returns:
        dict: 感情分析結果(レスポンス)
    """
    requests_headers = get_requests_headers()
    url = requests_headers.pop('base_url')+'nlp/v1/sentiment'
    requests_body = {'sentence': sentence}
    sentiment = requests.post(
        url=url, json=requests_body, headers=requests_headers)
    return sentiment.json()


def get_summary(document: str, sent_len: int) -> dict:
    """
    要約を行う.

    Args:
        document (str): 要約対象.
        sent_len (int): 要約文数.

    Returns:
        dict: 要約結果(レスポンス)
    """
    requests_headers = get_requests_headers()
    url = requests_headers.pop('base_url')+'nlp/beta/summary'
    requests_body = {'document': document, 'sent_len': sent_len}
    summary = requests.post(
        url=url, json=requests_body, headers=requests_headers)
    return summary.json()


if __name__ == "__main__":
    # アクセストークンの有効期限の確認
    if not(check_token()):
        get_access_token()
        print('Update Access Token')

    # 構文解析
    print('構文解析')
    test_text = '犬は歩く。'
    parse = get_parse(test_text)
    pprint.pprint(parse)
    print()

    # 固有表現抽出
    print('固有表現抽出')
    test_text = '昨日は東京駅を利用した。'
    ne = get_ne(test_text)
    pprint.pprint(ne)
    print()

    # 照応解析
    print('照応解析')
    test_text = '太郎は友人です。彼は焼き肉を食べた。'
    coreference = get_coreference(test_text)
    pprint.pprint(coreference)
    print()

    # キーワード抽出
    print('キーワード抽出')
    test_text = 'レストランで昼食を食べた。'
    keyword = get_keyword(test_text)
    pprint.pprint(keyword)
    print()

    # 類似度算出
    print('類似度算出')
    test_text1 = '近くのレストランはどこですか？'
    test_text2 = 'このあたりの定食屋はどこにありますか？'
    similarity = get_similarity(test_text1, test_text2)
    pprint.pprint(similarity)
    print()

    # 文タイプ判定
    print('文タイプ判定')
    test_text = 'あなたの名前は何ですか？'
    sentence_type = get_sentence_type(test_text)
    pprint.pprint(sentence_type)
    print()

    # ユーザ属性推定
    print('ユーザ属性推定')
    test_text = '私は昨日田町駅で飲みに行ったら奥さんに怒られた。'
    user_attribute = get_user_attribute(test_text)
    pprint.pprint(user_attribute)
    print()

    # 言い淀み除去
    print('言い淀み除去')
    test_text = '''えーーっと、あの、今日の打ち合わせでしたっけ。
                    すみません、ちょっと、急用が入ってしまって。'''
    remove_filler = get_remove_filler(test_text)
    pprint.pprint(remove_filler)
    print()

    # 音声認識誤り検知
    print('音声認識誤り検知')
    test_text = '温泉認識は誤りを起こす'
    detect_misrecognition = get_detect_misrecognition(test_text)
    pprint.pprint(detect_misrecognition)
    print()

    # 感情分析
    print('感情分析')
    test_text = '人生の春を謳歌しています'
    sentiment = get_sentiment(test_text)
    pprint.pprint(sentiment)
    print()

    # 要約
    print('要約')
    test_text = '''
                前線が太平洋上に停滞しています。
                一方、高気圧が千島近海にあって、北日本から東日本をゆるやかに覆っています。
                関東地方は、晴れ時々曇り、ところにより雨となっています。
                東京は、湿った空気や前線の影響により、晴れ後曇りで、夜は雨となるでしょう。
                '''
    summary = get_summary(test_text, 1)
    pprint.pprint(summary)
    print()
