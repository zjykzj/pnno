# -*- coding: utf-8 -*-

"""
@date: 2020/7/13 下午4:11
@file: utility.py
@author: zj
@description: 常用操作
"""

import json
import xmltodict


# xml转json
def xml_to_json(xml_str):
    # parse是的xml解析器
    xml_parse = xmltodict.parse(xml_str)
    # json库dumps()是将dict转化成json格式,loads()是将json转化成dict格式。
    # dumps()方法的ident=1,格式化json
    json_str = json.dumps(xml_parse, indent=1)
    return json_str


# json转xml
def json_to_xml(json_str, file_name=None):
    assert file_name is not None
    # xmltodict库的unparse()json转xml
    # 参数pretty 是格式化xml
    xml_str = xmltodict.unparse(json_str, output=file_name, pretty=1)
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
