# -*- coding: utf-8 -*-

"""
@date: 2020/7/17 下午7:29
@file: tlt_anno.py
@author: zj
@description: 
"""

import os
import cv2
import numpy as np
import json

from pnno.anno.base_anno import BaseAnno
from pnno.util.misc import get_img_name, check_input_output_folder
from pnno.anno import registry

from pnno.util.logger import setup_logger


@registry.ANNOS.register('tlt')
class TltAnno(BaseAnno):
    """
    [Nvidia TLT](https://docs.nvidia.com/metropolis/TLT/tlt-getting-started-guide/index.html)训练需要Kitti格式
    参考：
    [Object Detection Data Extension](https://github.com/NVIDIA/DIGITS/blob/v4.0.0-rc.3/digits/extensions/data/objectDetection/README.md)
    [Object Detection: About KITTI format #992](https://github.com/NVIDIA/DIGITS/issues/992)
    每行表示一个标注对象，共15个字段（空格隔开），第一个字段表示类名，第5-9表示xmin/ymin/xmax/ymax（浮点表示），其余设为0即可
    整体保存架构
    root/
        images/
            1.png
            2.png
        labels/
            1.txt
            2.txt
    """

    def __init__(self, cfg):
        self.name = cfg.TLT.NAME
        self.img_extension = cfg.TLT.IMG_EXTENSION
        self.anno_extension = cfg.TLT.ANNO_EXTENSION

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
        super(TltAnno, self).save(input_data)

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
                logger.info('保存{}'.format(img_name))

            size = anno_obj['size']
            objects = anno_obj['objects']

            label_list = list()
            for obj in objects:
                name = obj['name']
                bndbox = obj['bndbox']

                xmin, ymin, xmax, ymax = bndbox
                label_list.append([name, 0, 0, 0, xmin, ymin, xmax, ymax, 0, 0, 0, 0, 0, 0, 0])
            # 保存
            img = cv2.imread(img_path)
            dst_img_path = os.path.join(dst_image_dir, img_name + img_extension)
            cv2.imwrite(dst_img_path, img)

            dst_label_path = os.path.join(dst_label_dir, img_name + anno_extension)
            np.savetxt(dst_label_path, label_list, fmt='%s', delimiter=' ')

        if verbose:
            logger.info('保存classmap.json')
        classmap_path = os.path.join(dst_dir, 'classmap.json')
        with open(classmap_path, 'w') as f:
            json.dump(classmap, f)
        if verbose:
            print(__name__ + ' done')
