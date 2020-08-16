# -*- coding: utf-8 -*-

"""
@date: 2020/8/16 上午10:14
@file: test_label_anno.py
@author: zj
@description: 
"""

import pytest

from pnno.config import cfg
from pnno.anno.labelimg_anno import LabelImgAnno


class TestLabelAnno(object):

    def test_process(self):
        config_file = 'tests/labelimg_anno_test/config.yaml'
        cfg.merge_from_file(config_file)
        cfg.freeze()

        labelImgAnno = LabelImgAnno(cfg)
        output_data = labelImgAnno.process()
        print(output_data)

        classmap = {'box': 0}
        anno_data = {
            'tests/labelimg_anno_test/input_data/lena.jpg': {
                'size': (512, 512),
                'objects': [{'name': 'box', 'bndbox': [100, 100, 400, 400]}]
            }
        }
        real_data = {
            'classmap': classmap,
            'anno_data': anno_data
        }

        assert output_data == real_data
