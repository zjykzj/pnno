# -*- coding: utf-8 -*-

"""
@date: 2020/7/15 下午7:05
@file: base_anno.py
@author: zj
@description: 
"""

from abc import ABCMeta, abstractmethod


class BaseAnno(metaclass=ABCMeta):

    @abstractmethod
    def process(self) -> dict:
        pass

    @abstractmethod
    def save(self, input_data: dict):
        assert isinstance(input_data, dict)
        pass
