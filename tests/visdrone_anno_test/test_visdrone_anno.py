# -*- coding: utf-8 -*-

"""
@date: 2020/8/20 下午8:50
@file: test_visdrone_anno.py
@author: zj
@description: 
"""

from pnno.config import cfg
from pnno.anno.visdrone_anno import VisDroneAnno


class TestVisdroneAnno(object):

    def test_process(self):
        config_file = 'tests/visdrone_anno_test/process_config.yaml'
        cfg.merge_from_file(config_file)
        cfg.freeze()

        visdroneAnno = VisDroneAnno(cfg)
        output_data = visdroneAnno.process()
        print(output_data)

        real_data = self.get_output_data()

        assert output_data == real_data

    def get_output_data(self):
        """
        {'classmap': {'box': 0},
        'anno_data': {'tests/visdrone_anno_test/input_data/images/lena.jpg':
        {'size': (512, 512), 'objects': [{'name': 'box', 'bndbox': [100, 100, 400, 400]}]}}}
        """
        classmap = {'ignored-regions': 0, 'pedestrian': 1, 'people': 2, 'bicycle': 3, 'car': 4, 'van': 5, 'truck': 6,
                    'tricycle': 7, 'awning-tricycle': 8, 'bus': 9, 'motor': 10, 'others': 11}
        anno_data = {
            'tests/visdrone_anno_test/input_data/images/lena.jpg': {
                'size': (512, 512, 3),
                'objects': [{'name': 'truck', 'bndbox': [100, 100, 400, 400]}]
            }
        }
        real_data = {
            'classmap': classmap,
            'anno_data': anno_data
        }

        return real_data
