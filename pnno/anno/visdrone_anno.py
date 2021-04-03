# -*- coding: utf-8 -*-

"""
@date: 2020/7/17 下午7:40
@file: visdrone_anno.py
@author: zj
@description: 
"""

import os
import glob
import numpy as np
import cv2

from pnno.anno import registry
from pnno.anno.base_anno import BaseAnno
from pnno.util.misc import check_image_label, check_input_output_folder
from pnno.util.logger import setup_logger


@registry.ANNOS.register('visdrone')
class VisDroneAnno(BaseAnno):
    """
    [VisDrone](http://aiskyeye.com/) data set for UAV target detection training
    Download address: [VisDrone/VisDrone-Dataset](https://github.com/VisDrone/VisDrone-Dataset)
    Data storage format:
    root/
        images/
        annotations/
    The annotation file (. Txt) corresponds to the image one by one, and each line represents a annotation object, with a total of 8 fields
    refer to [Object Detection in Images](http://aiskyeye.com/evaluate/results-format/). The format is as follows
    <bbox_left>,<bbox_top>,<bbox_width>,<bbox_height>,<score>,<object_category>,<truncation>,<occlusion>
    Ignore in category ignored-regions/others
    """

    classmap = {'ignored-regions': 0, 'pedestrian': 1, 'people': 2, 'bicycle': 3, 'car': 4, 'van': 5, 'truck': 6,
                'tricycle': 7, 'awning-tricycle': 8, 'bus': 9, 'motor': 10, 'others': 11}

    def __init__(self, cfg):
        self.name = cfg.VISDRONE.NAME
        self.img_extension = cfg.VISDRONE.IMG_EXTENSION
        self.anno_extension = cfg.VISDRONE.ANNO_EXTENSION

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

    def get_class_name(self, value):
        return [k for k, v in self.classmap.items() if v == value][0]

    def create_anno(self, anno_line) -> dict:
        # ignore ignored-regions/others
        xmin, ymin, width, height, _, cate = anno_line[:6].astype(np.int)
        xmax = xmin + width
        ymax = ymin + height
        if cate == 0 or cate == 11:
            return dict()
        name = self.get_class_name(cate)
        return {'name': name, 'bndbox': [xmin, ymin, xmax, ymax]}

    def parse_anno(self, img_path, anno_path) -> dict:
        """
        Parse vistrone image and annotation file
        :returns: anno_obj
        """
        anno_obj = dict()

        img = cv2.imread(img_path)
        if len(img.shape) == 3:
            h, w, d = img.shape[:3]
            anno_obj['size'] = (w, h, d)
        else:
            h, w = img.shape[:2]
            anno_obj['size'] = (w, h, 1)

        anno_array = np.loadtxt(anno_path, dtype=np.str, delimiter=',')
        objects = list()
        if len(anno_array.shape) == 1:
            # Just one annotation object
            obj = self.create_anno(anno_array)
            if obj:
                objects.append(obj)
        else:
            for anno_line in anno_array:
                obj = self.create_anno(anno_line)
                if obj:
                    objects.append(obj)
        if len(objects) == 0:
            return dict()
        anno_obj['objects'] = objects
        return anno_obj

    def process(self) -> dict:
        src_dir = self.src_dir
        image_folder = self.image_folder
        label_folder = self.label_folder
        img_extension = self.img_extension
        anno_extension = self.anno_extension
        verbose = self.verbose
        logger = self.logger

        image_dir, label_dir = check_input_output_folder(src_dir, image_folder, label_folder, is_input=True)

        img_path_list = sorted(glob.glob(os.path.join(image_dir, '*' + img_extension)))
        anno_path_list = sorted(glob.glob(os.path.join(label_dir, '*' + anno_extension)))
        check_image_label(img_path_list, anno_path_list)

        anno_data = dict()
        for i, (img_path, anno_path) in enumerate(zip(img_path_list, anno_path_list), 1):
            if verbose:
                logger.info('parse {}'.format(anno_path))

            anno_obj = self.parse_anno(img_path, anno_path)
            if anno_obj:
                anno_data[img_path] = anno_obj
            else:
                self.logger.info('{} is a annotation object that only contains targets whose annotation type is ignored regions or others'.format(img_path))

        return {'classmap': self.classmap, 'anno_data': anno_data}

    def save(self, input_data):
        super(VisDroneAnno, self).save(input_data)
        pass
