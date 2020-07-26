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
    parser.add_argument('-f', "--config_file", default="", metavar="CONFIG_FILE", help="path to config file")
    parser.add_argument('-v', '--version', help='output version information', action="store_true")
    return parser
