import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token='crystal901217', 
    appId = 'wx4b4055dd0d06f37e',
    appSecret = '84d49e751a3b04c56296444cca23d89c'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    return msg['Content']

itchatmp.run()
