# -*- coding: utf-8 -*-

"""
@date: 2020/8/16 下午3:57
@file: create_data.py
@author: zj
@description: 
"""

import numpy as np

from pnno.util.utility import xyxy_2_xywh

if __name__ == '__main__':
    """
    创建yolov5标签数据
    """
    class_name = 'box'
    bndbox = [100, 100, 400, 400]
    # 图像大小
    size = (512, 512)

    xywh = xyxy_2_xywh(bndbox, size)
    x_center, y_center, width, height = xywh

    label_path = './input_data/labels/lena.txt'
    with open(label_path, 'w') as f:
        f.write(f'0 {x_center} {y_center} {width} {height}')
