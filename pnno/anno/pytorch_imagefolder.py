# -*- coding: utf-8 -*-

"""
@date: 2021/4/3 下午3:16
@file: pytorch_imagefolder.py
@author: zj
@description: 
"""

import os
from PIL import Image
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

from . import registry
from .base_anno import BaseAnno
from ..util.logger import setup_logger
from ..util.misc import get_cpu_count


def raw_reader(path):
    # with open(path, 'rb') as f:
    #     bin_data = f.read()
    return Image.open(path).convert('RGB')


# fix TypeError: batch must contain tensors, numbers, dicts or lists; found <class ‘PIL.Image.Image’>
def collate_fn(batch):
    assert len(batch) == 1
    image, target = batch[0]
    return image, target


@registry.ANNOS.register('imagefolder')
class PytorchImageFolder(BaseAnno):

    def __init__(self, cfg) -> None:
        self.name = cfg.IMAGEFOLDER.NAME

        if cfg.ANNO.PARSER == self.name:
            self.src_dir = cfg.INPUT.DIR
            self.image_folder = cfg.INPUT.IMAGE_FOLDER

        self.num_workers = int(
            get_cpu_count() / 2) if cfg.IMAGEFOLDER.NUM_WORKERS == -1 else cfg.IMAGEFOLDER.NUM_WORKERS

        self.verbose = cfg.ANNO.VERBOSE
        self.logger = setup_logger(__name__)

    def process(self) -> dict:
        image_path = os.path.join(self.src_dir, self.image_folder)
        data_set = ImageFolder(image_path, loader=raw_reader)
        data_loader = DataLoader(data_set, num_workers=self.num_workers, collate_fn=collate_fn, batch_size=1)

        return {'dataloader': data_loader, 'classes': data_set.classes}

    def save(self, input_data: dict):
        super(PytorchImageFolder, self).save(input_data)
        pass
