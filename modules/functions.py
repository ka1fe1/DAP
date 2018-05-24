# -*- coding: utf-8 -*-
# from snownlp import SnowNLP
from dataProcess.dap.modules.connector_mysql import MySQLConnector
from dataProcess.dap.modules.constants import Constants
import datetime


def translate_full_shaped_to_half(string):
    """
    全角转半角函数
    :param string: 字符串
    :return:
    """
    translated_str = ""
    for char in string:
        inside_code = ord(char)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        translated_str += chr(inside_code)
    return translated_str


# def complex_font_to_simple_font(string):
#     """
#     繁体中文转简体中文
#     :param string:
#     :return:
#     """
#     s = SnowNLP(string)
#     return s.han


def translate_hash_table(string, scope):
    """
    读取数据库 hash table 执行转换
    :param string:
    :return:
    """
    connector = MySQLConnector()
    sql = """
        SELECT b.name,b.alias
        FROM {table_name} b
        where b.scope = "{scope}" and "{aliasStr}" regexp b.regexp_a
        order by b.w desc
    """.format(table_name=Constants.table_hash_table, aliasStr={string}, scope=scope)
    data = connector.query_data(sql)

    for i, v in enumerate(data):
        name = v['name'].decode()
        alias = v['alias'].decode()
        string = string.replace(alias, name)

    return string


def format_time(time: datetime=datetime.datetime.now(), pattern="%Y-%m-%d %H:%M:%S"):
    """
    格式化输出时间
    :param time:
    :param pattern:
    :return:
    """
    return time.strftime(pattern)


if __name__ == '__main__':
    # b = translate_full_shaped_to_half("ｍｎ1２3　abc＂博客园＂！ｓｄ")
    # b = complex_font_to_simple_font('「繁體字」「繁體中文」的叫法在臺灣亦很常見。')
    # b = translate_hash_table('洛克35克', 's')
    print(format_time())


