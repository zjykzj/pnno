# -*- coding: utf-8 -*-

"""
@date: 2021/4/3 下午3:26
@file: lmdb.py
@author: zj
@description: 
"""

import os
import lmdb
import pickle

from . import registry
from .base_anno import BaseAnno
from ..util.logger import setup_logger


def dumps_data(obj):
    """
    Serialize an object.
    Returns:
        Implementation-dependent bytes-like object
    """
    return pickle.dumps(obj)


@registry.ANNOS.register('lmdb')
class LMDB(BaseAnno):

    def __init__(self, cfg) -> None:
        self.name = cfg.LMDB.NAME

        if cfg.ANNO.CREATOR == self.name:
            self.dst_dir = cfg.OUTPUT.DIR
            self.image_folder = cfg.OUTPUT.IMAGE_FOLDER

        self.verbose = cfg.ANNO.VERBOSE

        self.logger = setup_logger(__name__)

    def process(self) -> dict:
        pass

    def save(self, input_data: dict):
        super(LMDB, self).save(input_data)
        verbose = self.verbose
        logger = self.logger

        data_loader = input_data['data_loader']
        lmdb_path = os.path.join(self.dst_dir, f'{self.image_folder}.lmdb')
        if verbose:
            logger("Generate LMDB to %s" % lmdb_path)
        self.folder2lmdb(lmdb_path, data_loader)

        if self.verbose:
            logger.info(__name__ + ' done')

    def folder2lmdb(self, dpath, data_loader, write_frequency=5000):
        verbose = self.verbose
        logger = self.logger

        db = lmdb.open(dpath, subdir=False,
                       map_size=1099511627776 * 2, readonly=False,
                       meminit=False, map_async=True)

        txn = db.begin(write=True)
        for idx, data in enumerate(data_loader):
            image, label = data[0]

            txn.put(u'{}'.format(idx).encode('ascii'), dumps_data((image, label)))
            if idx % write_frequency == 0:
                if verbose:
                    logger("[%d/%d]" % (idx, len(data_loader)))
                txn.commit()
                txn = db.begin(write=True)

        # finish iterating through dataset
        txn.commit()
        keys = [u'{}'.format(k).encode('ascii') for k in range(len(data_loader))]
        with db.begin(write=True) as txn:
            txn.put(b'__keys__', dumps_data(keys))
            txn.put(b'__len__', dumps_data(len(keys)))

        if verbose:
            logger("Flushing database ...")
        db.sync()
        db.close()
