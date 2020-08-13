# -*- coding: utf-8 -*-

"""
@date: 2020/8/8 下午3:48
@file: test_labelimg_2_yolov5.py
@author: zj
@description: 
"""

from pnno.config import cfg
from pnno.engine import AnnoProcessor


class TestLabelImg2YoloV5():

    def test(self):
        config_file = 'configs/labelimg_2_yolov5.yaml'
        cfg.merge_from_file(config_file)
        cfg.freeze()

        processor = AnnoProcessor(cfg)
        processor.process()
