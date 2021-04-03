# -*- coding: utf-8 -*-

"""
@date: 2020/7/26 上午10:36
@file: misc.py
@author: zj
@description: 
"""

from .. import __version__
import os


def get_version():
    return __version__


def is_dir(src_dir):
    """
    Determine whether it is a directory
    """
    if not os.path.isdir(src_dir):
        raise ValueError('{} is not a directory'.format(src_dir))


def get_img_name(img_path):
    """
    Resolve the image name. like /path/to/lena.jpg get lena
    """
    return os.path.splitext(os.path.split(img_path)[1])[0]


def parse_img_path(img_path):
    """
    Analyze the image path, get the image folder, file name, image name and image suffix
    like /path/to/input_data/lena.jpg，then return
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
    Find classmap from middle format annotation data
    :param anno_list: [{'size':(width, height), 'objects':[{'name': '', 'bndbox':[xmin,ymin,xmax,ymax]}, ...]}, ...]
    :param classmap: Existing class name and number map
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
    Check whether the image file corresponds to the annotation file one by one
    """
    assert len(img_path_list) == len(anno_path_list), \
        'Number of image files: {} - Number of label files: {}'.format(len(img_path_list), len(anno_path_list))

    for img_path, anno_path in zip(img_path_list, anno_path_list):
        img_name = get_img_name(img_path)
        anno_name = get_img_name(anno_path)

        if img_name != anno_name:
            raise ValueError('{} and {} do not correspond'.format(img_path, anno_path))


def check_input_output_folder(dir: str, image_folder: str, label_folder: str, is_input=True):
    """
    Check the root directory as well as the image and label folders
    Check input directory
    1. Check whether the root path exists: if not, throw an exception
    2. Check whether the image folder exists: if not, throw an exception
    3. Check whether the label folder exists: if not, throw an exception
    Check output directory
    1. Check whether the root path exists: if not, create a new one
    2. Check whether the image folder exists: if so, throw an exception
    3. Check whether the label folder exists: if so, throw an exception
    :param dir: Root path
    :param image_folder: Image folder name
    :param label_folder: Label folder name
    :return: Return the image folder path and label folder path
    """
    assert isinstance(dir, str) and isinstance(image_folder, str) and isinstance(label_folder, str)

    img_dir = os.path.join(dir, image_folder)
    label_dir = os.path.join(dir, label_folder)

    if is_input:
        if not os.path.exists(dir) or not os.path.exists(img_dir) or not os.path.exists(label_dir):
            raise ValueError('Please check whether the input data is correct')
    else:

        if not os.path.exists(dir):
            os.mkdir(dir)

        if os.path.exists(img_dir):
            raise ValueError('{} already exists'.format(img_dir))
        os.mkdir(img_dir)

        if img_dir != label_dir:
            if os.path.exists(label_dir):
                raise ValueError('{} already exists'.format(label_dir))
            os.mkdir(label_dir)

    return img_dir, label_dir


def parse_classmap(classmap: dict, objects: list):
    """
    Parse the class name and add the corresponding number
    """
    assert isinstance(classmap, dict) and isinstance(objects, list)

    for obj in objects:
        name = obj['name']

        if name not in classmap.keys():
            classmap[name] = len(classmap.keys())
