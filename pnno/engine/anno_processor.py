# -*- coding: utf-8 -*-

"""
@date: 2020/7/14 下午8:34
@file: anno_processor.py
@author: zj
@description: 
"""

import os
import glob

from pnno.anno import build_anno
from pnno.util.logger import setup_logger


class AnnoProcessor(object):
    """
    对标注数据进行处理，创建指定格式的训练数据
    """

    def __init__(self, cfg):
        self.parser = build_anno(cfg.ANNO.PARSER, cfg)
        self.creator = build_anno(cfg.ANNO.CREATOR, cfg)

        self.logger = setup_logger(__name__)
        self.verbose = cfg.ANNO.VERBOSE

    def process(self):
        verbose = self.verbose
        logger = self.logger

        if verbose:
            logger.info('处理原始标注数据')
        output_data = self.parser.process()
        if verbose:
            logger.info('保存指定格式数据')
        self.creator.save(output_data)
        if verbose:
            logger.info('完成')
