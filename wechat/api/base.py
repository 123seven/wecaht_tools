# @Time        : 2019-07-08 18:19
# @Author      : Seven
# @File        : base.py
# @Description : BaseWeChatAPI


class BaseWeChatAPI:
    """ WeChat API base class """

    def __init__(self, client=None):
        self._client = client
        self.api_base_url = 'https://api.weixin.qq.com/cgi-bin'

    def _get(self, url, base_url=True, **kwargs):
        if base_url:
            url = f'{self.api_base_url}/{url}'
        return self._client.get(url=url, **kwargs)

    def _post(self, url, base_url=True, **kwargs):
        if base_url:
            url = f'{self.api_base_url}/{url}'
        return self._client.post(url=url, **kwargs)

    @property
    def access_token(self):
        return self._client.access_token

    @property
    def session(self):
        return self._client.session

    @property
    def app_id(self):
        return self._client.appid

    @property
    def secret(self):
        return self._client.secret


__all__ = ['BaseWeChatAPI']
