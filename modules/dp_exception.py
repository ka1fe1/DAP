# -*- coding: utf-8 -*-
from dataProcess.dap.vo.base_response import BaseResponse
from dataProcess.dap.modules.constants import ErrorConstants


class DpException(Exception):
    """
    自定义异常类
    """

    def __init__(self, error_code=ErrorConstants.ec_bad_request,
                 error_message=ErrorConstants.error_code_message.get(ErrorConstants.ec_bad_request),
                 status_code=400):
        error_vo = {
            "errorCode": error_code,
            "errorMsg": error_message
        }
        self.status_code = status_code
        self.message = "error occur"
        error_response = BaseResponse(error_vo, self.status_code, self.message)
        super(DpException, self).__init__(error_response)


