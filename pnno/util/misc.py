# -*- coding: utf-8 -*-

"""
@date: 2020/7/26 上午10:36
@file: misc.py
@author: zj
@description: 
"""

import pnno
import cv2
import os
import glob


def get_version():
    return pnno.__version__


def is_dir(src_dir):
    """
    判断是否是目录
    """
    if not os.path.isdir(src_dir):
        raise ValueError('{}不是目录'.format(src_dir))


def get_img_name(img_path):
    """
    解析图像名。比如/path/to/lena.jpg得到lena
    """
    return os.path.splitext(os.path.split(img_path)[1])[0]


def parse_img_path(img_path):
    """
    解析图像路径，得到图像所在文件夹，文件名，图像名和图像后缀
    比如/path/to/input_data/lena.jpg，则返回
    ['input_data', 'lena.jpg', 'lena', '.jpg']
    """
    base_name = os.path.basename(img_path)
    dir_name = os.path.dirname(img_path)

    folder = os.path.basename(dir_name)
    file_name = base_name
    img_name, img_extension = os.path.splitext(base_name)

    return [folder, file_name, img_name, img_extension]


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


def check_image_label(img_path_list, anno_path_list):
    """
    检查图像文件和标注文件是否一一对应
    """
    assert len(img_path_list) == len(anno_path_list), \
        '图像文件数：{} - 标注文件数：{}'.format(len(img_path_list), len(anno_path_list))

    for img_path, anno_path in zip(img_path_list, anno_path_list):
        img_name = get_img_name(img_path)
        anno_name = get_img_name(anno_path)

        if img_name != anno_name:
            raise ValueError('{}和{}不对应'.format(img_path, anno_path))


def check_input_output_folder(dir: str, image_folder: str, label_folder: str, is_input=True):
    """
    检查根目录以及图像和标签文件夹
    检查输入目录
    1. 检查根路径是否存在：如果不存在，抛出异常
    2. 检查图像文件夹是否存在：如果不存在，抛出异常
    3. 检查标签文件夹是否存在：如果不存在，抛出异常
    检查输出目录
    1. 检查根路径是否存在：如果不存在，则新建
    2. 检查图像文件夹是否存在：如果存在，抛出异常
    3. 检查标签文件夹是否存在：如果存在，抛出异常
    :param dir: 根路径
    :param image_folder: 图像文件夹名
    :param label_folder: 标签文件夹名
    :return: 返回图像文件夹路径以及标签文件夹路径
    """
    assert isinstance(dir, str) and isinstance(image_folder, str) and isinstance(label_folder, str)

    img_dir = os.path.join(dir, image_folder)
    label_dir = os.path.join(dir, label_folder)

    if is_input:
        if not os.path.exists(dir) or not os.path.exists(img_dir) or not os.path.exists(label_dir):
            raise ValueError('请检查输入数据是否正确')
    else:

        if not os.path.exists(dir):
            os.mkdir(dir)

        if os.path.exists(img_dir):
            raise ValueError('{}已存在'.format(img_dir))
        os.mkdir(img_dir)

        if img_dir != label_dir:
            if os.path.exists(label_dir):
                raise ValueError('{}已存在'.format(label_dir))
            os.mkdir(label_dir)

    return img_dir, label_dir


def parse_classmap(classmap: dict, objects: list):
    """
    解析类名，添加对应的数字
    """
    assert isinstance(classmap, dict) and isinstance(objects, list)

    for obj in objects:
        name = obj['name']

        if name not in classmap.keys():
            classmap[name] = len(classmap.keys())
