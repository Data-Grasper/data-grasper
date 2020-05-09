import json
import jieba
import re
import os
from collections import Counter
import pandas as pd
import numpy as np

stopwordsDict_root = "data/stopwords"
domainDict_root = "data/domainDicts"
sensitive_root = "data/sensitiveDicts/清华大学——李军中文褒贬义词典"


def getTextExample():
    '''
    with open('data/317739794_0.json','r',encoding="utf8") as f:
        line = f.readline()
    json_str = json.loads(line)[0]
    keys = json_str.keys()
    content = json_str["content"]
    text = re.sub(r'<[^>]+>'," ", content)
    '''
    text = \
    "AI技术发展至今，已有六十多年的历史。从最初的梦想，到后来的质疑，再到今天的认同与大力发展， AI技术已经走入我们生活的方方面面。中央电视台纪录频道五集科技类纪录片《AI梦想曲》中央电视台纪录频道拍摄并制作的五集科技纪录片《AI梦想曲》日前正在热播，该片分别聚焦医疗、体育、工业、教育等五个不同行业及领域，跟踪记录了科创一线的开发者与使用者们的故事。其中由联奕科技研发的智慧教学系统“奕课堂”应用于华南理工大学的个性化教学的场景，入选该部纪录片。第四集《智教序章》，正是讲述了联奕科技首席信息官舒畅积极探索AI技术助力个性化教学和因材施教的心路历程。联奕首席信息官舒畅与华南理工大学学生们交流的拍摄场景" \
    "\在舒畅看来，“智慧教学”的关键在于因材施教和“学科知识库”，他希望未来的AI助教可以基于每一个学生的学习特点，通过他的团队创建的庞大且完备的“学科知识库”，精准地识别每一个学生的强项弱项，给出个性化匹配的学习路径。“就像魔兽世界中每一个英雄法师都有自己独特的成长路径，我希望有一天AI教育也能实现真正意义上的因材施教。”舒畅说。\
    华南理工大学学生使用奕课堂系统拍摄场景" \
    "\舒畅及团队讨论法学AI知识库拍摄场景" \
    "奕课堂 + AI助教”在华南理工大学的个性化教学尝试" \
    "2018年10月《教育部关于加快建设高水平本科教育全面提高人才培养能力的意见》发布以来，推动课堂教学革命成为高校工作的重中之重。全国高校大力推进智慧教室建设，构建线上线下相结合的教学模式，以学生发展为中心，积极引导学生自我管理、主动学习，激发求知欲望，提高学习效率，提升自主学习能力，从而不断提高课堂教学质量。" \
    "在国家发改委专项经费的支持下，华南理工大学于2019年携手联奕科技共同建设智慧学习空间，在智慧教室加入了一些新元素。除了根据不同的课堂形态和教学需求从功能上设计多种教室类型，配备智能教学设施以实现教学互动、教学活动自动录制以外，奕课堂智慧教学系统则成为华南理工大学智慧教室的最强大脑与灵魂。" \
    "华南理工大学学生使用奕课堂系统拍摄场景" \
    "华南理工大学教育技术中心视频部部长刘广接受纪录片导演采访" \
    "“奕课堂”，是联奕科技于2018年10月10日在第三届智慧校园广州论坛上首次发布的用于解决高校现代教学过程中缺乏互动以及无法进行过程数据采集的问题，同时围绕课前、课中、课后三个教学环节构建的全过程教学环境空间的方案。通过改变教学模式、学习方式、教学空间、教学管理、教学评价，有效帮助教师提高教学效率，强化师生交互。教学过程中的教与学的行为都在无感知的情况下被记录下来，而基于这些数据，奕课堂能指导教师对教学过程进行精准改善，针对不同程度的学生调整不同的教学方式或教学重点，实现了“因材施教”中的“因材“目的。" \
    "而因材之后的目的是施教，在发现了每一个学生不同的学习特点、偏好之后，如何帮助教师尽可能的通过个性化引导、游戏化任务来教授知识呢？这才是我们希望通过" \
    "AI助教" \
    "来扮演任课教师的“哆啦A梦”的目的，也是联奕科技智慧教学" \
    "的目标。" \
    "AI助教”，综合利用大数据、人工智能等技术，通过采集并深度分析教学过程中的动态数据，识别学生的学习特点及兴趣偏好，并根据预先建立的各个学科专业知识库，动态关联及智能推荐相关知识点内容，辅助教师进行课前指导及课后复习，同时借助游戏化学习理念，根据学科知识地图设计学习任务进行引导学习。" \
    "华南理工大学法学院副教授林志毅接受纪录片导演采访拍摄场景" \
    "AI助教由于需要结合各个专业知识库，而目前华宇集团的学科知识库，能够达到全国领先水平的主要还是覆盖在法学相关专业。因此，我们在华南理工大学挑选部分法学专业的学科开启了AI助教试点，已取得了阶段性试验成果。" \
    "这一次的实践，华宇集团旗下教育信息化版块联奕科技，联合法律科技版块元典，通过对高校法学教育的实地调研和分析，结合自身在教育行业多年深耕以及华宇法律科技的积累，着力打造了以法律知识图谱为核心，以智能检索和推荐为特色的面向法学院教学及研究场景的智能知识服务平台。系统可对数千万份公开裁判文书和相关法律知识内容进行深度挖掘和分析，并与“法学教学知识点”和“典型案例问题评析”相结合，一方面帮助老师在备课过程中快速查找和关联案例等相关的知识素材，丰富教学内容，另一方面也可以基于法学学生的专业方向、兴趣和学习需求，主动推送相关的知识进行参考和阅读。" \
    "奕课堂与AI助教的有机融合，形成了更智能化的教学系统，相当于奕课堂" \
    "升级版，让教师的“教”与学生的“学”都更加有的放矢，朝实现真正的个性化教学和“因材施教”的终极目标又迈进一大步。" \
    "推出市场一年多来，除了在华南理工大学得到了有效尝试，奕课堂目前还在中山大学、华南师范大学、广东石油化工学院、暨南大学、兰州理工大学、合肥工业大学等50余所高校上线使用，其中不乏全国双一流、985、211" \
    "院校。而AI助教也即将在全国高校的法学专业逐步推广，也更加坚定了联奕科技运用AI技术推进个性化教学和“因材施教”的决心。"
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



domainDicts = getDomainDicts()
sensitiveDicts = getSensitiveDicts()



sentence = getTextExample()
sentence = sentenceProcess(sentence)
domainDicts_definate = getSentenceDomain(domainDicts,sentence)
sensitiveDicts_definate = getSentenceSensitive(sensitiveDicts,sentence)
print(domainDicts_definate)
print(sensitiveDicts_definate)