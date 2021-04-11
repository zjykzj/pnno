# -*- coding: utf-8 -*-

"""
@date: 2020/7/21 下午9:27
@file: setup.py.py
@author: zj
@description: 
"""

import setuptools
import os
import sys
import shutil

# ---------------------- #
# 超参数设置
NAME = "pnno"
AUTHOR = "zj"
AUTHOR_EMAIL = "wy163zhuj@163.com"
DESCRIPTION = "Script for annotation data processing"
URL = "https://github.com/zjykzj/pnno"
PYTHON_REQUIRES = ">=3.6"
INSTALL_REQUIRES = [
    "Pillow >= 8.1.0",
    "imageio >= 2.9.0",
    "lmdb >= 1.1.1",
    "numpy >= 1.19.5",
    "opencv_python >= 4.5.1.48",
    "torch >= 1.7.1",
    "torchvision >= 0.8.2",
    "tqdm >= 4.56.0",
    "xmltodict >= 0.12.0",
    "yacs >= 0.1.8"
]
CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: Apache Software License"
]


# ---------------------- #

def get_version():
    init_py_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "pnno", "__init__.py")
    init_py = open(init_py_path, "r").readlines()
    version_line = [l.strip() for l in init_py if l.startswith("__version__")][0]
    version = version_line.split("=")[-1].strip().strip("'\"")

    return version


with open("README.md", "r") as fh:
    long_description = fh.read()


class UploadCommand(setuptools.Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            here = os.path.abspath(os.path.dirname(__file__))
            self.status('Removing previous builds…')
            shutil.rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(get_version()))
        os.system('git push --tags')

        sys.exit()


setuptools.setup(
    name=NAME,
    version=get_version(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=setuptools.find_packages(),
    classifiers=CLASSIFIERS,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    # scripts=['pnno/tool/cli.py']
    entry_points={
        'console_scripts': [
            'pnno=pnno.tool.cli:main',
            'simg=pnno.tool.show:show_image'
        ]
    },
    cmdclass={
        'upload': UploadCommand,
    },
)
