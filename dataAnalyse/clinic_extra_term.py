# -*- coding: utf-8 -*-
from dataProcess.dap.modules.connector_mysql import MySQLConnector
from dataProcess.dap.modules.log_initiate import initiate_log
import re
from dataProcess.dap.modules.constants import Constants


def extract_clinic_term(str_origin, separator='||'):
    """
    函数主要用于在特定位置加入分隔符（||）
    a. 连续数字被其他字符分隔 --> ||
    b. ; --> ||
    c. ? --> ||
    :param str_origin 待处理的字符串
    :param separator 分隔符
    :return:
    """
    logger = initiate_log(logger_name=Constants.log_name_default)
    logger.debug('原始的字符串：%s', str_origin)
    pattern = re.compile(r'(\d+)(\D+)')
    data = pattern.findall(str_origin)
    nums = [int(v[0]) for v in data if len(data) > 0]
    nums_new = is_element_increment(nums)
    logger.debug('连续递增的数字: %s', nums_new)
    if nums_new:
        for i in nums_new:
            regex = ''
            for j in i:
                regex += '({num})(\D+)'.format(num=j)
            pattern = re.compile(r'{regex}'.format(regex=regex))
            str_origin = pattern.sub(regex_replace, str_origin)
    pattern = re.compile(r'(;|\?)+')
    str_origin = pattern.sub(r'{separator}'.format(separator=separator), str_origin)
    pattern = re.compile(r'\|\|{2,}')  # 去除重复的 ||
    return pattern.sub(separator, str_origin)


def regex_replace(m):
    res = ''
    for i in range(1, len(m.groups()) + 1):
        if m.group(i).title().isdigit():
            res += '||' + m.group(i) + '||'
        else:
            res += m.group(i)
    return res


def is_element_increment(nums):
    """
    将列表中连续递增的数字分组返回
    :param nums 列表
    :return: res 分组后的结果
    """
    res = []
    a = [i for i in range(nums[0], nums[len(nums) - 1] + 1)] if len(nums) > 2 else []
    if a == nums and len(a) > 1:
        res.append(a)
    else:
        index = 0
        for i, v1 in enumerate(nums[:]):
            # 外层循环指针的下标
            if i < index and i != 0:
                continue
            # 外层循环结束
            # if i == len(nums)-1 and v1 != nums[i-1] + 1:
            #     res.append(v1)
            for v2 in nums[i+1:]:
                # 内层循环指针的下标
                index = nums[:].index(v2, i)
                if v2 == v1+(index-i):
                    # 内层循环结束
                    if index == len(nums)-1 and len(nums[i:index+1]) > 1:
                        res.append(nums[i:index+1])
                    else:
                        continue
                else:
                    if len(nums[i:index]) > 1:
                        res.append(nums[i:index])
                    break
    return res


def main():
    logger = initiate_log(logger_name=Constants.log_name_brief)
    separator = '||'
    table_name_wip_cterm = 'wip_cterm'
    table_name_wip_cterm_element = 'wip_cterm_element'
    connector = MySQLConnector()
    sql = """
        select * from {table_name} where origin_cd;
    """.format(table_name=table_name_wip_cterm)
    data = connector.query_data(sql=sql)

    for i, d in enumerate(data[:]):
        for k, v in d.items():
            data[i]
            if k == 'str_new':
                str_ret = extract_clinic_term(v)
                data[i]['str_ret'] = str_ret

    '''
    构造 sql
    '''
    length = len(data)
    sql_value_wip_cterm = sql_value_wip_cterm_element = ''
    for i, v in enumerate(data[:length]):
        str_ret = v['str_ret'].replace('"', '\\"')
        sql_value_wip_cterm += '("{origin_cd}", "{str_ret}")'.format(origin_cd=v['origin_cd'], str_ret=str_ret)
        if i != length - 1:
            sql_value_wip_cterm += ', '
        for j, k in enumerate(str_ret.split(separator)):
            sql_value_wip_cterm_element += '("{origin_cd}", "{term}")'.format(origin_cd=v['origin_cd'], term=k)
            if j != len(str_ret.split(separator)) - 1:
                sql_value_wip_cterm_element += ', '
        if i != length - 1:
            sql_value_wip_cterm_element += ', '

    '''
    wip_cterm 表插入数据
    '''
    logger.info('begin insert data into wip_cterm')
    sql = """
        insert into {table_name}(`origin_cd`, `str_ret`) values{sql_value}
        on DUPLICATE key update str_ret = values(`str_ret`);
    """.format(table_name=table_name_wip_cterm, sql_value=sql_value_wip_cterm)
    connector = MySQLConnector()
    connector.manipulate_data(sql)
    logger.info('end insert data into wip_cterm')

    '''
    wip_cterm_element 表插入数据
    '''
    logger.info('begin insert data into wip_cterm_element')
    sql = """
        insert ignore into {TABLE_NAME}(`origin_cd`, `term`) values{sql_value}
    """.format(TABLE_NAME=table_name_wip_cterm_element, sql_value=sql_value_wip_cterm_element)
    connector = MySQLConnector()
    connector.manipulate_data(sql)
    logger.info('end insert data into wip_cterm_element')

if __name__ == '__main__':
    main()
    # print(extract_clinic_term('13tang1.AB2.DF3们;发炎?PICC封管;5ha;7感冒8流感9突发性感冒14+6周1为2qq3eeds'))
    # print(extract_clinic_term('传染性单核细胞增多症'))
    # print(extract_clinic_term('46死髓;27隐裂牙髓炎'))

    # nums = [13, 1, 2, 3, 5, 7, 8, 9, 14, 1, 2, 3, 15]
    # print(is_element_increment(nums))
    pass




