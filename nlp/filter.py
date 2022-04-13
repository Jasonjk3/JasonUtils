# -*- ecoding: utf-8 -*-
# @ModuleName: fillter
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2021/4/24 16:06
# @Desc: 正则表达式过滤类

import re


def filter_normal_chinese(text):
    # 只保留中文、大小写字母和阿拉伯数字和常用的标点符号
    reg = "[^0-9A-Za-z\u4e00-\u9fa5，,()。.《》？！?!:：……]"
    text = re.sub(reg, '', text)
    return text.strip()


def punctuation_cn_to_eng(text):
    """
    中文标点符号转英文
    :param text:
    :return:
    """
    text = re.sub('，', ',', text)
    text = re.sub('。', '.', text)
    text = re.sub('？', '?', text)
    text = re.sub('；', ';', text)
    text = re.sub('【', '[', text)
    text = re.sub('】', ']', text)
    text = re.sub('（', '(', text)
    text = re.sub('）', ')', text)

    return text.strip()


def punctuation_eng_to_cn(text):
    """
    英文标点符号转中文
    :param text:
    :return:
    """
    text = re.sub(r',', '，', text)
    text = re.sub(r'\.', '。', text)
    text = re.sub(r'\?', '？', text)
    text = re.sub(r';', '；', text)
    text = re.sub(r'\[', '【', text)
    text = re.sub(r']', '】', text)
    text = re.sub(r'\(', '（', text)
    text = re.sub(r'\)', '）', text)

    return text.strip()


def filter_emoji(text, restr=''):
    """
    过滤emoji表情
    eg:大赛艾佛欧锦🐕
    output:大赛艾佛欧锦
    :param text: 输入文本
    :param restr: 替换字符，默认空
    :return:
    """
    #
    pattern = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    text = pattern.sub(restr, text)
    return text.strip()

def emoji_to_chinese(text):
    """
    TODO emoji表情 转中文
    :param desstr:
    :param restr:
    :return:
    """
    pass



def filter_url(text, restr=''):
    """
    过滤网址URL
    eg:大师傅似的https://www.baidu.com sds大师傅士大夫
    output:大师傅似的 sds大师傅士大夫
    :param text:
    :param restr:
    :return:
    """
    pattern = re.compile(
        r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]',
        re.IGNORECASE)
    text = re.sub(pattern, restr, text)  # 去除网址
    return text.strip()


def filter_emoticon(text, restr=''):
    """
    过滤[doge]这类带括号的表情
    :param text:
    :param restr:
    :return:
    """
    text = re.sub(r"\[\S+\]", "", text)  # 去除表情符号
    return text.strip()


def merge_space(text):
    """
    合并正文中过多的空格
    example:大师傅士大夫    s当时    sdfsd
    output :大师傅士大夫 s当时 sdfsd
    :param text:
    :return:
    """
    text = re.sub(r"\s+", " ", text)  # 合并为一个空格
    return text.strip()

def filter_html(text, tag=None,restr=''):
    """
    过滤HTML标签 TODO 嵌套 bug
    example: 郑爽日薪108万<span class="url-icon"><img alt=[微笑] src="https://h5.sinaimg.cn/m/emoticon/icon/default/d_hehe-0be7e6251f.png" style="width:1em; height:1em;" /></span>正常人卷几辈子也挣不了这么多钱吧
    output : 郑爽日薪108万正常人卷几辈子也挣不了这么多钱吧
    :param text:
    :param tag:
    :return:
    """
    if tag:
        start_tag = tag
        end_tag = tag
    else:
        start_tag = '[A-Za-z]{1,}'
        end_tag = '[A-Za-z]{1,}'
    result = re.sub(f"<{start_tag}.*?>(.*)</{end_tag}>",restr, text)  # 前后标签必须一样才能匹配
    return result

def filter_html_code(text,restr=''):
    """
    过滤html转义符 如 &nbsp;
    example:过滤html转义符 如&nbsp;撒旦发射点发射点
    output: 过滤html转义符 如撒旦发射点发射点
    :param text:
    :param restr:
    :return:
    """
    text = re.sub('&[a-zA-Z].*?;',restr,text)
    return text
def filter_unprintable(text):
    """
    移除所有不可见字符
    example: A\u2029十大
    output: A十大
    :param text:
    :return:
    """
    return ''.join(x for x in text if x.isprintable())


if __name__ == '__main__':
    text = "姜行止转发了@王者好物的微博:#王者荣耀[超话]##小鲁班的礼物#【关➕转，并@一位好友，小鲁班会送出荣耀水晶、猫王收音机、小夜灯、钥匙扣和永久皮肤】今天是#中国航天日#，扬帆起航，逐梦九天～小鲁班也要努力追逐梦想，勇于探索，快来和峡谷星球上最靓的崽一起向中国航天人致敬吧～ "
    print(punctuation_cn_to_eng(text))
    print(punctuation_eng_to_cn(text))

    text = "大赛艾佛欧锦🐕"
    print(filter_emoji(text))

    text = "大师傅似的https://www.baidu.com sds大师傅士大夫"
    print(filter_url(text))

    text = "大师傅士大夫    s当时    sdfsd"
    print(merge_space(text))

    print(filter_html('郑爽日薪108万<span class="url-icon"><img alt=[微笑] src="https://h5.sinaimg.cn/m/emoticon/icon/default/d_hehe-0be7e6251f.png" style="width:1em; height:1em;" /></span>正常人卷几辈子也挣不了这么多钱吧'))

    print(filter_unprintable('A\u2029十大'))

    print(filter_html_code('过滤html转义符 如&nbsp;撒旦发射点发射点'))