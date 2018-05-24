# -*- coding: utf-8 -*-


class BaseRequest:
    """
    base request vo
    """
    def convert_json_object(self, json_dict):
        for k, v in json_dict.items():
            self.__dict__[k] = v
        return self



