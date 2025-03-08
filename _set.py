# -*- coding:utf-8 -*-
import json
import random


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


def change_setting(file_name, key, value):
    with open(file_name, 'r', encoding='utf-8') as f:
        t_gsetting = json.load(f)
    t_gsetting[key] = value
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(t_gsetting, f, ensure_ascii=False, indent=4)


def choose_model():
    w_c_models = []
    for c_model in setdir["chat_models"]:
        w_c_models += [c_model]*c_model["weight"]
    model_info = random.choice(w_c_models)
    return model_info["model_api"], model_info["model_name"], model_info["model_key"], model_info["remark"]
