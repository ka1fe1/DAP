# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Validator(metaclass=ABCMeta):
    """
    参数校验
    """

    @abstractmethod
    def validate(self):
        pass

