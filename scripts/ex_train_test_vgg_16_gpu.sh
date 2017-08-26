#!/bin/bash
#

MODEL_NAME=vgg_16
WEIGHT_LOSS=10
LEARNING_RATE=0.0001
END_LEARNING_RATE=0.000001
DATA_NAME=kitti_calib
LIST_PARAM=20,1.5

python deep_calib_train.py \
    --dataset_dir=data_ex/tf/${DATA_NAME} \
    --train_dir=checkpoints/${DATA_NAME} \
    --max_number_of_steps=1000 \
    --list_param=${LIST_PARAM} \
    --weight_loss=${WEIGHT_LOSS} \
    --clone_on_cpu=False \
    --model_name=${MODEL_NAME} \
    --checkpoint_path=pretrained/${MODEL_NAME}.ckpt \
    --checkpoint_exclude_scopes=${MODEL_NAME}/lidar_feat,${MODEL_NAME}/match_feat,${MODEL_NAME}/regression \
    --learning_rate=${LEARNING_RATE} \
    --end_learning_rate=${END_LEARNING_RATE} \
    # --trainable_scopes=vgg_16/lidar_feat,vgg_16/match_feat,vgg_16/regression
    # --ignore_missing_vars=

python deep_calib_test.py \
    --dataset_dir=data_ex/tf/${DATA_NAME} \
    --checkpoint_path=checkpoints/${DATA_NAME}/${MODEL_NAME}/weight_${WEIGHT_LOSS} \
    --list_param=${LIST_PARAM} \
    --model_name=${MODEL_NAME} \
    --weight_loss=${WEIGHT_LOSS}