# -*- coding: utf-8 -*-

"""
@date: 2020/8/16 下午3:54
@file: test_yolov5_anno.py
@author: zj
@description: 
"""

import numpy as np
import shutil

from pnno.config import cfg
from pnno.anno.yolov5_anno import YoLoV5Anno
from pnno.util.utility import xml_to_dict


class TestYoLoV5Anno(object):

    def test_save(self):
        config_file = 'tests/yolov5_anno_test/save_config.yaml'
        cfg.merge_from_file(config_file)
        cfg.freeze()

        labelImgAnno = YoLoV5Anno(cfg)
        output_data = self.get_output_data()
        labelImgAnno.save(output_data)

        input_data = np.loadtxt('tests/yolov5_anno_test/input_data/labels/lena.txt', dtype=np.float, delimiter=' ')
        output_data = np.loadtxt('tests/yolov5_anno_test/output_data/labels/lena.txt', dtype=np.float, delimiter=' ')
        print(input_data)
        print(output_data)

        assert np.sum(input_data == output_data) == 1

        shutil.rmtree('tests/yolov5_anno_test/output_data')

    def get_output_data(self):
        """
        {'classmap': {'box': 0},
        'anno_data': {'tests/yolov5_anno_test/input_data/images/lena.jpg':
        {'size': (512, 512, 3), 'objects': [{'name': 'box', 'bndbox': [100, 100, 400, 400]}]}}}
        """
        classmap = {'box': 0}
        anno_data = {
            'tests/labelimg_anno_test/input_data/lena.jpg': {
                'size': (512, 512, 3),
                'objects': [{'name': 'box', 'bndbox': [100, 100, 400, 400]}]
            }
        }
        real_data = {
            'classmap': classmap,
            'anno_data': anno_data
        }

        return real_data
