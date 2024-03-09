import json
import re
import requests
from bs4 import BeautifulSoup
import datetime

def get_text_detail(url):
    cookies = {
        'BAIDU_SSP_lcr': 'https://www.google.com/',
        'SUB': '_2A25JOx8YDeRhGeNI41cT9CzIzjiIHXVqx6FQrDV6PUJbktANLRLbkW1NSDGezUx-jDi5M3ChvsGbxz1tAWRMgd6x',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5YuffAHEOr7NWB8PUSHKz55NHD95QfSonfeoBESh-XWs4DqcjVi--4iKn7iK.Ni--ci-8siK.Xi--Xi-zRiKy2i--4iKn7iK.NSKqRSKzXeoBfS5tt',
        'WEIBOCN_FROM': '1110006030',
        '__bid_n': '187992d1f6d920dbe84207',
        '_T_WM': '13968635202',
        'MLOGIN': '1',
        'BAIDU_SSP_lcr': 'https://www.google.com.hk/',
        'FPTOKEN': '28mhzisvkMxdUM4qcjdltqW4T6JOK819AeQGeaCEbhJVSo+MKeeeT4LTbtC6pcnmE9+P7kDSfJEzm7B6/dnkUv9vKNHpEQm8uhyU9wbMfMKWecxUuTawSEVh13Th5UItlwBc4OvQnZK7BWwyWcw+pqb5YMHn2I2rz6Uh6j5cmRE5S1d2aFrm2bkQCn2Ok8PdTnXbxd7eFXf1m4MsgxEwyWOzIy42CCxBul0Wo8S7ePscv5JZHChmb/LLUC8Wi+qUcMWWcsfoz6rIsoM85V+jtkmRG5SbH7gb+wKDzRsIILA/FmAZK9HNFRhb4ihaD5yNR+IAKeunuah7y3Igt7BMuuyFeGL+3eUvz4ICLqKxP62c9/CPLG5kERNJMDb42JsZDyLoJLDJyW15MNY7UMbWQQ==|v3XpfgtpBtM61pwiYFCJR16nENXNTVcI8wST0HVcA2I=|10|423f350117b43823f2487f227b08a80b',
        'XSRF-TOKEN': '75c4a9',
        'mweibo_short_token': 'b869032a49',
        'M_WEIBOCN_PARAMS': 'oid%3D4886854849529005%26luicode%3D10000011%26lfid%3D100103type%253D60%2526q%253D%25E6%25B1%259F%25E8%258B%258F%25E5%25A4%25A7%25E5%25AD%25A6%2526t%253D%26uicode%3D20000061%26fid%3D4886854849529005',
    }
    headers = {
        'authority': 'm.weibo.cn',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }
    response = requests.get(url, cookies=cookies, headers=headers)
    html = response.content.decode('utf-8')
    html_text = BeautifulSoup(html, features="lxml")
    html_value = html_text.find_all('script')[2].get_text()
    text = re.findall('"text": "(.*?)",', html_value)[0]
    result = handle_tagg(text)
    return result
def get_comment(mid, id_):
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    params = {
        'id': id_,
        'mid': mid,
        'max_id_type': '0',
    }
    response = requests.get('https://m.weibo.cn/comments/hotflow', params=params, headers=headers)
    data = json.loads(response.text)
    try:
        data_list = data['data']['data']
        comments = []
        for i, data in enumerate(data_list):
            text = handle_tagg(data['text'])
            if not text:
                text = "非文本"
            user_name = data['user']['screen_name']
            ctime = handle_time(data['created_at'])
            comments.append([user_name, ctime, text])
            if data['comments']:
                for data_ in data['comments']:
                    text = handle_tagg(data_['text'])
                    if not text:
                        text = "非文本"
                    user_name = data_['user']['screen_name']
                    ctime = handle_time(data_['created_at'])
                    comments.append([user_name, ctime, text])
    except KeyError:
        print(mid)
        print(data)
        return [[0, 0, 0]]
    return comments
def get_mid(page):
    print(page)
    comments = []
    articles = []
    cookies = {
        'SUB': '_2A25JOx8YDeRhGeNI41cT9CzIzjiIHXVqx6FQrDV6PUJbktANLRLbkW1NSDGezUx-jDi5M3ChvsGbxz1tAWRMgd6x',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5YuffAHEOr7NWB8PUSHKz55NHD95QfSonfeoBESh-XWs4DqcjVi--4iKn7iK.Ni--ci-8siK.Xi--Xi-zRiKy2i--4iKn7iK.NSKqRSKzXeoBfS5tt',
        'WEIBOCN_FROM': '1110006030',
        '__bid_n': '187992d1f6d920dbe84207',
        '_T_WM': '13968635202',
        'MLOGIN': '1',
        'BAIDU_SSP_lcr': 'https://www.google.com.hk/',
        'FPTOKEN': '28mhzisvkMxdUM4qcjdltqW4T6JOK819AeQGeaCEbhJVSo+MKeeeT4LTbtC6pcnmE9+P7kDSfJEzm7B6/dnkUv9vKNHpEQm8uhyU9wbMfMKWecxUuTawSEVh13Th5UItlwBc4OvQnZK7BWwyWcw+pqb5YMHn2I2rz6Uh6j5cmRE5S1d2aFrm2bkQCn2Ok8PdTnXbxd7eFXf1m4MsgxEwyWOzIy42CCxBul0Wo8S7ePscv5JZHChmb/LLUC8Wi+qUcMWWcsfoz6rIsoM85V+jtkmRG5SbH7gb+wKDzRsIILA/FmAZK9HNFRhb4ihaD5yNR+IAKeunuah7y3Igt7BMuuyFeGL+3eUvz4ICLqKxP62c9/CPLG5kERNJMDb42JsZDyLoJLDJyW15MNY7UMbWQQ==|v3XpfgtpBtM61pwiYFCJR16nENXNTVcI8wST0HVcA2I=|10|423f350117b43823f2487f227b08a80b',
        'M_WEIBOCN_PARAMS': 'luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E6%25B1%259F%25E8%258B%258F%25E5%25A4%25A7%25E5%25AD%25A6%2526t%253D%26fid%3D100103type%253D60%2526q%253D%25E6%25B1%259F%25E8%258B%258F%25E5%25A4%25A7%25E5%25AD%25A6%2526t%253D%26uicode%3D10000011',
        'XSRF-TOKEN': 'f5534a',
    }
    headers = {
        'authority': 'm.weibo.cn',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'mweibo-pwa': '1',
        'referer': 'https://m.weibo.cn/p/index?containerid=100103type%3D60%26q%3D%E6%B1%9F%E8%8B%8F%E5%A4%A7%E5%AD%A6%26t%3D&title=%E7%83%AD%E9%97%A8-%E6%B1%9F%E8%8B%8F%E5%A4%A7%E5%AD%A6&cardid=weibo_page&extparam=title%3D%E7%83%AD%E9%97%A8%26mid%3D%26q%3D%E6%B1%9F%E8%8B%8F%E5%A4%A7%E5%AD%A6&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%B1%9F%E8%8B%8F%E5%A4%A7%E5%AD%A6%26t%3D',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': 'f5534a',
    }
    params = {
        'containerid': '100103type=60&q=',
        'title': '',
        'cardid': 'weibo_page',
        'extparam': 'title=',
        'luicode': '10000011',
        'lfid': '100103type=1&q=',
        'page': page,
    }
    response = requests.get('https://m.weibo.cn/api/container/getIndex', params=params, cookies=cookies,
                            headers=headers)
    if response.status_code == 200:
        data = response.json()
        data_list = data['data']['cards']
        for card in data_list:
            id = card['mblog']['id']
            mid = card['mblog']['mid']
            comment_count = card['mblog']['comments_count']
            text = handle_tagg(card['mblog']['text'])
            u_id = card['mblog']['user']['id']
            u_name = card['mblog']['user']['screen_name']
            cre_time = handle_time(card['mblog']['created_at'])
            url = generate_url(mid)
            if comment_count == 0:
                articles.append([mid, u_id, u_name, cre_time, url, text])
            else:
                articles.append([mid, u_id, u_name, cre_time, url, text])
                comment = get_comment(mid, id)
                for i in comment:
                    comments.append([mid, url, text, i[0], i[1], i[2]])
    return articles, comments
def generate_url(mid):
    return 'https://m.weibo.cn/detail/{}'.format(mid)
def handle_time(time_s):
    raw_time = datetime.datetime.strptime(time_s, '%a %b %d %H:%M:%S %z %Y')
    formatted_time = raw_time.strftime('%Y-%m-%d %H:%M:%S')
    formatted_str = str(formatted_time)
    return formatted_str
def handle_tagg(string_):
    regex = re.compile('<[^>]*>')
    res_string = regex.sub('', string_).strip()
    return res_string
