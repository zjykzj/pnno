
# ImageNet LMDB

convert [ImageNet](http://www.image-net.org/) to LMDB

## Convert

Assume that the train / val directory is in the current path after Imagenet decompression

Execute the following command:

```angular2html
$ bash imagenet_2_lmdb.sh
```

if not, you can add the decompression path to `train_imagenet_to_lmdb.yaml` and `val_imagenet_to_lmdb.yaml`

```
INPUT:
  DIR: '.'               <------------  here
  IMAGE_FOLDER: 'train'
OUTPUT:
  DIR: '.'               <------------ here
  IMAGE_FOLDER: 'train'
```

## Usage

See `tests/att_face_to_lmdb/lmdb_to_att_face.py`. And you can refer to [ZJCV/ZCls](https://github.com/ZJCV/ZCls)