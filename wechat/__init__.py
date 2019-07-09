# @Time        : 2019-07-08 09:46
# @Author      : Seven
# @File        : __init__.py.py
# @Description :
import inspect
import json
import logging

import requests

from wechat import api
from wechat.api.base import BaseWeChatAPI
from wechat.exceptions import WeChatClientException
from wechat.session.json_storage import JsonStorage

logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, BaseWeChatAPI)


class WeChatClient:
    qr_code = api.WeChatQRCode()
    wx_qr_code = api.WeChatMiniProgramQRCode()
    template_message = api.WeChatTemplateMessage()

    def __new__(cls, *args, **kwargs):
        self = super(WeChatClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, cls_obj in api_endpoints:
            api_cls = type(cls_obj)
            cls_obj = api_cls(self)
            setattr(self, name, cls_obj)
        return self

    def __init__(self, app_id=None, app_secret=None, access_token=None, storage=None):
        self.requests = requests.Session()
        self.access_token_url = 'https://api.weixin.qq.com/cgi-bin/token'
        self.app_id = app_id
        self.app_secret = app_secret
        self.storage = storage or JsonStorage()
        if access_token:
            self.storage.set(self.access_token_key, access_token, 7000)

    def post(self, url, data, token=None, json_encode=True, buffer=False):
        params = {}
        params.setdefault("access_token", token or self.access_token())
        headers = {}
        if json_encode:
            data = json.dumps(data, ensure_ascii=False).encode()
            headers["Content-Type"] = "application/json;charset=UTF-8"
        res = self.requests.post(url, params=params, data=data, headers=headers)
        try:
            if buffer:
                return res.content
            res = res.json()
            if res.get('errcode'):
                raise WeChatClientException
        except requests.RequestException:
            raise WeChatClientException(
                errcode=res.json().get('errcode'),
                errmsg=res.json().get('errmsg'),
            )
        return res

    def get(self, url, params, get_token=False):
        if not get_token:
            params.setdefault("access_token", self.access_token())
        res = self.requests.get(url, params=params)
        try:
            res.raise_for_status()
            data = res.json()
            if data.get('errcode'):
                raise Exception
            return data
        except Exception:
            raise WeChatClientException(
                errcode=res.json().get('errcode') or 40000,
                errmsg=res.json().get('errmsg') or 'ERROR',
            )

    def _fetch_access_token(self):
        """ 请求微信接口获取 access_toke """
        logging.info('Fetching access token')
        args = {'grant_type': 'client_credential', 'appid': self.app_id, 'secret': self.app_secret}
        result = self.get(self.access_token_url, params=args, get_token=True)
        logger.debug(result)
        self.storage.set(self.access_token_key, result['access_token'], result['expires_in'] - 1)
        return result['access_token']

    @property
    def access_token_key(self):
        return '{0}_access_token'.format(self.app_id)

    def access_token(self):
        """ 获取 access_token """
        data = self.storage.get(self.access_token_key)
        if data:
            logging.debug(f'get access_token{data.value}')
            return data.value
        self._fetch_access_token()
        return self.storage.get(self.access_token_key).value


__all__ = ['WeChatClient']
