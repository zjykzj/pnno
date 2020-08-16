# -*- coding: utf-8 -*-

"""
@date: 2020/7/21 下午8:32
@file: cli.py
@author: zj
@description: 
"""

import sys
from pnno.config import cfg
from pnno.engine import AnnoProcessor, default_argument_parser
from pnno.util.misc import get_version


def main():
    parser = default_argument_parser()
    args = parser.parse_args()

    if args.version:
        print('pnno: v{}'.format(get_version()))
        sys.exit(0)

    if not args.config_file:
        parser.print_usage()
        sys.exit(1)

    cfg.merge_from_file(args.config_file)
    cfg.freeze()

    processor = AnnoProcessor(cfg)
    processor.process()


if __name__ == '__main__':
    main()
