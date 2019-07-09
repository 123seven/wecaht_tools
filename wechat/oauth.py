# @Time        : 2019-07-08 09:47
# @Author      : Seven
# @File        : oauth.py
# @Description : 微信授权
from urllib.parse import urlencode

import requests

from wechat.exceptions import WeChatOAuthException


class WeChatOauth(object):
    """ 微信授权 """

    def __init__(self):
        self.requests = requests.Session()
        self.app_id = 'you wechat app_id'
        self.app_secret = 'you wechat app_secret'
        self.oauth_url = 'https://open.weixin.qq.com/connect/oauth2/authorize'
        self.qr_connect_url = 'https://open.weixin.qq.com/connect/qrconnect'
        self.access_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        self.refresh_token_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token'
        self.user_info_url = 'https://api.weixin.qq.com/sns/userinfo'
        self.auth_url = 'https://api.weixin.qq.com/sns/auth'
        self.js_code_2_session_url = 'https://api.weixin.qq.com/sns/jscode2session'

    def get(self, url, params):
        """ 封装get方法
        :tips: requests.Session() 所以如果你向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升
        """
        res = self.requests.get(url, params=params)
        try:
            res.raise_for_status()
        except requests.RequestException as e:
            raise WeChatOAuthException(
                errcode=res.json().get('errcode'),
                errmsg=res.json().get('errmsg'),
                client=self,
                request=e.request,
                response=e.response
            )
        data = res.json()
        if data.get('errcode'):
            msg = '%(errcode)d %(errmsg)s' % data
            return {'err': msg}
        return data

    def authorize(self, redirect_uri, scope='snsapi_userinfo', state=None):
        """ 生成授权跳转地址
        :param redirect_uri: 授权后重定向的回调链接地址， 请使用 urlEncode 对链接进行处理
        :param scope: 微信认证方式，有`snsapi_base`跟`snsapi_userinfo`两种
        :param state: 认证成功后会原样带上此字段,开发者可以填写a-zA-Z0-9的参数值，最多128字节
        :tips 微信授权参考:https://mp.weixin.qq.com/wiki?action=doc&id=mp1421140842&t=0.4622491167403
        """
        assert scope in ['snsapi_base', 'snsapi_userinfo']

        args = dict()
        args.setdefault('appid', self.app_id)
        args.setdefault('redirect_uri', redirect_uri)
        args.setdefault('response_type', 'code')
        args.setdefault('scope', scope)
        args.setdefault('state', state) if state else None
        args = urlencode(args)

        return f'{self.oauth_url}?{args}#wechat_redirect'

    def qr_connect(self, redirect_uri, state=None):
        """ 生成扫码登录地址
        :return: URL 地址
        """
        args = dict()
        args.setdefault('appid', self.app_id)
        args.setdefault('redirect_uri', redirect_uri)
        args.setdefault('response_type', 'code')
        args.setdefault('scope', 'snsapi_login')
        args.setdefault('state', state) if state else None
        args = urlencode(args)

        return f'{self.qr_connect_url}?{args}#wechat_redirect'

    def access_token(self, code):
        """ 获取令牌 access_token
        :param code: 授权完成跳转回来后 URL 中的 code 参数
        """
        args = dict()
        args.setdefault('appid', self.app_id)
        args.setdefault('secret', self.app_secret)
        args.setdefault('code', code)
        args.setdefault('grant_type', 'authorization_code')

        return self.get(self.access_token_url, args)

    def refresh_access_token(self, refresh_token):
        """ 刷新access_token
        :param refresh_token: WeChat OAuth2 refresh token
        """
        args = dict()
        args.setdefault('appid', self.app_id)
        args.setdefault('grant_type', 'refresh_token')
        args.setdefault('refresh_token', refresh_token)

        return self.get(self.refresh_token_url, args)

    def check_access_token(self, access_token, openid):
        """ 检验授权凭证
        :param access_token: 授权凭证
        :param openid: 用户的唯一标识
        :return: 有效返回 True，否则 False
        """
        args = dict()
        args.setdefault('access_token', access_token)
        args.setdefault('openid', openid)

        res = self.get(self.auth_url, args)
        return True if res['errcode'] == 0 else False

    def userinfo(self, access_token, openid, lang='zh_CN'):
        """ 获取用户信息
        :param access_token: 微信返回的 access_token
        :param openid: 用户id，每个应用内唯一
        :param lang: 可选，语言偏好, 默认为 zh_CN，zh_CN 简体，zh_TW 繁体，en 英语
        """
        args = dict()
        args.setdefault('access_token', access_token)
        args.setdefault('openid', openid)
        args.setdefault('lang', lang)

        return self.get(self.user_info_url, args)

    def js_code_2_session(self, js_code):
        """ 小程序获取 session_key 和 openid
        :param js_code: 使用wx.login登录时获取到的code参数数据
        """
        args = dict()
        args.setdefault('appid', self.app_id)
        args.setdefault('secret', self.app_secret)
        args.setdefault('js_code', js_code)
        args.setdefault('grant_type', 'authorization_code')

        return self.get(self.js_code_2_session_url, args)


__all__ = ['WeChatOauth']
