# -*- coding: utf-8 -*-

"""
@date: 2020/7/15 下午7:04
@file: labelimg_anno.py
@author: zj
@description: 
"""

import os
import cv2
import json
import glob
import numpy as np
from collections import OrderedDict

from pnno.util.utility import json_to_xml
from pnno.util.misc import check_image_label, get_file_name, parse_classmap, check_input_output_folder
from pnno.util.parse_voc_xml import ParseVocXml
from pnno.anno import registry
from pnno.anno.base_anno import BaseAnno

from pnno.util.logger import setup_logger


@registry.ANNOS.register('labelimg')
class LabelImgAnno(BaseAnno):
    """
    使用LabelImg标注的数据集。默认情况下：
    1. 图像为png格式
    2. 标注文件为PASCAL VOC格式的xml文件
    3. 其图像和标注文件放置于同一目录下。比如1.txt/1.xml/2.txt/2.xml/...
    关于LabelImg，参考：[tzutalin/labelImg](https://github.com/tzutalin/labelImg)
    """

    def __init__(self, cfg):
        self.name = cfg.LABELIMG.NAME
        self.img_extension = cfg.LABELIMG.IMG_EXTENSION
        self.anno_extension = cfg.LABELIMG.ANNO_EXTENSION

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
                logger.info('解析{}'.format(anno_path))
            parser = ParseVocXml(anno_path)

            anno_obj = dict()
            anno_obj['size'] = parser.get_width_height()
            anno_obj['objects'] = parser.get_objects()
            anno_data[img_path] = anno_obj

            parse_classmap(self.classmap, anno_obj['objects'])

        return {'classmap': self.classmap, 'anno_data': anno_data}

    def save(self, input_data):
        super(LabelImgAnno, self).save(input_data)

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
            img_name = get_file_name(img_path)
            if verbose:
                logger.info('保存{}'.format(img_name))

            root_dict = OrderedDict()
            # 根节点
            annotation_dict = OrderedDict()
            root_dict['annotation'] = annotation_dict

            annotation_dict['folder'] = 'image'
            annotation_dict['filename'] = img_name
            annotation_dict['path'] = img_path
            annotation_dict['source'] = OrderedDict({'database': 'Unknown'})

            size = anno_obj['size']
            if len(size.shape) == 2:
                h, w = size.shape[:2]
                d = 1
            else:
                h, w, d = size.shape[:3]
            size_dict = OrderedDict()
            size_dict['width'] = w
            size_dict['height'] = h
            size_dict['depth'] = d
            annotation_dict['size'] = size_dict

            annotation_dict['segmented'] = 0

            objects = anno_obj['objects']
            for obj in objects:
                name = obj['name']
                bndbox = obj['bndbox']
                xmin, ymin, xmax, ymax = bndbox

                object_dict = OrderedDict()
                object_dict['name'] = name
                object_dict['pose'] = 'Unspecified'
                object_dict['truncated'] = 0
                object_dict['difficult'] = 0

                bndbox_dict = OrderedDict()
                bndbox_dict['xmin'] = xmin
                bndbox_dict['ymin'] = ymin
                bndbox_dict['xmax'] = xmax
                bndbox_dict['ymax'] = ymax
                object_dict['bndbox'] = bndbox_dict
            # 保存
            img = cv2.imread(img_path)
            dst_img_path = os.path.join(dst_image_dir, img_name + img_extension)
            cv2.imwrite(dst_img_path, img)

            dst_label_path = os.path.join(dst_label_dir, img_name + anno_extension)
            annotation_json = json.dumps(annotation_dict, indent=1)
            json_to_xml(annotation_json, dst_label_path)

        if verbose:
            logger.info('保存classmap.json')
        classmap_path = os.path.join(dst_dir, 'classmap.json')
        with open(classmap_path, 'w') as f:
            json.dump(classmap, f)
        if verbose:
            logger.info(__name__ + ' done')
