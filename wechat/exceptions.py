# @Time        : 2019-07-08 09:56
# @Author      : Seven
# @File        : exceptions.py
# @Description : 异常处理


from __future__ import absolute_import, unicode_literals


class WeChatException(Exception):
    """Base exception for wechat"""

    def __init__(self, errcode, errmsg):
        """
        :param errcode: Error code
        :param errmsg: Error message
        """
        self.errcode = errcode or 40000
        self.errmsg = errmsg

    def __str__(self):
        _repr = {
            'retCode': self.errcode,
            'retMsg': self.errmsg
        }

        return _repr

    def __repr__(self):
        _repr = {
            'Class': self.__class__.__name__,
            'retCode': self.errcode,
            'retMsg': self.errmsg
        }

        return _repr


class WeChatClientException(WeChatException):
    """WeChat API client exception class"""

    def __init__(self, errcode, errmsg, client=None, request=None, response=None):
        super(WeChatClientException, self).__init__(errcode, errmsg)
        self.request = request
        self.response = response


class InvalidSignatureException(WeChatException):
    """Invalid signature exception class"""

    def __init__(self, errcode=-40001, errmsg='Invalid signature'):
        super(InvalidSignatureException, self).__init__(errcode, errmsg)


class APILimitedException(WeChatClientException):
    """WeChat API call limited exception class"""
    pass


class InvalidAppIdException(WeChatException):
    """Invalid app_id exception class"""

    def __init__(self, errcode=-40005, errmsg='Invalid AppId'):
        super(InvalidAppIdException, self).__init__(errcode, errmsg)


class WeChatOAuthException(WeChatClientException):
    """WeChat OAuth API exception class"""
    pass


class WeChatComponentOAuthException(WeChatClientException):
    """WeChat Component OAuth API exception class"""
    pass
