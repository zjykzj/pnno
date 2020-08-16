# -*- coding: utf-8 -*-

"""
@date: 2020/8/16 上午10:14
@file: test_label_anno.py
@author: zj
@description: 
"""

from pnno.config import cfg
from pnno.anno.labelimg_anno import LabelImgAnno
from pnno.util.utility import xml_to_dict
import shutil


class TestLabelAnno(object):

    def test_process(self):
        config_file = 'tests/labelimg_anno_test/process_config.yaml'
        cfg.merge_from_file(config_file)
        cfg.freeze()

        labelImgAnno = LabelImgAnno(cfg)
        output_data = labelImgAnno.process()
        print(output_data)

        real_data = self.get_output_data()

        assert output_data == real_data

    def test_save(self):
        config_file = 'tests/labelimg_anno_test/save_config.yaml'
        cfg.merge_from_file(config_file)
        cfg.freeze()

        labelImgAnno = LabelImgAnno(cfg)
        output_data = self.get_output_data()
        labelImgAnno.save(output_data)

        input_data = xml_to_dict('tests/labelimg_anno_test/input_data/lena.xml')
        output_data = xml_to_dict('tests/labelimg_anno_test/output_data/labels/lena.xml')

        assert input_data == output_data

        shutil.rmtree('tests/labelimg_anno_test/output_data')

    def get_output_data(self):
        """
        {'classmap': {'box': 0},
        'anno_data': {'tests/labelimg_anno_test/input_data/lena.jpg':
        {'size': (512, 512), 'objects': [{'name': 'box', 'bndbox': [100, 100, 400, 400]}]}}}
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
