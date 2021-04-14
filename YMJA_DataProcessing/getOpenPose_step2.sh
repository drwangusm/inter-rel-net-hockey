#!/bin/bash

for file in $(find ./examples/media/clipsTrimmedBen/ -type f -name "*.mp4");
do
    echo "$file"
    tarbas="${file%.*}"
    mkdir -p output_json/"${tarbas//.\//}"
    mkdir -p output_images/"${tarbas//.\//}"
    ./build/examples/openpose/openpose.bin --video "$file" --write_images output_images/"${tarbas//.\//}" --write_json output_json/"${tarbas//.\//}" --display 0
done