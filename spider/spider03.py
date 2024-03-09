import requests
from bs4 import BeautifulSoup
import re
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}
def get_text(url, header):
    response = requests.get(url, header)
    soup = BeautifulSoup(response.content, "html.parser")
    times = soup.find("div", {"class": "pages-date"})
    if not times:
        return 0,0
    times=times.get_text(strip=True, separator=' ')
    pattern = r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}"
    match = re.search(pattern, times)
    if match:
        times=match.group()
    else:
        return 0,0
    ucap_content = soup.find("div", {"id": "UCAP-CONTENT"})
    if ucap_content:
        paragraphs = ucap_content.find_all("p")
    else:
        return 0, 0
    if paragraphs:
        text = ""
        for p in paragraphs:
            text += p.text.strip()
        print(text)
        return text, times
    else:
        return 0, 0
def get_page():
    url = ""
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', {'class': 'menu_tab'})
    p = divs[1].find_all('p')
    title = []
    urls = []
    text = []
    times = []
    for i in p:
        i = str(i)
        url_0 = re.findall('<a href="(.*?)"', i)
        title_0 = re.findall('target="_blank">(.*?)</a>', i)
        if url_0 and title_0:
            text_0, time_0 = get_text(url_0[0], headers)
            if not text_0 and not time_0:
                continue
            urls.append(url_0[0])
            text.append(text_0)
            times.append(time_0)
            title.append(title_0[0])
    return urls, text, title, times

base_url = ''

def get_page_num(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    fanye141411 = soup.find('td', id='fanye141411')
    text = fanye141411.text.strip()
    match = re.search(r'(\d+)$', text)
    if match:
        page_num = match.group(1)
        return int(page_num)
    else:
        print('未找到页码')
def get_text(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_div = soup.find('div', {'class': 'v_news_content'})
    if not content_div:
        print(url)
        return 0
    p_tags = content_div.find_all('p')
    if not p_tags:
        print(url)
        return 0
    text = ''
    for p in p_tags:
        if p.text:
            text += p.text.strip() + '\n'
    return text
def generate_url(num):
    urls = ['https://www.ujs.edu.cn/xxyw.htm']
    for i in range(num - 1, 99, -1):
        urls.append('https://www.ujs.edu.cn/xxyw/{}.htm'.format(i))
    return urls

cookies = {
    'JSESSIONID': '1E79A3E4854E99644072957052E16216',
}

headers = {
    'authority': 'jdqn.ujs.edu.cn',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'JSESSIONID=1E79A3E4854E99644072957052E16216',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

def generate_text_urls(urls):
    result = []
    for url in urls:
        temp = 'https://jdqn.ujs.edu.cn{}'.format(url)
        result.append(temp)
    return result

titles = []
times = []
texts = []
res_urls = []
def get_text(urls):
    for url in urls:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        form = soup.find('form')
        tables = form.find_all('table')
        title = tables[0].text.strip()
        time_ = tables[2].text.strip()
        pattern = r"\d{4}-\d{2}-\d{2}"
        match = re.search(pattern, time_)
        time_ = match.group()
        text = tables[4].text.strip()
        if time_ and title and text:
            print(title)
            titles.append(title)
            times.append(time_)
            res_urls.append(url)
            texts.append(text)
        else:
            print("未知错误:{}".format(url))

def generate_page_url(num):
    urls = ['']
    for i in range(num - 1, 0, -1):
        urls.append(''.format(i))
    return urls

