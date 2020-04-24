# coding = utf8
import requests
import itchatmp
import time
import tornado

KEY = 'fc5730155a3f4f4a898d8df37d9bcca2'


def tuling_get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,  # 这是要发送出去的信息
        'userid': 'wechat-robot',  # 这里随意写点什么都行
    }
    try:
        # 发送一个post请求
        r = requests.post(apiUrl, data=data).json()
        # 获取文本信息，若没有‘Text’ 值，将返回Nonoe
        return r.get('text')
    except:
        return


def getweatherinfo():
    weatherInfo = xiaobing("北京天气")
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
    response = requests.post(url_send, data=data, headers=headers, proxies=proxies).json()
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
    appSecret='a25e2e849f4a7b1f50286cdd063d94a5'))


@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    print('get message from:' + msg['User']['NickName'] + "\n" + msg['Text'])
    defaultReply = '[自动回复]已收到消息，谢谢'
    if msg['User']['NickName'] == 'D &amp; E' or msg['User']['NickName'] == 'Lori Liu':
        reply = xiaobing(msg['Text'])  # tuling_get_response
        if reply:
            print('ai reply with:' + reply)
            return reply
        else:
            return defaultReply
    else:
        return defaultReply


itchatmp.run()
