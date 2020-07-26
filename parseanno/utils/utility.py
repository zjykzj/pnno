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


def check_dst_folder(dst_dir, dst_image_folder, dst_label_folder):
    """
    1. 检查结果根目录dst_dir是否存在：如果不存在，则新建
    2. 检查结果图像文件夹是否存在：如果存在，抛出异常
    3. 检查结果标签文件夹是否存在：如果存在，抛出异常
    :param dst_dir: 结果根目录
    :param dst_image_folder: 图像文件夹名
    :param dst_label_folder: 标签文件夹名
    :return: 返回结果图像文件夹路径以及结果标签文件夹路径
    """
    dst_img_dir = os.path.join(dst_dir, dst_image_folder)
    dst_label_dir = os.path.join(dst_dir, dst_label_folder)

    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    if os.path.exists(dst_img_dir):
        raise ValueError('{}已存在'.format(dst_img_dir))
    if os.path.exists(dst_label_dir):
        raise ValueError('{}已存在'.format(dst_label_dir))
    os.mkdir(dst_img_dir)
    os.mkdir(dst_label_dir)

    return dst_img_dir, dst_label_dir
