# -*- ecoding: utf-8 -*-
# @ModuleName: temp
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2021/1/8 15:33
# @Desc:

import numpy as np
import torch
from JasonToolKit.nlp.models.bert import Bert


def cos_similar( sen_a_vec, sen_b_vec):
    '''
    计算两个句子的余弦相似度
    :param sen_a_vec:
    :param sen_b_vec:
    :return:
    '''
    if isinstance(sen_a_vec, list) or isinstance(sen_b_vec, list):
        vector_a = np.mat(sen_a_vec)
        vector_b = np.mat(sen_b_vec)
        num = float(vector_a * vector_b.T)
        denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        cos = num / denom
        result = cos.item()
    elif isinstance(sen_a_vec,torch.Tensor) or isinstance(sen_b_vec,torch.Tensor):
        sen_a_vec = sen_a_vec.numpy()
        sen_b_vec = sen_b_vec.numpy()
        # cos = (sen_a_vec * sen_b_vec).sum(-1) / torch.sqrt((sen_a_vec * sen_b_vec).sum(-1))
        vector_a = np.mat(sen_a_vec)
        vector_b = np.mat(sen_b_vec)
        num = float(vector_a * vector_b.T)
        denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        cos = num / denom
        result = cos.item()
    else:
        result=0
    return result


def bert_calculate( a, b):
    model = Bert()
    vec_a=model.generate_vec(a)[1]
    vec_b=model.generate_vec(b)[1]
    cos = cos_similar(vec_a, vec_b)
    return cos

def set_similar(a,b):
    '''
    交集除于并集计算相似度
    :param a:
    :param b:
    :return:
    '''
    set_a = set(a)
    set_b = set(b)
    count = len(set_a & set_b)
    all_num= len(set_a | set_b)
    result = count / all_num
    return result


if __name__ == '__main__':

    a = '看漫天飞雪的百川'
    b = '看漫天飞雪百川方式'
    print(set_similar(a,b))
    print(bert_calculate(a,b))

