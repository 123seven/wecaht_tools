# @Time        : 2019-07-08 17:46
# @Author      : Seven
# @File        : qr_code.py
# @Description : 微信二维码


import requests
from requests.utils import quote

from wechat.api.base import BaseWeChatAPI


class WeChatQRCode(BaseWeChatAPI):

    def create(self, scene_id, action_name='QR_SCENE', scene_str=None, expires=60):
        """ 创建二维码
        参考: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1443433542
        :param scene_id: 场景值ID
        :param action_name: 二维码类型，QR_SCENE / QR_STR_SCENE / QR_LIMIT_SCENE / QR_LIMIT_STR_SCENE
        :param scene_str: 场景值ID（字符串形式的ID）
        :param expires: 二维码有效时间，以秒为单位, 默认60
        """
        assert action_name in ['QR_SCENE', 'QR_STR_SCENE', 'QR_LIMIT_SCENE', 'QR_LIMIT_STR_SCENE']

        data = dict(
            action_name=action_name, expire_seconds=expires,
            action_info=dict(scene={'scene_id': scene_id, 'scene_str': scene_str}),
        )

        return self._post('qrcode/create', data=data)

    @classmethod
    def show(cls, ticket):
        """ 通过ticket换取二维码 """
        if isinstance(ticket, dict):
            ticket = ticket['ticket']
        return requests.get('https://mp.weixin.qq.com/cgi-bin/showqrcode', params={'ticket': ticket})

    @classmethod
    def get_url(cls, ticket):
        """ 通过ticket换取二维码地址 """
        if isinstance(ticket, dict):
            ticket = ticket['ticket']
        ticket = quote(ticket)
        return f'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}'


__all__ = ['WeChatQRCode']
