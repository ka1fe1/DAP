# -*- coding: utf-8 -*-
from dataProcess.dap.vo.base_request import BaseRequest


class DcmResDTO(BaseRequest):
    """

    """

    def __init__(self, **entries):
        self.__dict__.update(entries)

    @property
    def id_s(self):
        return self.idS

    @id_s.setter
    def id_s(self, value):
        self.idS = value

    @property
    def id_m(self):
        return self.idM

    @id_m.setter
    def id_m(self, value):
        self.idM = value

    @property
    def total_score(self):
        return self.score

    @property
    def total_rank(self):
        return self.rank

    @total_rank.setter
    def total_rank(self, value):
        self.rank = value

    @total_score.setter
    def total_score(self, value):
        self.score = value

    @property
    def an_score(self):
        return self.anScore

    @an_score.setter
    def an_score(self, value):
        self.anScore = value

    @property
    def an_s(self):
        return self.anS

    @an_s.setter
    def an_s(self, value):
        self.anS = value

    @property
    def an_s_srch(self):
        return self.anSSrch

    @an_s_srch.setter
    def an_s_srch(self, value):
        self.anSSrch = value

    @property
    def an_m(self):
        return self.anM

    @an_m.setter
    def an_m(self, value):
        self.anM = value

    @property
    def an_m_srch(self):
        return self.anMSrch

    @an_m_srch.setter
    def an_m_srch(self, value):
        self.anMSrch = value

    @property
    def name_score(self):
        return self.nameScore

    @name_score.setter
    def name_score(self, value):
        self.nameScore = value

    @property
    def name_s(self):
        return self.nameS

    @name_s.setter
    def name_s(self, value):
        self.nameS = value

    @property
    def name_s_srch(self):
        return self.nameSSrch

    @name_s_srch.setter
    def name_s_srch(self, value):
        self.nameSSrch = value

    @property
    def name_m(self):
        return self.nameM

    @name_m.setter
    def name_m(self, value):
        self.nameM = value

    @property
    def name_m_srch(self):
        return self.nameMSrch

    @name_m_srch.setter
    def name_m_srch(self, value):
        self.nameMSrch = value

    @property
    def df_score(self):
        return self.dfScore

    @df_score.setter
    def df_score(self, value):
        self.dfScore = value

    @property
    def df_s(self):
        return self.dfS

    @df_s.setter
    def df_s(self, value):
        self.dfS = value

    @property
    def df_s_srch(self):
        return self.dfSSrch

    @df_s_srch.setter
    def df_s_srch(self, value):
        self.dfSSrch = value

    @property
    def df_m(self):
        return self.dfM

    @df_m.setter
    def df_m(self, value):
        self.dfM = value

    @property
    def df_m_srch(self):
        return self.dfMSrch

    @df_m_srch.setter
    def df_m_srch(self, value):
        self.dfMSrch = value

    @property
    def spec_score(self):
        return self.specScore

    @spec_score.setter
    def spec_score(self, value):
        self.specScore = value

    @property
    def spec_s(self):
        return self.specS

    @spec_s.setter
    def spec_s(self, value):
        self.specS = value

    @property
    def spec_s_srch(self):
        return self.specSSrch

    @spec_s_srch.setter
    def spec_s_srch(self, value):
        self.specSSrch = value

    @property
    def spec_m(self):
        return self.specM

    @spec_m.setter
    def spec_m(self, value):
        self.specM = value

    @property
    def spec_m_srch(self):
        return self.specMSrch

    @spec_m_srch.setter
    def spec_m_srch(self, value):
        self.specMSrch = value

    @property
    def company_score(self):
        return self.companyScore

    @company_score.setter
    def company_score(self, value):
        self.companyScore = value

    @property
    def company_s(self):
        return self.companyS

    @company_s.setter
    def company_s(self, value):
        self.companyS = value

    @property
    def company_s_srch(self):
        return self.companySSrch

    @company_s_srch.setter
    def company_s_srch(self, value):
        self.companySSrch = value

    @property
    def company_m(self):
        return self.companyM

    @company_m.setter
    def company_m(self, value):
        self.companyM = value

    @property
    def company_m_srch(self):
        return self.companyMSrch

    @company_m_srch.setter
    def company_m_srch(self, value):
        self.companyMSrch = value

    @property
    def p_src(self):
        return self.src

    @p_src.setter
    def p_src(self, value):
        self.src = value

    @property
    def case_id(self):
        return self.caseId

    @case_id.setter
    def case_id(self, value):
        self.caseId = value

    @property
    def sme_score(self):
        return self.smeScore

    @sme_score.setter
    def sme_score(self, value):
        self.smeScore = value

    @property
    def sub_score(self):
        return self.subScore

    @sub_score.setter
    def sub_score(self, value):
        self.subScore = value

    @property
    def srch_t(self):
        return self.srchT

    @srch_t.setter
    def srch_t(self, value):
        self.srchT = value

    @property
    def srch_iter(self):
        return self.srchIter

    @srch_iter.setter
    def srch_iter(self, value):
        self.srchIter = value

    @property
    def p_note(self):
        return self.note

    @p_note.setter
    def p_note(self, value):
        self.note = value

    @property
    def is_single_res(self):
        return self.isSingleRes

    @is_single_res.setter
    def is_single_res(self, value):
        self.isSingleRes = value

if __name__ == '__main__':
    dto = DcmResDTO()
    print(dto.__dict__)

