# @Time        : 2019-07-08 12:14
# @Author      : Seven
# @File        : redis_storage.py
# @Description : redis 方式存储


import json

from wechat.session import SessionStorage


class RedisStorage(SessionStorage):

    def __init__(self, redis, prefix='wechat'):
        for method_name in ('get', 'set', 'delete'):
            assert hasattr(redis, method_name)
        self.redis = redis
        self.prefix = prefix

    def key_name(self, key):
        return '{0}:{1}'.format(self.prefix, key)

    def get(self, key, default=None):
        key = self.key_name(key)
        value = self.redis.get(key)
        if value is None:
            return default
        return json.loads(value)

    def set(self, key, value, ttl=None):
        if value is None:
            return
        key = self.key_name(key)
        value = json.dumps(value)
        self.redis.set(key, value, ex=ttl)

    def delete(self, key):
        key = self.key_name(key)
        self.redis.delete(key)


__all__ = ['RedisStorage']
