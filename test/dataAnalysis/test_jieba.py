# -*- coding: utf-8 -*-

import jieba
import os
import jieba.analyse as analyse
from dataProcess.dap.modules.log_initiate import initiate_log
import unittest


class Jieba(unittest.TestCase):
    """
    jieba 中文分词
    """
    logger = initiate_log()

    # def __init__(self):
    #     self.logger = initiate_log()

    def get_split_line(self, topic):
        return '='*30 + topic + '='*30

    def test_split_mode(self):
        """
        分词模式
        """
        topic = '分词模式'
        split_line = self.get_split_line(topic)
        self.logger.debug(split_line)
        """
        全模式：把句子中所有的金额已成词的词语都扫描出来，速度非常快，但不能解决歧义
        """
        seg_list = jieba.cut("中华人民共和国", cut_all=True)
        self.logger.info("{topic}_全模式: {msg}".format(topic=topic, msg="/ ".join(seg_list)))

        """
        精确模式：试图将句子最精确的切开，适合文本分析
        """
        seg_list = jieba.cut("中华人民共和国", cut_all=False)
        self.logger.info("{topic}_精确模式(默认): {msg}".format(topic=topic, msg="/".join(seg_list)))

        """
        搜索模式：在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词
        """
        seg_list = jieba.cut_for_search("中华人民共和国")
        self.logger.info("{topic}_搜索模式: {msg}".format(topic=topic, msg=", ".join(seg_list)))

    def test_user_dict(self):
        """
        2. 自定义词典
        """
        topic = '添加自定义词典'
        split_line = self.get_split_line(topic)
        self.logger.debug(split_line)
        test_sent = """李小福是创新办主任也是云计算方面的专家; 什么是八一双鹿\n
        例如我输入一个带“韩玉赏鉴”的标题，在自定义词库中也增加了此词为N类\n
        台中」正確應該不會被切開。mac上可分出「石墨烯」；此時又可以分出來凱特琳了。
        """
        words = jieba.cut(test_sent)
        self.logger.debug('{topic}_原始: {msg}'.format(topic=topic, msg='/'.join(words)))

        """
                调整词典：动态修改词典
                """
        userdict_path = os.path.dirname(__file__) + "/jieba_dict/dict.txt"
        jieba.add_word('石墨烯')
        jieba.add_word('凱特琳')
        jieba.del_word('自定义词')
        jieba.load_userdict(userdict_path)
        words = jieba.cut(test_sent)
        self.logger.debug('{topic}_自定义字典分词：{msg}'.format(topic=topic, msg='/'.join(words)))

        self.logger.debug('test split words' + "=" * 40)
        terms = jieba.cut('easy_install is great')
        self.logger.debug('{topic}_字典分词: {msg}'.format(topic=topic, msg='/'.join(terms)))
        jieba.del_word('easy_install')
        terms = jieba.cut('easy_install is great')
        self.logger.debug('{topic}_删除单词: {msg}'.format(topic=topic, msg='/'.join(terms)))
        terms = jieba.cut('python 的正则表达式是好用的')
        self.logger.debug('{topic}_单词: {msg}'.format(topic=topic, msg='/'.join(terms)))

        self.logger.debug('test frequency tune' + "=" * 40)
        word = '这里中将应该被切开'
        self.logger.debug('{topic}_调低词频之前: {msg}'.format(topic=topic, msg='/'.join(jieba.cut(word))))
        self.logger.debug('{topic}_调整词频: {msg}'.format(
            topic=topic,
            msg='before: {before}, after: {after}'.format(
                before=jieba.get_FREQ('中将'),
                after=jieba.suggest_freq(('中', '将'), True))))
        self.logger.debug('{topic}_调低词频之后: {msg}'.format(topic=topic, msg='/'.join(jieba.cut(word, HMM=False))))

        jieba.del_word('台中')
        word = '[台中]正确应该不会被切开'
        self.logger.debug('{topic}_调高词频之前: {msg}'.format(topic=topic, msg='/'.join(jieba.cut(word))))
        self.logger.debug('{topic}_调整词频: {msg}'.format(
            topic=topic,
            msg='before: {before}, after: {after}'.format(
                before=jieba.get_FREQ('台中'),
                after=jieba.suggest_freq('台中', True))))
        self.logger.debug('{topic}_调高词频之后: {msg}'.format(topic=topic, msg='/'.join(jieba.cut(word, HMM=False))))

    def test_extract_tags(self):
        """
        3. 关键词抽取
        """
        topic = '关键词抽取'
        split_line = self.get_split_line(topic=topic)
        self.logger.info(split_line)

        term = '我们时人中国的可是is of super man'
        res = analyse.extract_tags(term)
        self.logger.info('{topic}_标准抽取: {term} -> {msg}'.format(topic=topic, term=term, msg=res))

        #  TODO: 自定义语料库运行有问题
        user_idf_path = os.path.dirname(__file__) + '/jieba_dict/idf.txt.big'
        analyse.set_idf_path(user_idf_path)
        res = analyse.extract_tags(term)
        self.logger.info('{topic}_自定义逆向文件频率: {term} -> {msg}'.format(topic=topic, term=term, msg=res))

    def test_tokenize(self):
        """
        Tokenize: 返回词语在原文的位置
        """
        topic = '返回词语在原文的位置'
        split_line = self.get_split_line(topic)
        self.logger.debug(split_line)

        term = '我们都是炎黄子孙'
        res = jieba.tokenize(term)
        for tk in res:
            self.logger.debug('{topic}_默认模式_{term}: {msg}'.format(topic=topic,
                                                             term=term,
                                                             msg="word %s\t\t start: %d \t\t end:%d" % (
                                                             tk[0], tk[1], tk[2])))

        res = jieba.tokenize(term, mode='search')
        for tk in res:
            self.logger.debug('{topic}_搜索模式_{term}: {msg}'.format(topic=topic,
                                                             term=term,
                                                             msg="word %s\t\t start: %d \t\t end:%d" % (
                                                             tk[0], tk[1], tk[2])))












