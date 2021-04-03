# -*- coding: utf-8 -*-

"""
@date: 2020/7/14 下午8:34
@file: processor.py
@author: zj
@description: 
"""

from ..anno import build_anno
from ..util.logger import setup_logger


class Processor(object):
    """
    The labeled data is processed to create training data with specified format
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
            logger.info('Processing original data')
        output_data = self.parser.process()
        if verbose:
            logger.info('Save data in specified format')
        self.creator.save(output_data)
        if verbose:
            logger.info('Finish!!!')
