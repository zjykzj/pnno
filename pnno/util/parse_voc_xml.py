# -*- coding: utf-8 -*-

"""
@date: 2020/7/14 下午7:14
@file: parse_voc_xml.py
@author: zj
@description: Parsing Pascal VOC format XML file
"""

import os
import collections
import xml.etree.cElementTree as ET


class ParseVocXml(object):
    """
    Parsing a single xml file
    """

    def __init__(self, xml_path):
        self.target = self.preprocess(xml_path)

    def preprocess(self, xml_path):
        if not os.path.exists(xml_path):
            raise ValueError('{} does not exist'.format(xml_path))
        if not self.check_xml_suffix(xml_path):
            raise ValueError('{} is not an XML file'.format(xml_path))

        return self.parse_voc_xml(ET.parse(xml_path).getroot())

    def check_xml_suffix(self, xml_path):
        """
        Check if it is an XML file
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

    def get_size(self):
        """
        :return: Image width and height
        """
        size = self.target['annotation']['size']
        width = int(size['width'])
        height = int(size['height'])
        depth = int(size['depth'])
        return (width, height, depth)

    def get_objects(self, difficult=False):
        """
        Returns all dimension objects
        @:param difficult: False - Do not return bounding boxes marked as difficult
        :return: [{'name': '', 'bndbox': [xmin, ymin, xmax, ymax]}]
        """
        object_list = self.target['annotation']['object']

        res_object_list = list()
        if object_list is not None:
            if not isinstance(object_list, list):
                # Contains only a single target
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
        :return: Returns the coordinates of the upper left and lower right corners
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
