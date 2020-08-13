# -*- coding: utf-8 -*-

"""
@date: 2020/7/16 下午8:17
@file: build.py
@author: zj
@description: 
"""

from pnno.anno import registry
from .yolov5_anno import YoLoV5Anno
from .labelimg_anno import LabelImgAnno
from .visdrone_anno import VisDroneAnno
from .tlt_anno import TltAnno


def build_anno(name, cfg):
    return registry.ANNOS[name](cfg)
