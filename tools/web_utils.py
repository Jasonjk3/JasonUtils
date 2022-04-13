# -*- ecoding: utf-8 -*-
# @ModuleName: toolkit
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2021/4/27 16:10
# @Desc:工具类

import random
from urllib.request import quote, unquote

def url_encode(text,encoding='utf-8'):
    """
    url 编码
    :return:
    """
    result = quote(text,encoding=encoding)
    return result
def url_decode(text,encoding='utf-8'):
    """
    url 解码
    :param text:
    :param encoding:
    :return:
    """
    result = unquote(text, encoding=encoding)
    return result

def cookie_str_to_dict(input_cookie):
    """
    cookie 字符串 反序列化成字典
    :param input_cookie:
    :return:
    """
    cookie = {}
    for line in input_cookie.split(';'):
        key, value = line.split('=', 1)
        cookie[key] = value
    return cookie

def cookie_dict_to_str(input_cookie):
    """
    cookie 字典对象序列化成字符串
    :param input_cookie:
    :return:
    """
    return ';'.join([f"{key}={input_cookie[key]}"for key in input_cookie])

def unicode_to_chinese(text):
    """
    unicode转中文
    :param text:
    :return:
    """
    return text.encode('utf-8').decode('unicode_escape')

def get_userAgent(num =1):
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

    return random.choices(USER_AGENT_LIST,k=num)

if __name__ == '__main__':
    print(url_encode('中是'))
    print(url_decode('%E4%B8%AD%E6%98%AF'))
    print(unicode_to_chinese(r'\u8fd9\u5c31\u662f\u5377\u7684\u4e00\u4e2a\u8868\u73b0\u5427'))
    print(get_userAgent())