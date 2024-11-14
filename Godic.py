import requests
import os
from bs4 import BeautifulSoup
import edge_tts
import asyncio
import sys
import re
import pandas as pd
current_dir = os.path.dirname(os.path.abspath(__file__))
multi_path = os.path.join(current_dir, "multi.txt")
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
cookies_dict = {'pgv_pvid': '8972623698', 'EudicWebSession': 'QYNeyJoYXNfb2xkX3Bhc3N3b3JkIjpmYWxzZSwidG9rZW4iOiJmL3NzVUxNTUhQMVB3L1B2STcxVTYxV3pMeEE9IiwiZXhwaXJlaW4iOjEzMTQwMDAsInVzZXJpZCI6IjM2ZWIzOGVmLTZlYjktMTFlZi04MTA4LTAwNTA1Njg2NmVkYSIsInVzZXJuYW1lIjoiemtrYnhsZjF1QG1vem1haWwuY29tIiwiY3JlYXRpb25fZGF0ZSI6IjIwMjQtMDktMDlUMDY6Mzg6NDVaIiwicm9sZXMiOm51bGwsIm9wZW5pZF90eXBlIjpudWxsLCJvcGVuaWRfZGVzYyI6bnVsbCwicHJvZmlsZSI6eyJuaWNrbmFtZSI6IuadjuS4g%252bW8piIsImVtYWlsIjoiemtrYnhsZjF1QG1vem1haWwuY29tIiwiZ2VuZGVyIjpudWxsLCJwYXNzd29yZCI6bnVsbCwidm9jYWJ1bGFyaWVzIjp7fX0sImxhc3RfcGFzc3dvcmRfY2hhbmdlZF9kYXRlIjoiMjAyNC85LzkgMTQ6Mzg6NDUiLCJyZWRpcmVjdF91cmwiOm51bGx9', 'sta-state': 'off', 'display': 'block', 'word': 'Lehrerin', '.AspNetCore.Antiforgery.d6VYMxgCCvI': 'CfDJ8EvsCc1ozlhGvRdc6S4AiLvan8loWwmyj6tPI3fdeuU3LyzN79DEezr0dWXeJMF_it07BnMXpL_1Z9bb-SFjZGxn0n7LeULRsuEXq4kPTLAbIZiLbKX40WpWls8eTO2z1hTH6HYsmPKjuRUtKxvqxXE', '.AspNetCore.Session': 'CfDJ8EvsCc1ozlhGvRdc6S4AiLtQR2GuCy8dRZFRpcS5TeRZmbiLdQkG3ZltA260LCtLwIlE5%2BA98nQFaR1kgw1ANROG9yc1nOMiRiputgDn3%2F53%2BwX%2FmqKswPWvNUfXq8EZjrRJ4WA28HqwyJRcnPON7uWigQi5n4MiAcR19rcaHsX7'}
headers = {'User-Agent': UA}
def get_html(keyword):
    try:
        url = f'http://www.godic.net/dicts/de/{keyword}'
        response = requests.get(url, headers=headers,cookies=cookies_dict)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup
        else:
            print(response.status_code+' Request Error!')
            sys.exit(1)
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
    print('正在获取例句...')
    items = soup.find_all('div', class_='lj_item')
    if items:
        text = ''
        notes = '#### Die Beispiele\n'
        for item in items:
            content_div = item.find('div', class_='content')
            p_line = content_div.find('p',class_ = 'line')
            p_exp = content_div.find('p',class_ = 'exp')
            notes += f'- {p_line.text}\n'
            notes += f'    {p_exp.text}\n'
            #print('- '+p_line.text)
            #print('    '+p_exp.text)
            text += p_line.text+' '
        #print(notes)
        return notes
    else:
        return ''

def get_specific(soup):
    print('正在获取专业词典...')
    item = soup.find('div', id = 'ExpSPECChild')
    if item:
        text_content = item.get_text(separator="\n").strip()
        lines = text_content.splitlines()
        lines = lines[:-1]
        text = '#### 德语专业词典\n'
        for line in lines:
            text += line+'\n'
        return text
    else:
        return ''
#get_specific(get_html('lernen'))
def get_basic_exp(soup):
    print('正在获取基本释义...')
    item = soup.find('div', id = 'ExpFCChild')
    if item:
        spans = item.find_all('span')
        title = '#### 基本释义\n'
        result_text = title
        for span in spans:
        # 检查 style 属性，过滤掉不要的 span
            if 'color: transparent !important' in span.get('style', '') or 'display:none' in span.get('style', ''):
                continue
            # 如果 span 的 class 包含 'cara'，则用五级标题进行处理
            if 'cara' in span.get('class', []):
                result_text += f'##### {span.get_text(strip=True)}\n'
            else:
                # 对于其他的 span 标签，直接获取文本
                result_text += f'{span.get_text(strip=True)}\n'
        grammatik_exp = soup.find('div', class_ = 'eudic_grammarmatch')
        if grammatik_exp:
            result_text += f'#### 语法匹配\n{grammatik_exp.get_text(strip=True)}\n'
        return result_text
    else:
        return ''
#get_basic_exp(get_html('lernen'))
async def pronounce(text,keyword):
    try:
        file = edge_tts.Communicate(text, voice='de-DE-SeraphinaMultilingualNeural')
        await file.save(os.path.join(current_dir, f'{keyword}.mp3'))
    except edge_tts.exceptions.NoAudioReceived as e:
        print(f"Error: No audio received for {keyword}. The file will be removed.")
        os.remove(os.path.join(current_dir, f'{keyword}.mp3'))
    except Exception as e:
        print(f"An error occurred while processing {keyword}. \nError details: {e}\nThe file will be removed.")
        os.remove(os.path.join(current_dir, f'{keyword}.mp3'))

def ask_mode():
    mode = input('请选择模式：1.单词查询 2.多词查询：')
    if mode == '1':
        mode1()
    elif mode == '2':
        mode2()
    else:
        print('输入错误，请重新输入！')
        ask_mode()
#ask_mode()

def write_markdown(keyword):
    soup = get_html(keyword)
    part1 = get_basic_exp(soup)
    
    part2 = get_specific(soup)
    
    part3 = get_sentences(soup)
    
    with open(os.path.join(current_dir, f'{keyword}.md'), 'w', encoding='utf-8') as f:
        f.write(part1)
        f.write(part2)
        f.write(part3)
        f.close()

#write_markdown('kalt')
def now_table():
    with open(r'E:\CODE\test2.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        tables = soup.find('div', id='cg_table')
        markdown_tables = []

    for table in tables.find_all("table"):
        markdown = ""
        rows = []
        max_cols = 0

        # 遍历每个行
        for tr in table.find_all("tr"):
            row = []
            for cell in tr.find_all(["th", "td"]):
                colspan = int(cell.get("colspan", 1))
                content = cell.get_text(strip=True)
                row.extend([content] * colspan)  # 按colspan填充
            max_cols = max(max_cols, len(row))  # 更新最大列数
            rows.append(row)
        
        # 生成表头
        header = rows[0] if rows else []
        header_line = "| " + " | ".join(header + [""] * (max_cols - len(header))) + " |"
        separator_line = "|" + "|".join([":---"] * max_cols) + "|"
        markdown += header_line + "\n" + separator_line + "\n"

        # 添加数据行
        for row in rows[1:]:
            row_line = "| " + " | ".join(row + [""] * (max_cols - len(row))) + " |"
            markdown += row_line + "\n"
        
        markdown_tables.append(markdown.strip())

    return markdown_tables
def test_table():
    markdown_tables = now_table()
    for i, table in enumerate(markdown_tables, 1):
        print(f"### 表格 {i}\n")
        print(table)
        print("\n")