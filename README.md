<div align="right">
  Language:
    🇺🇸
  <a title="Chinese" href="./README.zh-CN.md">🇨🇳</a>
</div>

 <div align="center"><a title="" href="https://github.com/zjykzj/pnno"><img align="center" src="./imgs/PNNO.png"></a></div>

<p align="center">
  «pnno» realizes the conversion of dataset or annotation data in different formats
<br>
<br>
  <a href="https://github.com/RichardLitt/standard-readme"><img src="https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square"></a>
  <a href="https://conventionalcommits.org"><img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg"></a>
  <a href="http://commitizen.github.io/cz-cli/"><img src="https://img.shields.io/badge/commitizen-friendly-brightgreen.svg"></a>
  <a href="https://pypi.org/project/pnno/"><img src="https://img.shields.io/badge/PYPI-PNNO-brightgreen"></a>
</p>

This repo provides several script tools for the following aspects:

1. convert different data sets into the format specified by the algorithm. Currently implemented
   1. `LabelImg` annotation -> `YoloV5` data format
   2. `VisDrone` data set -> `TLT KITTI` data format
2. convert PyTorch ImageFolder dataset to LMDB format
3. show image in command line

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Background](#background)
- [Install](#install)
- [Usage](#usage)
  - [Dataset/Label Convert](#datasetlabel-convert)
  - [Show Image in Command Line](#show-image-in-command-line)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

The processing of data sets is often involved in the process of algorithm development, which needs to be converted into the format specified in algorithm training. Many scripts are accumulated over time. Whether these programs can be integrated together can not only be reused, but also reduce the difficulty of the next implementation. Let's Do It ! ! !

## Install

```
$ pip install pnno
```

## Usage

### Dataset/Label Convert

Basic operation as follows:

```
$ pnno -f <cfg_file>
```

Operation 1: convert [ tzutalin/labelImg](https://github.com/tzutalin/labelImg) label file to [ ultralytics/yolov5](https://github.com/ultralytics/yolov5)  specified dataset format. **Refer to the configuration file `configs/labelimg_2_yolov5.yaml`**

Operation 1: convert [ VisDrone/VisDrone-Dataset](https://github.com/VisDrone/VisDrone-Dataset) dataset to [KITTI](http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=2d) label format. **Refer to the configuration file `configs/visdrone_2_tlt.yaml`**

Operation 3: convert PyTorch ImageFolder dataset to LMDB format. **Refer to `demo/imagefolder_lmdb`**

For more usage, refert to `demo/`

### Show Image in Command Line

```
$ simg -f <IMG_FILE>
```

## Maintainers

* zhujian - *Initial work* - [zjykzj](https://github.com/zjykzj)

## Contributing

Anyone's participation is welcome! Open an [issue](https://github.com/zjykzj/pnno/issues) or submit PRs.

Small note:

* Git submission specifications should be complied with [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/)
* If versioned, please conform to the [Semantic Versioning 2.0.0](https://semver.org) specification
* If editing the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

[Apache License 2.0](LICENSE) © 2020 zjykzj