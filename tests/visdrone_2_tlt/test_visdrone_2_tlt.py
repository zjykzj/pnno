# -*- coding: utf-8 -*-

"""
@date: 2020/8/8 下午4:16
@file: test_visdrone_2_tlt.py
@author: zj
@description: 
"""

from pnno.config import cfg
from pnno.engine import AnnoProcessor


class TestVisdrone2Tlt():

    def test(self):
        config_file = 'configs/visdrone_2_tlt.yaml'
        cfg.merge_from_file(config_file)
        cfg.freeze()

        processor = AnnoProcessor(cfg)
        processor.process()
