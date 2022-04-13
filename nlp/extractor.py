# -*- ecoding: utf-8 -*-
# @ModuleName: extractor
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2021/2/25 10:31
# @Desc:
import re
from phone import Phone
from itertools import groupby
import phonenumbers
from pyhanlp import *
import json


# https://github.com/fighting41love/cocoNLP


def extract_email(text):
    """
    extract all email addresses from texts<string>
    eg: extract_email('我的email是ifee@baidu.com和dsdsd@dsdsd.com,李林的邮箱是eewewe@gmail.com哈哈哈')


    :param: raw_text
    :return: email_addresses_list<list>
    """
    if text == '':
        return []
    eng_texts = replace_chinese(text)
    eng_texts = eng_texts.replace(' at ', '@').replace(' dot ', '.')
    sep = ',!?:; ，。！？《》、|\\/'
    eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]

    email_pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z_-]+)+$'

    emails = []
    for eng_text in eng_split_texts:
        result = re.match(email_pattern, eng_text, flags=0)
        if result:
            emails.append(result.string)
    return emails


def extract_ids(text, person_info=False):
    """
    extract all ids from texts<string>
    eg: extract_ids('my ids is 150404198812011101 m and dsdsd@dsdsd.com,李林的邮箱是eewewe@gmail.com哈哈哈')


    :param: raw_text
    :return: ids_list<list>
    """
    if text == '':
        return []

    WEIGHTS = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    IDCHECK = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

    AREA = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", "23": "黑龙江",
            "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东", "41": "河南", "42": "湖北",
            "43": "湖南", "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏",
            "61": "陕西", "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}

    def check_id(id):
        # 检测身份证最后的校验码是否正确
        if len(id) != 18:
            return False
        else:
            ID_check = id[17]
            ID_aXw = 0
            for i in range(len(WEIGHTS)):
                ID_aXw = ID_aXw + int(id[i]) * WEIGHTS[i]
            ID_Check = ID_aXw % 11

            if ID_check != IDCHECK[ID_Check]:
                return False
            else:
                return True

    id_pattern = r'[1-9]\d{5}(?:18|19|(?:[23]\d))\d{2}(?:(?:0[1-9])|(?:10|11|12))(?:(?:[0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]'

    result = re.findall(id_pattern, text)
    data = []
    for id in result:
        if check_id(id):
            if person_info:
                birth = id[6:14]
                sex = id[16:17]
                sex = int(sex)
                area = AREA.get(id[0:2])
                data.append((id, area, birth, sex))
            else:
                data.append(id)
    return data


def replace_chinese(text):
    """
    remove all the chinese characters in text
    eg: replace_chinese('我的email是ifee@baidu.com和dsdsd@dsdsd.com,李林的邮箱是eewewe@gmail.com哈哈哈')


    :param: raw_text
    :return: text_without_chinese<str>
    """
    if text == '':
        return []
    filtrate = re.compile(u'[\u4E00-\u9FA5]')
    text_without_chinese = filtrate.sub(r' ', text)
    return text_without_chinese


def extract_cellphone(text, nation):
    """
    extract all cell phone numbers from texts<string>
    eg: extract_email('my email address is sldisd@baidu.com and dsdsd@dsdsd.com,李林的邮箱是eewewe@gmail.com哈哈哈')


    :param: raw_text
    :return: email_addresses_list<list>
    """
    if text == '':
        return []
    eng_texts = replace_chinese(text)
    sep = ',!?:; ：，.。！？《》、|\\/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]
    eng_split_texts_clean = [ele for ele in eng_split_texts if len(ele) >= 7 and len(ele) < 17]
    if nation == 'CHN':
        phone_pattern = r'^((\+86)?([- ])?)?(|(13[0-9])|(14[0-9])|(15[0-9])|(17[0-9])|(18[0-9])|(19[0-9]))([- ])?\d{3}([- ])?\d{4}([- ])?\d{4}$'

    phones = []
    for eng_text in eng_split_texts_clean:
        result = re.match(phone_pattern, eng_text, flags=0)
        if result:
            phones.append(result.string.replace('+86', '').replace('-', ''))
    return phones


def extract_cellphone_location(phoneNum, nation='CHN'):
    """
    extract cellphone number locations according to the given number
    eg: extract_cellphone_location('181000765143',nation=CHN)


    :param: phoneNum<string>, nation<string>
    :return: location<dict>{'phone': '18100065143', 'province': '上海', 'city': '上海', 'zip_code': '200000', 'area_code': '021', 'phone_type': '电信'}

    """
    if nation == 'CHN':
        p = Phone()
        loc_dict = p.find(phoneNum)
    if nation != 'CHN':
        x = phonenumbers.parse(phoneNum, 'GB')
        if phonenumbers.is_possible_number(x):
            loc_dict = x
    # print(loc_dict)
    return loc_dict


def get_location(word_pos_list):
    """
    get location by the pos of the word, such as 'ns'
    eg: get_location('内蒙古赤峰市松山区')


    :param: word_pos_list<list>
    :return: location_list<list> eg: ['陕西省安康市汉滨区', '安康市汉滨区', '汉滨区']

    """
    location_list = []
    if word_pos_list == []:
        return []

    for i, t in enumerate(word_pos_list):
        word = t[0]
        nature = t[1]
        if nature == 'ns':
            loc_tmp = word
            count = i + 1
            while count < len(word_pos_list):
                next_word_pos = word_pos_list[count]
                next_pos = next_word_pos[1]
                next_word = next_word_pos[0]
                if next_pos == 'ns' or 'n' == next_pos[0]:
                    loc_tmp += next_word
                else:
                    break
                count += 1
            location_list.append(loc_tmp)

    return location_list  # max(location_list)


def extract_locations(text):
    """
    extract locations by from texts
    eg: extract_locations('我家住在陕西省安康市汉滨区。')


    :param: raw_text<string>
    :return: location_list<list> eg: ['陕西省安康市汉滨区', '安康市汉滨区', '汉滨区']

    """
    if text == '':
        return []
    seg_list = [(str(t.word), str(t.nature)) for t in HanLP.segment(text)]
    location_list = get_location(seg_list)
    return location_list


def replace_cellphoneNum(text):
    """
    remove cellphone number from texts. If text contains cellphone No., the extract_time will report errors.
    hence, we remove it here.
    eg: extract_locations('我家住在陕西省安康市汉滨区，我的手机号是181-0006-5143。')


    :param: raw_text<string>
    :return: text_without_cellphone<string> eg: '我家住在陕西省安康市汉滨区，我的手机号是。'

    """
    eng_texts = replace_chinese(text)
    sep = ',!?:; ：，.。！？《》、|\\/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]
    eng_split_texts_clean = [ele for ele in eng_split_texts if len(ele) >= 7 and len(ele) < 17]
    for phone_num in eng_split_texts_clean:
        text = text.replace(phone_num, '')
    return text


def replace_ids(text):
    """
    remove cellphone number from texts. If text contains cellphone No., the extract_time will report errors.
    hence, we remove it here.
    eg: extract_locations('我家住在陕西省安康市汉滨区，我的身份证号是150404198412011312。')


    :param: raw_text<string>
    :return: text_without_ids<string> eg: '我家住在陕西省安康市汉滨区，我的身份证号号是。'

    """
    if text == '':
        return []
    eng_texts = replace_chinese(text)
    sep = ',!?:; ：，.。！？《》、|\\/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]
    eng_split_texts_clean = [ele for ele in eng_split_texts if len(ele) == 18]

    id_pattern = r'^[1-9][0-7]\d{4}((19\d{2}(0[13-9]|1[012])(0[1-9]|[12]\d|30))|(19\d{2}(0[13578]|1[02])31)|(19\d{2}02(0[1-9]|1\d|2[0-8]))|(19([13579][26]|[2468][048]|0[48])0229))\d{3}(\d|X|x)?$'
    ids = []
    for eng_text in eng_split_texts_clean:
        result = re.match(id_pattern, eng_text, flags=0)
        if result:
            ids.append(result.string)

    for phone_num in ids:
        text = text.replace(phone_num, '')
    return text


def extract_name(text):
    """
    extract chinese names from texts
    eg: extract_time('急寻王龙，短发，王龙，男，丢失发型短发，...如有线索，请迅速与警方联系：19909156745')


    :param: raw_text<string>
    :return: name_list<list> eg: ['王龙', '王龙']

    """
    if text == '':
        return []
    seg_list = [(str(t.word), str(t.nature)) for t in HanLP.segment(text)]
    names = []
    for ele_tup in seg_list:
        if 'nr' in ele_tup[1]:
            names.append(ele_tup[0])
            # print(ele_tup[0],ele_tup[1])
    return names


def extract_url(text, restr=''):
    pattern = re.compile(
        r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]',
        re.IGNORECASE)
    text = re.findall(pattern, restr, text)  # 去除网址
    return text


def extract_html(text, tag=None):
    """
    提取HTML标签 TODO 嵌套 bug
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
    result = re.findall(f"<{start_tag}.*?>(.*)</{end_tag}>", text)  # 前后标签必须一样才能匹配
    return result


def extract_json(text):
    """
    TODO 简单提取json字符串
    :param text:
    :return:
    """
    result = re.findall(r'[{].*[}]', text)  # 最大匹配
    return result


def extract_json_to_dict(text):
    """
    提取json字符串并转成字典
    :param text:
    :return:
    """
    result = re.findall(r'[{].*[}]', text)  # 最大匹配
    try:
        result = json.loads(result[0])
    except Exception:
        return None
    return result


def most_common(content_list):
    """
    return the most common element in a list
    eg: extract_time(['王龙'，'王龙'，'李二狗'])


    :param: content_list<list>
    :return: name<string> eg: '王龙'
    """
    if content_list == []:
        return None
    if len(content_list) == 0:
        return None
    return max(set(content_list), key=content_list.count)


if __name__ == '__main__':
    text = '急寻特朗普，男孩，于2018年11月27号11时在陕西省安康市汉滨区走失。习近平,450502199709121219,丢失发型短发，...如有线索，请迅速与警方联系：18100065143，132-6156-2938，baizhantang@sina.com.cn 和yangyangfuture at gmail dot com'

    emails = extract_email(text)
    print(emails)

    cellphones = extract_cellphone(text, nation='CHN')
    print(cellphones)

    ids = extract_ids(text, person_info=True)
    print(ids)

    name = extract_name(text)
    print(name)

    print(extract_locations(text))

    print(extract_cellphone_location('13517596501'))

    text = r'<a href="www.baidu.com" title="河南省"><p>你好</p></a>'
    print(extract_html(text))

    text = 'ds{s{as}ad}s'
    print(extract_json(text))
