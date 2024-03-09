import csv
import requests
import json

def bili_sp():
    cookies = {
        'buvid3': '9C3D9417-2C56-4E89-9351-0BD82BAE0E8E148814infoc',
        'buvid4': '81912292-E0BC-4055-3B98-FB75A9D69C8077002-022041216-xxaMMcKA84QrxYTrRktgmQ%3D%3D',
        'i-wanna-go-back': '-1',
        '_uuid': '729FD10F10-262D-3CB6-5E810-5FCDD95B8A9502942infoc',
        'fingerprint': '209e93c714456a2b89e1635e118ed825',
        'buvid_fp_plain': 'undefined',
        'buvid_fp': '209e93c714456a2b89e1635e118ed825',
        'DedeUserID': '2017980162',
        'DedeUserID__ckMd5': '008b9505776fee7a',
        'b_ut': '5',
        'nostalgia_conf': '-1',
        'CURRENT_FNVAL': '4048',
        'rpdid': "|(u))kllYRJ)0J'uY~|ul)YRJ",
        'PVID': '2',
        'header_theme_version': 'CLOSE',
        'SESSDATA': '56b88f8b%2C1693706917%2C9afbe%2A32',
        'bili_jct': '22c1f547bd938576195d055be38e2c13',
        'FEED_LIVE_VERSION': 'V8',
        'CURRENT_PID': '54826080-ddd0-11ed-9362-a9df71ea1f12',
        'innersign': '0',
        'b_lsid': '3D78E997_187981FC645',
        'home_feed_column': '4',
        'share_source_origin': 'COPY',
        'bsource': 'share_source_copy_link',
    }
    headers = {
        'authority': 'app.bilibili.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://www.bilibili.com',
        'referer': 'https://www.bilibili.com/blackboard/activity-trending-topic.html?navhide=1&plat_id=124&share_from=h5&share_medium=android&share_plat=android&share_session_id=60626139-618a-4df7-a4eb-e5dc37349601&share_source=COPY&share_tag=s_i&timestamp=1681884678&unique_k=A4LwrHq',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }
    params = {
        'csrf': '22c1f547bd938576195d055be38e2c13',
        'limit': '30',
    }
    contents = []
    response = requests.get('https://app.bilibili.com/x/v2/search/trending/ranking', params=params, cookies=cookies,
                            headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        word_list = data['data']['list']
        for word in word_list:
            rank = word['position']
            note = word['keyword']
            contents.append([rank, note, 'Bilibili'])
        with open('Spider/output/bili_hot.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Rank', 'Note', 'Source'])
            for i in contents:
                writer.writerow(i)
        return contents
    else:
        print('请求失败')
def wc_sp():
    cookies = {
        'ABTEST': '0|1681883656|v1',
        'SNUID': 'DD348ECBBBBE4216B651460CBC1041AD',
        'IPLOC': 'CN3211',
        'SUID': '66883570BA18960A00000000643F8208',
        'SUID': '668835707B51960A00000000643F8209',
        'JSESSIONID': 'aaahrpTW_PYoG-Gtmi8vy',
        'SUV': '003A887470358866643F8209BD205646',
        'cuid': 'AAGJs9VORAAAAAqMWU2RowEASQU=',
        'LSTMV': '757%2C194',
        'LCLKINT': '3277',
        'ariaDefaultTheme': 'undefined',
    }
    headers = {
        'authority': 'weixin.sogou.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 'cookie': 'ABTEST=0|1681883656|v1; SNUID=DD348ECBBBBE4216B651460CBC1041AD; IPLOC=CN3211; SUID=66883570BA18960A00000000643F8208; SUID=668835707B51960A00000000643F8209; JSESSIONID=aaahrpTW_PYoG-Gtmi8vy; SUV=003A887470358866643F8209BD205646; cuid=AAGJs9VORAAAAAqMWU2RowEASQU=; LSTMV=757%2C194; LCLKINT=3277; ariaDefaultTheme=undefined',
        'referer': 'https://weixin.sogou.com/weixin?p=01030402&query=%E4%BC%A0%E9%80%92%E4%B8%AD%E5%9B%BD%E5%A3%B0%E9%9F%B3&type=2&ie=utf8',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    params = {
        't': '1681886073083',
    }
    response = requests.get('https://weixin.sogou.com/pcindex/pc/web/web.js', params=params, cookies=cookies,
                            headers=headers)
    contents = []
    if response.status_code == 200:
        data = json.loads(response.text)
        band_list = data['topwords']
        for i, band in enumerate(band_list):
            rank = i
            note = band['word']
            contents.append([rank, note, 'weixin'])
        with open('Spider/output/wechat_hot.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Rank', 'Note', 'Source'])
            for i in contents:
                writer.writerow(i)
        return contents
    else:
        print('请求失败')

def wb_sp():
    url = 'https://weibo.com/ajax/statuses/hot_band'
    cookies = {
        '_s_tentry': 'passport.weibo.com',
        'Apache': '4121942161125.1206.1681878788407',
        'SINAGLOBAL': '4121942161125.1206.1681878788407',
        'ULV': '1681878788473:1:1:1:4121942161125.1206.1681878788407:',
        'XSRF-TOKEN': 'RTMkGL7arnVkKFVqiskcNYhT',
        'SSOLoginState': '1681878855',
        'SUB': '_2A25JOx8XDeRhGeNI41cT9CzIzjiIHXVqx6FfrDV8PUJbkNANLULfkW1NSDGezWIjXBbHODMKigxnYUPjWNXWVfgZ',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5YuffAHEOr7NWB8PUSHKz55NHD95QfSonfeoBESh-XWs4DqcjVi--4iKn7iK.Ni--ci-8siK.Xi--Xi-zRiKy2i--4iKn7iK.NSKqRSKzXeoBfS5tt',
        'PC_TOKEN': '0701c841ce',
        'WBPSESS': '_tKurGSdmLVxNHC170O3plCAH1ywLz6epW4k6teDzfQORUhsKbX8Ei-3esCig2fcdrlH9_JWIY_7Dqwp95JFLwFwelkoF45gPTL7iH6WZmz8AEeGZskM4ppnaFz3f69MIruDFBYgv7Pmr564v9LkEg==',
    }
    headers = {
        'authority': 'weibo.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }
    response = requests.get(url, cookies=cookies, headers=headers)
    content = []
    if response.status_code == 200:
        data = json.loads(response.text)
        band_list = data['data']['band_list']
        for band in band_list:
            rank = band['rank']
            note = band['note']
            num = band['num']
            content.append([rank, note, num, '微博'])
        with open('Spider/output/weibo_hot.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Rank', 'Note', 'Num', 'Source'])
            for i in content:
                writer.writerow(i)
        return content
    else:
        print('请求失败')
def dy_sp():
    headers = {
        'authority': 'www.douyin.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'SEARCH_RESULT_LIST_TYPE=%22single%22; ttwid=1%7CYQT8Gkwab7epPUGd3SgxoGPIOTbmllVNVaBc7LjO7dY%7C1681688078%7C93f1d1c570514e58ee809b1e93275aa5920867dc2b00b77fbf01ef0ac4439a44; passport_csrf_token=e10eccc9f8882c7cc799255937829773; passport_csrf_token_default=e10eccc9f8882c7cc799255937829773; s_v_web_id=verify_lgk1or9m_LHuRhwMo_bvEE_4HSM_BTvb_UBcc62dL2KsJ; __ac_signature=_02B4Z6wo00f01Cuby4wAAIDAq5kxzR0eGlwru88AAG7g19r22MOTWtbhuxHpO9jr4Z5vSi7h5DPARmJHiPAY0VJMyhMj0.KGoWQsOeknY9CKlQX32goHFSZ9AQZCgnVNLON2sTzSCnCZsh9W8a; download_guide=%223%2F20230419%22; pwa2=%221%7C0%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNzciI6Ii0tLS0tQkVHSU4gQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbk1JSUJEakNCdFFJQkFEQW5NUXN3Q1FZRFZRUUdFd0pEVGpFWU1CWUdBMVVFQXd3UFltUmZkR2xqYTJWMFgyZDFcclxuWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERBUWNEUWdBRUtra2JjMkdwLzl1UU9wOUlFT21zc2JCeVxyXG5iMXRsNzN1Q3RLSFQrWXIyVGw2eUExZGphSzZXZzN0eFVaMWhYWHVFL1FqL0toSzVWaGMzMTRjNG9PODhMS0FzXHJcbk1Db0dDU3FHU0liM0RRRUpEakVkTUJzd0dRWURWUjBSQkJJd0VJSU9kM2QzTG1SdmRYbHBiaTVqYjIwd0NnWUlcclxuS29aSXpqMEVBd0lEU0FBd1JRSWhBTXRKQkFWUnJlMDAvOTdCQ29wZFRwbVpnSnd6ODYyKzRPY1hFSWpMT0k0cVxyXG5BaUJlbWdiMnhnWUVtdG50L1IwWUpEaTdFMzVYYUtORGRXc3I5Z3hDR1ovVlRnPT1cclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9; douyin.com; strategyABtestKey=%221681881037.118%22; csrf_session_id=14fa0738e04e2ba2f27ac996bf11331d; msToken=CCxfSyw-bJ40ErLBZfVS49K_O_ruDh8aIAZBkVy15vBKspqAqimFLxO_FhyYeXGVVYOErkEV1CTetN7ZOWptU8NxEO4bJe7z2Uw3mwbiTTrPz-xp3HdUrA==; home_can_add_dy_2_desktop=%221%22; tt_scid=LveLEeWQNJR9Py8RxeHe-ZHpkL377geRD5hdYJJvaLWK8JUvcuY.54LKxE9QMT7dc8db; msToken=cP94CsKwwD_9NOup-aIZQ3KuOxZpOl14ylDOkY1zTY8h1f-HxEdkclduapAlK9uAz7B3LZ2OqxWEXIa6IG6ht3InoOo2YrfmFYeIlaphaJt_ruzRaZ2tUoctKenpR_Y=',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }
    contens = []
    url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        wordlist = data['data']['word_list']
        for word in wordlist:
            ranks = word['position']
            notes = word['word']
            nums = word['hot_value']
            contens.append([ranks, notes, nums, '抖音'])
        with open('Spider/output/douyin_hot.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Rank', 'Note', 'Num', 'Source'])
            for i in contens:
                writer.writerow(i)
        return contens
    else:
        print('请求失败')