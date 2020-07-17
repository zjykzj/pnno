# -*- coding: utf-8 -*-

"""
@date: 2020/7/14 下午7:14
@file: parse_voc_xml.py
@author: zj
@description: 解析PASCAL VOC格式xml文件
"""

import os
import collections
import xml.etree.cElementTree as ET


class ParseVocXml(object):
    """
    解析单个xml文件
    """

    def __init__(self, xml_path):
        self.target = self.preprocess(xml_path)

    def preprocess(self, xml_path):
        if not os.path.exists(xml_path):
            raise ValueError('{}不存在'.format(xml_path))
        if not self.check_xml_suffix(xml_path):
            raise ValueError('{}不是xml文件'.format(xml_path))

        return self.parse_voc_xml(ET.parse(xml_path).getroot())

    def check_xml_suffix(self, xml_path):
        """
        检查是否是xml文件
        """
        suffix = os.path.splitext(os.path.split(xml_path)[1])[1]
        return True if suffix == '.xml' else False

    def parse_voc_xml(self, node):
        voc_dict = {}
        children = list(node)
        if children:
            def_dic = collections.defaultdict(list)
            for dc in map(self.parse_voc_xml, children):
                for ind, v in dc.items():
                    def_dic[ind].append(v)
            if node.tag == 'annotation':
                def_dic['object'] = [def_dic['object']]
            voc_dict = {
                node.tag:
                    {ind: v[0] if len(v) == 1 else v
                     for ind, v in def_dic.items()}
            }
        if node.text:
            text = node.text.strip()
            if not children:
                voc_dict[node.tag] = text
        return voc_dict

    def get_width_height(self):
        """
        :return: 图像宽高
        """
        size = self.target['annotation']['size']
        width = int(size['width'])
        height = int(size['height'])
        return (width, height)

    def get_objects(self, difficult=False):
        """
        返回所有标注对象
        @:param difficult: False - 不返回标记为difficult的边界框
        :return: [{'name': '', 'bndbox': [xmin, ymin, xmax, ymax]}]
        """
        object_list = self.target['annotation']['object']

        res_object_list = list()
        if object_list is not None:
            if not isinstance(object_list, list):
                # 仅包含单个目标
                object_list = [object_list]
            for object_dict in object_list:
                isdifficult = object_dict['difficult']
                if difficult == False and isdifficult == 1:
                    continue
                name = object_dict['name']
                bndbox = self.get_bndbox(object_dict['bndbox'])
                res_object_list.append({'name': name, 'bndbox': bndbox})
        return res_object_list

    def get_bndbox(self, bndbox):
        """
        :return: 返回左上角和右下角的坐标
        """
        xmin = int(bndbox['xmin'])
        ymin = int(bndbox['ymin'])
        xmax = int(bndbox['xmax'])
        ymax = int(bndbox['ymax'])

        if xmin > xmax:
            tmp = xmax
            xmax = xmin
            xmin = tmp
        if ymin > ymax:
            tmp = ymax
            ymax = ymin
            ymin = tmp
        return [xmin, ymin, xmax, ymax]
