# -*- coding: utf-8 -*-

"""
@date: 2020/7/18 下午2:00
@file: defaults.py
@author: zj
@description: 
"""

import argparse


def default_argument_parser():
    """
    Create a parser with some common arguments used by users.

    Returns:
        argparse.ArgumentParser:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", default="", metavar="FILE", help="path to config file")
    return parser
