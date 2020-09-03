<div align="right">
  语言:
    🇨🇳
  <a title="英语" href="./README.en.md">🇺🇸</a>
  <!-- <a title="俄语" href="../ru/README.md">🇷🇺</a> -->
</div>

 <div align="center"><a title="" href="https://github.com/zjykzj/pnno"><img align="center" src="./imgs/PNNO.png"></a></div>

<p align="center">
  «pnno» 实现了不同格式标注数据的自动转换
<br>
<br>
  <a href="https://github.com/RichardLitt/standard-readme"><img src="https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square"></a>
  <a href="https://conventionalcommits.org"><img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg"></a>
  <a href="http://commitizen.github.io/cz-cli/"><img src="https://img.shields.io/badge/commitizen-friendly-brightgreen.svg"></a>
  <a href="https://pypi.org/project/pnno/"><img src="https://img.shields.io/badge/PYPI-PNNO-brightgreen"></a>
</p>

将不同数据集转换成算法指定格式。当前已实现

1. `LabelImg`标注 `-> YoloV5`数据格式
2. `VisDrone`数据集 `-> TLT Kitti`数据格式

## 内容列表

- [内容列表](#内容列表)
- [背景](#背景)
- [主要维护人员](#主要维护人员)
- [参与贡献方式](#参与贡献方式)
- [许可证](#许可证)

## 背景

算法开发过程中经常会涉及到数据集的处理，需要将数据集转换成算法训练时指定的格式，日积月累下来积攒了不少脚本，能不能将这些程序整合在一起，既能够重复使用，也能够降低下一次实现的难度。Let's Do It !!!

## 主要维护人员

* zhujian - *Initial work* - [zjykzj](https://github.com/zjykzj)

## 参与贡献方式

欢迎任何人的参与！打开[issue](https://github.com/zjykzj/pnno/issues)或提交合并请求。

注意:

* `GIT`提交，请遵守[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/)规范
* 语义版本化，请遵守[Semantic Versioning 2.0.0](https://semver.org)规范
* `README`编写，请遵守[standard-readme](https://github.com/RichardLitt/standard-readme)规范

## 许可证

[Apache License 2.0](LICENSE) © 2020 zjykzj