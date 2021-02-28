<div align="right">
  Language:
    🇺🇸
  <a title="Chinese" href="./README.zh-CN.md">🇨🇳</a>
</div>

 <div align="center"><a title="" href="https://github.com/zjykzj/pnno"><img align="center" src="./imgs/PNNO.png"></a></div>

<p align="center">
  «pnno» realizes the automatic conversion of annotation data in different formats
<br>
<br>
  <a href="https://github.com/RichardLitt/standard-readme"><img src="https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square"></a>
  <a href="https://conventionalcommits.org"><img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg"></a>
  <a href="http://commitizen.github.io/cz-cli/"><img src="https://img.shields.io/badge/commitizen-friendly-brightgreen.svg"></a>
  <a href="https://pypi.org/project/pnno/"><img src="https://img.shields.io/badge/PYPI-PNNO-brightgreen"></a>
</p>

Convert different data sets into the format specified by the algorithm. Currently implemented

1. `LabelImg` annotation -> `YoloV5` data format
2. `VisDrone` data set -> `TLT KITTI` data format

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Background](#background)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

The processing of data sets is often involved in the process of algorithm development, which needs to be converted into the format specified in algorithm training. Many scripts are accumulated over time. Whether these programs can be integrated together can not only be reused, but also reduce the difficulty of the next implementation. Let's Do It ! ! !

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