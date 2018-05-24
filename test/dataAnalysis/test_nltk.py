# -*- coding: utf-8 -*-
import nltk
import unittest
from dataProcess.dap.modules.log_initiate import initiate_log
import jieba

class TestNltk(unittest.TestCase):
    """
    nltk: natural language toolkit
    """
    logger = initiate_log()

    def setUp(self):
        pass
        # nltk.download("all")

    def test_simple(self):
        sentence = """我最爱吃的东西是凤梨"""
        tokens = jieba.lcut(sentence)
        self.logger.debug(','.join(tokens))
        jieba.add_word('爱吃')
        references_1 = jieba.lcut('我爱吃的东西是凤梨啊')
        self.logger.debug('references 1: %s', references_1)
        references_2 = jieba.lcut('他不爱吃苹果')
        self.logger.debug('references 2: %s', references_2)
        references_3 = jieba.lcut('我们都是中国人地地道道')
        self.logger.debug('references 3: %s', references_3)
        score = nltk.bleu([references_1], tokens)
        self.logger.debug('bleu score is %s', score)
        pass