# -*- ecoding: utf-8 -*-
# @ModuleName: pandas_utils.py
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2021/11/19
# @Desc: pandas 常用操作封装



import numpy as np
import pandas as pd
import re




def fill_cols(df, cols=None, cols_dict=None):
    """
    补充字段
    :param df: dataframe数据集
    :param cols: 要补充的字段，补充默认为空字符,传入的为list
    :param cols_dict: 要补充字段的对应的值的字典,传入为dict
    :return: df
    """
    if cols:
        for col in cols:
            if col not in df.columns:
                df[col] = ''
    if cols_dict:
        for col in cols_dict.keys():
            df[col] = cols_dict[col]
    return df



def replaceNa(df, rep_str=''):
    """
    空值替换
    :param df:
    :param rep_str:
    :return:
    """
    return df.replace([np.nan, None], [rep_str, rep_str])


def processing_dot(ser):
    """
    比如将liters 2 转成2.0 然后再转成字符串
    :param ser:
    :return:
    """
    return np.round(ser.replace([''], [-1]).astype(np.float64), 1).replace([-1, np.nan], ['', '']).astype(str)


def split_df(df, num=10):
    """
    dataframe 分块,返回迭代器
    :param df:
    :param num: 分块数
    :return: 迭代器
    """
    split_num = len(df) // num
    for i in range(0, len(df), split_num):
        yield df.iloc[i:i + split_num]


def count_cols(origin_df):
    '''
    统计每个字段列不为空的数量
    :param origin_df:
    :return:
    '''
    df = origin_df.copy()
    df = replaceNa(df) # nan替换成空字符串
    for col in df.columns:
        t = sum(df[col] != '')
        print(col, t)

def get_small_cols(origin_df, num, retain_cols=None):
    '''
    获取列中小于一定阈值的列，如果传入retain_cols，则保留指定的列
    :param origin_df:
    :param num: 小于的数量
    :param retain_cols: 保留的列 (list)
    :return:
    '''
    if retain_cols is None:
        retain_cols = []
    df = origin_df.copy()
    df = replaceNa(df) # nan替换成空字符串
    res = []
    for col in df.columns:
        t = sum(df[col] != '')
        if t<= num and col not in retain_cols:
            res.append(col)

    return res

def drop_cols(origin_df,num=0, retain_cols=None):
    df = origin_df.copy()
    df = replaceNa(df) # nan替换成空字符串

    cols=get_small_cols(df,num,retain_cols)
    print('删除->',cols)
    origin_df = origin_df.drop(cols,axis=1)
    return origin_df

def split_col_data(origin_df,split_col,split_str):
    """
    在origin_df中切分split_col字段中的split_str字符，一行切分成多行
    例如:
       a    b  c
    0  1  a,b  2
    1  2  c,c  3
    2  3    d  5
    3  4    e  7

    split_data(origin_df,b,',') ->

       a  c  b
    0  1  2  a
    0  1  2  b
    1  2  3  c
    1  2  3  c
    2  3  5  d
    3  4  7  e

Process finished with exit code 0

    :param origin_df: 需要切分的df
    :param split_col: 需要切分的列
    :param split_str: 需要切分的字符串
    :return: 切分后的数据集
    """
    df = origin_df.copy()
    df = df.reset_index(drop=True) # index可能会导致切割结果不正确，所以需要reset
    df = df.drop([split_col], axis=1).join(
        df[split_col].str.split(split_str, expand=True).stack().reset_index(level=1, drop=True).rename(split_col)).reset_index(drop=True).drop_duplicates()
    return df


def data_strip(origin_df):
    """
    给dataframe所有值进行strip操作
    :param origin_df:
    :return:
    """
    df = origin_df.copy()
    for i in df.columns:
        if str(df[i].dtype)!='object':
            continue
        df.loc[:, i] = np.char.strip(df[i].tolist())
    return df


def check_df_info(df):
    """
    数据探索

    """
    print('-' * 30, '基础信息', '-' * 30)
    print('cols:', df.columns)
    print('shape:', df.shape)

    print('-' * 30, '缺失值检查', '-' * 30)
    print(df.isnull().sum())
    print()

    print('-' * 30, '重复值检查', '-' * 30)
    duplicates_Flag = True
    for i in df.columns:
        na = df[i].duplicated().sum()
        if na == 0:
            print(f'字段 {i} 无重复值')
            duplicates_Flag = False
    if duplicates_Flag:
        print('所有字段都有重复值')
    print('重复数据：', df.duplicated().sum())

    print()
    print('-' * 30, 'info', '-' * 30)
    df.info()

    print()
    print('-' * 30, 'describe', '-' * 30)
    print(df.describe())


def get_date_info(df, col):
    """
    拆分日期字段的信息

    :param df:
    :param col:
    :return:
    """
    df[col] = pd.to_datetime(df[col])
    df[f'{col}_year'] = df[col].dt.year
    df[f'{col}_month'] = df[col].dt.month
    df[f'{col}_week'] = df[col].dt.week
    df[f'{col}_day'] = df[col].dt.day
    df[f'{col}_hour'] = df[col].dt.hour
    df[f'{col}_dayofweek'] = df[col].dt.dayofweek+1
    return df


if __name__ == '__main__':
    print(get_sku2partnumber_dict())
