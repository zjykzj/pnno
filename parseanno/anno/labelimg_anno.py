# -*- coding: utf-8 -*-

"""
@date: 2020/7/15 下午7:04
@file: labelimg_anno.py
@author: zj
@description: 
"""

import os
import glob

from parseanno.utils.utility import check
from parseanno.utils.parse_voc_xml import ParseVocXml
from parseanno.anno import registry
from parseanno.anno.base_anno import BaseAnno

from parseanno.utils.logger import setup_logger


@registry.ANNOS.register('labelimg')
class LabelImgAnno(BaseAnno):
    """
    使用LabelImg标注的数据集，其图像和标注文件放置于同一目录下。比如1.txt/1.xml/2.txt/2.xml/...
    图像默认为png文件
    标注文件为PASCAL VOC格式的xml文件
    """

    def __init__(self, cfg):
        self.src_dir = cfg.LABELIMG.SRC_DIR
        self.img_extension = cfg.LABELIMG.IMG_EXTENSION
        self.anno_extension = cfg.LABELIMG.ANNO_EXTENSION
        self.verbose = cfg.ANNO.VERBOSE

        self.classmap = dict()

        self.logger = setup_logger(__name__)

    def _parse_classmap(self, objects):
        """
        解析类名，添加对应的数字
        """
        for obj in objects:
            name = obj['name']

            if name not in self.classmap.keys():
                self.classmap[name] = len(self.classmap.keys())

    def process(self) -> dict:
        src_dir = self.src_dir
        img_extension = self.img_extension
        anno_extension = self.anno_extension
        verbose = self.verbose

        if not os.path.isdir(src_dir):
            raise ValueError('{}不是文件夹'.format(src_dir))

        img_path_list = sorted(glob.glob(os.path.join(src_dir, '*' + img_extension)))
        anno_path_list = sorted(glob.glob(os.path.join(src_dir, '*' + anno_extension)))
        check(img_path_list, anno_path_list)

        anno_data = dict()
        for i, (img_path, anno_path) in enumerate(zip(img_path_list, anno_path_list), 1):
            if verbose:
                self.logger.info('解析{}'.format(anno_path))
            parser = ParseVocXml(anno_path)

            anno_obj = dict()
            anno_obj['size'] = parser.get_width_height()
            anno_obj['objects'] = parser.get_objects()
            anno_data[img_path] = anno_obj

            self._parse_classmap(anno_obj['objects'])

        return {'classmap': self.classmap, 'anno_data': anno_data}

    def save(self, anno_data):
        super(LabelImgAnno, self).save(anno_data)
        pass
