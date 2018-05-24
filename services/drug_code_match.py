# -*- coding: utf-8 -*-

from dataProcess.dap.modules.connector_mysql import MySQLConnector
from dataProcess.dap.modules.constants import TableName
from dataProcess.dap.modules.constants import Constants
from dataProcess.dap.dto.dcm_res_dto import DcmResDTO
from dataProcess.dap.modules.dp_exception import DpException
from dataProcess.dap.modules.constants import ErrorConstants
from collections import namedtuple


class Dcm:
    """
    药品配码
    """
    @staticmethod
    def get_dcm_detail_result(dto: DcmResDTO):
        """
        获取药品配码详细结果
        :param dto: 请求参数
        :return:
        """
        connect = MySQLConnector()
        sql = """
            select id_m, src
            from {table_name}
            where case_id = {case_id} and id_s = {id_s}
        """.format(table_name=TableName.tbn_case_dcm_res, case_id=dto.case_id, id_s=dto.id_s)
        data = connect.query_data(sql)

        res_list = []
        for i in data:
            dto = DcmResDTO()
            dto.convert_json_object(i)
            res_list.append(dto.__dict__)

        return res_list

    def update_dcm_data_sme_score(self, dto: DcmResDTO, sme_score_dcm_data: int):
        """
        更新 case_dcm_data 的 sme_score
        如果 case_dcm_res 表中存在 sme_score=1 的记录，则须将这些记录的 sme_score 更新为 0
        :param dto:
        :param sme_score_dcm_data:
        :return:
        """
        case_id = dto.case_id
        id_s = dto.id_s
        if sme_score_dcm_data == 0:
            # 没有合适的匹配项
            '''
            将 case_dcm_res 中所有 sme_score=1 的数据更新为 sme_score=0
            '''
            connect = MySQLConnector()
            sql = """
                select case_id, id_s, id_m, score, note, 0 as `sme_score`, 0 as `is_single_res`
                from {table_name}
                where case_id = {case_id} and id_s = {id_s} and sme_score = 1
            """.format(
                table_name=TableName.tbn_case_dcm_res,
                case_id=case_id, id_s=id_s
            )
            data = connect.query_data(sql=sql)

            if len(data) > 0:
                for i in data[:]:
                    dto = DcmResDTO()
                    dto.case_id = i['case_id']
                    dto.id_s = i['id_s']
                    dto.id_m = i['id_m']
                    dto.score = i['score']
                    dto.p_note = i['note']
                    dto.sme_score = i['sme_score']
                    dto.is_single_res = i['is_single_res']

                    self.update_res_sme_score(dto=dto)

        '''
        更新 case_dcm_data 的 sme_score
        '''
        connect = MySQLConnector()
        sql = """
            update {table_name}
            set sme_score = {sme_score}
            where case_id = {case_id} and id_s = {id_s}
        """.format(
            table_name=TableName.tbn_case_dcm_data,
            sme_score=sme_score_dcm_data,
            case_id=case_id, id_s=id_s
        )
        connect.manipulate_data(sql=sql)

    def insert_dcm_single_data(func):

        def wrapper(self, dto: DcmResDTO):
            """
            将标记为正确的单条配码数据插入 case_dcm_res 中
            :param self: class instance
            :param dto: 请求参数
            :return:
            """
            '''
            查询 case_dcm_data 表中的 sme_score,
            当 sme_score=0 时，不允许更新 case_dcm_res 表中的 sme_score
            '''
            connect = MySQLConnector()
            sql = """
                select sme_score
                from {table_name}
                where case_id = {case_id} and id_s = {id_s}
            """.format(table_name=TableName.tbn_case_dcm_data,
                       case_id=dto.case_id, id_s=dto.id_s
            )
            data = connect.query_data(sql=sql)
            if len(data) <= 0:
                raise DpException()
            else:
                sme_score_dcm_data = data[0]['sme_score']

            if sme_score_dcm_data == 0:
                raise DpException(error_code=ErrorConstants.ec_dcm_update_res_sme_score_forbidden,
                                  error_message=ErrorConstants.error_code_message.
                                  get(ErrorConstants.ec_dcm_update_res_sme_score_forbidden))

            connect = MySQLConnector()
            sql = """
              select note, sme_score
              from {table_name}
              where case_id = {case_id} and id_s = {id_s} and id_m = {id_m}
            """.format(table_name=TableName.tbn_case_dcm_res,
                       case_id=dto.case_id, id_s=dto.id_s, id_m=dto.id_m)
            data = connect.query_data(sql=sql)

            if len(data) <= 0:
                if dto.sme_score == 0:
                    return
                connect = MySQLConnector()
                sql = """
                INSERT ignore INTO {table_name} (
                    `case_id`, `id_s`, `id_m`,
                    `score`, `sub_score`, `rank`,
                    `an_score`, `an_s`, `an_s_srch`, `an_m`, `an_m_srch`,
                    `name_score`, `name_s`, `name_s_srch`, `name_m`, `name_m_srch`,
                    `df_score`, `df_s`, `df_s_srch`, `df_m`, `df_m_srch`,
                    `spec_score`, `spec_s`, `spec_s_srch`, `spec_m`, `spec_m_srch`,
                    `company_score`, `company_s`, `company_s_srch`, `company_m`, `company_m_srch`,
                    `src`, `srch_t`, `srch_iter`, `note`)
                VALUES(
                    {case_id}, {id_s}, {id_m},
                    {score}, {sub_score}, {rank},
                    {an_score}, '{an_s}', '{an_s_srch}', '{an_m}', '{an_m_srch}',
                    {name_score}, '{name_s}', '{name_s_srch}', '{name_m}', '{name_m_srch}',
                    {df_score}, '{df_s}', '{df_s_srch}', '{df_m}', '{df_m_srch}',
                    {spec_score}, '{spec_s}', '{spec_s_srch}', '{spec_m}', '{spec_m_srch}',
                    {company_score}, '{company_s}', '{company_s_srch}', '{company_m}', '{company_m_srch}',
                    '{src}', '{srch_t}', '{srch_iter}', '{note}'
                )
                """.format(
                    table_name=TableName.tbn_case_dcm_res,
                    case_id=dto.case_id, id_s=dto.id_s, id_m=dto.id_m,
                    score=dto.score, sub_score=dto.sub_score, rank=dto.rank,
                    an_score=dto.an_score, an_s=dto.an_s, an_s_srch=dto.an_s_srch, an_m=dto.an_m,
                    an_m_srch=dto.an_m_srch,
                    name_score=dto.name_score, name_s=dto.name_s, name_s_srch=dto.name_s_srch, name_m=dto.name_m,
                    name_m_srch=dto.name_m_srch,
                    df_score=dto.df_score, df_s=dto.df_s, df_s_srch=dto.df_s_srch, df_m=dto.df_m,
                    df_m_srch=dto.df_m_srch,
                    spec_score=dto.spec_score, spec_s=dto.spec_s, spec_s_srch=dto.spec_s_srch, spec_m=dto.spec_m,
                    spec_m_srch=dto.spec_m_srch,
                    company_score=dto.company_score, company_s=dto.company_s, company_s_srch=dto.company_s_srch,
                    company_m=dto.company_m, company_m_srch=dto.company_m_srch,
                    src=dto.p_src, srch_t=dto.srch_t, srch_iter=dto.srch_iter, note=dto.p_note
                )
                connect.manipulate_data(sql=sql)
            else:
                # 异常情况：
                original_sme_score = data[0]['sme_score']
                if dto.sme_score == 0:
                    if original_sme_score is None or original_sme_score == 0:
                        return
                else:
                    if original_sme_score == 1:
                        return
                dto.p_note = data[0]['note']

            func(self, dto)

            #  更新 case_dcm_data 表中的数据，取 res 中 rank=1 的数据
            self.update_dcm_data(dto.case_id, dto.id_s, int(dto.sme_score))

        return wrapper

    '''
    1. 查询 case_dcm_data 表中的 sme_score,
        当 sme_score=0 时，不允许更新 case_dcm_res 表中的 sme_score
    2. 对与单条配码结果的数据，先执行插入操作
    3. 更新 case_dcm_res 表中的 sme_score 并重新根据 score 给 rank 排序
        1 if sme_score = 1(匹配正确)：
            update sme_score=1, score=120, note='原始分||批量or单条||original_note'
        2 if sme_score = null(取消匹配正确操作):
            update sme_score=0, score=原始分, note='批量or单条||original_note'
    4. 更新 case_dcm_data：取 case_dcm_res 中 rank = 1 的记录并更新 sme_score
        当 sme_score=0 时(取消标记正确)，若 case_dcm_res 中没有被标记为正确的记录，
        则将 case_dcm_data 表中的 sme_score 更新为 null
    '''
    @insert_dcm_single_data
    def update_res_sme_score(self, dto: DcmResDTO):
        """
        更新 case_dcm_res 中 sme_score
        :param dto:
        :return:
        """
        '''
        更新 case_dcm_res 表中的 sme_score 并重新根据 score 给 rank 排序
        1 if sme_score = 1(匹配正确)：
            update sme_score=1, score=120, note='原始分||批量or单条||original_note'
        2 if sme_score = null(取消匹配正确操作):
            update sme_score=0, score=原始分, note='批量or单条||original_note'
        '''
        sme_score = dto.sme_score
        operator_or = Constants.operator_or
        if sme_score == 1:
            sme_score = 1
            score = Constants.dcm_update_sme_score_correct
            res_src = Constants.res_src_single if dto.is_single_res == 1 else ''
            note_list = [str(dto.score)]
            note_list.append(res_src) if res_src else None
            note_list.extend(dto.p_note.split(operator_or))
            s = set()
            s_add = s.add
            note = operator_or.join([x for x in note_list if not (x in s or s_add(x))])
        else:
            original_note = dto.p_note
            strs = original_note.split(operator_or)
            sme_score = 0
            score = int(dto.score) if len(strs) == 1 else strs[0]
            note = original_note if len(strs) == 1 else operator_or.join([strs[1]] if len(strs) == 2 else [strs[1], strs[2]])

        sql = """
            update {table_name}
            set sme_score = {sme_score}, score = {score}, note = '{note}'
            where case_id = {case_id} and id_s = {id_s} and id_m = {id_m}
        """.format(
            table_name=TableName.tbn_case_dcm_res,
            sme_score=sme_score, score=score, note=note,
            case_id=dto.case_id, id_s=dto.id_s, id_m=dto.id_m
            )
        connect = MySQLConnector()
        connect.manipulate_data(sql=sql)

        # 根据 score 给 rank 排序并更新
        self.calc_rank(dto.case_id, dto.id_s)

    def calc_rank(self, case_id, id_s):
        """
        根据 score 给 rank 排序并更新
        :param case_id:
        :param id_s:
        :return:
        """
        connect = MySQLConnector()
        sql = """select id_m, score
                 from {table_name}
                 where case_id = {case_id} and id_s = {id_s}
        """.format(table_name=TableName.tbn_case_dcm_res,
                   case_id=case_id, id_s=id_s)
        data = connect.query_data(sql=sql)
        if len(data) > 0:
            new_elements = self.rank(data)

            for e in new_elements:
                score, id, rank = e
                connect = MySQLConnector()
                sql = """
                    update {table_name}
                    set rank = {rank}
                    where case_id = {case_id} and id_s = {id_s} and id_m = {id_m}
                """.format(table_name=TableName.tbn_case_dcm_res,
                           rank=rank,
                           case_id=case_id, id_s=id_s, id_m=id)
                connect.manipulate_data(sql=sql)
        else:
            pass

    def update_dcm_data(self, case_id, id_s, sme_score):
        """
        更新 case_dcm_data：取 case_dcm_res 中 rank = 1 的记录并更新 sme_score
        当 sme_score=0 时(取消标记正确)，若 case_dcm_res 中没有被标记为正确的记录，
        则将 case_dcm_data 表中的 sme_score 更新为 null
        :param case_id: case id
        :param id_s: original id
        :return:
        """

        '''
        更新 case_dcm_data：取 case_dcm_res 中 rank = 1 的记录并更新 sme_score
        '''
        connect = MySQLConnector()
        sql = """
            update {table_name_data} t
            inner join (
                select *
                from {table_name_res}
                where case_id = {case_id} and id_s = {id_s} and rank = 1 limit 1) r
            on t.id_s = r.id_s
            set t.id_m = r.id_m,
                t.score = r.score, t.sme_score = 1,
                t.an_m = r.an_m, t.an_m_srch = r.an_m_srch,
                t.name_m = r.name_m, t.name_m_srch = r.name_m_srch,
                t.df_m = r.df_m, t.df_m_srch = r.df_m_srch,
                t.spec_m = r.spec_m, t.spec_m_srch = r.spec_m_srch,
                t.company_m = r.company_m, t.company_m_srch = r.company_m_srch
            where t.case_id = {case_id}
        """.format(
                table_name_data=TableName.tbn_case_dcm_data,
                table_name_res=TableName.tbn_case_dcm_res,
                case_id=case_id, id_s=id_s)
        connect.manipulate_data(sql=sql)

        '''
        当 sme_score=0 时(取消标记正确)，若 case_dcm_res 中没有被标记为正确的记录，
        则需将 case_dcm_data 表中的 sme_score 更新为 null
        '''
        if sme_score != 1:
            # 查询 case_dcm_res 表中被标记为正确的记录总数
            connect = MySQLConnector()
            sql = """
                select count(*)
                from {table_name}
                where case_id = {case_id} and id_s = {id_s} and sme_score = 1
            """.format(
                table_name=TableName.tbn_case_dcm_res,
                case_id=case_id, id_s=id_s)
            data = connect.query_data(sql=sql)

            if data[0]['count(*)'] == 0:
                connect = MySQLConnector()
                sql = """
                                update {table_name}
                                set sme_score = NULL
                                where case_id = {case_id} and id_s = {id_s}
                            """.format(table_name=TableName.tbn_case_dcm_data,
                                       case_id=case_id, id_s=id_s
                                       )
                connect.manipulate_data(sql=sql)

    def rank(self, data: list):
        """
        按分数由高到低进行排序
        :param data: data = [
                            {'id_m': 12, 'score': 105},
                            {'id_m': 13, 'score': 101},
                            {'id_m': 15, 'score': 103},
                            {'id_m': 11, 'score': 105},
                            {'id_m': 14, 'score': 103},
                            ]
        :return: [(105, 12, 1), (105, 11, 2), (103, 15, 3), (103, 14, 4), (101, 13, 5)]
        """
        scores = []
        elements = []
        for i in data:
            id = i['id_m']
            score = i['score']
            scores.append(score)
            elements.append((score, id, 0))

        scores.sort(reverse=True)

        new_elements = []
        handled_elements = []
        for i, v in enumerate(scores[:]):
            for e in elements[:]:
                score, id, rank = e
                if score == v and rank == 0 and handled_elements.count(e) == 0:
                    new_elements.append((score, id, i+1))
                    handled_elements.append(e)
                    break

        return new_elements

if __name__ == '__main__':
    dcm = Dcm()
    data = [
        {'id_m': 12, 'score': 105},
        {'id_m': 13, 'score': 101},
        {'id_m': 15, 'score': 103},
        {'id_m': 11, 'score': 105},
        {'id_m': 14, 'score': 103},
    ]
    print(dcm.rank(data))