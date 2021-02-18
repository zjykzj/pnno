# -*- coding: utf-8 -*-

"""
@date: 2020/7/15 下午1:29
@file: uav123.py
@author: zj
@description: 
"""

import os
import glob
import shutil
import json
import numpy as np
from itertools import groupby

img_dir = '/home/zj/work/南航无人机/data/UAV123/data_seq/UAV123'
anno_dir = '/home/zj/work/南航无人机/data/UAV123/anno/UAV123'
dst_anno_dir = '/home/zj/work/南航无人机/data/UAV123/anno/UAV123_anno'

dst_dir = '/home/zj/work/南航无人机/data/UAV123_deal'

merge_dict = {'bird1': 3, 'car1': 3, 'car6': 5, 'car8': 2, 'car16': 2, 'group1': 4, 'group2': 3, 'group3': 4,
              'person2': 2, 'person4': 2, 'person5': 2, 'person7': 2, 'person8': 2, 'person12': 2, 'person14': 3,
              'person17': 2, 'person19': 3, 'truck4': 2, 'uav1': 3}


def merge_anno(anno_dir, dst_dir, merge_dict):
    """
    解析标注文件夹，合并同一图像目录下的标注信息
    """
    # 读取所有txt文件
    anno_txt_list = glob.glob(os.path.join(anno_dir, '*.txt'))

    for anno_txt_path in anno_txt_list:
        # 遍历所有txt文件，直接复制不需要合并的标注
        name = os.path.splitext(os.path.split(anno_txt_path)[1])[0]
        name_list = name.split('_')
        if len(name_list) == 1 or name_list[1] == 's':
            # 不需要合并，那么直接复制即可
            dst_txt_path = os.path.join(dst_dir, name + '.txt')
            shutil.copyfile(anno_txt_path, dst_txt_path)
    print('begin merge')
    for name, v in merge_dict.items():
        print(name)
        label_list = list()
        for i in range(1, v + 1):
            anno_txt_path = os.path.join(anno_dir, '{}_{}.txt'.format(name, i))
            anno_list = np.loadtxt(anno_txt_path, dtype=np.str, delimiter=',')
            label_list.extend(anno_list)
        dst_txt_path = os.path.join(dst_dir, '{}.txt'.format(name))
        np.savetxt(dst_txt_path, label_list, fmt='%s', delimiter=',')
    print('done')


def process(img_dir, anno_dir, dst_dir):
    dst_img_dir = os.path.join(dst_dir, 'images')
    dst_label_dir = os.path.join(dst_dir, 'labels')
    if os.path.exists(dst_img_dir):
        shutil.rmtree(dst_img_dir)
    if os.path.exists(dst_label_dir):
        shutil.rmtree(dst_label_dir)
    os.mkdir(dst_img_dir)
    os.mkdir(dst_label_dir)

    img_folder_list = sorted(os.listdir(img_dir))
    anno_txt_list = sorted(os.listdir(anno_dir))

    for i, (img_folder_name, anno_txt_name) in enumerate(zip(img_folder_list, anno_txt_list), 1):
        img_folder_path = os.path.join(img_dir, img_folder_name)
        img_full_name_list = sorted(os.listdir(img_folder_path))

        anno_txt_path = os.path.join(anno_dir, anno_txt_name)
        label_array = np.loadtxt(anno_txt_path, dtype=np.str, delimiter=',')

        print(img_folder_name, '#' * 10, anno_txt_name)
        # 遍历每个图像和对应标注
        num_img = len(img_full_name_list)
        num_label = len(label_array)
        num = num_img if num_img < num_label else num_label
        for j in range(num):
            label_list = label_array[j]
            img_full_name = img_full_name_list[j]

            if 'NaN' in label_list:
                # 不存在标注，跳过
                continue
            src_img_path = os.path.join(img_dir, img_folder_name, img_full_name)
            dst_img_path = os.path.join(dst_img_dir, '{}_{}'.format(img_folder_name, img_full_name))
            shutil.copyfile(src_img_path, dst_img_path)

            img_name, _ = os.path.splitext(img_full_name)
            dst_label_path = os.path.join(dst_label_dir, '{}_{}.txt'.format(img_folder_name, img_name))
            np.savetxt(dst_label_path, [label_list], delimiter=' ', fmt='%s')
            print(j, img_name)
        print('*' * 10, img_folder_name)
    print('done')


def convert_anno(src_anno_dir, dst_anno_dir):
    """
    将UAV123标注(xmin/ymin/width/height)转换成KITTI标注(xmin/ymin/xmax/ymax)
    """
    label_list = sorted(os.listdir(src_anno_dir))

    classmap = list()
    for i, label_full_name in enumerate(label_list, 1):
        src_anno_path = os.path.join(src_anno_dir, label_full_name)
        dst_anno_path = os.path.join(dst_anno_dir, label_full_name)

        src_label_array = np.loadtxt(src_anno_path, dtype=np.str, delimiter=' ')
        if len(src_label_array) != 4:
            raise ValueError('{}有多个标注'.format(src_anno_path))
        xmin, ymin, width, height = src_label_array.astype(np.int)
        xmax = xmin + width
        ymax = ymin + height

        label_name = os.path.splitext(label_full_name)[0]
        classname = [''.join(list(g)) for k, g in groupby(label_name, key=lambda x: x.isdigit())][0]
        if classname not in classmap:
            classmap.append(classname)

        dst_label_list = [classname, 0, 0, 0, xmin, ymin, xmax, ymax, 0, 0, 0, 0, 0, 0, 0]
        np.savetxt(dst_anno_path, [dst_label_list], fmt='%s', delimiter=' ')
        print(i, label_full_name)
    print('done')
    print(classmap)
    print()
    classmap_path = os.path.join(dst_anno_dir, 'classmap.json')
    with open(classmap_path, 'w') as f:
        json.dump(classmap, f)


if __name__ == '__main__':
    # merge_anno(anno_dir, dst_anno_dir, merge_dict)
    # process(img_dir, dst_anno_dir, dst_dir)

    src_anno_dir = '/home/zj/work/南航无人机/data/UAV123_deal/labels'
    kitti_anno_dir = '/home/zj/work/南航无人机/data/UAV123_deal/labels_kitti'
    convert_anno(src_anno_dir, kitti_anno_dir)
