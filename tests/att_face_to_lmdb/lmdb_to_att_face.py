# -*- coding: utf-8 -*-

"""
@date: 2021/4/3 下午8:40
@file: att_face_to_lmdb.py
@author: zj
@description: 
"""

import os
from PIL import Image

from lmdb_dataset import LMDBDataset


def lmdb_to_imagefolder():
    res_root = 'res_png'
    if not os.path.exists(res_root):
        os.makedirs(res_root)

    root = './train.lmdb'
    data_set = LMDBDataset(root)
    classes = data_set.get_classes()
    print('classes:', classes)
    for class_name in classes:
        class_path = os.path.join(res_root, class_name)
        if not os.path.exists(class_path):
            os.makedirs(class_path)

    for index, (image, target) in enumerate(iter(data_set)):
        print(image.size, target, classes[target])

        class_dir = os.path.join(res_root, classes[target])
        if not os.path.exists(class_dir):
            raise ValueError(f"{class_dir} doesn't exists")
        number = len(os.listdir(class_dir))

        img_path = os.path.join(class_dir, f'{number}.png')
        print(img_path)
        image.save(img_path)


if __name__ == '__main__':
    lmdb_to_imagefolder()
