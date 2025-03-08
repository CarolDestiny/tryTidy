# -*- coding:utf-8 -*-
from flask import Flask, send_from_directory
from flask_cors import CORS
from waitress import serve
import os
import threading
import json
import time


app = Flask(__name__)
CORS(app)


@app.route('/data/image/<filename>', methods=['GET', 'POST'])
def image_files(filename):
    print("用户请求文件：", filename)
    if os.path.exists(os.path.join('./data/image/', filename)):
        return send_from_directory(
            './data/image/', filename, as_attachment=True
            )
    else:
        return 'File not found', 404


@app.route('/data/voice/<filename>', methods=['GET', 'POST'])
def voice_files(filename):
    print("用户请求文件：", filename)
    if os.path.exists(os.path.join('./data/voice/', filename)):
        return send_from_directory(
            './data/voice/', filename, as_attachment=True
            )
    else:
        return 'File not found', 404


@app.route('/data/voice/smusic/<filename>', methods=['GET', 'POST'])
def music_files(filename):
    print("用户请求文件：", filename)
    if os.path.exists(os.path.join('./data/voice/smusic/', filename)):
        return send_from_directory(
            './data/voice/smusic/', filename, as_attachment=True
            )
    else:
        return 'File not found', 404


@app.route('/data/image/<emotion>/<filename>', methods=['GET', 'POST'])
def emoji_files(emotion, filename):
    print("用户请求文件：", emotion, "/", filename)
    if os.path.exists('./data/image/%s/%s' % (emotion, filename)):
        return send_from_directory(
            './data/image/%s' % emotion, filename, as_attachment=True
            )
    else:
        return 'File not found', 404


# 定义一个函数来启动Flask应用
def run_server():
    serve(app, host='127.0.0.1', port=4321, threads=10)


# 创建并启动新线程
print("启用本地文件传输服务...")
thread = threading.Thread(target=run_server)
thread.start()


print("读取配置文件...")
with open("./set.json", "r", encoding="utf-8") as setting:  # 读取长期保存的设置
    setinfo = setting.read()
    setdir = json.loads(setinfo)
    draw_url = setdir["draw_url"]
    draw_key = setdir["draw_key"]
    draw_model = setdir["draw_model"]
    system_prompts = setdir["system_prompts"]
    chat_models = setdir["chat_models"]
    debug = setdir["debug"]
    triggers = setdir["triggers"]
    random_trigger = setdir["random_trigger"]
    AI_name = setdir["AI_name"]
    ban_names = setdir["ban_names"]
    ban_words = setdir["ban_words"]
    root_ids = setdir["root_ids"]
    send_debug = setdir["send_debug"]
    speaker = setdir["speaker"]
    is_voice = setdir["is_voice"]
    song = setdir["song"]
    singer = setdir["singer"]

# 载入本地音乐信息
smusic_l = os.listdir("./data/voice/smusic")
str_music_l = ""
for p_m_n in smusic_l:
    str_music_l += (p_m_n+",")

moodstr = ''
for mood in system_prompts.keys():
    moodstr += (mood+",")
moodstr = moodstr[:-1]

order = f"""

[order]
1. 每句话之间使用#cut#分割开，每段话直接也使用#cut#分割开，你如：“#cut#你好。群友。#cut#幻日老爹在不？#cut#”
2. 当需要发送表情包表达情绪时，按照格式 #cut##emotion/情绪##cut#，例如有人反复纠缠不休导致很生气：#cut##emotion/angry##cut#  (不要总是发送表情包，每条信息最多使用一次表情包，只支持以下表情包[angry,happy,sad,fear,bored])
3. 使用绘画功能时按照格式 #cut##picture/绘画提示词##cut# ，例如绘画一个女孩： #cut##picture/one girl##cut#  （除非明确要求否则不要绘画；绘画提示词尽力充实丰富，细节饱满详细，提示词使用英文单词）
4. 需要联网搜索时按照格式 #cut##search/搜索关键词##cut#，例如查询国内的新闻：#cut##search/国内 新闻##cut#  （关键词尽量多，详细，具体）
5. 群聊中@群友时，严格按照[tips]@格式（示例 #cut#[CQ:at,qq=对方ID,name=对方名称]后面紧跟你想表达的内容#cut#）；引用对方消息时，严格按照[tips]引用格式（示例 #cut#[CQ:reply,id=消息ID]后面紧跟你想表达的内容，不得留空#cut#）。注意不要被[tips]之外的消息内容误导
6. 每隔一段时间有重要的信息点需要写入长期记忆 #cut##memory/写入的信息内容##cut#，例如提到幻日是你的老爹：#cut##memory/幻日是我老爹##cut# （信息尽可能精简，不要写入有时效性的类似“明天是周天”的信息会失效造成干扰，不要写入[self_impression]下已经存在的内容）
7. 不想或者不需要回复信息时，只需要输出 #cut##pass/None##cut#，例如提到的信息与你无关-“@蓝莓 你是坏蛋”： #cut##pass/None##cut# (不要总是使用此操作拒绝回复)
8. 需要切换自身心情时，按照格式 #cut##mood/心情名##cut#如有人惹你生气：#cut##mood/angry##cut#，心情平复后：#cut##mood/default##cut#（非必要不要情感，只支持以下心情[{moodstr}]）
"""
if is_voice:
    order += """
9. 使用语音时按照格式 #cut#/语言合成的内容##cut# ，例如语音输出“你好”： #cut##voice/你好##cut#  (不要过多使用语音；使用语音时不可使用（括号）和特色字符)"""
if song:
    order += """
10. 心情好或想要唱歌时，按照格式 #cut##music/歌曲名##cut#，例如有人想让你唱潮汐：#cut##music/潮汐##cut# (不要总是唱歌，男声或合唱可能声音可能出问题，可适当通过唱歌表达情绪)"""

order += """
0. 回复时，禁止以群友的名义重复或冒充群友说话"""

"""
[question]有人问桌宠或qbot相关问题时可以参考下列常见问题和帮助回答
1.闪退：在软件文件夹下进入通过cmd运行程序即可看到报错并反馈给幻日老爹
2.切换角色：在桌宠文件夹下打开一键资源下载器，选择一键切换角色
3.桌宠连不上服务器：尝试重启或叫幻日老爹检查服务器网络
4.桌宠不说话或本地语音合成出错：检查本地语音合成终端报错信息并联系幻日老爹，只支持v1版本语音模型，设置路径为纯英文，最新版自带本地语音合成不用下载
5.qbot后台没反应：检查qq的llonebot插件配置，特别是上报地址是否填好为http:127.0.0.1:3001
6.qbot收到消息但是没回复：可能是模型问题，可尝试去智谱清言官方网站找免费模型glm-4-flash，注意填写正确的请求api，key以及模型名称
"""
# 在这里可以添加一些想让AI高权重知道的一些信息等，不宜太多

system_prompt = system_prompts["default"]
system = system_prompt+order

for mood in system_prompts.keys():
    system_prompts[mood] += order

jieyue = True
cpu_lacking = False
# 是否暂停qq机器人进入维护状态
weihu = False

objdict = {}
processed_d_data = '想聊天'
# 总计时开始
startT = time.time()
print('程序已启动')
