#!/bin/bash

tarbas=$(docker ps | grep 'cwaffles/openpose' | awk '{ print $1 }')

docker cp "$tarbas":/openpose/output_json /usr/local/data02/dpdataset/DP17_PostProcessing/openposeTrimmedBen
docker cp "$tarbas":/openpose/output_images /usr/local/data02/dpdataset/DP17_PostProcessing/openposeTrimmedBen