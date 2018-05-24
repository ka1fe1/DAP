# -*- coding:utf-8 -*-
from dataProcess.dap.modules.connector_mysql import MySQLConnector
from dataProcess.dap.modules.constants import TableName
import codecs
import jieba
from dataProcess.dap.modules.log_initiate import initiate_log
import os

logger = initiate_log()


def get_split_line(topic):
    return '=' * 30 + topic + '=' * 30


def create_user_dict():
    """
    读取 wip_cterm_element 中的 term 作为自定义的字典
    :return:
    """
    connect = MySQLConnector()
    sql = """
        select term
        from {table_name}
    """.format(table_name=TableName.tbn_wip_cterm_element)
    data = connect.query_data(sql=sql)

    if len(data) > 0:
        file_object = codecs.open('dict_term.txt', 'w', 'utf-8')
        for i in data[:]:
            term = i['term']
            file_object.write(term + '\n')
        file_object.close()


def split_term(term: str, use_user_dict: bool = False):
    """
    分词
    :param term:
    :return:
    """
    topic = '添加自定义词典'
    split_line = get_split_line(topic)
    logger.debug(split_line)
    test_sent = term
    words = jieba.cut(test_sent)
    logger.debug('{topic}_原始: {msg}'.format(topic=topic, msg='/'.join(words)))

    """
        调整词典：动态修改词典
    """
    if not use_user_dict:
        return
    userdict_path = os.path.dirname(__file__) + "/dict_term.txt"
    # jieba.add_word('凱特琳')
    # jieba.del_word('自定义词')
    jieba.load_userdict(userdict_path)
    words = jieba.cut(test_sent)
    logger.debug('{topic}_自定义字典分词：{msg}'.format(topic=topic, msg='/'.join(words)))


if __name__ == '__main__':
    # create_user_dict()
    split_term('下呼吸系统感染', True)
