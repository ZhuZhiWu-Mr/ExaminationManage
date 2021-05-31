# -*- coding: UTF-8 -*-

from scipy.spatial.distance import cosine
import codecs
import numpy as  np
import jieba

import pickle as pkl

from .sentence2vec import Word, Sentence, sentence_to_vec


def cosine(a, b):
    a1 = np.squeeze(a)
    b1 = np.squeeze(b)
    s = a1.dot(b1) / (np.linalg.norm(a1) * np.linalg.norm(b1))
    # s = ('%.3f' % s)
    return s


def get_lensim(sent1_list, sent2_list):
    lsim_list = []
    for sent_1, sent_2 in zip(sent1_list, sent2_list):
        lsim = 1 - abs((sent_1.len() - sent_2.len()) / (sent_1.len() + sent_2.len()))
        lsim_list.append(lsim)
    return lsim_list


# 加载词频字典
def load_sts(file_path):
    dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                line = line.split()
                if len(line) == 2:
                    dict[line[0]] = float(line[1])
                # else:
                #     #print(line)
    return dict


# sif 抽取关键词，然后加权计算词向量
def get_sif_vec(content, embedding_size, mydict):
    """
    对两列数据，分别进行加权计算embedding，然后计算相似度
    """
    # vec_list = []
    sentence_vectors_list = sentence_to_vec(content, embedding_size, mydict)  # all vectors converted together
    return sentence_vectors_list


# 中文分词，去除停用词，去除空格，换行符
def tokenization(sent):
    # 加载中文停用词文件
    stop_words_file = "hit_stopwords.txt"
    stopwords = codecs.open(stop_words_file, 'r', encoding='utf8').readlines()
    stopw = [w.strip() for w in stopwords]
    result = []

    words = jieba.lcut(sent)
    for word in words:
        if word not in stopw and word != ' ':
            result.append(word)
    result = list(set(result))
    return result


# 输入的是一个句子list
# 中文分词，去除停用词，去除空格，换行符
def get_cn_fenci_sentenceList(sent_list):
    # 加载中文停用词文件
    stop_words_file = "hit_stopwords.txt"
    stopwords = codecs.open(stop_words_file, 'r', encoding='utf8').readlines()
    stopw = [w.strip() for w in stopwords]

    result = []

    for sent in sent_list:
        words_list = []
        words = jieba.lcut(sent)
        for word in words:
            if word not in stopw and word != ' ':
                words_list.append(word)
        words_set = list(set(words_list))
        result.append(words_set)

    return result


def get_sif_sim(vec1, vec2, lsim_list):
    cou = 1
    similarity_list = []
    for x, y, lsim in zip(vec1, vec2, lsim_list):
        print(cou)
        cou = cou + 1
        a1 = 0.4
        b1 = 0.6
        r = -1
        # 得到两个句子向量相似度
        # simi_score = cosine(vec1,vec2)
        simi_score = 10 * (cosine(x, y) * a1 + b1 * lsim) + r
        # print(simi_score)
        similarity_list.append(simi_score)
        # similarity_list.append(10 * cosine(x,y))
    return similarity_list


# 计算得分函数
def auto_score(user_answer, answer) -> float:
    '''
    :param user_answer: 用户答案
    :param answer: 标准答案
    :return: 分数
    '''
    if (len(user_answer) == 0):
        return 0

    # 加载中文模型
    f = open('pickled_simv2_model', 'rb')
    word2vec_model = pkl.load(f)
    embedding_size = 200

    # 加载词频字典
    mydict = load_sts('wiki_cn_all.txt')

    # 读取数据，将answer和user_answer转为list
    content_1 = [answer]
    content_2 = [user_answer]

    # 分词，去除停用词
    content_1_fenci = get_cn_fenci_sentenceList(content_1)
    content_2_fenci = get_cn_fenci_sentenceList(content_2)

    sentence_list1 = []
    for sentence in content_1_fenci:
        word_list = []
        for word in sentence:
            # token = nlp(word)
            try:
                word_list.append(Word(word, word2vec_model[word]))
            except KeyError:
                # word_list.append(Word(word, np.random.uniform(-1, 1, 300)))
                # if token.has_vector:  # ignore OOVs
                continue

        if len(word_list) > 0:  # did we find any words (not an empty set)
            sentence_list1.append(Sentence(word_list))

    sentence_list2 = []
    for sentence in content_2_fenci:
        word_list = []
        for word in sentence:
            # token = nlp(word)
            try:
                word_list.append(Word(word, word2vec_model[word]))
            except KeyError:
                # word_list.append(Word(word, np.random.uniform(-1, 1, 300)))
                # if token.has_vector:  # ignore OOVs
                continue

        if len(word_list) > 0:  # did we find any words (not an empty set)
            sentence_list2.append(Sentence(word_list))

    vec1_list = get_sif_vec(sentence_list1, embedding_size, mydict)
    vec2_list = get_sif_vec(sentence_list2, embedding_size, mydict)

    # 句长相似度
    lsim_list = get_lensim(sentence_list1, sentence_list2)

    # 计算相似度，得到分数
    similarity_list = get_sif_sim(vec1_list, vec2_list, lsim_list)

    # 抄袭检测

    # sum_score = content_1[0]

    print('test', similarity_list[0])
    similarity_score = round(similarity_list[0], 2)
    # similarity_score = str(similarity_score)
    return similarity_score
