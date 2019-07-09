# @Time        : 2019-07-09 09:12
# @Author      : Seven
# @File        : wx_qr_code.py
# @Description : 小程序二维码

import os
import uuid

from wechat.api.base import BaseWeChatAPI


class WeChatMiniProgramQRCode(BaseWeChatAPI):
    def create(self, path=None, width=430):
        """ 获取小程序二维码，通过该接口生成的小程序码，永久有效，有数量限制
        参考:https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/qr-code/wxacode.createQRCode.html
        :param path: 扫码进入的小程序页面路径
        :param width:二维码的宽度 px
        :return: 返回的图片 Buffer / 异常JSON
        """
        data = dict(width=width or 430)
        path and data.setdefault('path', path)
        return self._post('wxaapp/createwxaqrcode', data=data)

    def get_wx_qrcode(self, path=None, width=430, auto_color=None, line_color=None, is_hyaline=True):
        """ 获取小程序码，适用于需要的码数量较少的业务场景。通过该接口生成的小程序码，永久有效，有数量限制
        :param path: 扫码进入的小程序页面路径
        :param width:二维码的宽度 px
        :param auto_color: 自动配置线条颜色
        :param line_color: auto_color 为 false 时生效，使用 rgb 设置颜色
        :param is_hyaline: 是否需要透明底色
        """
        data = dict(width=width or 430)
        path and data.setdefault('path', path)
        auto_color and data.setdefault('auto_color', auto_color)
        line_color and data.setdefault('line_color', line_color)
        is_hyaline and data.setdefault('is_hyaline', is_hyaline)
        return self._post('https://api.weixin.qq.com/wxa/getwxacode', data=data, base_url=False, buffer=True)

    def get_unlimited(self, scene, page=None, width=None, auto_color=None, line_color=None, is_hyaline=True):
        """ 获取小程序码，通过该接口生成的小程序码，永久有效，数量暂无限制。
        :param scene: 自定义二维码参数，最大32个可见字符，只支持数字，大小写英文以及部分特殊字符
        :param page: 需要跳转到的小程序页面路径(必须是已经发布的小程序存在的页面)
        :param width:二维码的宽度 px
        :param auto_color: 自动配置线条颜色
        :param line_color: auto_color 为 false 时生效，使用 rgb 设置颜色
        :param is_hyaline: 是否需要透明底色
        """
        data = dict(width=width or 430, scene=scene)
        page and data.setdefault('page', page)
        auto_color and data.setdefault('auto_color', auto_color)
        line_color and data.setdefault('line_color', line_color)
        is_hyaline and data.setdefault('is_hyaline', is_hyaline)
        return self._post('https://api.weixin.qq.com/wxa/getwxacodeunlimit', data=data, base_url=False, buffer=True)

    @classmethod
    def save_buffer(cls, buffer):
        """  使用 buffer 生成图片
        :param buffer: 图片 Buffer
        """
        image_path = f'{os.getcwd()}/wechat/api/images/{str(uuid.uuid4())}.png'
        with open(image_path, 'wb') as f:
            f.write(buffer)
        f.close()
        return image_path


__all__ = ['WeChatMiniProgramQRCode']
