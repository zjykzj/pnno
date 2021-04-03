# -*- coding: utf-8 -*-

"""
@date: 2020/7/14 下午7:39
@file: yolov5_anno.py
@author: zj
@description: 
"""

import os
import cv2
import numpy as np
import json

from . import registry
from .base_anno import BaseAnno
from ..util.utility import xyxy_2_xywh
from ..util.misc import get_img_name, check_input_output_folder
from ..util.logger import setup_logger


@registry.ANNOS.register('yolov5')
class YoLoV5Anno(BaseAnno):
    """
    Create [ultralytics/yolov5](https://github.com/ultralytics/yolov5) training data set
    The image and annotation files are arranged as follows:
    ├── yolov5-dataset
        ── images
            ├── 201.png
            ├── 202.png
        ── labels
            ├── 201.txt
            ├── 202.txt
    The format of the annotation file is as follows:
    class_num x_center y_center width height
    class_num is the category, starting from 0
    x_center/y_center/width/height use coordinates relative to the width and height of the image
    Examples are as follows:
    0 0.110547 0.051621 0.154554 0.023163

    Save one extra classmap.txt , save class_num and the corresponding class name
    """

    def __init__(self, cfg):
        self.name = cfg.YOLOV5.NAME
        self.img_extension = cfg.YOLOV5.IMG_EXTENSION
        self.anno_extension = cfg.YOLOV5.ANNO_EXTENSION

        if cfg.ANNO.PARSER == self.name:
            self.src_dir = cfg.INPUT.DIR
            self.image_folder = cfg.INPUT.IMAGE_FOLDER
            self.label_folder = cfg.INPUT.LABEL_FOLDER
        if cfg.ANNO.CREATOR == self.name:
            self.dst_dir = cfg.OUTPUT.DIR
            self.image_folder = cfg.OUTPUT.IMAGE_FOLDER
            self.label_folder = cfg.OUTPUT.LABEL_FOLDER

        self.verbose = cfg.ANNO.VERBOSE

        self.logger = setup_logger(__name__)
        self.classmap = dict()

    def process(self) -> dict:
        pass

    def save(self, input_data):
        super(YoLoV5Anno, self).save(input_data)

        dst_dir = self.dst_dir
        image_folder = self.image_folder
        label_folder = self.label_folder
        img_extension = self.img_extension
        anno_extension = self.anno_extension
        verbose = self.verbose
        logger = self.logger

        dst_image_dir, dst_label_dir = check_input_output_folder(dst_dir, image_folder, label_folder, is_input=False)

        classmap = input_data['classmap']
        for i, (img_path, anno_obj) in enumerate(input_data['anno_data'].items(), 1):
            img_name = get_img_name(img_path)
            if verbose:
                logger.info('save {}'.format(img_name))

            size = anno_obj['size']
            objects = anno_obj['objects']

            label_list = list()
            for obj in objects:
                name = obj['name']
                bndbox = obj['bndbox']

                x_center, y_center, box_w, box_h = xyxy_2_xywh(bndbox, size)
                label_list.append([classmap[name], x_center, y_center, box_w, box_h])
            # 保存
            img = cv2.imread(img_path)
            dst_img_path = os.path.join(dst_image_dir, img_name + img_extension)
            cv2.imwrite(dst_img_path, img)

            dst_label_path = os.path.join(dst_label_dir, img_name + anno_extension)
            np.savetxt(dst_label_path, label_list, fmt='%d %.6f %.6f %.6f %.6f', delimiter=' ')

        if verbose:
            logger.info('save classmap.json')
        classmap_path = os.path.join(dst_dir, 'classmap.json')
        with open(classmap_path, 'w') as f:
            json.dump(classmap, f)
        if verbose:
            logger.info(__name__ + ' done')
