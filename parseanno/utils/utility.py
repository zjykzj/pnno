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
