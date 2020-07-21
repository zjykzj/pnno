# -*- coding: utf-8 -*-

"""
@date: 2020/7/14 下午8:34
@file: anno_processor.py
@author: zj
@description: 
"""

import os
import glob

from parseanno.anno import build_anno
from parseanno.utils.logger import setup_logger


class AnnoProcessor(object):
    """
    对标注数据进行处理，创建指定格式的训练数据
    """

    def __init__(self, cfg):
        self.parser = build_anno(cfg.ANNO.PARSER, cfg)
        self.creator = build_anno(cfg.ANNO.CREATOR, cfg)

        self.logger = setup_logger(__name__)

    def process(self):
        self.logger.info('处理原始标注数据')
        anno_data = self.parser.process()
        self.logger.info('保存指定格式数据')
        self.creator.save(anno_data)
        self.logger.info('完成')
