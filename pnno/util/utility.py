# -*- coding: utf-8 -*-

"""
@date: 2020/7/13 下午4:11
@file: utility.py
@author: zj
@description: 常用操作
"""

import json
import xmltodict


def xml_to_dict(xml_path):
    with open(xml_path, 'rb') as f:
        xml_parse = xmltodict.parse(f)
    return xml_parse


def dict_to_xml(data_dict, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        xml_str = xmltodict.unparse(data_dict, output=f, pretty=1)
    return xml_str


def xyxy_2_xywh(bndbox, size):
    """
    创建yolov5
    :param bndbox: [xmin, ymin, xmax, ymax]
    :param size: (width, height)
    :return: [x_center, y_center, width, height]相对格式
    """
    xmin, ymin, xmax, ymax = bndbox
    img_w, img_h = size[:2]

    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    width = xmax - xmin
    height = ymax - ymin

    x_center = 1.0 * x_center / img_w
    y_center = 1.0 * y_center / img_h
    width = 1.0 * width / img_w
    height = 1.0 * height / img_h

    return [x_center, y_center, width, height]
