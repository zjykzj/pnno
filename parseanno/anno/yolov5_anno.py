# -*- coding: utf-8 -*-

"""
@date: 2020/7/14 下午7:39
@file: yolov5_anno.py
@author: zj
@description: 
"""

import os
import copy
import shutil
import cv2
import numpy as np
import json

from parseanno.utils.utility import get_file_name, check_dst_folder
from parseanno.anno import registry
from parseanno.anno.base_anno import BaseAnno
from parseanno.utils.logger import setup_logger


@registry.ANNOS.register('yolov5')
class YoLoV5Anno(BaseAnno):
    """
    创建[ultralytics/yolov5](https://github.com/ultralytics/yolov5)训练所需数据集
    其图像和标注文件排列如下：
    ├── ocr-task3-detect
       ├── images
            ├── 201.png
            ├── 202.png
       └── labels
            ├── 201.txt
            ├── 202.txt
    标注文件格式如下：
    class_num x_center y_center width height
    class_num表示类别，从0开始
    x_center/y_center/width/height使用相对图像宽高的坐标
    示例如下：
    0 0.110547 0.051621 0.154554 0.023163

    额外保存一个classmap.txt，保存class_num和对应类名
    """

    def __init__(self, cfg):
        self.img_extension = cfg.YOLOV5.IMG_EXTENSION
        self.anno_extension = cfg.YOLOV5.ANNO_EXTENSION
        self.save_classmap = cfg.ANNO.SAVE_CLASSMAP
        self.verbose = cfg.ANNO.VERBOSE

        self.logger = setup_logger(__name__)

        if cfg.ANNO.CREATOR == cfg.YOLOV5.NAME:
            # 转换成Yolov5数据格式
            dst_dir = cfg.YOLOV5.DST_DIR
            dst_img_dir, dst_label_dir = check_dst_folder(dst_dir, cfg.OUTPUT.IMAGE_FOLDER, cfg.OUTPUT.LABEL_FOLDER)

            self.dst_dir = dst_dir
            self.dst_img_dir = dst_img_dir
            self.dst_label_dir = dst_label_dir

    def xyxy_2_xywh(self, bndbox, size):
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

    def process(self) -> dict:
        pass

    def save(self, anno_data):
        super(YoLoV5Anno, self).save(anno_data)

        dst_dir = self.dst_dir
        dst_img_dir = self.dst_img_dir
        dst_label_dir = self.dst_label_dir
        save_classmap = self.save_classmap
        verbose = self.verbose

        classmap = anno_data['classmap']

        for i, (img_path, anno_obj) in enumerate(anno_data['anno_data'].items(), 1):
            img_name = get_file_name(img_path)
            if verbose:
                self.logger.info('保存{}'.format(img_name))

            size = anno_obj['size']
            objects = anno_obj['objects']

            label_list = list()
            for obj in objects:
                name = obj['name']
                bndbox = obj['bndbox']

                x_center, y_center, box_w, box_h = self.xyxy_2_xywh(bndbox, size)
                label_list.append([classmap[name], x_center, y_center, box_w, box_h])
            # 保存
            img = cv2.imread(img_path)
            dst_img_path = os.path.join(dst_img_dir, img_name + self.img_extension)
            cv2.imwrite(dst_img_path, img)

            dst_label_path = os.path.join(dst_label_dir, img_name + self.anno_extension)
            np.savetxt(dst_label_path, label_list, fmt='%d %.6f %.6f %.6f %.6f', delimiter=' ')
        if save_classmap:
            classmap_path = os.path.join(dst_dir, 'classmap.json')
            with open(classmap_path, 'w') as f:
                json.dump(classmap, f)
        if verbose:
            self.logger.info(__name__ + ' done')
