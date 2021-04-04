#!/bin/bash

echo 'begin process train imagenet'
pnno -f train_imagenet_to_lmdb.yaml
echo 'begin process val imagenet'
pnno -f val_imagenet_to_lmdb.yaml
