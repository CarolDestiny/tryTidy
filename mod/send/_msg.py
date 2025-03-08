# -*- coding:utf-8 -*-
import requests
import json


def msg(resp_dict):
    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    number = resp_dict['number']  # 回复账号（群号/好友号）
    msg = resp_dict['msg'].strip()  # 要回复的消息
    if msg:
        if msg_type == 'group':
            res = requests.post(
                'http://localhost:3000/send_group_msg',
                json={
                    'group_id': number,
                    'message': msg
                    }
                )
            print("send_group_msg:", msg, json.loads(res.content))
        elif msg_type == 'private':
            res = requests.post(
                'http://localhost:3000/send_private_msg',
                json={
                    'user_id': number,
                    'message': msg
                    }
            )
            print("send_private_msg:", msg, json.loads(res.content))
    return 0
