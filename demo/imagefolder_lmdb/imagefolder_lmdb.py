# -*- coding: utf-8 -*-

"""
@date: 2021/4/3 下午8:40
@file: imagefolder_lmdb.py
@author: zj
@description: 
"""

from pnno.config import cfg
from pnno.anno.build import build_anno


def imagefolder_to_lmdb():
    config_file = 'demo/imagefolder_lmdb/imagefolder_to_lmdb.yaml'
    cfg.merge_from_file(config_file)
    cfg.freeze()

    parser = build_anno(cfg.ANNO.PARSER, cfg)
    creator = build_anno(cfg.ANNO.CREATOR, cfg)

    input_data = parser.process()
    creator.save(input_data)


if __name__ == '__main__':
    imagefolder_to_lmdb()
