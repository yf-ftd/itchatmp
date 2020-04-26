#coding=utf8
import requests
import itchatmp
import time
import tornado
import thread
from apscheduler.schedulers.background import BlockingScheduler

KEY = ''
KEY_BARRY = '7f37aa284ef847eeaa6de19e6b7a198a'
KEY_LORI = '973729946b3e4b19a0188b4da1b34a06'
KEY_LINK = '54736610220840e3836ac573d9bcaf05'
KEY_VIC = '736dcf722ad846e7ac92051d62fdcac6'
KEY_CRYSTAL = 'b958e1635cfb4614a627c4590ffafe17'
key_list = (KEY_LORI,KEY_LINK,KEY_VIC,KEY_BARRY,KEY_CRYSTAL)
key_map = {}
userName='oXYjFjq1DBOQEDLX8PRlrWxg4g_k'

def send_weather_info_to_user():
    global key_map
    key_map.clear()
    #itchatmp.messages.send_all(itchatmp.content.TEXT,getweatherinfo())
    #itchatmp.send(getweatherinfo(),userName)

def tuling_get_response(msg):
    global KEY
    for key in key_list:
        if key_map.has_key(key):
            if key_map[key] == 100:
                pass
            else:
                key_map[key] = key_map[key] + 1
                print('current num:'+ str(key_map[key]))
                KEY = key
                break
        else:
            key_map[key] = 1
            KEY = key
            break
    print('current key:' + KEY)
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,  
        'userid': 'wechat-robot',  
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        if r.has_key('url'):
            return r.get('text') + '\n' + r.get('url')
        else:
            return r.get('text')
    except:
        return


def getweatherinfo():
    weatherInfo = tuling_get_response("明天朝阳天气")
    print(weatherInfo)
    return weatherInfo


def xiaobing(msg):
    uid = '5175429989'
    source = '209678993'
    SUB = '_2A25zpVgdDeRhGeRO6VIX9y7FwjmIHXVQ087VrDV8PUNbmtANLVHgkW9NUJEp5YIg84_GTvGQaCWNuZFdxf48os0V'
    url_send = 'https://api.weibo.com/webim/2/direct_messages/new.json'
    data = {'text': msg, 'uid': uid, 'source': source}
    headers = {'cookie': 'SUB=' + SUB, 'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/79.0.3945.130 Safari/537.36',
               'Referer': 'https://api.weibo.com/chat/'}
    response = requests.post(url_send, data=data, headers=headers).json()
    print(str(response))
    sendMsg = response['text']
    time.sleep(1)
    while True:
        url_get = 'https://api.weibo.com/webim/2/direct_messages/conversation.json?uid={}&source={}'.format(uid, source)
        response = requests.get(url_get, headers=headers).json()
        getMsg = response['direct_messages'][0]['text']
        if sendMsg == getMsg:
            time.sleep(1)
        else:
            return getMsg


itchatmp.update_config(itchatmp.WechatConfig(
    token='crystal901217',
    appId='wx4b4055dd0d06f37e',
    appSecret='84d49e751a3b04c56296444cca23d89c'))


@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    print('from user:' + msg['FromUserName'])
    print('get message:' + "\n" + msg['Content'])
    defaultReply = '[自动回复]已收到消息，谢谢'
    reply = tuling_get_response(msg['Content'])  # tuling_get_response
    if reply:
        print('ai reply with:' + reply)
        return reply
    else:
        return defaultReply


def get_user_list():
    nextId = ''
    totalUserSet = set()
    while 1:
        r = itchatmp.users.get_users(nextId)
        totalUserSet.update(r['data']['openid'])
        if len(totalUserSet) == r['total']:
            break
        else:
            nextId = r['next_openid']
    print(totalUserSet)


def keep_run(app):
    app.run()

thread.start_new_thread(keep_run,(itchatmp,))
scheduler = BlockingScheduler()
scheduler.add_job(send_weather_info_to_user,'cron',hour=23,minute=59)
try:
    scheduler.start()
except(KeyboardInterrupt,SystemExit):
    pass


