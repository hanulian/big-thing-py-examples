#!/bin/bash

sed -i 's/GPU=0/GPU=1/' darknet/Makefile
sed -i 's/CUDNN=0/CUDNN=1/' darknet/Makefile
sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' darknet/Makefile
sed -i 's/OPENMP=0/OPENMP=1/' darknet/Makefile
sed -i 's/LIBSO=0/LIBSO=1/' darknet/Makefile
sed -i 's/OPENCV=0/OPENCV=1/' darknet/Makefile

cd darknet
make -j

wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg
wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg
wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-csp.cfg
wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-csp-swish.cfg
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-csp.weights
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-csp-swish.weights

cp yolov4.cfg ./cfg
cp yolov4-tiny.cfg ./cfg
cp yolov4-csp.cfg ./cfg
cp yolov4-csp-swish.cfg ./cfg

cp -rf data ../
cd -
