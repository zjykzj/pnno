# -*- coding: utf-8 -*-

"""
@date: 2021/4/3 下午3:16
@file: pytorch_imagefolder.py
@author: zj
@description: 
"""

import os
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

from . import registry
from .base_anno import BaseAnno
from ..util.logger import setup_logger


def raw_reader(path):
    with open(path, 'rb') as f:
        bin_data = f.read()
    return bin_data


@registry.ANNOS.register('imagefolder')
class PytorchImageFolder(BaseAnno):

    def __init__(self, cfg) -> None:
        self.name = cfg.IMAGEFOLDER.NAME

        if cfg.ANNO.PARSER == self.name:
            self.src_dir = cfg.INPUT.DIR

        self.verbose = cfg.ANNO.VERBOSE
        self.logger = setup_logger(__name__)

    def process(self) -> dict:
        train_path = os.path.join(self.src_dir, 'train')
        train_dataset = ImageFolder(train_path, loader=raw_reader)
        train_dataloader = DataLoader(train_dataset, num_workers=16)

        val_path = os.path.join(self.src_dir, 'val')
        val_dataset = ImageFolder(val_path, loader=raw_reader)
        val_dataloader = DataLoader(val_dataset, num_workers=16)

        return {'train': train_dataloader, 'val': val_dataloader}

    def save(self, input_data: dict):
        super(PytorchImageFolder, self).save(input_data)
        pass
