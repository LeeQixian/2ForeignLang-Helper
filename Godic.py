import requests
import os
from bs4 import BeautifulSoup
import edge_tts
import asyncio
current_dir = os.path.dirname(os.path.abspath(__file__))
multi_path = os.path.join(current_dir, "multi.txt")
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
headers = {'User-Agent': UA}
def get_html(keyword):
    try:
        url = f'http://www.godic.net/dicts/de/{keyword}'
        response = requests.get(url, headers=headers)
        assert response.status_code == 200
        response.encoding = 'utf-8'
        return response.text
    except requests.exceptions.RequestException as e:
        print(e)

def mode1():
    keyword = input('请输入要查询的单词：')
    res = get_html(keyword)
    soup = BeautifulSoup(res, 'html.parser')
    txt = get_sentences(soup)
    asyncio.run(pronounce(txt,keyword))

def mode2():
    with open(multi_path, 'r', encoding='utf-8') as f:
        keywords = f.readlines()
        f.close()
    for keyword in keywords:
        keyword = keyword.strip('\n')
        print (f'正在查询{keyword}...')
        html_file = get_html(keyword)
        soup = BeautifulSoup(html_file, 'html.parser')
        txt = get_sentences(soup)
        asyncio.run(pronounce(txt,keyword))

def get_sentences(soup):
    items = soup.find_all('div', class_='lj_item')
    text = ''
    for item in items:
        content_div = item.find('div', class_='content')
        p_line = content_div.find('p',class_ = 'line')
        p_exp = content_div.find('p',class_ = 'exp')
        print('- '+p_line.text)
        print('    '+p_exp.text)
        text += p_line.text+' '
    return text

async def pronounce(text,keyword):
    file = edge_tts.Communicate(text, voice = 'de-DE-SeraphinaMultilingualNeural')
    await file.save(os.path.join(current_dir, f'{keyword}.mp3'))

def ask_mode():
    mode = input('请选择模式：1.单词查询 2.多词查询：')
    if mode == '1':
        mode1()
    elif mode == '2':
        mode2()
    else:
        print('输入错误，请重新输入！')
        ask_mode()
ask_mode()