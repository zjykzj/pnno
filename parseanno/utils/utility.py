# -*- coding: utf-8 -*-

"""
@date: 2020/7/13 下午4:11
@file: utility.py
@author: zj
@description: 常用操作
"""

import cv2
import os
import glob


def get_file_name(file_path):
    """
    解析文件名
    """
    return os.path.splitext(os.path.split(file_path)[1])[0]


def get_classmap(anno_data):
    """
    从中间格式标注数据中找到classmap
    :param anno_list: [{'size':(width, height), 'objects':[{'name': '', 'bndbox':[xmin,ymin,xmax,ymax]}, ...]}, ...]
    :return: {'a': 0, 'b':1 ,...}
    """
    classmap = dict()
    for _, anno_obj in anno_data.items():
        objects = anno_obj['objects']
        for obj in objects:
            name = obj['name']
            if name not in classmap.keys():
                classmap[name] = len(classmap.keys())
    return classmap
