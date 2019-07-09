# @Time        : 2019-07-08 11:43
# @Author      : Seven
# @File        : __init__.py.py


from wechat.api.qr_code import WeChatQRCode  # NOQA
from wechat.api.template_msg import WeChatTemplateMessage  # NOQA
from wechat.api.wx_qr_code import WeChatMiniProgramQRCode  # NOQA

__all__ = ['WeChatQRCode', 'WeChatMiniProgramQRCode', 'WeChatTemplateMessage']
