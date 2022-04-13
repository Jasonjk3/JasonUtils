# -*- coding: utf-8 -*-

import random

from tools.identity_utils import IdNumber


def create_phone():
    # 第二位数字
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]

    # 第三位数字
    third = {
        3: random.randint(0, 9),
        4: [5, 7, 9][random.randint(0, 2)],
        5: [i for i in range(10) if i != 4][random.randint(0, 8)],
        7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
        8: random.randint(0, 9),
    }[second]

    # 最后八位数字
    suffix = random.randint(9999999,100000000)

    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)

# 生成手机号
phone = create_phone()
print(phone)

import json
results = []
with open('普通人名.json','r',encoding='utf-8') as f:
    datas=json.loads(f.read())
    datas = random.choices(datas,k=100)
for row in datas:
    item ={}
    item['name'] = row['full_name']
    # item['gender'] = row['gender']
    item['phone'] = create_phone()
    item['idcard'] = IdNumber.generate_id()
    results.append(item)

import pandas as pd
pd.DataFrame(results).to_excel('forlipei.xlsx')
