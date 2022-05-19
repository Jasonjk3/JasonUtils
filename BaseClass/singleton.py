# -*- ecoding: utf-8 -*-
# @ModuleName: singleton.py
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2022/5/20
# @Desc:单例


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance



# class MyClass(Singleton):
#     a = 1