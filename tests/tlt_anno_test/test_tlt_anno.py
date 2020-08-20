# -*- coding: utf-8 -*-

"""
@date: 2020/8/20 下午9:09
@file: test_tlt_anno.py
@author: zj
@description: 
"""

import numpy as np
import shutil

from pnno.config import cfg
from pnno.anno.tlt_anno import TltAnno


class TestTltAnno(object):

    def test_save(self):
        config_file = 'tests/tlt_anno_test/save_config.yaml'
        cfg.merge_from_file(config_file)
        cfg.freeze()

        tltAnno = TltAnno(cfg)
        output_data = self.get_output_data()
        tltAnno.save(output_data)

        input_data = np.loadtxt('tests/tlt_anno_test/input_data/labels/lena.txt', dtype=np.str, delimiter=' ')
        output_data = np.loadtxt('tests/tlt_anno_test/output_data/labels/lena.txt', dtype=np.str, delimiter=' ')
        print(input_data)
        print(output_data)

        res = input_data == output_data
        print(res)
        assert np.sum(res) == 15

        shutil.rmtree('tests/tlt_anno_test/output_data')

    def get_output_data(self):
        """
        {'classmap': {'box': 6},
        'anno_data': {'tests/tlt_anno_test/input_data/lena.jpg':
        {'size': (512, 512, 3), 'objects': [{'name': 'box', 'bndbox': [100, 100, 400, 400]}]}}}
        """
        classmap = {'truck': 6}
        anno_data = {
            'tests/labelimg_anno_test/input_data/lena.jpg': {
                'size': (512, 512, 3),
                'objects': [{'name': 'truck', 'bndbox': [100, 100, 400, 400]}]
            }
        }
        real_data = {
            'classmap': classmap,
            'anno_data': anno_data
        }

        return real_data
