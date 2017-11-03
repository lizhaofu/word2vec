#! /usr/bin/python
# -*- encoding=utf-8 -*-
import sys
import jieba
import re
import gensim
from gensim.models import word2vec
from gensim.models.word2vec import LineSentence
import imp

imp.reload(sys)
#sys.setdefaultencoding('utf8')

def get_fenci(inputfilename, outputfilename):
    # jieba.initialize()
    inf = open(inputfilename, 'r',encoding='utf-8')
    inf1 = open(outputfilename, 'a',encoding='utf-8')
    all_text = re.split('。|；|！|？|\.|;|!|\?', inf.read().strip())

    # print all_text
    for i in range(all_text.__len__()):
        words = jieba.lcut(all_text[i])
        for word in words:
           # word.decode('utf-8')
            if not check_contain_other_words(word):
                inf1.write(word + ' ')
        #inf1.write('\n') #每个句子占分词文件的一行
    inf.close()
    inf1.close()



def check_contain_other_words(check_str):
    """判断字符串是否只含有汉字数字和英文字母,含有其他字符返回Ture"""
    for ch in check_str:
        if not (is_chinese(ch) or is_number(ch) or is_alphabet(ch)):
            return True
    return False

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if '\u4e00' <= uchar <= '\u9fa5':
        return True
    else:
        return False

def is_number(uchar):
    """判断一个unicode是否是数字"""
    if '\u0030' <= uchar <= '\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if ('\u0041' <= uchar <= '\u005a') or ('\u0061' <= uchar <= '\u007a'):
        return True
    else:
        return False

def get_model(input, output):
    """训练分好词的样本"""
    model = word2vec.Word2Vec(LineSentence(input), size=100, min_count=8, workers=4)
    # model.most_similar(u'股票')
    model.save(output)






if __name__ == '__main__':
    original_output = 'data\\text.txt'
    output = 'data\\example.model'
    filename = 'data\\C000008\\'
    for i1 in range(11, 2000):
        tmp = filename + str(i1) + '.txt'
        get_fenci(tmp, original_output)
    print('分词结束，开始训练模型')

    get_model(original_output, output)
    print('训练模型结束')

    model = gensim.models.Word2Vec.load(output)
    print('股票的词向量为：')
    print(model['效应'])
    print('------------')









