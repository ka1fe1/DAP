# -*- coding: utf-8 -*-

from flask import Flask, request
from dataProcess.dap.services import script_service
from dataProcess.dap.modules.constants import Constants
from dataProcess.dap.vo.dcm_single_record_request import DcmSingleRecordRequest
from dataProcess.dap.vo.base_response import BaseResponse
from dataProcess.dap.modules.dp_exception import DpException
from dataProcess.dap.confs.env import env
from dataProcess.dap.dto.dcm_res_dto import DcmResDTO
from dataProcess.dap.services.drug_code_match import Dcm
from dataProcess.dap.modules.zk_config import ZkConfig

app = Flask(__name__)

zk = ZkConfig()

@app.before_request
def get_config():
    if env == "beta" or env == "pro":
        node_path_env = Constants.zk_node_root + env + "/"
        node_path_db = node_path_env + "mysql"
        zk.get_db_config(node_path_env, node_path_db)
    else:
        pass



@app.route('/api_py')
def test():
    return BaseResponse({"name": "this is test", 'env': env})


@app.route('/api_py/execute_sql_script/<script_type>', methods=['POST'])
def execute_sql_script(script_type):
    request_data_json = request.get_json(force=True)
    request_vo = DcmSingleRecordRequest().convert_json_object(request_data_json)
    script_name = Constants.script_type.get(script_type)
    case_cd = Constants.dcm_single_code
    try:
        request_vo.validate()
        response_data = script_service.execute_script(request_vo, script_name, Constants.sp_name_dcm_batch_srch,
                                                      case_cd, 1)
    except DpException as e:
        return e.args
    return BaseResponse(response_data)


@app.route('/api_py/dcm_detail_res', methods=['POST'])
def get_dcm_detail_res():
    param_json = request.get_json(force=True)
    request_vo = DcmResDTO().convert_json_object(param_json)
    try:
        response = Dcm.get_dcm_detail_result(request_vo)
    except DpException as e:
        return e.args
    return BaseResponse(response)


@app.route('/api_py/dcm_res', methods=['PUT'])
def update_dcm_res_sme_score():
    param_json = request.get_json(force=True)
    request_vo = DcmResDTO().convert_json_object(param_json)
    try:
        response = Dcm().update_res_sme_score(request_vo)
    except DpException as e:
        return e.args
    return BaseResponse(response)


@app.route('/api_py/dcm_data', methods=['PUT'])
def update_dcm_data_sme_score():
    param_json = request.get_json(force=True)
    request_vo = DcmResDTO().convert_json_object(param_json)
    try:
        response = Dcm().update_dcm_data_sme_score(request_vo, int(param_json['smeScore']))
    except DpException as e:
        return e.args
    return BaseResponse(response)


if __name__ == '__main__':
    pass
    # app.run()
    app.run('0.0.0.0', port=9902, debug=True)
