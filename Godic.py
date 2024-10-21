import requests
import os
from bs4 import BeautifulSoup
import edge_tts
import asyncio
current_dir = os.path.dirname(os.path.abspath(__file__))
multi_path = os.path.join(current_dir, "multi.txt")
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
headers = {'User-Agent': UA}
def get_html(keyword):
    try:
        url = f'http://www.godic.net/dicts/de/{keyword}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
    except requests.exceptions.RequestException as e:
        print(e)

# 发送 GET 请求获取网页内容
keyword = input('请输入要查询的单词：')
res = get_html(keyword)
soup = BeautifulSoup(res, 'html.parser')
items = soup.find_all('div', class_='lj_item')
text = ''
for item in items:
    content_div = item.find('div', class_='content')
    p_line = content_div.find('p',class_ = 'line')
    p_exp = content_div.find('p',class_ = 'exp')
    print('- '+p_line.text)
    print('    '+p_exp.text)
    text += p_line.text+'\n'
async def main():
    file = edge_tts.Communicate(text, voice = 'de-DE-SeraphinaMultilingualNeural')
    await file.save(os.path.join(current_dir, f'{keyword}.mp3'))
asyncio.run(main())