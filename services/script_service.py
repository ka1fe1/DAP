# -*- coding: utf-8 -*-

from dataProcess.dap.modules.script import Script
from dataProcess.dap.modules.connector_mysql import MySQLConnector
from dataProcess.dap.dto.dcm_res_dto import DcmResDTO
from dataProcess.dap.vo.dcm_single_record_request import DcmSingleRecordRequest
from dataProcess.dap.modules.constants import Constants, ErrorConstants
from dataProcess.dap.modules.dp_exception import DpException
from dataProcess.dap.modules.functions import format_time


def check_task_is_conflict(func):
    """
    检查是否有其他配码任务进行中，
    若有，则提醒用户等待稍后再试
    :param func:
    :return:
    """

    def wrapper(request_vo: DcmSingleRecordRequest, script_name, sp_name, *args):
        mysql_client = MySQLConnector()
        sql = """
                select * from case_dcm where state = "{state}"
            """.format(state=Constants.dcm_state_work_in_process)
        case_dcm = mysql_client.query_data(sql=sql)
        if case_dcm:
            raise DpException(ErrorConstants.ec_dcm_tasK_conflict,
                              ErrorConstants.error_code_message.get(ErrorConstants.ec_dcm_tasK_conflict))
        result = func(request_vo, script_name, sp_name, *args)
        return result

    return wrapper


def prepare_dcm_data(request_vo: DcmSingleRecordRequest):
    """
    准备配码数据：主要涉及往 case_dcm 和 case_dcm_data 表中插入数据
    :param request_vo:
    :return:
    """
    mysql_client = MySQLConnector()

    sql = """
            insert into case_dcm(`cd`, `an_w`, `name_w`, `df_w`, `spec_w`, `company_w`, `note`)
            values ("{cd}", {an_w}, {name_w}, {df_w}, {spec_w}, {company_w}, "{note}")
            on duplicate key update updatetime="{updatetime}",
             an_w=values(`an_w`), name_w=values(`name_w`), df_w=values(`df_w`),
             spec_w=values(`spec_w`), company_w=values(`company_w`);
        """.format(cd=Constants.dcm_single_code,
                   an_w=Constants.dcm_weight.get(Constants.dcm_w_name_an_w) if request_vo.an_s != '' else 0,
                   name_w=Constants.dcm_weight.get(Constants.dcm_w_name_name_w) if request_vo.name_s != '' else 0,
                   df_w=Constants.dcm_weight.get(Constants.dcm_w_name_df_w) if request_vo.df_s != '' else 0,
                   spec_w=Constants.dcm_weight.get(Constants.dcm_w_name_spec_w) if request_vo.spec_s != '' else 0,
                   company_w=Constants.dcm_weight.get(Constants.dcm_w_name_company_w)
                   if request_vo.company_s != '' else 0,
                   note='single dcm request data',
                   updatetime=format_time()
                   )
    mysql_client.manipulate_data(sql)

    mysql_client = MySQLConnector()
    sql = """
            select id from case_dcm where cd = "{case_cd}";
        """.format(case_cd=Constants.dcm_single_code)
    case_dcm = mysql_client.query_data(sql=sql)
    if case_dcm:
        case_id = case_dcm[0].get('id')
    else:
        case_id = 0

    if case_id == 0:
        raise DpException(ErrorConstants.ec_dcm_internal_error,
                          ErrorConstants.error_code_message.get(ErrorConstants.ec_dcm_internal_error))

    mysql_client = MySQLConnector()
    sql = """
            replace into case_dcm_data(`case_id`, `id_s`, `an_s`, `name_s`, `df_s`, `spec_s`, `company_s`)
            VALUES ({case_id}, {id_s}, "{an_s}", "{name_s}", "{df_s}", "{spec_s}", "{company_s}")
        """.format(case_id=case_id, id_s=Constants.dcm_single_id_s,
                   an_s=request_vo.an_s, name_s=request_vo.name_s,
                   df_s=request_vo.df_s, spec_s=request_vo.spec_s,
                   company_s=request_vo.company_s)
    mysql_client.manipulate_data(sql=sql)


@check_task_is_conflict
def execute_script(request_vo: DcmSingleRecordRequest, script_name, sp_name, *args):
    """
    执行 stored procedure 并返回结果
    :param request_vo: DcmSingleRecordRequest instance
    :param script_name: sql script 的名称
    :param sp_name: stored procedure 的名称
    :param args: stored procedure 的参数
    :return:
    """
    prepare_dcm_data(request_vo)

    mysql_client = MySQLConnector()
    script = Script()
    output = script.execute_sql_script(script_name)
    response = list()
    if output:
        data = mysql_client.call_stored_procedure(sp_name, *args)

        for k, v in enumerate(data):
            results = v.fetchall()

        for index, value in enumerate(results):
            dto = DcmResDTO()

            dto.id_s, dto.id_m, dto.total_score, dto.sub_score, dto.total_rank, \
            dto.an_score, dto.an_s, dto.an_s_srch, dto.an_m, dto.an_m_srch, \
            dto.name_score, dto.name_s, dto.name_s_srch, dto.name_m, dto.name_m_srch, \
            dto.df_score, dto.df_s, dto.df_s_srch, dto.df_m, dto.df_m_srch, \
            dto.spec_score, dto.spec_s, dto.spec_s_srch, dto.spec_m, dto.spec_m_srch, \
            dto.company_score, dto.company_s, dto.company_s_srch, dto.company_m, dto.company_m_srch, \
            dto.p_src, dto.srch_t, dto.srch_iter, dto.p_note = value
            response.append(dto.__dict__)
    return response


if __name__ == '__main__':
    pass
