# -*- coding: utf-8 -*-


class Constants:

    table_hash_table = 'b_alias'

    script_type = {
        'dcm': 'dcm_1_processingV9.sql'
    }
    #  store procedure name
    sp_name_dcm_batch_srch = 'dcm_batch_srch'
    #  单条配码请求的 case cd
    dcm_single_code = 'single'
    #  单条配码请求的 id_s
    dcm_single_id_s = 10000
    #  配码状态：进行中
    dcm_state_work_in_process = 'w'

    #  日志名称
    log_name_default = 'default'
    log_name_brief = 'brief'

    # 配码项权重
    dcm_w_name_an_w = 'an_w'
    dcm_w_name_name_w = 'name_w'
    dcm_w_name_df_w = 'df_w'
    dcm_w_name_spec_w = 'spec_w'
    dcm_w_name_company_w = 'company_w'
    dcm_weight = {
        dcm_w_name_an_w: 14,
        dcm_w_name_name_w: 13,
        dcm_w_name_df_w: 10,
        dcm_w_name_spec_w: 10,
        dcm_w_name_company_w: 10
    }

    # 更新配码分数：人工标记为正确的数据的分数
    dcm_update_sme_score_correct = 120

    # or 操作符
    operator_or = '||'

    # 配码结果来源：单条 or 批量
    res_src_single = '单条'
    res_src_batch = '批量'

    # zookeeper 配置
    zk_node_root = "/dcm/"

class TableName:
    """
    定义 table name
    """
    tbn_case_dcm_res = 'case_dcm_res'
    tbn_case_dcm_data = 'case_dcm_data'
    tbn_wip_cterm_element = 'wip_cterm_element'


class ErrorConstants:
    """
    定义 error_code 与 error_message
    """

    ec_bad_request = "bad request"
    ec_unauthorized = "unauthorized"
    ec_dcm_tasK_conflict = "ec_dcm_task_conflict"
    ec_dcm_internal_error = "ec_dcm_internal_error"
    ec_dcm_update_res_sme_score_forbidden = 'ec_dcm_update_res_sme_score_forbidden'
    ec_sys_error = "system_error"
    error_code_message = {
        ec_bad_request: "参数校验失败",
        ec_unauthorized: "无效的授权",
        ec_dcm_tasK_conflict: "系统中存在正在运行的配码任务，请稍后再试",
        ec_dcm_internal_error: "配码服务内部错误，终止配码",
        ec_dcm_update_res_sme_score_forbidden: "人工审核结果为【没有合适的匹配项】时，禁止此操作！请更改审核结果后再来操作",
        ec_sys_error: "系统异常, "
    }




