# -*- ecoding: utf-8 -*-
# @ModuleName: jasonNLP
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2021/4/27 10:44
# @Desc:
from snownlp import SnowNLP
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def chinese_to_Pinyin(text):
    """
    TODO 汉字转拼音
    :param text:
    :return:
    """
    return SnowNLP(text).pinyin

def traditional_to_simplified():
    """
    TODO 繁体转简体
    :return:
    """
    pass

def simplified_to_traditional():
    """
    TODO 繁体转简体
    :return:
    """
    pass

def cut_word_and_count():
    """
    TODO 分词并统计词频
    :return:
    """
    pass

def TF_IDF():
    """
    TF-IDF是一种统计方法，用以评估一字词对于一个文件集或一个语料库中的其中一份文件的重要程度。
    TF词频越大越重要，但是文中会的“的”，“你”等无意义词频很大，却信息量几乎为0，这种情况导致单纯看词频评价词语重要性是不准确的。因此加入了idf
    IDF的主要思想是：如果包含词条t的文档越少，也就是n越小，IDF越大，则说明词条t越重要
    TF-IDF综合起来，才能准确的综合的评价一词对文本的重要性。
    :return:
    """
    pass

def cut_count_word(text, stopword_path=None, customword_file=None):
    '''
    文本处理 TODO 加载文件错误处理
    分词并统计
    :param text:  输入字符串或list 文本
    :param stopword_path:  停用词路径
    :param customword_file:  自定义词路径

    :return: 返回统计词频并排序的list
    '''
    if stopword_path is None:
        stopword_path = '../src/cn_stopwords.txt'
    if customword_file is None:
        customword_file = "../src/custom_words.txt"
    with open(stopword_path, 'r+', encoding='utf-8') as f:
        stopwords = f.read().split("\n")
    word_dict = {}

    def cut(row):
        # 导入自定义词典
        jieba.load_userdict(customword_file)
        seg_list = list(jieba.cut(row, HMM=True))
        # 遍历分词表
        for word in seg_list:
            # 去除停用词，去除单字，去除重复词
            if not (word.strip() in stopwords) and len(word.strip()) > 1:
                if word_dict.get(word) != None:
                    word_dict[word] = word_dict[word] + 1
                else:
                    word_dict[word] = 1

    if isinstance(text, list):
        for row in text:
            cut(row)
    else:
        cut(text)
    result = sorted(word_dict.items(), key=lambda d: d[1], reverse=True)
    return result


def generate_wordcloud(lists, max_words=30, scale=32,
                       background_color='White',
                       save_file=None,
                       show=True,
                       font=None):
    """
    生成词云图
    :param lists: data
    :param max_words: 最大生成词数,默认30
    :param scale: 尺寸,默认32
    :param background_color: 背景颜色,默认白色
    :param save_file: 保存文件路径 默认none
    :param show: 绘制图像 默认true
    :param font: 词云的中文字体所在路径
    :return:
    """
    if font is None:
        font = "../src/simhei.TTF"
    wc = WordCloud(font_path=font, background_color=background_color, max_words=max_words, scale=scale)
    wc.generate_from_frequencies(dict(lists))
    if save_file:
        wc.to_file(save_file)
    if show:
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.show()

if __name__ == '__main__':

    text = """
        印度政府的数据有瞒报吗？

    在印度中国人爆料：不但有，而且很严重。

    他觉得目前印度公布的死亡人数绝对是有问题的，不可能那么少，因为有些地方真的是死人多到来不及烧。4月22号有个新闻，一个记者在中央邦博帕尔（Bohpal）各个火葬场计数，当天一共烧了187具尸体，里面137具是死于新冠，但政府公布的数据只死了5个人。博帕尔的现存确诊患者11267人，规模只占全印度的0.4%，我们假设博帕尔的死亡人数规模也是0.4%，大家可以反推一下，如果137人只占了全印度的0.4%，那么印度现在实际上每天至少要死3万多人，而印度公布的数据只有2千多人。

    他在德里的一个朋友告诉他一件刷新三观的事情：德里由于死人来不及烧，一些火葬场都是几具尸体堆在一起烧，烧完之后家属们各自扒拉一点灰带回家。

    他说，死亡人数的瞒报是医院在政府授意下做的，比方说因肺炎死于无法呼吸的病人可以写成“缺氧”，如果病人本身有基础疾病的话那就写死于XX基础疾病……反正不提“新冠”就行了。然后反正尸体当天就烧了，死无对证——要知道即便是在平时，也只有五分之一的死者会有医学死亡报告，80%的印度人都死得“不明不白”。

    印度政府在死亡率这件事情上当然有很大的瞒报动机，死亡率高的话会引起社会恐慌和政治动荡；相反他相信印度的检测数据不会瞒报，因为一方面进行检测可以体现政府在行动，另一方面高检测率和确诊人数可以衬托出低死亡率。之前印度政府一直都把“低死亡率”作为一个政绩的吹嘘点——一开始先是说确诊率很低，确诊人数多了之后又说死亡率很低——多少人确诊没关系，只要这些人不死那就是政府领导抗疫的功劳；但如果死的人多了，那就让政府脸上很难看了。
        """
    data = cut_count_word(text)
    generate_wordcloud(data)
