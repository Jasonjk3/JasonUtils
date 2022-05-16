# -*- ecoding: utf-8 -*-
# @ModuleName: city_toolkit
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2021/5/27 14:47
# @Desc:

import json

path_file = '../src/city_geo.json'

with open(path_file,'r',encoding='utf-8') as f:
    datas = json.loads(f.read())

print(len(datas))

text = '山东 青岛'

