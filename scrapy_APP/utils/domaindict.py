import json
import jieba
import re
import os
from collections import Counter
import pandas as pd
import numpy as np

stopwordsDict_root = "utils/data/stopwords"
domainDict_root = "utils/data/domainDicts"
sensitive_root = "utils/data/sensitiveDicts/清华大学——李军中文褒贬义词典"


def getTextExample():

    with open('data/317739794_0.json','r',encoding="utf8") as f:
        line = f.readline()
    json_str = json.loads(line)[0]
    keys = json_str.keys()
    content = json_str["content"]
    text = re.sub(r'<[^>]+>'," ", content)

    return text



def sentenceCut(sentence):
    sentence_depart = jieba.lcut(sentence,cut_all=False, HMM=True)
    return sentence_depart


def get_stopwords_list():
    stopwords = []
    for root, dirs, files in os.walk(stopwordsDict_root):
        for file in files:
            if "stopwords" in file:
                allRoot = os.path.join(root,file)
                stopwords.extend([line.strip() for line in open(allRoot, encoding='UTF-8').readlines()])
    stopwords = list(set(stopwords))
    return stopwords

def remove_digits(input_str):
    punc = u'0123456789.'
    output_str = re.sub(r'[{}]+'.format(punc), '', input_str)
    output_str = re.sub(r'[ |-]+', '', output_str)
    return output_str

# 去除停用词
def move_stopwords(sentence_list, stopwords_list):
    # 去停用词
    out_list = []
    for word in sentence_list:
        if word not in stopwords_list:
            if not remove_digits(word):
                continue
            if word != '\t' :
                out_list.append(word)
    return out_list

def wordsBag(wordsList):
    data  = Counter(wordsList)
    return data


def getDomain(file,domain,sep = "\t",poem=False):
    data = np.unique(pd.read_csv(file,sep=sep,header=None,encoding="ISO8859-1").values[:,0])
    temp = []
    if poem:
        for i in data:
            temp.extend(re.split("[，|。|？|！|\u3000|\xa0| ]+",
                                 str(i).encode("ISO8859-1").decode("utf-8",errors="ignore")))
    else:
        temp.extend([str(i).encode("ISO8859-1").decode("utf-8",errors="ignore")
            for i in data])
    data = list(set(temp))
    data.remove("") if "" in data else None
    del temp
    data = [(i,domain) for i in data]
    return data

def getDomainDicts():
    allDomainDicts = {}
    domain = ["教育","IT","动物","医学","历史名人","古诗","敏感词","汽车品牌、零件","法律","财经","食物"]
    for root, dirs, files in os.walk(domainDict_root):
        flag = list(set([i if  i in root else 0 for i in domain]))
        flag.remove(0)
        if len(flag) == 0 : continue
        flag = flag[0]
        sep = ", "if flag == "敏感词" else "\t"

        for file in files:
            if ".md" in file: continue
            domain_root = os.path.join(root,file)
            dict_word = getDomain(domain_root,
                                  file.split(".txt")[0]+flag if flag == "敏感词" else flag,
                                  sep,flag =="古诗")
            if flag in allDomainDicts:
                #print(flag,domain_root)
                temp = allDomainDicts[flag]
                temp.extend(dict_word)
                allDomainDicts[flag] = temp
            else:
                allDomainDicts[flag] = dict_word
        allDomainDicts[flag] = dict(dict_word)
    return allDomainDicts

                #    allDomainDicts[file] = getDomain(file)
    #return allDomainDicts

def getScore(dicts,sentence,type="dict"):
    scoreDict = {}
    for words in dicts.keys():
        scoreDict[words] = 0
    for word in sentence.keys() :
        for i in dicts:
            if word in (dicts[i].keys() if type == "dict" else dicts[i]):
                scoreDict[i] += 1 * sentence[word]
    all_count = 0.001
    for words in dicts.keys():
        all_count += scoreDict[words]
    return {i : (scoreDict[i])/ all_count for i in scoreDict.keys()}



def sentenceProcess(sentence):
    sentence = sentenceCut(sentence)
    stopwords = get_stopwords_list()
    out_list = move_stopwords(sentence,stopwords)
    sentence = wordsBag(out_list)
    return sentence

def getSentenceDomain(domainDicts,sentence):
    domainDicts_definate = getScore(domainDicts,sentence)
    return domainDicts_definate



def getSensitive(file,sep = "\t"):
    data = np.unique(pd.read_csv(file,sep=sep,header=None,encoding="GBK").values[:,0])
    data = [str(i) for i in data]
    return data

def getSensitiveDicts():
    allSensitiveDicts = {}
    for root, dirs, files in os.walk(sensitive_root):
        for file in files:
            sensitiveFileRoot = os.path.join(root,file)
            allSensitiveDicts[file.split(".")[1]] = getSensitive(sensitiveFileRoot)
    return allSensitiveDicts

def getSentenceSensitive(sensitiveDicts,sentence):
    domainDicts_definate = getScore(sensitiveDicts,sentence,"list")
    return domainDicts_definate



