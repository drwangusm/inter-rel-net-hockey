#!/bin/bash

# docker run -it --rm --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=0 cwaffles/openpose

tarbas=$(docker ps | grep 'cwaffles/openpose' | awk '{ print $1 }')

docker cp /usr/local/data02/dpdataset/DP17_PostProcessing/clipsTrimmedBen/  "$tarbas":/openpose/examples/media/

docker cp ./getOpenPose_step2.sh  "$tarbas":/openpose/