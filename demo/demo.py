# -*- coding: utf-8 -*-

"""
@date: 2020/7/16 下午8:44
@file: demo.py
@author: zj
@description: 将LabelImg标注数据保存为YoLoV5指定数据集
"""

from parseanno.config import cfg
from parseanno.engine import AnnoProcessor


def main(cfg):
    processor = AnnoProcessor(cfg)
    processor.process()


if __name__ == '__main__':
    # config_file = '../configs/labelimg_2_yolov5.yaml'
    config_file = 'configs/visdrone_2_tlt.yaml'
    cfg.merge_from_file(config_file)
    cfg.freeze()

    main(cfg)
