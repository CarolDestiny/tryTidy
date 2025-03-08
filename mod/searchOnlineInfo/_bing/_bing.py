# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup


def bing(keywords):
    # 必应搜索结果URL
    url = 'https://cn.bing.com/search?q=' + keywords
    # 请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 \
                (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        # 发送GET请求
        response = requests.get(url)
        # 确保请求成功
        response.raise_for_status()
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找搜索结果
        search_items = soup.find_all('li', class_='b_algo')
        if not search_items:
            print("未找到搜索结果，可能是因为HTML结构发生了变化。")
            return ""
        result = ""
        for index, item in enumerate(search_items):
            # 提取标题
            title = item.find('h2').get_text()
            # 提取链接
            link = item.find('a')['href']
            # 提取摘要
            summary_div = item.find('div', class_='b_caption')
            if summary_div:
                summary_p = summary_div.find_all('p')
                if summary_p:
                    summary = ''.join(p.get_text() for p in summary_p)
                else:
                    summary = summary_div.get_text(strip=True)
            else:
                summary = ''
            # 对于前三个结果，获取详细页面内容
            if index < 10:
                try:
                    # 发送GET请求到详细页面
                    response_detail = requests.get(link, headers=headers)
                    response_detail.raise_for_status()
                    soup_detail = BeautifulSoup(
                        response_detail.text, 'html.parser'
                        )
                    # 假设详细页面中的主要内容在 <div id="content"> 中
                    content_div = soup_detail.find('div', id='content')
                    if content_div:
                        content = content_div.get_text(strip=True)
                        # 保留前500个字符
                        content = (
                            content[:500]
                            if len(content) > 500
                            else content
                        )
                    else:
                        content = '无法找到详细内容。'
                    result += f'\
                        标题：{title}\n\
                        链接：{link}\n\
                        摘要：{summary}\n\
                        详细内容：{content}\n\
                        '
                    print(f'\
                            标题：{title}\n\
                            链接：{link}\n\
                            摘要：{summary}\n\
                            详细内容：{content}\n\
                        ')
                except requests.RequestException as e:
                    print(f'请求详细页面错误：{e}')
            else:
                # 打印摘要
                result += f'\
                    标题：{title}\n\
                    链接：{link}\n\
                    摘要：{summary}\n\
                    详细内容：{content}\n\
                    '
                print(f'标题：{title}\n链接：{link}\n摘要：{summary}\n')
            if len(result) > 5000:
                return result
        return result

    except requests.RequestException as e:
        print(f'请求错误：{e}')
    except Exception as e:
        print(f'解析错误：{e}')
