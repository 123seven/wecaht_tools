# @Time        : 2019-07-09 14:56
# @Author      : Seven
# @File        : template_msg.py
# @Description : 模板消息


from wechat.api.base import BaseWeChatAPI


class WeChatTemplateMessage(BaseWeChatAPI):

    def set_industry(self, industry_id1, industry_id2):
        """ 设置所属行业
        参考: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433751277
        :param industry_id1: 公众号模板消息所属行业编号
        :param industry_id2: 公众号模板消息所属行业编号
        """
        data = {
            "industry_id1": industry_id1,
            "industry_id2": industry_id2,
        }
        return self._post('template/api_set_industry', data=data)

    def get_industry(self):
        """ 获取设置的行业信息 """
        return self._get('template/get_industry', params={})

    def get(self, template_id_short):
        """ 获得模板ID
        :param template_id_short: 模板库中模板的编号，有“TM**”和“OPENTMTM**”等形式
        :return: 模板 ID
        """
        data = {"template_id_short": template_id_short}
        return self._post('template/api_add_template', data=data)

    def get_all_private_template(self):
        """ 获取模板列表 """
        return self._get('template/get_all_private_template', params={})

    def del_private_template(self, template_id):
        """ 删除模板
        :param template_id: 公众帐号下模板消息ID
        """
        return self._post('template/del_private_template', data={'template_id': template_id})

    def send(self, open_id, template_id, data=None, url=None, mini_program=None, keyword_list=None, **kwargs):
        """ 发送模板消息
        :param open_id: 接收者openid
        :param template_id: 模板ID
        :param data: 模板数据
        :param url: 模板跳转链接
        :param mini_program: 跳小程序所需数据，不需跳小程序可不用传该数据
        :param keyword_list: 传入一个 keyword 列表
        """
        # o0fuLwfGN36wb6uLEtfmqHp1LKzU
        # RWErFfHyuTTHBMwP265x6ikNCA49CxfLITIPe7o-c4w

        send_data = {
            "touser": open_id,
            "template_id": template_id,
            "url": url,
        }

        if keyword_list:
            send_data['data'] = dict()
            send_data['data'].update(**kwargs)
            for index, value in enumerate(keyword_list):
                send_data['data'].setdefault(f'keyword{index + 1}', value)
        else:
            data and send_data.setdefault('data', data)

        mini_program and send_data.setdefault('mini_program', mini_program)
        return self._post('message/template/send', data=send_data)


__all__ = ['WeChatTemplateMessage']

if __name__ == '__main__':
    from wechat import WeChatClient

    w = WeChatClient()
    w.template_message.send('o0fuLwfGN36wb6uLEtfmqHp1LKzU', 'RWErFfHyuTTHBMwP265x6ikNCA49CxfLITIPe7o-c4w',
                            keyword_list=[{'value': '112'}, {'value': '111'}, {'value': '2019-7-10'}],
                            **{'first': {'value': '你好 seven'}, 'remark': {'value': '112'}})
