# -*- coding:utf-8 -*-
import requests
import json
import random
from ..send import send
import sys
sys.path.append("...")
import _set as set


def draw_group(prompt, to):
    try:
        urldraw = set.draw_url
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + set.draw_key
            }
        if "cogview" in set.draw_model or "stabilityai/" in set.draw_model:
            data = {
                "model": set.draw_model,
                "prompt": prompt,
            }
        else:
            data = {
                # claude-3-opus-vf
                "model": set.draw_model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            }
        send.msg({
            'msg_type': 'group', 'number': to, 'msg': '正在绘画[%s]中...' % prompt
                })
        response = \
            requests.post(
                url=urldraw,
                headers=headers,
                stream=True,
                data=json.dumps(data)
                )
        if response.status_code == 200:
            send.msg({'msg_type': 'group', 'number': to, 'msg': '绘画完毕发送中...'})
        processed_d_data_draw = ''
        for line in response.iter_lines():
            try:
                decoded = \
                    line.decode('utf-8').\
                    replace('\n', '\\n').\
                    replace('\b', '\\b').\
                    replace('\f', '\\f').\
                    replace('\r', '\\r').\
                    replace('\t', '\\t')
                if decoded != '':
                    if (
                        "cogview" in set.draw_model
                        or "stabilityai/" in set.draw_model
                    ):
                        processed_d_data_draw += json.loads
                        (decoded)["data"][0]["url"]
                    else:
                        processed_d_data_draw += json.loads
                        (decoded[5:])["choices"][0]["delta"]["content"]

                    print(decoded)
            except Exception as e:
                print(e)
        image_url = processed_d_data_draw.split('(')[-1].replace(')', '')
        print(image_url)
        max_n = 500
        for n in range(0, max_n):
            try:
                image_response = requests.get(image_url)
                name = str(random.randrange(100000, 999999))+'.png'
                with open("./data/image/%s" % name, 'wb') as f_image:
                    f_image.write(image_response.content)
                send.image({'msg_type': 'group', 'number': to, 'msg': name})
                break
            except:
                print(n)
                if n == max_n-1:
                    raise TimeoutError("重试无效")
    except Exception as e:
        print('绘画错误:', e)
        send.msg({'msg_type': 'group', 'number': to, 'msg': 'AI绘画操作无法执行'})
