#!/bin/bash
#

MODEL_NAME=vgg_16
WEIGHT_LOSS=100

python deep_calib_train.py \
    --dataset_dir=/data/tf/kitti_calib \
    --train_dir=/data/tf/checkpoints/kitti_calib \
    --max_number_of_steps=50000 \
    --list_param=20,1.5 \
    --weight_loss=${WEIGHT_LOSS} \
    --clone_on_cpu=False \
    --model_name=${MODEL_NAME} \
    --checkpoint_path=pretrained/${MODEL_NAME}.ckpt \
    --checkpoint_exclude_scopes=${MODEL_NAME}/lidar_feat,${MODEL_NAME}/match_feat,${MODEL_NAME}/regression \
    --learning_rate=0.00001 \
    --end_learning_rate=0.0000001
    # --trainable_scopes=
    # --ignore_missing_vars=

python deep_calib_test.py \
    --dataset_dir=/data/tf/kitti_calib \
    --checkpoint_path=/data/tf/checkpoints/kitti_calib/${MODEL_NAME}/weight_${WEIGHT_LOSS} \
    --list_param=20,1.5 \
    --model_name=${MODEL_NAME} \
    --weight_loss=${WEIGHT_LOSS}