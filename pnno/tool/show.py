# -*- coding: utf-8 -*-

"""
@date: 2020/8/20 下午9:27
@file: show.py
@author: zj
@description: 
"""

import os
import cv2
import sys
import argparse
from ..util.misc import get_version


def show_image():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--img_file", default="", metavar="IMG_FILE", help="path to img file")
    parser.add_argument('-v', '--version', help='output version information', action="store_true")

    args = parser.parse_args()
    if args.version:
        print('pnno: v{}'.format(get_version()))
        sys.exit(0)

    if not args.img_file:
        parser.print_usage()
        sys.exit(1)

    img_path = args.img_file
    if not os.path.exists(img_path):
        parser._print_message(f'{img_path}不存在\n')
        exit(0)
    if not os.path.isfile(img_path):
        parser._print_message(f'{img_path}不是文件\n')
        exit(0)

    suffix = os.path.splitext(os.path.basename(img_path))[1]
    if suffix.lower() not in ['.jpg', '.png', '.tif', '.bmp']:
        parser._print_message('当前支持jpg/png/tif/bmp格式图像的显示\n')
        exit(0)

    img_name = os.path.basename(img_path)
    img = cv2.imread(img_path)
    cv2.namedWindow(img_name, cv2.WINDOW_NORMAL)
    cv2.imshow(img_name, img)
    cv2.waitKey(0)


if __name__ == '__main__':
    show_image()
