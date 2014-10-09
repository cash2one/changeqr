#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-09-28 12:06:58
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-09 16:06:19

import time

from handler import handler, BaseHandler
from messages import TextMessage
from reply import ImageReply, TextReply
from wechat import Wechat

APP_ID = 'wx359b54263ab9dca2'
APP_SECRET = 'cb6f31c61fa644783cfab1ae736e5786'

UID = 'oFZijt71j9NzhSqQzVf1_Im3Ucn0'


@handler.register('text')
class SystemHandler(BaseHandler):

    def handle(self, message):
        reply = ImageReply(message=message, media_id='_media_id_')
        return reply.render()


@handler.register('event')
# @handler.register('text')
class AutoReplyHandler(BaseHandler):

    def handle(self, message):
        # reply = TextReply(message=message, content=u'Welcome')
        # return reply.render()
        # print message.wechat.get_menu()
        print message.scancodeinfo
        return message.wechat.reply_text('Hello')

menu = '''
{
	"button": [{
		"name": "扫码",
		"sub_button": [{
			"type": "scancode_waitmsg",
			"name": "扫码带提示",
			"key": "rselfmenu_0_0",
			"sub_button": []
		}, {
			"type": "scancode_push",
			"name": "扫码推事件",
			"key": "rselfmenu_0_1",
			"sub_button": []
		}]
	}, {
		"name": "发图",
		"sub_button": [{
			"type": "pic_sysphoto",
			"name": "系统拍照发图",
			"key": "rselfmenu_1_0",
			"sub_button": []
		}, {
			"type": "pic_photo_or_album",
			"name": "拍照或者相册发图",
			"key": "rselfmenu_1_1",
			"sub_button": []
		}, {
			"type": "pic_weixin",
			"name": "微信相册发图",
			"key": "rselfmenu_1_2",
			"sub_button": []
		}, {
			"name": "发送位置",
			"type": "location_select",
			"key": "rselfmenu_2_0"
		}]
	}, {
		"name": "菜单",
		"sub_button": [{
			"type": "view",
			"name": "搜索",
			"url": "http://www.baidu.com/"
		}, {
			"type": "view",
			"name": "视频",
			"url": "http://v.qq.com/"
		}, {
			"type": "click",
			"name": "赞一下我们",
			"key": "V1001_GOOD"
		}]
	}]
}
'''

wechat = Wechat(token='token', appid=APP_ID, appsecret=APP_SECRET)
# ret = wechat.create_menu(menu)
# ret = wechat.delete_menu()

# ret = wechat.upload_media('image', open('/tmp/1.jpg'))
# {u'media_id': u'JOFBapqABUkh70aBDdJsMrzwquGTkWiNISqVJrWTtXVm7D0BQxryZZRtLR8HqX7e', u'created_at': 1412060923, u'type': u'image'}

# ret = wechat.download_media('JOFBapqABUkh70aBDdJsMrzwquGTkWiNISqVJrWTtXVm7D0BQxryZZRtLR8HqX7e')
# with open('/tmp/tmp.jpg', 'w') as fp:
# 	fp.write(ret.content)

# print wechat.access_token

# ret = wechat.parse({
#     'signature': 'abc',
#     'timestamp': '1234',
#     'nonce': '1234'
# }, '''
# <xml><ToUserName><![CDATA[gh_95d589f53556]]></ToUserName>
# <FromUserName><![CDATA[oPfCTuMfbVNck6fjMjUUwGEhkWCE]]></FromUserName>
# <CreateTime>1409552501</CreateTime>
# <MsgType><![CDATA[event]]></MsgType>
# <Event><![CDATA[CLICK]]></Event>
# <EventKey><![CDATA[__CHANGWEI_WEIDIAN_KEY]]></EventKey>
# </xml>''')

# wechat.parse({
#     'signature': 'abc',
#     'timestamp': '1234',
#     'nonce': '1234'
# }, '''
# <xml>
#     <ToUserName><![CDATA[gh_b66be13d826e]]></ToUserName>
#     <FromUserName><![CDATA[oFZijt11OjA4i3Fq1jSjf1agboxw]]></FromUserName>
#     <CreateTime>1412062092</CreateTime>
#     <MsgType><![CDATA[event]]></MsgType>
#     <Event><![CDATA[scancode_waitmsg]]></Event>
#     <EventKey><![CDATA[rselfmenu_0_0]]></EventKey>
#     <ScanCodeInfo>
#         <ScanType><![CDATA[qrcode]]></ScanType>
#         <ScanResult><![CDATA[Hello World]]></ScanResult>
#         <EventKey><![CDATA[rselfmenu_0_0]]></EventKey>
#     </ScanCodeInfo>
# </xml>
# ''')

# ret = wechat.get_groups()
# {u'groups': [{u'count': 1, u'id': 0, u'name': u'\u672a\u5206\u7ec4'}, {u'count': 0, u'id': 1, u'name': u'\u9ed1\u540d\u5355'}, {u'count': 0, u'id': 2, u'name': u'\u661f\u6807\u7ec4'}]}
# {u'groups': [{u'count': 1, u'id': 0, u'name': u'\u672a\u5206\u7ec4'}, {u'count': 0, u'id': 1, u'name': u'\u9ed1\u540d\u5355'}, {u'count': 0, u'id': 2, u'name': u'\u661f\u6807\u7ec4'}, {u'count': 0, u'id': 100, u'name': u'\u4f60\u7684\u597d\u53cb'}]}

# ret = wechat.create_group(u'我的好友')
# {u'group': {u'id': 100, u'name': u'\u6211\u7684\u597d\u53cb'}}

# ret = wechat.get_group_by_openid('oFZijt11OjA4i3Fq1jSjf1agboxw')
# {u'groupid': 0}

# ret = wechat.update_group(100, u'你的好友')
# {u'errcode': 0, u'errmsg': u'ok'}

# ret = wechat.move_user('oFZijt11OjA4i3Fq1jSjf1agboxw', 100)
# {u'errcode': 0, u'errmsg': u'ok'}

# ret = wechat.get_followers()
# {u'count': 1, u'total': 1, u'data': {u'openid': [u'oFZijt11OjA4i3Fq1jSjf1agboxw']}, u'next_openid': u'oFZijt11OjA4i3Fq1jSjf1agboxw'}
# ret = wechat.get_followers(first_user_id='oFZijt11OjA4i3Fq1jSjf1agboxw')
# {u'count': 0, u'total': 1, u'next_openid': u''}


# ret = wechat.send_text_message(UID, u'你好')
# ret = wechat.send_image_message(UID, 'JOFBapqABUkh70aBDdJsMrzwquGTkWiNISqVJrWTtXVm7D0BQxryZZRtLR8HqX7e')

# ret = wechat.download_media('RrC5PV8nRPTdz0EVvOxUa_1nTOKN1HbjzVUEUmgWOmCCNKoRoJg9hxLCza4oldLB')
# with open('/tmp/voice.amr', 'w') as fp:
# 	fp.write(ret.content)

# ret = wechat.get_user_info(UID)
# {u'province': u'\u5317\u4eac', u'city': u'\u6d77\u6dc0', u'subscribe_time': 1412060454, u'headimgurl': u'http://wx.qlogo.cn/mmopen/5pztFxoEeQWnZKPz8FfPGmkmQB1RKp4nicroiaAe8BibtibTfkOaMUaPicpoiaYHvuQQCjzM64a3tXbPftia7N19GGgltlPka2ScfiaY/0', u'language': u'zh_CN', u'openid': u'oFZijt11OjA4i3Fq1jSjf1agboxw', u'country': u'\u4e2d\u56fd', u'remark': u'', u'sex': 1, u'subscribe': 1, u'nickname': u'\u7d2b\u7535\u9752\u971c'}

ret = wechat.send_text_message(UID, 
u'''1. 菜单1\n
2. <a href="http://www.baidu.com/" >超链接</a>\n
3. /::)\n
4. [呲牙]/呲牙/::D[难过]  /难过
5. /:bye/:xx/:!!!/:,@!/::8/:,@@/::L/::>/::,@/:,@f/::-S/:?/:,@x/::!/:|-)/::g/:,@o/::d/:,@-D/:,@P/::T/::Q/:--b/::+/::(/::O/::X/::Z/::'(/::-|/::@/::P/::D/::$/::</:8-)/::|
6. \ue136 \ue138 \ue12f \ue428 \ue341`
''')
print ret
