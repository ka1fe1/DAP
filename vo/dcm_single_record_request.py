# -*- coding: utf-8 -*-
from dataProcess.dap.vo.base_request import BaseRequest
from dataProcess.dap.vo.validator import Validator
from dataProcess.dap.modules.dp_exception import DpException


class DcmSingleRecordRequest(BaseRequest, Validator):
    """

    """

    @property
    def an_s(self):
        return self.anS

    @an_s.setter
    def an_s(self, value):
        self.anS = value

    @property
    def name_s(self):
        return self.nameS

    @name_s.setter
    def name_s(self, value):
        self.nameS = value

    @property
    def df_s(self):
        return self.dfS

    @df_s.setter
    def df_s(self, value):
        self.dfS = value

    @property
    def spec_s(self):
        return self.specS

    @spec_s.setter
    def spec_s(self, value):
        self.specS = value

    @property
    def company_s(self):
        return self.companyS

    @company_s.setter
    def company_s(self, value):
        self.companyS = value

    def validate(self):
        if (self.an_s == "" and
                self.name_s == ""and
                self.df_s == "" and
                self.spec_s == "" and
                self.company_s == ""):
            raise DpException()
        else:
            return True
