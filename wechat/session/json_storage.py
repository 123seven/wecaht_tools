# @Time        : 2019-07-08 12:20
# @Author      : Seven
# @File        : json_storage.py
# @Description : json 方式存储

import json
import logging
import time
from json.decoder import JSONDecodeError

from wechat.session import SessionStorage

logger = logging.getLogger(__name__)


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class JsonStorage(SessionStorage):

    def __init__(self):
        self.path = '.wechat_json_data.json'
        self._check_overdue()

    def _save(self, data):
        """ 保存 """
        s = json.dumps(data, indent=2, ensure_ascii=False)
        with open(self.path, 'w+', encoding='utf-8') as f:
            logger.info('save', self.path, s, data)
            f.write(s)

    def _load(self):
        """ 加载 """
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                s = f.read()
                logger.info('load', s)
                return json.loads(s)
        except (FileNotFoundError, JSONDecodeError):
            return []

    def _check_overdue(self):
        """ 过期时间检查 """
        all_data = self.all()
        for i, e in enumerate(all_data):
            if e.get('ttl') != -1 and e.get('ttl') <= time.time():
                all_data.pop(i)
        self._save(all_data)
        return True

    def all(self):
        """ 获取所有数据 """
        data = self._load()
        ms = [item for item in data]
        return ms

    def get(self, key, default=None):
        """ 取出
        :param key: 名称
        :param default: 没有取到默认返回的数据
        :return:
        """
        self._check_overdue()
        logger.info('key', key)
        k, v = 'key', key
        all_data = self.all()
        for m in all_data:
            if v == m[k]:
                return AttrDict(m)

        return default

    def set(self, key, value, ttl=None):
        """ 保存
        :param key: 名称
        :param value: 值
        :param ttl: 过期时间
        """
        self._check_overdue()
        self.delete(key)
        all_data = self.all()
        logging.info(f'all_data{all_data}')
        all_data.append({'key': key, 'value': value, 'ttl': int(time.time() + ttl if ttl else -1)})
        self._save(all_data)

    def delete(self, key):
        """ 删除
        :param key: 名称
        :return: 成功返回 True，否则 False/None
        """
        self._check_overdue()
        all_data = self.all()
        index = -1
        for i, e in enumerate(all_data):
            if e.get('key') == key:
                index = i
                break
        # 判断是否找到了这条数据
        if index == -1:
            # 没找到
            return False
        else:
            all_data.pop(index)
            self._save(all_data)
            logging.info(f'delete{key}')
            return True


__all__ = ['JsonStorage']
