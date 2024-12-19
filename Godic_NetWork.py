import requests
import os
from bs4 import BeautifulSoup
import random
import time
import re
from urllib3.util.retry import Retry
from bs4 import Tag,Comment
from requests.adapters import HTTPAdapter
import json

def process_cookies(str):
    cookies_dict = dict(cookie.split('=') for cookie in str.split('; '))
    return cookies_dict
class configuration:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.markdown_dir = os.path.join(self.current_dir, 'Godic_markdown')
        self.html_path = os.path.join(self.current_dir, 'Godic_html')

        os.makedirs(self.markdown_dir, exist_ok=True)
        os.makedirs(self.html_path, exist_ok=True)
        
        self.failed_set = set()
        self.exclude_set = {'cara', 'eg', 'exp', 'phrase', '/cara', '/eg', '/exp', '/phrase', 'word-thumbnail-image'}
#启用日志，等级error。
config = configuration()
class processor:
    def __init__(self, html,div_ids=None):
        self.html = html
        self.div_ids = div_ids if div_ids is not None else {}
        self.div_ids['basic'] = 'ExpFC'
        self.div_ids['specific'] = 'ExpSPEC'
        self.div_ids['synonyms'] = 'ExpSYN'
        self.div_ids['z. B.'] = 'ExpLJ'
    #调用format函数，返回格式化后的文本，字符串
    def handler(self):
        formated_content = ''
        
        for key, div_id in self.div_ids.items():
            item = self.html.find('div', id=div_id)
            content = ''
            if item:
                if key == 'basic':
                    content = self.format_basic(item)
                elif key == 'specific':
                    content = self.format_specific(item)
                elif key == 'synonyms':
                    content = self.format_synonyms(item)
                elif key == 'z. B.':
                    content = self.format_example(item)
                else:
                    pass  
            formated_content += content
        if formated_content == '':
            return ""
        return formated_content
        
    def format_basic(self, item):
        # 处理标题
        div_Head = item.find('div', class_='expHead')
        title = div_Head.get_text(strip=True) if div_Head else "无标题"
        result_text = '### ' + title + '\n'

        target_div = item.find('div', id='ExpFCChild')
        for element in target_div.children:
            if isinstance(element, Comment):
                continue
            if isinstance(element, Tag):
                if 'cara' in element.get('class', []):
                    result_text += f'#### {element.get_text(strip=True)}\n'
                elif 'eg' in element.get('class', []):
                    result_text += f"- 示例：{element.get_text(strip=True)}\n"
                elif 'exp' in element.get('class', []):
                    result_text += f'##### {element.get_text(strip=True)}\n'
                elif 'phrase' in element.get('class', []):
                    result_text += f'**短语**: {element.get_text(strip=True)}\n'
                elif 'BAB_CPDefenitionStyle' and element.get('class',[]):
                    result_text += f'{element.get_text(strip=True)}\n'
                elif element.name == 'p':
                    result_text += element.get_text(strip=True) + '\n'
            elif isinstance(element, str) and element.strip():
                if element.strip() not in self.exclude_set:
                    result_text += element.strip() + '\n'
                
        grammatik_exp = target_div.find('div', class_='eudic_grammarmatch')
        if grammatik_exp:
            result_text += f'#### 语法匹配\n{grammatik_exp.get_text(strip=True)}\n'
            
        return result_text
        
    def format_specific(self, item):
        div_Head = item.find('div', class_='expHead')
        title = div_Head.get_text(strip=True) if div_Head else "无标题"
        result_text = '\n### ' + title + '\n'
        
        target_div = item.find('div', id='ExpSPECChild')
        seen_elements = set()
        for element in target_div.children:
            if element.name == 'span' and 'cara' in element.get('class', []):
                cara_text = element.get_text(strip=True)
                if cara_text not in seen_elements:
                    result_text += '\n#### ' + cara_text + '\n'
                    seen_elements.add(cara_text)
            
            elif element.name == 'span' and 'exp' in element.get('class', []):
                exp_text = element.get_text(strip=True)
                if exp_text not in seen_elements:
                    result_text += f"{exp_text}\n"
                    seen_elements.add(exp_text)
            
            elif element.name == 'span' and 'eg' in element.get('class', []):
                eg_text = element.get_text(strip=True)
                if eg_text not in seen_elements:
                    result_text += f"- 示例：{eg_text}\n"
                    seen_elements.add(eg_text)
            
            else:
                result_text += element.get_text(strip=True)
                continue  # Ignore irrelevant elements
        
        return result_text

    def format_synonyms(self, item):
        
        div_Head = item.find('div', class_='expHead')
        title = div_Head.get_text(strip=True)
        result_text = '\n### ' + title + '\n'

        target_div = item.find('div', id='ExpSYNChild')
        for element in target_div.descendants:
            if element.name == "h5":
                sub_title = element.get_text(strip=True)
                result_text += f'\n#### {sub_title}\n'
            elif element.name == 'a':
                result_text += f'[[{element.text}]]'
            elif element.name == 'div':
                for sub_element in element.descendants:
                    if sub_element.name == 'w':
                        result_text += f'[[{sub_element.get_text(strip=True)}]]\n'
        
        return result_text

    def format_example(self, item):

        div_Head = item.find('div', class_='expHead')
        title = div_Head.get_text(strip=True)
        result_text = '\n### ' + title + '\n'

        target_div = item.find('div', id='ExpLJChild')
        items = target_div.find_all('div', class_='lj_item')
        for item in items:
            content_div = item.find('div', class_='content')
            p_line = content_div.find('p',class_ = 'line')
            result_text += f'- {p_line.text}\n'
            p_exp = content_div.find('p',class_ = 'exp')
            result_text += f'    {p_exp.text}\n'
        
        return result_text
    #接受关键词名和格式化后的文本，写入文件。
    def write_to_file(self, keyword, string, filepath = config.markdown_dir):
        with open(os.path.join(filepath, f'{keyword}.md'), 'w', encoding='utf-8') as f:
            f.write(string)
            f.close()
    #接受一个soup，返回一个词集。
    def get_synonyms_set(self, soup):
        syn_div = soup.find('div', id='ExpSYNChild')
        if not syn_div:
            return set()
        syn_set = set()
        lins = syn_div.find_all('a')
        for lin in lins:
            syn_set.add(lin.text)
        return syn_set

class crawler:
    def __init__(self):
        self.session = requests.Session()
        self.cookies = json.load(open('./cookies.json'))
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',}
        self.results_dict = {}
        self.session.headers.update(self.headers)
        self.session.cookies.update(self.cookies)
        
        retries = Retry(total=5, backoff_factor=1)  # 1秒退避因子
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
    #接受一个关键字，返回一个bs4对象，失败则返回none。
    def get_soup(self, keyword):
        try:
            url = f'https://www.godic.net/dicts/de/{keyword}'
            print(f"正在请求 {url}...")
            response = self.session.get(url)
            response.raise_for_status()  # 自动抛出非200状态码的异常
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except requests.RequestException as e:
            status_code = getattr(e.response, 'status_code', None)
            config.failed_set.add(keyword)  # 只记录失败的 keyword
            print(f"请求失败：关键字: {keyword}，状态码: {status_code}")
        return None
    #不接受参数，随即等待。
    def random_wait(self):
        wait_time = random.uniform(3,5)
        print(f'随机等待{wait_time}秒...')
        time.sleep(wait_time)
    #询问用户是否继续，返回布尔值。
    def ask_for_continue(self):
        whether_continue = input('是否继续查询？(y/n)')
        if whether_continue == 'y':
            return True
        else:
            return False
    #接受一个同义词集，可选参数为已经爬了的词集，默认为空，返回结果字典。递归直到爬完
    #格式如：[keyword]:(soup, extracted_syns)
    def recursive_crawling(self,syns_set, already_crawled=None):
        if already_crawled is None:
            already_crawled = set()
        if not syns_set:
            return self.results_dict
        current_syns = syns_set - already_crawled - config.failed_set
        if not current_syns:
            return self.results_dict
        current_round_results = {}
        new_syns = set()
        for syn in current_syns:
            try:
                soup = self.get_soup(syn)
                if soup:
                    #对于已经爬到的soup，写入文件
                    processed_content = processor(soup).handler()
                    processor(soup).write_to_file(keyword = syn, string = processed_content)
                    #进行同义词set的处理
                    extracted_syns = processor(soup).get_synonyms_set(soup)
                    new_syns.update(extracted_syns)
                    #更新结果字典
                    current_round_results[syn] = (soup, extracted_syns)
                    already_crawled.add(syn)
                    self.random_wait()
                else:
                    config.failed_set.add(syn)
            except Exception as e:
                config.failed_set.add(syn)
        self.results_dict.update(current_round_results)
        if self.ask_for_continue():
            # 递归调用，传递新的词集
            self.recursive_crawling(new_syns, already_crawled)
        return self.results_dict
#接受一个soup，检查是否存在无效词条，返回布尔值。
def checker(soup):
    target = soup.find('div', class_='dicBox')
    return not bool(target)
#接受一个soup，检查重定向词条，默认返回第一条智能建议，字符串。
def redirect(soup):
    target = soup.find('div',class_='dicBox')
    if target:
        boxs = target.find_all('div',class_='infobox')
        for box in boxs:
            h3_text = box.find('h3').get_text() if box.find('h3') else ""
            if '智能搜索建议' in h3_text:
                all_links_text = [a_tag.get_text(strip=True) for a_tag in box.find_all('a')]
                if len (all_links_text) ==1 :
                    return all_links_text[0]
                else:
                    if all_links_text:
                        return all_links_text
                    else:
                        return None
#接受一个字典，格式如：[旧词]:[soup]，用于检查是否存在无效词条，返回一个包含需要重定向词典的字典。无需重定向将返回none。
def link_check(dict):
    for key, value in dict.items():
        if not value:
            continue
        soup = value
        
        if checker(soup):
            redirect_word = redirect(soup)
            if redirect_word:
                dict[key] = redirect_word
            else:
                dict[key] = None
    return dict
#接受一个字典，格式如：[旧词]:[新词]，用于处理重定向链接，无返回值。
def redirector(dict):
    for key, value in dict.items():
        if not value:
            continue
        redirect_word = key
        newword = value
        for filename in os.listdir(configuration.markdown_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(configuration.markdown_dir, filename)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查 redirect_word 是否在文件内容中
                if f'[[{redirect_word}]]' in content:
                    print(f"找到重定向词 [[{redirect_word}]] 在文件 {filename} 中")

                # 替换匹配模式
                    pattern = r'\[\[' + re.escape(redirect_word) + r'\]\]'
                    replacement = f'[{newword}](https://www.dwds.de/wb/{newword})'
                    new_content = re.sub(pattern, replacement, content)

                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f'文件 {filename} 中的 "{redirect_word}" 已替换为链接格式')

def test(keyword):
    spider = crawler()
    soup = spider.get_soup(keyword)
    if soup:
        #处理得到的soup，得到处理后的文本，并写入文件。
        processed_content = processor(soup).handler()
        processor(soup).write_to_file(keyword = keyword,string = processed_content)
        #得到词集，递归爬行。
        extracted_syns = processor(soup).get_synonyms_set(soup)
        word_dict = spider.recursive_crawling(extracted_syns)
        #检查是否存在无效词条，并进行重定向。
        direct_words = dict()
        for key, value in word_dict.items():
            if not value or not key:
                continue
            #单个soup进行检查，确认重定向词条
            single_soup = value[0]
            if checker(single_soup):
                redirect_word = redirect(single_soup)
                #如果得到了重定向词条，按照[旧词]:[新词]的格式加入字典。
                if redirect_word:
                    direct_words[key] = redirect_word
        return direct_words

tests = test('kalt')

redirector(tests)