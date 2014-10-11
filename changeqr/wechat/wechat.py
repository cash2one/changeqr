#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 未实现接口：
# 高级群发接口、模板消息接口、设置用户备注名、获取用户地理位置、网页授权获取用户基本信息
# 多客服相关接口、微店接口、设备功能接口
# @Author: Hollay.Yan
# @Date:   2014-09-28 12:08:33
# @Last Modified by:   hollay
# @Last Modified time: 2014-10-11 22:01:10

import hashlib
import requests
import time
import json

from xml.dom import minidom

from messages import messager
from handler import handler
from reply import *
from exception import *

# from setting import token_cache_clazz
from conf import token_cache_clazz


class Wechat():

    __version = '1.0'
    __weixinversion = '2014-10-08'

    def __init__(self, token=None, appid=None, appsecret=None):
        '''
        access_token 使用redis进行缓存，key为appid，每次获取后将自动缓存到redis至过期;
        若redisserver 未指定，则
        :param token: 微信 Token
        :param appid: App ID
        :param appsecret: App Secret
        '''
        self.__token = token
        self.__appid = appid
        self.__appsecret = appsecret

        self.__handler = handler
        self.__is_parse = False

        self._token_cache = token_cache_clazz()

    def version(self):
        return 'SDK version %s, release at %s' % (self.__version, self.__weixinversion)

    def validate(self):
        '''
        验证微信消息真实性
        :param signature: 微信加密签名
        :param timestamp: 时间戳
        :param nonce: 随机数
        :return: 通过验证返回 True, 未通过验证返回 False
        '''
        self._check_token()

        if not self._timestamp or not self._nonce or not self._signature:
            return False

        tmp_list = [self.__token, self._timestamp, self._nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)
        if self._signature == hashlib.sha1(tmp_str).hexdigest():
            return True
        else:
            return False

    def _xml2dict(self, doc):
        result = {}

        params = [ele for ele in doc
                  .childNodes if isinstance(ele, minidom.Element)]

        for param in params:
            length = len(param.childNodes)

            if length > 1:
                result[param.tagName] = self._xml2dict(param)
            else:
                result[param.tagName] = len(param.childNodes) > 0 and param.childNodes[0].data or ''

        return result

    def parse(self, get, data, method='post'):
        '''
        解析微信服务器发送过来的数据并保存类中
        :param get: 微信服务器请求中的URL参数
        :param data: 微信服务器请求中的POST数据
        :param echo: 如果是GET请求，则返回echorstr
        :raises ParseError: 解析微信服务器数据错误, 数据不合法
        '''

        self._signature = get.get('signature', None)
        self._timestamp = get.get('timestamp', None)
        self._nonce = get.get('nonce', None)
        self._echostr = get.get('echostr', '')

        # 检查签名有效性
        if not self.validate():
            raise ParseError('签名错误')

        if method.lower() == 'get':
            return self._echostr

        # 解析消息
        result = {}
        if type(data) == unicode:
            data = data.encode('utf-8')
        elif type(data) == str:
            pass
        else:
            raise ParseError()

        try:
            doc = minidom.parseString(data)
        except Exception:
            raise ParseError('数据解析出错')

        result = self._xml2dict(doc.childNodes[0])

        result['raw'] = data
        result['type'] = result.pop('MsgType').lower()

        message_type = messager.get_message_class(result['type'])
        self.__message = message_type(result)
        self.__is_parse = True

        self.__message.wechat = self

        # 处理消息
        return self.__handler.handle(self.__message) or ''

    @property
    def access_token(self):
        '''
        微信接口access_token参数
        '''

        self._check_appid_appsecret()

        actoken = self._token_cache.get(self.__appid)

        if actoken:
            return actoken

        response_json = self.grant_token()
        self._token_cache.set(self.__appid, response_json['access_token'])

        return response_json['access_token']

    def grant_token(self):
        '''
        获取 access_token
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._get(
            url='https://api.weixin.qq.com/cgi-bin/token',
            params={
                'grant_type': 'client_credential',
                'appid': self.__appid,
                'secret': self.__appsecret,
            }
        )

    # 消息回复
    def reply_text(self, content):
        '''
        将文字信息 content 组装为符合微信服务器要求的响应数据
        :param content: 回复文字
        :return: 符合微信服务器要求的 XML 响应数据
        '''

        return TextReply(message=self.__message, content=content).render()

    def reply_image(self, media_id):
        '''
        将 media_id 所代表的图片组装为符合微信服务器要求的响应数据
        :param media_id: 图片的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据
        '''
        self._check_parse()

        return ImageReply(message=self.__message, media_id=media_id).render()

    def reply_voice(self, media_id):
        '''
        将 media_id 所代表的语音组装为符合微信服务器要求的响应数据
        :param media_id: 语音的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据
        '''
        self._check_parse()

        return VoiceReply(message=self.__message, media_id=media_id).render()

    def reply_video(self, media_id, title=None, description=None):
        '''
        将 media_id 所代表的视频组装为符合微信服务器要求的响应数据
        :param media_id: 视频的 MediaID
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :return: 符合微信服务器要求的 XML 响应数据
        '''
        self._check_parse()

        return VideoReply(message=self.__message, media_id=media_id, title=title, description=description).render()

    def reply_music(self, music_url, title=None, description=None, hq_music_url=None, thumb_media_id=None):
        '''
        将音乐信息组装为符合微信服务器要求的响应数据
        :param music_url: 音乐链接
        :param title: 音乐标题
        :param description: 音乐描述
        :param hq_music_url: 高质量音乐链接, WIFI环境优先使用该链接播放音乐
        :param thumb_media_id: 缩略图的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据
        '''
        self._check_parse()

        return MusicReply(
            message=self.__message, title=title, description=description, music_url=music_url,
            hq_music_url=hq_music_url, thumb_media_id=thumb_media_id).render()

    def reply_news(self, articles):
        '''
        将新闻信息组装为符合微信服务器要求的响应数据
        :param articles: list 对象, 每个元素为一个 dict 对象, key 包含 `title`, `description`, `picurl`, `url`
        :return: 符合微信服务器要求的 XML 响应数据
        '''
        self._check_parse()

        news = ArticleReply(message=self.__message)
        for article in articles:
            article = Article(**article)
            news.add_article(article)
        return news.render()

    # 菜单相关
    def create_menu(self, menu_data):
        '''
        创建自定义菜单
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单创建接口
        :param menu_data: Python dict
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/menu/create',
            data=menu_data
        )

    def get_menu(self):
        '''
        查询自定义菜单
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单查询接口
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._get('https://api.weixin.qq.com/cgi-bin/menu/get')

    def delete_menu(self):
        '''
        删除自定义菜单
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单删除接口
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._get('https://api.weixin.qq.com/cgi-bin/menu/delete')

    # 多媒体相关
    def upload_media(self, media_type, media_file):
        '''
        上传多媒体文件
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=上传下载多媒体文件
        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media_file:要上传的文件，一个 File-object
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._post(
            url='http://file.api.weixin.qq.com/cgi-bin/media/upload',
            params={
                'access_token': self.access_token,
                'type': media_type,
            },
            files={
                'media': media_file,
            }
        )

    def download_media(self, media_id):
        '''
        下载多媒体文件
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=上传下载多媒体文件
        :param media_id: 媒体文件 ID
        :return: requests 的 Response 实例
        '''
        self._check_appid_appsecret()

        return requests.get(
            'http://file.api.weixin.qq.com/cgi-bin/media/get',
            params={
                'access_token': self.access_token,
                'media_id': media_id,
            },
            stream=True,
        )

    # 用户、组相关
    def create_group(self, name):
        '''
        创建分组
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口
        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/groups/create',
            data={
                'group': {
                    'name': name,
                },
            }
        )

    def get_groups(self):
        '''
        查询所有分组
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._get('https://api.weixin.qq.com/cgi-bin/groups/get')

    def get_group_by_openid(self, openid):
        '''
        查询用户所在分组
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口
        :param openid: 用户的OpenID
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/groups/getid',
            data={
                'openid': openid,
            }
        )

    def update_group(self, group_id, name):
        '''
        修改分组名
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口
        :param group_id: 分组id，由微信分配
        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/groups/update',
            data={
                'group': {
                    'id': int(group_id),
                    'name': name,
                }
            }
        )

    def move_user(self, user_id, group_id):
        '''
        移动用户分组
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口
        :param user_id: 用户 ID 。 就是你收到的 WechatMessage 的 source
        :param group_id: 分组 ID
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/groups/members/update',
            data={
                'openid': user_id,
                'to_groupid': group_id,
            }
        )

    def get_user_info(self, user_id, lang='zh_CN'):
        '''
        获取用户基本信息
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=获取用户基本信息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._get(
            url='https://api.weixin.qq.com/cgi-bin/user/info',
            params={
                'access_token': self.access_token,
                'openid': user_id,
                'lang': lang,
            }
        )

    def get_followers(self, first_user_id=None):
        '''
        获取关注者列表
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=获取关注者列表
        :param first_user_id: 可选。第一个拉取的OPENID，不填默认从头开始拉取
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        params = {
            'access_token': self.access_token,
        }
        if first_user_id:
            params['next_openid'] = first_user_id
        return self._get('https://api.weixin.qq.com/cgi-bin/user/get', params=params)

    # 客服消息相关
    def send_text_message(self, user_id, content):
        '''
        发送文本消息
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param content: 消息正文
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'text',
                'text': {
                    'content': content
                },
            }
        )

    def send_image_message(self, user_id, media_id):
        '''
        发送图片消息
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param media_id: 图片的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'image',
                'image': {
                    'media_id': media_id
                },
            }
        )

    def send_voice_message(self, user_id, media_id):
        '''
        发送语音消息
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param media_id: 发送的语音的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'voice',
                'voice': {
                    'media_id': media_id,
                },
            }
        )

    def send_video_message(self, user_id, media_id, title=None, description=None):
        '''
        发送视频消息
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param media_id: 发送的视频的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        video_data = {
            'media_id': media_id,
        }
        if title:
            video_data['title'] = title
        if description:
            video_data['description'] = description

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'video',
                'video': video_data,
            }
        )

    def send_music_message(self, user_id, url, hq_url, thumb_media_id, title=None, description=None):
        '''
        发送音乐消息
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param url: 音乐链接
        :param hq_url: 高品质音乐链接，wifi环境优先使用该链接播放音乐
        :param thumb_media_id: 缩略图的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 音乐标题
        :param description: 音乐描述
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        music_data = {
            'musicurl': url,
            'hqmusicurl': hq_url,
            'thumb_media_id': thumb_media_id,
        }
        if title:
            music_data['title'] = title
        if description:
            music_data['description'] = description

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'music',
                'music': music_data,
            }
        )

    def send_article_message(self, user_id, articles):
        '''
        发送图文消息
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param articles: list 对象, 每个元素为一个 dict 对象, key 包含 `title`, `description`, `picurl`, `url`
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        articles_data = []
        for article in articles:
            article = Article(**article)
            articles_data.append({
                'title': article.title,
                'description': article.description,
                'url': article.url,
                'picurl': article.picurl,
            })
        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'news',
                'news': {
                    'articles': articles_data,
                },
            }
        )

    # 二维码相关
    def create_qrcode(self, **data):
        '''
        创建二维码
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=生成带参数的二维码
        :param data: 你要发送的参数 dict
        :return: 返回的 JSON 数据包
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/qrcode/create',
            data=data
        )

    def show_qrcode(self, ticket):
        '''
        通过ticket换取二维码
        官方文档地址 http://mp.weixin.qq.com/wiki/index.php?title=生成带参数的二维码
        :param ticket: 二维码 ticket 。可以通过 :func:`create_qrcode` 获取到
        :return: 返回的 Request 对象
        '''
        self._check_appid_appsecret()

        return requests.get(
            url='https://mp.weixin.qq.com/cgi-bin/showqrcode',
            params={
                'ticket': ticket
            }
        )

    # 内部方法
    def _check_token(self):
        '''
        检查 Token 是否存在
        :raises ParamError: Token 未初始化
        '''
        if not self.__token:
            raise ParamError('Token未初始化')

    def _check_parse(self):
        if not self.__is_parse:
            raise ParamError('消息未初始化')

    def _check_appid_appsecret(self):
        '''
        检查 AppID 和 AppSecret 是否存在
        :raises ParamError: AppID 或 AppSecret 未初始化
        '''
        if not self.__appid or not self.__appsecret:
            raise ParamError('appid 或 appsecret 未初始化')

    def _check_api_error(self, json_data):
        '''
        检测微信公众平台返回值中是否包含错误的返回码
        :raises OfficialAPIError: 如果返回码提示有错误，抛出异常；否则返回 True
        '''
        if 'errcode' in json_data and json_data['errcode'] != 0:
            raise APIError(
                '{}: {}'.format(json_data['errcode'], json_data['errmsg']))

    def _request(self, method, url, **kwargs):
        '''
        向微信服务器发送请求
        :param method: 请求方法
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        '''
        if 'params' not in kwargs:
            kwargs['params'] = {
                'access_token': self.access_token,
            }
        if isinstance(kwargs.get('data', ''), dict):
            body = json.dumps(kwargs['data'], ensure_ascii=False)
            body = body.encode('utf8')
            kwargs['data'] = body

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
        response_json = r.json()
        self._check_api_error(response_json)
        return response_json

    def _get(self, url, **kwargs):
        '''
        使用 GET 方法向微信服务器发出请求
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        '''
        return self._request(
            method='get',
            url=url,
            **kwargs
        )

    def _post(self, url, **kwargs):
        '''
        使用 POST 方法向微信服务器发出请求
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        '''
        return self._request(
            method='post',
            url=url,
            **kwargs
        )
