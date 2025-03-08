# -*- coding:utf-8 -*-
# 唐千尝试对代码进行整理
from threading import Thread
from receive import rev_msg
from ._main import main
import _file

'''
print('\n欢迎使用由幻日编写的幻蓝AI程序',end='')
print('有疑问请联系:')
print('q:2141073363')
print('q:1967444797')
'''

while 1:
    try:
        rev = rev_msg()
        try:
            botID = rev['self_id']
        except:
            pass
        if rev is None:
            continue
    except:
        continue
    Thread(target=main, args=(rev,)).start()
