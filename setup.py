# -*- coding: utf-8 -*-

"""
@date: 2020/7/21 下午9:27
@file: setup.py.py
@author: zj
@description: 
"""

import setuptools
from os import path


def get_version():
    init_py_path = path.join(path.abspath(path.dirname(__file__)), "parseanno", "__init__.py")
    init_py = open(init_py_path, "r").readlines()
    version_line = [l.strip() for l in init_py if l.startswith("__version__")][0]
    version = version_line.split("=")[-1].strip().strip("'\"")

    return version


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ParseAnno",
    version=get_version(),
    author="zj",
    author_email="wy163zhuj@163.com",
    description="Script for annotation data processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zjZSTU/ParseAnno",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License"
    ],
    python_requires='>=3.6',
    install_requires=[
        "yacs >= 0.1.7",
        "opencv_contrib_python >= 4.2.0",
        "numpy >= 1.17.2"
    ],
    # scripts=['parseanno/tools/parse-anno.py']
    entry_points={
        'console_scripts': [
            'parse-anno=parseanno.tools.cli:main'
        ]
    }
)
