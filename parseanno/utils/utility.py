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


def is_dir(src_dir):
    """
    判断是否是目录
    """
    if not os.path.isdir(src_dir):
        raise ValueError('{}不是目录'.format(src_dir))


def get_file_name(file_path):
    """
    解析文件名
    """
    return os.path.splitext(os.path.split(file_path)[1])[0]


def get_classmap(anno_data, classmap):
    """
    从中间格式标注数据中找到classmap
    :param anno_list: [{'size':(width, height), 'objects':[{'name': '', 'bndbox':[xmin,ymin,xmax,ymax]}, ...]}, ...]
    :param classmap: 已有类名和数字对应图
    :return: {'a': 0, 'b':1 ,...}
    """
    for _, anno_obj in anno_data.items():
        objects = anno_obj['objects']
        for obj in objects:
            name = obj['name']
            if name not in classmap.keys():
                classmap[name] = len(classmap.keys())
    return classmap


def check(img_path_list, anno_path_list):
    """
    检查图像文件和标注文件是否一一对应
    """
    assert len(img_path_list) == len(anno_path_list), \
        '图像文件数：{} - 标注文件数：{}'.format(len(img_path_list), len(anno_path_list))

    for img_path, anno_path in zip(img_path_list, anno_path_list):
        img_name = get_file_name(img_path)
        anno_name = get_file_name(anno_path)

        if img_name != anno_name:
            raise ValueError('{}和{}不对应'.format(img_path, anno_path))
