from yacs.config import CfgNode as CN

_C = CN()

_C.ANNO = CN()
# Original annotation
_C.ANNO.PARSER = ''
# Result annotation
_C.ANNO.CREATOR = ''
# Detailed output or not
_C.ANNO.VERBOSE = True

# ---------------------------------------------------------------------------- #
# input
# ---------------------------------------------------------------------------- #

_C.INPUT = CN()
# Input image data path
_C.INPUT.IMAGE_FOLDER = 'images'
# Label data path entered
_C.INPUT.LABEL_FOLDER = 'labels'
# Root directory - as parser
_C.INPUT.DIR = ''

# ---------------------------------------------------------------------------- #
# output
# ---------------------------------------------------------------------------- #

_C.OUTPUT = CN()
# Processed image data path
_C.OUTPUT.IMAGE_FOLDER = 'images'
# Processed label data path
_C.OUTPUT.LABEL_FOLDER = 'labels'
# Root directory - as a saver
_C.OUTPUT.DIR = ''

# ---------------------------------------------------------------------------- #
# LabelImg
# ---------------------------------------------------------------------------- #

_C.LABELIMG = CN()
_C.LABELIMG.NAME = 'labelimg'
# Image suffix
_C.LABELIMG.IMG_EXTENSION = '.png'
# Label file suffix
_C.LABELIMG.ANNO_EXTENSION = '.xml'

# ---------------------------------------------------------------------------- #
# YoLoV5
# ---------------------------------------------------------------------------- #

_C.YOLOV5 = CN()
_C.YOLOV5.NAME = 'yolov5'
_C.YOLOV5.IMG_EXTENSION = '.png'
_C.YOLOV5.ANNO_EXTENSION = '.txt'

# ---------------------------------------------------------------------------- #
# TLT
# ---------------------------------------------------------------------------- #

_C.TLT = CN()
_C.TLT.NAME = 'tlt'
_C.TLT.IMG_EXTENSION = '.png'
_C.TLT.ANNO_EXTENSION = '.txt'

# ---------------------------------------------------------------------------- #
# VisDrone
# ---------------------------------------------------------------------------- #

_C.VISDRONE = CN()
_C.VISDRONE.NAME = 'visdrone'
_C.VISDRONE.IMG_EXTENSION = '.jpg'
_C.VISDRONE.ANNO_EXTENSION = '.txt'

# ---------------------------------------------------------------------------- #
# PyTorch ImageFolder
# ---------------------------------------------------------------------------- #

_C.IMAGEFOLDER = CN()
_C.IMAGEFOLDER.NAME = 'imagefolder'

# ---------------------------------------------------------------------------- #
# LMDB
# ---------------------------------------------------------------------------- #

_C.LMDB = CN()
_C.LMDB.NAME = 'lmdb'
