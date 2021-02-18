# -*- coding: utf-8 -*-

"""
@date: 2020/7/14 下午8:44
@file: img_format_converter.py
@author: zj
@description: 
"""

import os
import glob


def convert_jpeg_to_png(src_dir, dst_dir, verbose=True):
    """
    遍历src_dir路径下的所有.jpeg图像，转换成.png格式保存在dst_dir路径下
    """
    jpeg_img_list = glob.glob(os.path.join(src_dir, '*.jpg')) + glob.glob(os.path.join(src_dir, '*.jpeg'))

    for i, jpeg_img_path in enumerate(jpeg_img_list, 1):
        name = os.path.splitext(os.path.split(jpeg_img_list)[1])[0]

        img = cv2.imread(jpeg_img_path)
        png_img_path = os.path.join(dst_dir, name + ".png")
        cv2.imwrite(png_img_path, img)

        if verbose:
            print(i, name)
    if verbose:
        print(__name__, 'done')
