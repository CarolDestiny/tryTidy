# -*- coding:utf-8 -*-
# flake8: noqa


def main(rev):
    global objdict
    user_api,user_chat_model,user_key,remark=choose_model()
    try:
        timestamp = time.time()
        localtime = time.localtime(timestamp)
        current_time = time.strftime(
                "%Y-%m-%d %H:%M:%S", localtime
            )
        e_information="[information](准确 有时效性)\n当前时间：%s\n"%current_time
        if rev["message_type"] == "private":
            if "banaijian%schat"%rev["sender"]["user_id"] not in objdict.keys():
                objdict["banaijian%schat"%rev["sender"]["user_id"]]=""
            if not os.path.exists("./user/p%s"%rev["sender"]["user_id"]):
                os.makedirs("./user/p%s"%rev["sender"]["user_id"])
                with open("./user/p%s/memory.txt"%rev["sender"]["user_id"],"w") as tpass:
                    pass
            if not os.path.exists("./user/p%s/I_memory.txt"%rev["sender"]["user_id"]):
                with open("./user/p%s/I_memory.txt"%rev["sender"]["user_id"],"w") as tpass:
                    pass
            if not os.path.exists("./user/p%s/setting.json"%rev["sender"]["user_id"]):
                data={'mood':'default','random_trigger':random_trigger,"root_id":root_ids}
                with open("./user/p%s/setting.json"%rev["sender"]["user_id"], 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            if "[CQ:image,"  not in rev['raw_message']:
                objdict["banaijian%schat"%rev["sender"]["user_id"]]+=(rev["sender"]["nickname"]+"："+rev['raw_message'].replace('[CQ:at,qq=%d]'%rev['self_id'],'')+'\n\n')
                objdict["banaijian%schat"%rev["sender"]["user_id"]]=objdict["banaijian%schat"%rev["sender"]["user_id"]][-50:]

            if True:
                a=objdict["banaijian%schat"%rev["sender"]["user_id"]]
                print(a)
                self_id=random.randrange(100000,999999)
                objdict["banaijian%sgeneing"%rev["sender"]["user_id"]]=[self_id] 
                rev['raw_message']=rev['raw_message'].replace('[CQ:at,qq=%d]'%rev['self_id'],'')
                if "banaijian%s"%rev["sender"]["user_id"] not in objdict.keys():
                    objdict["banaijian%s"%rev["sender"]["user_id"]]=[[{'role':'system','content':system}]]
                if '#reset' in rev['raw_message']:
                    objdict["banaijian%s"%rev["sender"]["user_id"]]=[[{'role':'system','content':system}]]
                    send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': '[已清空对话历史]'})
                if '#clear' in rev['raw_message']:
                    delete_subfolders("./user/p%s"%rev["sender"]["user_id"])
                    send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': '[已清空个人私聊记忆]'})
                if '#erase' in rev['raw_message'] and rev['user_id'] in root_ids:
                    delete_subfolders("./user/")
                    send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': '[已清空所有记忆]'})

                else:
                    processed_d_data="强制切换意图"
                    if random.randrange(0,2)==0:#在这里切换情感复原的概率
                        objdict["banaijian%s"%rev["sender"]["user_id"]][0][0]={"role":"system","content":system_prompts["default"]}
                    if weihu:
                        send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "维护中..."})
                        raise KeyboardInterrupt("维护ing")
                    
                    print(processed_d_data)
                    if not processed_d_data:
                        processed_d_data='.'

                    turl=user_api
                    headers={
                                "Content-Type": "application/json",
                                "Authorization": "Bearer "+user_key
                        }
                    messages=objdict["banaijian%s"%rev["sender"]["user_id"]][0]+[{"role":"user","content":objdict["banaijian%schat"%rev["sender"]["user_id"]]+"[tips]需要引用对方消息务必按照格式：[CQ:reply,id=%s]你要说的话"%rev['message_id']}]
                    keywords = jieba.analyse.extract_tags(rev['raw_message'].replace(AI_name,""), topK=50)
                    s_memory=get_memory("./user/p%s/memory.txt"%rev["sender"]["user_id"],keywords)
                    s_memory+=get_I_memory("./user/p%s/I_memory.txt"%rev["sender"]["user_id"])
                    char_memory=get_memory("./data/char.txt",keywords)
                    print(s_memory)
                    print(char_memory)
                    data={
                            "model": user_chat_model,##claude-3-opus-vf
                            "messages":merge_contents([{"role":"system","content":messages[0]["content"]+"[memory](经验 无时效性)\n%s\n"%char_memory+"[memory](模糊 无时效性)\n%s\n"%s_memory+e_information}]+messages[1:]),
                            "stream": True,
                            "use_search": False
                        }
                    is_return=True
                    while is_return:
                        is_return=False
                        for _ in range(0,3):
                            try:
                                response=requests.post(url=turl,headers=headers,stream=True,data=json.dumps(data))
                                if response.status_code==200:
                                    break
                                print("请求错误，尝试兜底模型")
                                data["model"]=chat_models[0]["model_name"]
                                turl=chat_models[0]["model_api"]
                                user_key=chat_models[0]["model_key"]
                                headers={
                                        "Content-Type": "application/json",
                                        "Authorization": "Bearer "+user_key
                                }
                            except Exception as e:
                                print("请求错误，尝试兜底模型：",e)
                                data["model"]=chat_models[0]["model_name"]
                                turl=chat_models[0]["model_api"]
                                user_key=chat_models[0]["model_key"]
                                headers={
                                        "Content-Type": "application/json",
                                        "Authorization": "Bearer "+user_key
                                }
                        is_not_remove_emoji=random.randrange(0,3)#设置清除emoji概率
                        temp_tts_list=[]
                        processed_d_data1=''
                        for line in response.iter_lines():
                            try:
                                decoded=line.decode('utf-8').replace('\n','\\n').replace('\b','\\b').replace('\f','\\f').replace('\r','\\r').replace('\t','\\t')
                                if decoded != '':
                                    temp_processed_d_data1=json.loads(decoded[5:])["choices"][0]["delta"]["content"]
                            except Exception as e:
                                continue
                                pass
                            if decoded != '':
                                for p_token in temp_processed_d_data1:
                                    processed_d_data1+=p_token
                                    if not is_not_remove_emoji:
                                        processed_d_data1=remove_emojis(processed_d_data1)
                                    lastlen=len(temp_tts_list)
                                    temp_tts_list=processed_d_data1.split("#cut#")
                                    if not temp_tts_list:
                                        temp_tts_list=temp_tts_list[:-1]
                                    if self_id not in objdict["banaijian%sgeneing"%rev["sender"]["user_id"]]:
                                        objdict["banaijian%s"%rev["sender"]["user_id"]][0]=objdict["banaijian%s"%rev["sender"]["user_id"]][0]+[{'role':'user','content':rev['raw_message']},{'role':'assistant','content':processed_d_data1}]
                                        raise InterruptedError("新消息中断") # 防人工刷屏
                                    
                                    if len(temp_tts_list)>1 and lastlen < len(temp_tts_list):
                                        if '#voice/' in temp_tts_list[-2]:
                                            try:
                                                voice=temp_tts_list[-2].split('#voice/')[-1].replace("#",'')
                                                tts_data = {
                                                "cha_name": speaker,#这里填本地语音合成包里面配置好的说话人
                                                "text": voice.replace("...", "…").replace("…", ","),
                                                "character_emotion":random.choice(['default','angry','excited','narration-relaxed','depressed'])
                                                }
                                                b_wav = requests.post(
                                                    url='http://127.0.0.1:5000/tts', json=tts_data
                                                    )
                                                n=random.randrange(10000,99999)
                                                name='%stts%d.wav'%((time.strftime('%F')+'-'+time.strftime('%T').replace(':','-')),n)
                                                to_path='./data/voice/%s'%name
                                                with open(to_path,'wb') as wbf:
                                                    wbf.write(b_wav.content)
                                                send_voice({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg':name })
                                            except Exception as e:
                                                send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "语音合成失败"})
                                                print("暂不支持语音合成")
                                        elif '#picture/' in temp_tts_list[-2]:
                                            picture=temp_tts_list[-2].split('#picture/')[-1].replace("#",'')
                                            print(picture)
                                            draw_private(picture,rev["sender"]["user_id"])
                                        elif '#search/' in temp_tts_list[-2]:
                                                response.close()
                                                temp_tts_list=temp_tts_list[:-1]
                                                break
                                        elif '#memory/' in temp_tts_list[-2]:
                                            memory=temp_tts_list[-1].split('#memory/')[-1].replace("#",'')
                                            print("写入记忆：",memory)    
                                            with open("./user/p%s/I_memory.txt"%rev["sender"]["user_id"],"a",encoding="utf-8") as mem:
                                                mem.write(" "+memory) 
                                            if send_debug:
                                                send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "[写入记忆]"})
                                        elif "#pass/" in temp_tts_list[-2]:
                                            response.close()
                                            if send_debug:
                                                send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "[pass]"})
                                            raise KeyboardInterrupt("AI认为应该跳过此回复！")
                                        elif "#emotion/" in temp_tts_list[-2]:
                                            t_emotion=temp_tts_list[-2].split("#emotion/")[-1].replace("#",'')
                                            e_image_list=os.listdir("./data/image/%s"%t_emotion)
                                            e_image=random.choice(e_image_list)
                                            send_image({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg':"%s/%s"%(t_emotion,e_image)})
                                        elif "#mood/" in temp_tts_list[-2]:
                                            t_mood=temp_tts_list[-2].split("#mood/")[-1].replace("#",'')
                                            try:
                                                objdict["banaijian%s"%rev["sender"]["user_id"]][0][0]={"role":"system","content":system_prompts[t_mood]}
                                                change_setting("./user/p%s/setting.json"%rev["sender"]["user_id"],"mood",t_mood)
                                                if send_debug:
                                                    send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "[%s]"%t_mood})
                                            except Exception as e:
                                                print("切换情感错误：",e)
                                        elif "#music/" in temp_tts_list[-2]:
                                            t_music_n=temp_tts_list[-2].split("#music/")[-1].replace("#",'')
                                            smusic_l=os.listdir("./data/voice/smusic")
                                            is_find_m=False
                                            for p_music_n in smusic_l:
                                                if t_music_n in p_music_n:
                                                    is_find_m=True
                                                    send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "《%s》"%p_music_n})
                                                    send_voice({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg':"smusic/"+p_music_n})
                                                    break
                                            if not is_find_m:
                                                send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "[未找到合适歌曲]"})
                                        else:
                                            for ban_word in ban_words:
                                                ban_text=temp_tts_list[-2].replace("%s"%ban_word,"")
                                                temp_tts_list[-2]=ban_text
                                            send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': temp_tts_list[-2].replace("%s："%AI_name,"").replace("%s:"%AI_name,"")})
                        if "抱歉" in temp_tts_list[-1]:
                            objdict["banaijian%s"%rev["sender"]["user_id"]][0]=[objdict["banaijian%s"%rev["sender"]["user_id"]][0][0]]
                            print("催眠失败，重置记忆")
                        else:
                            if '#voice/' in temp_tts_list[-1]:
                                voice=temp_tts_list[-1].split('#voice/')[-1].replace("#",'')
                                tts_data = {
                                    "cha_name": speaker,#这里填本地语音合成包里面配置好的说话人
                                    "text": voice.replace("...", "…").replace("…", ","),
                                    "character_emotion":random.choice(['default','angry','excited','narration-relaxed','depressed'])
                                    }
                                b_wav = requests.post(
                                    url='http://127.0.0.1:5000/tts', json=tts_data
                                    )
                                n=random.randrange(10000,99999)
                                name='%stts%d.wav'%((time.strftime('%F')+'-'+time.strftime('%T').replace(':','-')),n)
                                to_path='./data/voice/%s'%name
                                with open(to_path,'wb') as wbf:
                                    wbf.write(b_wav.content)
                                send_voice({'msg_type': 'private', 'number':rev["sender"]["user_id"], 'msg':name })
                            elif '#picture/' in temp_tts_list[-1]:
                                picture=temp_tts_list[-1].split('#picture/')[-1].replace("#",'')
                                print(picture)
                                draw_private(picture,rev["sender"]["user_id"])
                            elif '#search/' in temp_tts_list[-1]:
                                
                                s_prompt=temp_tts_list[-1].split('#search/')[-1].replace("#",'')
                                send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "正在联网搜索：%s"%s_prompt})
                                search_result=search(s_prompt)
                                print(search_result)
                                objdict["banaijian%s"%rev["sender"]["user_id"]][0]+=[{'role':'user','content':rev['raw_message']},{'role':'assistant','content':processed_d_data1+"""\nsystem[搜索结果不可见]：正在联网搜索：%s\n搜索结果：\n%s\n由于system返回的搜索结果你应该看不见，我将用自己的话详细，具体的讲述一下搜索结果。"""%(s_prompt,search_result)},{"role":"user","content":"开始详细具体的讲述吧"}]
                                messages=objdict["banaijian%s"%rev["sender"]["user_id"]][0]
                                data={
                                    "model": user_chat_model,##claude-3-opus-vf
                                    "messages":merge_contents([{"role":"system","content":system_prompt+"[order]\n1. 每句话之间使用#cut#分割开，每段话直接也使用#cut#分割开，你如：“#cut#你好。群友。#cut#幻日老爹在不？#cut#”\n"+e_information}]+messages[1:]),
                                    "stream": True,
                                    "use_search": False
                                }
                                is_return=True
                                continue
                            elif '#memory/' in temp_tts_list[-1]:
                                memory=temp_tts_list[-1].split('#memory/')[-1].replace("#",'')
                                print("写入记忆：",memory)    
                                with open("./user/p%s/I_memory.txt"%rev["sender"]["user_id"],"a",encoding="utf-8") as mem:
                                    mem.write(" "+memory) 
                                if send_debug:
                                    send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "[写入记忆]"})
                            elif "#pass/" in temp_tts_list[-1]:
                                if send_debug:
                                    send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "[pass]"})
                                raise KeyboardInterrupt("AI认为应该跳过此回复！")
                            elif "#emotion/" in temp_tts_list[-1]:
                                t_emotion=temp_tts_list[-1].split("#emotion/")[-1].replace("#",'')
                                e_image_list=os.listdir("./data/image/%s"%t_emotion)
                                e_image=random.choice(e_image_list)
                                send_image({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg':"%s/%s"%(t_emotion,e_image)})
                            elif "#mood/" in temp_tts_list[-1]:
                                t_mood=temp_tts_list[-1].split("#mood/")[-1].replace("#",'')
                                try:
                                    objdict["banaijian%s"%rev["sender"]["user_id"]][0][0]={"role":"system","content":system_prompts[t_mood]}
                                    change_setting("./user/p%s/setting.json"%rev["sender"]["user_id"],"mood",t_mood)
                                    if send_debug:
                                        send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "[%s]"%t_mood})
                                except Exception as e:
                                    print("切换情感错误：",e)
                            elif "#music/" in temp_tts_list[-1]:
                                t_music_n=temp_tts_list[-1].split("#music/")[-1].replace("#",'')
                                smusic_l=os.listdir("./data/voice/smusic")
                                is_find_m=False
                                for p_music_n in smusic_l:
                                    if t_music_n in p_music_n:
                                        is_find_m=True
                                        send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "《%s》"%t_music_n})
                                        send_voice({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg':"smusic/"+t_music_n})
                                        break
                                if not is_find_m:
                                    send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': "[未找到合适歌曲]"})
                            # 兼容思维链（春日）
                            else:
                                if "think" in processed_d_data1:
                                    keyword = "```"
                                    pattern = f"{keyword}(.*?)```"
                                    temp_msg = processed_d_data1.replace("\n", "")
                                    match = re.search(pattern, temp_msg)
                                    think = match.group(1)
                                    print(think)
                                    print(temp_msg)
                                    try:
                                        temp_msg = temp_msg.replace(think, "").replace("```", "")
                                        if temp_msg == "":
                                            print("无响应")
                                        temp_msg = temp_msg.split("#cut#")
                                        print(temp_msg)
                                        lenn = len(temp_msg)
                                        while lenn > 0:
                                            for ban_word in ban_words:
                                                ban_text=temp_msg[-lenn].replace("%s"%ban_word,"")
                                                temp_msg[-lenn]=ban_text
                                            send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"],
                                                      'msg': temp_msg[-lenn].replace("%s："%AI_name,"").replace("%s:"%AI_name,"").replace("```", "")})
                                            lenn -= 1
                                    except:
                                        pass
                                else:
                                    for ban_word in ban_words:
                                        ban_text=temp_tts_list[-1].replace("%s"%ban_word,"")
                                        temp_tts_list[-1]=ban_text
                                    send_msg({'msg_type': 'private', 'number': rev["sender"]["user_id"], 'msg': temp_tts_list[-1].replace("%s："%AI_name,"").replace("%s:"%AI_name,"")})
                            print(processed_d_data1)
                            objdict["banaijian%s"%rev["sender"]["user_id"]][0]=objdict["banaijian%s"%rev["sender"]["user_id"]][0]+[{'role':'user','content':rev['raw_message']},{'role':'assistant','content':processed_d_data1}]
                            with open(
                                    "./user/p%s/memory.txt"%rev["sender"]["user_id"],
                                    "a",
                                    encoding="utf-8",
                                ) as txt:
                                    timestamp = time.time()
                                    localtime = time.localtime(timestamp)
                                    current_time = time.strftime(
                                        "%Y-%m-%d %H:%M:%S", localtime
                                    )
                                    txt.write(
                                        "[%s]我说：%s\n" % (current_time, rev['raw_message'])
                                    )
                                    txt.write(
                                        "[%s]你回复：%s\n"
                                        % (current_time, processed_d_data1)
                                    )
            print("未发现新消息...运行时间：%f"%(time.time()-startT))
            if len(objdict["banaijian%s"%rev["sender"]["user_id"]][0])> 10:
                objdict["banaijian%s"%rev["sender"]["user_id"]][0]=[objdict["banaijian%s"%rev["sender"]["user_id"]][0][0]]+objdict["banaijian%s"%rev["sender"]["user_id"]][0][-6:]  
            objdict["banaijian%schat"%rev["sender"]["user_id"]]=''
            

        elif rev["message_type"] == "group":
            if ("团子" in rev["sender"]["nickname"] or "芙芙" in rev["sender"]["nickname"] or "炼丹师" in rev["sender"]["nickname"] or "行己之道" in rev["sender"]["nickname"]) and "[CQ:image," in rev['raw_message']:
                time.sleep(5+random.randrange(0,5))
                message_id=rev['message_id']
                res=requests.post('http://localhost:3000/delete_msg', json={
                    'message_id': message_id, #撤回机器人图片（需群管理员权限）
                })
                print("delete_msg:",rev['raw_message'],json.loads(res.content))

            pass_ban=False
            for ban_name in ban_names:
                if ban_name in rev["sender"]["nickname"]:
                    pass_ban = True
                    break
            if pass_ban:
                raise RuntimeError("break limitless turn")#屏蔽指定名称qq
            

            if "banaijian%schat"%rev['group_id'] not in objdict.keys():#创建目录
                objdict["banaijian%schat"%rev['group_id']]=""
            if not os.path.exists("./user/g%s"%rev['group_id']):
                os.makedirs("./user/g%s"%rev['group_id'])
                with open("./user/g%s/memory.txt"%rev['group_id'],"w") as tpass:
                    pass
            if not os.path.exists("./user/g%s/I_memory.txt"%rev['group_id']):
                with open("./user/g%s/I_memory.txt"%rev['group_id'],"w") as tpass:
                    pass
            if not os.path.exists("./user/g%s/setting.json"%rev['group_id']):
                data={'mood':'default','random_trigger':random_trigger,"root_id":root_ids}
                with open("./user/g%s/setting.json"%rev['group_id'], 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

            
            if "[CQ:image,"  not in rev['raw_message']:#组建单次回复上下文
                objdict["banaijian%schat"%rev['group_id']]=objdict["banaijian%schat"%rev['group_id']][-70:]
                objdict["banaijian%schat"%rev['group_id']]+=("["+rev["sender"]["nickname"]+"]说："+rev['raw_message'].replace('[CQ:at,qq=%d,name=%s]'%(rev['self_id'],AI_name),AI_name)+'\n\n')
                
            if "#settitle:" in rev['raw_message']:#自动设置头衔（暂时无效）
                title=rev['raw_message'].split(':',1)[-1][:5]
                res=requests.post('http://localhost:3000/set_group_special_title', json={
                    'group_id': rev['group_id'],
                    'user_id': rev['user_id'],
                    'special_title':title,
                    'duration':-1
                })
                print("set_group_special_title:",rev['raw_message'].split(':',1)[-1][:5],json.loads(res.content))
            with open("./user/g%s/setting.json"%rev['group_id'], 'r', encoding='utf-8') as f:
                tt_gsetting=json.load(f)
            tt_random_trigger=tt_gsetting["random_trigger"]
            root_id=tt_gsetting["root_id"]
            is_trigger=False#比对触发词
            for trigger in triggers:
                if trigger in rev['raw_message']:
                    is_trigger = True
                    break
            if (is_trigger or '[CQ:at,qq=%d]'%rev['self_id'] in rev['raw_message'] or random.randrange(0,tt_random_trigger)==0):#触发回复
                a=objdict["banaijian%schat"%rev['group_id']]
                print(a)
                self_id=random.randrange(100000,999999)
                objdict["banaijian%sgeneing"%rev['group_id']]=[self_id] 
                rev['raw_message']=rev['raw_message'].replace('[CQ:at,qq=%d,name=%s]'%(rev['self_id'],AI_name),'')
                if "banaijian%s"%rev['group_id'] not in objdict.keys():
                    objdict["banaijian%s"%rev['group_id']]=[[{'role':'system','content':system}]]
                if '#reset' in rev['raw_message']:
                    objdict["banaijian%s"%rev['group_id']]=[[{'role':'system','content':system}]]
                    send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': '[已清空对话历史]'})
                if '#clear' in rev['raw_message'] and rev['user_id'] in root_ids:
                    delete_subfolders("./user/g%s"%rev['group_id'])
                    send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': '[已清空此群聊记忆]'})
                if '#erase' in rev['raw_message'] and rev['user_id'] in root_ids:
                    delete_subfolders("./user/")
                    send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': '[已清空全部记忆]'})
                elif "#mood" in rev['raw_message'] and rev['user_id'] in root_id:
                    for tt_mood in system_prompts.keys():
                        if tt_mood in rev['raw_message'].replace("#mood",""):
                            objdict["banaijian%s"%rev['group_id']]=[[{'role':'system','content':system_prompts[tt_mood]}]]
                            change_setting("./user/g%s/setting.json"%rev['group_id'],"mood",tt_mood)
                            send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': '[%s]'%tt_mood}) 
                            break
                elif "#forcememory" in rev['raw_message'] and rev['user_id'] in root_id:
                    force_memory=rev['raw_message'].split("#forcememory")[-1]
                    with open("./user/g%s/I_memory.txt"%rev['group_id'],"a",encoding="utf-8") as mem:
                        mem.write(" "+force_memory)
                    send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': '[强制写入记忆]'}) 
                elif "#forceallmemory" in rev['raw_message'] and rev['user_id'] in root_ids:
                    force_memory=rev['raw_message'].split("#forceallmemory")[-1]
                    user_list_m=os.listdir("./user")
                    for per_user_m in user_list_m:
                        with open("./user/%s/I_memory.txt"%(per_user_m),"a",encoding="utf-8") as mem:
                            mem.write(" "+force_memory)
                    send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': '[全频道写入记忆]'}) 
                elif "#addid" in rev['raw_message'] and rev['user_id'] in root_ids:
                    addid=rev['raw_message'].split("#addid")[-1]
                    root_id.append(int(addid.replace(" ","")))
                    change_setting("./user/g%s/setting.json"%rev['group_id'],"root_id",root_id)  
                    send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': '[添加管理员ID]'})      
                elif "#random" in rev['raw_message'] and rev['user_id'] in root_id:
                    t_random_trigger=int(rev['raw_message'].split(" ")[-1])
                    change_setting("./user/g%s/setting.json"%rev['group_id'],"random_trigger",t_random_trigger)
                    if t_random_trigger<=0:
                        send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': '[已关机]'}) 
                    else:
                        send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': '[触发率设置为1/%d]'%t_random_trigger}) 
                    
                else:        
                    if tt_random_trigger < 1:
                        raise KeyboardInterrupt("群聊已停止回复")
                    processed_d_data="强制切换意图"
                    turl=user_api
                    # if rev['group_id'] != 930214132 and jieyue:
                    #     # send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': "[illue quota is not enough]"})
                    #     # raise KeyboardInterrupt("节约token")
                    #     user_key="sk-OBOxTsNA8Gz9DuMQAc4669399f7a4b3fAaE3Ee91C2068d0f"
                    #     user_chat_model="gpt-4o"
                    #     turl="http://154.37.221.52:3000/v1/chat/completions"
                    if random.randrange(0,7)==0:#在这里切换情感复原的概率
                        objdict["banaijian%s"%rev['group_id']][0][0]={"role":"system","content":system_prompts["default"]}
                    if weihu:
                        send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': "[维护中...]"})
                        raise KeyboardInterrupt("维护ing")
                    print(processed_d_data)
                    if not processed_d_data:
                        processed_d_data='.'
                    turl=user_api
                    headers={
                                "Content-Type": "application/json",
                                "Authorization": "Bearer "+user_key
                        }
                    messages=objdict["banaijian%s"%rev['group_id']][0]+[{"role":"user","content":objdict["banaijian%schat"%rev['group_id']]+"[tips]需要引用对方消息务必按照格式：[CQ:reply,id=%s]你要说的话 ，需要@对方务必按照格式：[CQ:at,qq=%s,name=%s]你要说的话"%(rev['message_id'],rev["sender"]["nickname"],rev['sender']['user_id'])}]
                    keywords = jieba.analyse.extract_tags(rev['raw_message'].replace(AI_name,""), topK=50)
                    s_memory=get_memory("./user/g%s/memory.txt"%rev['group_id'],keywords,match_n=500)
                    s_memory+=get_I_memory("./user/g%s/I_memory.txt"%rev['group_id'])
                    char_memory=get_memory("./data/char.txt",keywords)
                    print(s_memory)
                    print(char_memory)
                    data={
                            "model": user_chat_model,
                            "messages":merge_contents([{"role":"system","content":messages[0]["content"]+"[memory](经验 无时效性)\n%s\n"%char_memory+"[memory](模糊 无时效性)\n%s\n"%s_memory+e_information}]+messages[1:]),
                            "stream": True
                        }
                    is_return=True
                    while is_return:
                        is_return=False
                        for _ in range(0,3):
                            try:
                                response=requests.post(url=turl,headers=headers,stream=True,data=json.dumps(data))
                                if response.status_code==200:
                                    break
                                print("请求错误，尝试兜底模型")
                                data["model"]=chat_models[0]["model_name"]
                                turl=chat_models[0]["model_api"]
                                user_key=chat_models[0]["model_key"]
                                headers={
                                        "Content-Type": "application/json",
                                        "Authorization": "Bearer "+user_key
                                }
                            except Exception as e:
                                print("请求错误，尝试兜底模型：",e)
                                data["model"]=chat_models[0]["model_name"]
                                turl=chat_models[0]["model_api"]
                                user_key=chat_models[0]["model_key"]
                                headers={
                                        "Content-Type": "application/json",
                                        "Authorization": "Bearer "+user_key
                                }
                        is_not_remove_emoji=random.randrange(0,3)#设置清除emoji概率
                        temp_tts_list=[]
                        processed_d_data1=''
                        for line in response.iter_lines():
                            try:
                                decoded=line.decode('utf-8').replace('\n','\\n').replace('\b','\\b').replace('\f','\\f').replace('\r','\\r').replace('\t','\\t')
                                if decoded != '':
                                    temp_processed_d_data1=json.loads(decoded[5:])["choices"][0]["delta"]["content"]
                            except Exception as e:
                                print(decoded,e)
                                continue
                                pass
                            if decoded != '':
                                for p_token in temp_processed_d_data1:
                                    processed_d_data1+=p_token
                                    if not is_not_remove_emoji:
                                        processed_d_data1=remove_emojis(processed_d_data1)
                                    lastlen=len(temp_tts_list)
                                    temp_tts_list=processed_d_data1.split("#cut#")
                                    if not temp_tts_list:
                                        temp_tts_list=temp_tts_list[:-1]
                                    if self_id not in objdict["banaijian%sgeneing"%rev['group_id']]:
                                        objdict["banaijian%s"%rev['group_id']][0]=objdict["banaijian%s"%rev['group_id']][0]+[{'role':'user','content':rev['raw_message']},{'role':'assistant','content':processed_d_data1}]
                                        raise InterruptedError("新消息中断")
                                    
                                    if len(temp_tts_list)>1 and lastlen < len(temp_tts_list):
                                        if '#voice/' in temp_tts_list[-2]:
                                            try:
                                                voice=temp_tts_list[-2].split('#voice/')[-1].replace("#",'')
                                                tts_data = {
                                                "cha_name": speaker,#这里填本地语音合成包里面配置好的说话人
                                                "text": voice.replace("...", "…").replace("…", ","),
                                                "character_emotion":random.choice(['default','angry','excited','narration-relaxed','depressed'])
                                                }
                                                b_wav = requests.post(
                                                    url='http://127.0.0.1:5000/tts', json=tts_data
                                                    )
                                                n=random.randrange(10000,99999)
                                                name='%stts%d.wav'%((time.strftime('%F')+'-'+time.strftime('%T').replace(':','-')),n)
                                                to_path='./data/voice/%s'%name
                                                with open(to_path,'wb') as wbf:
                                                    wbf.write(b_wav.content)
                                                send_voice({'msg_type': 'group', 'number': rev['group_id'], 'msg':name })
                                            except Exception as e:
                                                print("暂不支持语音合成")
                                        elif '#picture/' in temp_tts_list[-2]:
                                            picture=temp_tts_list[-2].split('#picture/')[-1].replace("#",'')
                                            print(picture)
                                            draw_group(picture,rev['group_id'])
                                        elif '#search/' in temp_tts_list[-2]:
                                            response.close()
                                            temp_tts_list=temp_tts_list[:-1]
                                            break
                                        elif '#memory/' in temp_tts_list[-2]:
                                            memory=temp_tts_list[-2].split('#memory/')[-1].replace("#",'')
                                            print("写入记忆：",memory)    
                                            with open("./user/g%s/I_memory.txt"%rev['group_id'],"a",encoding="utf-8") as mem:
                                                mem.write(" "+memory)
                                            if send_debug:
                                                send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': "[写入记忆]"})
                                        elif "#pass/" in temp_tts_list[-2]:
                                            response.close()
                                            if send_debug:
                                                send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': "[pass]"})
                                            raise KeyboardInterrupt("AI认为应该跳过此回复！")
                                        elif "#emotion/" in temp_tts_list[-2]:
                                            t_emotion=temp_tts_list[-2].split("#emotion/")[-1].replace("#",'')
                                            e_image_list=os.listdir("./data/image/%s"%t_emotion)
                                            e_image=random.choice(e_image_list)
                                            send_image({'msg_type': 'group', 'number': rev['group_id'], 'msg':"%s/%s"%(t_emotion,e_image)})
                                        elif "#mood/" in temp_tts_list[-2]:
                                            t_mood=temp_tts_list[-2].split("#mood/")[-1].replace("#",'')
                                            try:
                                                objdict["banaijian%s"%rev['group_id']][0][0]={"role":"system","content":system_prompts[t_mood]}
                                                change_setting("./user/g%s/setting.json"%rev['group_id'],"mood",t_mood)
                                                if send_debug:
                                                    send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': "[%s]"%t_mood})
                                            except Exception as e:
                                                print("切换情感错误：",e)
                                        elif "#music/" in temp_tts_list[-2]:
                                            t_music_n=temp_tts_list[-2].split("#music/")[-1].replace("#",'')
                                            
                                            send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': f"歌曲《{t_music_n}》学习进度：0%"})
                                            datam={"name":t_music_n,"speaker":singer,"low":True}
                                            response1 = requests.post(url="http://127.0.0.1:3333",data=json.dumps(datam),stream=True)
                                            for line in response1.iter_lines():
                                                decoded = (
                                                    line.decode("unicode_escape")
                                                    .replace("\b", "\\b")
                                                    .replace("\f", "\\f")
                                                    .replace("\r", "\\r")
                                                    .replace("\t", "\\t")
                                                    .replace("\n", "\\n")
                                                )
                                                done = json.loads(decoded)["done"]
                                                send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': f"歌曲《{t_music_n}》学习进度：{done}%"})
                                                if done == 100:
                                                    file_name = json.loads(decoded)["name"]
                                                    if "error:" in file_name:
                                                        w_error = file_name.replace("error:","")
                                                        if w_error == "time":
                                                            send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': f"歌曲《{t_music_n}》学习失败，原因：歌曲过长"})
                                                        else:
                                                            send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': f"歌曲《{t_music_n}》学习失败，错误码：%s"%w_error})
                                                    else:
                                                        with open("./data/voice/smusic/%s"%file_name, "wb") as f:
                                                            response_wav = requests.get(url="http://127.0.0.1:3333/output/%s"%file_name).content
                                                            f.write(response_wav)
                                                        #copy_file("D:\\program-illusion\\realtime-song\\output\\%s"%file_name,"./data/voice/smusic")
                                                        requests.post(url="http://127.0.0.1:3333/removea/%s"%file_name,stream=True) 
                                                        send_voice({'msg_type': 'group', 'number': rev['group_id'], 'msg':"smusic/"+file_name})
                                                        time.sleep(random.randrange(0,3))
                                                        send_music({'msg_type': 'group', 'number': rev['group_id'], 'msg':"smusic/"+file_name})
                                                #send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': "[未找到合适歌曲]"})
                                        else:
                                            for ban_word in ban_words:
                                                ban_text=temp_tts_list[-2].replace("%s"%ban_word,"")
                                                temp_tts_list[-2]=ban_text
                                            send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': temp_tts_list[-2].replace("%s："%AI_name,"").replace("%s:"%AI_name,"")})
                        if "抱歉" in temp_tts_list[-1]:
                            objdict["banaijian%s"%rev['group_id']][0]=[objdict["banaijian%s"%rev['group_id']][0][0]]
                            print("催眠失败，重置记忆")
                        else:
                            if '#voice/' in temp_tts_list[-1]:
                                voice=temp_tts_list[-1].split('#voice/')[-1].replace("#",'')
                                tts_data = {
                                    "cha_name": speaker,#这里填本地语音合成包里面配置好的说话人
                                    "text": voice.replace("...", "…").replace("…", ","),
                                    "character_emotion":random.choice(['default','angry','excited','narration-relaxed','depressed'])
                                    }
                                b_wav = requests.post(
                                    url='http://127.0.0.1:5000/tts', json=tts_data
                                    )
                                n=random.randrange(10000,99999)
                                name='%stts%d.wav'%((time.strftime('%F')+'-'+time.strftime('%T').replace(':','-')),n)
                                to_path='./data/voice/%s'%name
                                with open(to_path,'wb') as wbf:
                                    wbf.write(b_wav.content)
                                send_voice({'msg_type': 'group', 'number': rev['group_id'], 'msg':name })
                            elif '#picture/' in temp_tts_list[-1]:
                                picture=temp_tts_list[-1].split('#picture/')[-1].replace("#",'')
                                print(picture)
                                draw_group(picture,rev['group_id'])
                            elif '#search/' in temp_tts_list[-1]:

                                s_prompt=temp_tts_list[-1].split('#search/')[-1].replace("#",'')
                                send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': "正在联网搜索：%s"%s_prompt})
                                search_result=search(s_prompt)
                                print(search_result)
                                objdict["banaijian%s"%rev['group_id']][0]+=[{'role':'user','content':rev['raw_message']},{'role':'assistant','content':processed_d_data1+"""\nsystem[搜索结果不可见]：正在联网搜索：%s\n搜索结果：\n%s\n由于system返回的搜索结果你应该看不见，我将用自己的话详细，具体的讲述一下搜索结果。"""%(s_prompt,search_result)},{"role":"user","content":"开始详细具体的讲述吧"}]
                                messages=objdict["banaijian%s"%rev['group_id']][0]
                                data={
                                    "model": user_chat_model,
                                    "messages":merge_contents([{"role":"system","content":system_prompt+"[order]\n1. 每句话之间使用#cut#分割开，每段话直接也使用#cut#分割开，你如：“#cut#你好。群友。#cut#幻日老爹在不？#cut#”\n"+e_information}]+messages[1:]),
                                    "stream": True,
                                    "use_search": False
                                }
                                is_return=True
                                continue
                            elif '#memory/' in temp_tts_list[-1]:
                                memory=temp_tts_list[-1].split('#memory/')[-1].replace("#",'')
                                print("写入记忆：",memory)    
                                with open("./user/g%s/I_memory.txt"%rev['group_id'],"a",encoding="utf-8") as mem:
                                    mem.write(" "+memory)
                                if send_debug:
                                    send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': "[写入记忆]"})
                            elif "#pass/" in temp_tts_list[-1]:
                                if send_debug:
                                    send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': "[pass]"})
                                raise KeyboardInterrupt("AI认为应该跳过此回复！")
                            elif "#emotion/" in temp_tts_list[-1]:
                                t_emotion=temp_tts_list[-1].split("#emotion/")[-1].replace("#",'')
                                e_image_list=os.listdir("./data/image/%s"%t_emotion)
                                e_image=random.choice(e_image_list)
                                send_image({'msg_type': 'group', 'number': rev['group_id'], 'msg':"%s/%s"%(t_emotion,e_image)})
                            elif "#mood/" in temp_tts_list[-1]:
                                t_mood=temp_tts_list[-1].split("#mood/")[-1].replace("#",'')
                                try:
                                    objdict["banaijian%s"%rev['group_id']][0][0]={"role":"system","content":system_prompts[t_mood]}
                                    change_setting("./user/g%s/setting.json"%rev['group_id'],"mood",t_mood)
                                    if send_debug:
                                        send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': "[%s]"%t_mood})
                                except Exception as e:
                                    print("切换情感错误：",e)
                            elif "#music/" in temp_tts_list[-1]:
                                t_music_n=temp_tts_list[-1].split("#music/")[-1].replace("#",'')
                                datam={"name":t_music_n,"speaker":singer,"low":True}
                                send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': f"歌曲《{t_music_n}》学习进度：0%"})
                                response1 = requests.post(url="http://127.0.0.1:3333",data=json.dumps(datam),stream=True) 
                                for line in response1.iter_lines():
                                    decoded = (
                                        line.decode("unicode_escape")
                                        .replace("\b", "\\b")
                                        .replace("\f", "\\f")
                                        .replace("\r", "\\r")
                                        .replace("\t", "\\t")
                                        .replace("\n", "\\n")
                                    )
                                    done = json.loads(decoded)["done"]
                                    send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': f"歌曲《{t_music_n}》学习进度：{done}%"})
                                    if done == 100:
                                        file_name = json.loads(decoded)["name"]
                                        if "error:" in file_name:
                                            w_error = file_name.replace("error:","")
                                            if w_error == "time":
                                                send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': f"歌曲《{t_music_n}》学习失败，原因：歌曲过长"})
                                            else:
                                                send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': f"歌曲《{t_music_n}》学习失败，错误码：%s"%w_error})
                                        else:
                                            with open("./data/voice/smusic/%s"%file_name, "wb") as f:
                                                response_wav = requests.get(url="http://127.0.0.1:3333/output/%s"%file_name).content
                                                f.write(response_wav)
                                            # copy_file("D:\\program-illusion\\realtime-song\\output\\%s"%file_name,"./data/voice/smusic")
                                            requests.post(url="http://127.0.0.1:3333/removea/%s"%file_name,stream=True) 
                                            send_voice({'msg_type': 'group', 'number': rev['group_id'], 'msg':"smusic/"+file_name})
                                            time.sleep(random.randrange(0,3))
                                            send_music({'msg_type': 'group', 'number': rev['group_id'], 'msg':"smusic/"+file_name})
                                    #send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': "[未找到合适歌曲]"})
                            # 兼容思维链（春日）
                            else:
                                if "think" in processed_d_data1:
                                    keyword = "```"
                                    pattern = f"{keyword}(.*?)```"
                                    temp_msg = processed_d_data1.replace("\n", "")
                                    match = re.search(pattern, temp_msg)
                                    think = match.group(1)
                                    print(think)
                                    print(temp_msg)
                                    try:
                                        temp_msg = temp_msg.replace(think, "").replace("```", "")
                                        if temp_msg == "":
                                            print("无响应")
                                        temp_msg = temp_msg.split("#cut#")
                                        print(temp_msg)
                                        lenn = len(temp_msg)
                                        while lenn > 0:
                                            for ban_word in ban_words:
                                                ban_text=temp_msg[-lenn].replace("%s"%ban_word,"")
                                                temp_msg[-lenn]=ban_text
                                            send_msg({'msg_type': 'group', 'number': rev['group_id'],
                                                      'msg': temp_msg[-lenn].replace("%s："%AI_name,"").replace("%s:"%AI_name,"").replace("```", "")})
                                            lenn -= 1
                                    except:
                                        pass
                                else:
                                    for ban_word in ban_words:
                                        ban_text=temp_tts_list[-2].replace("%s"%ban_word,"")
                                        temp_tts_list[-2]=ban_text
                                    send_msg({'msg_type': 'group', 'number': rev['group_id'], 'msg': temp_tts_list[-1].replace("%s："%AI_name,"").replace("%s:"%AI_name,"")})
                            print(processed_d_data1)
                            print(remark," ",user_chat_model)
                            objdict["banaijian%s"%rev['group_id']][0]=objdict["banaijian%s"%rev['group_id']][0]+[{'role':'user','content':rev['raw_message']},{'role':'assistant','content':processed_d_data1}]
                            with open(
                                "./user/g%s/memory.txt"%rev['group_id'],
                                "a",
                                encoding="utf-8",
                            ) as txt:
                                timestamp = time.time()
                                localtime = time.localtime(timestamp)
                                current_time = time.strftime(
                                    "%Y-%m-%d %H:%M:%S", localtime
                                )
                                txt.write(
                                    "[%s]%s\n" % (current_time, objdict["banaijian%schat"%rev['group_id']])
                                )
                                txt.write(
                                    "[%s]你回复：%s\n"
                                    % (current_time, processed_d_data1)
                                )
                        objdict["banaijian%schat"%rev['group_id']]=''
            print("未发现新消息...运行时间：%f"%(time.time()-startT))
            if len(objdict["banaijian%s"%rev['group_id']][0])> 18:
                objdict["banaijian%s"%rev['group_id']][0]=[objdict["banaijian%s"%rev['group_id']][0][0]]+objdict["banaijian%s"%rev['group_id']][0][-6:]
    except Exception as e:
        try:
            objdict["banaijian%schat"%rev['group_id']]=''
        except Exception as ee:
            print(remark," ",user_chat_model)
            print(ee)
        if debug:
            print(e)
            print(remark," ",user_chat_model)
        pass
