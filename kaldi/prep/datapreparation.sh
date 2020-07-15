#!/bin/bash

#### Data prerpocessnig #####
src=$1
to=$2


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

temp=./tmp
mkdir -p $to/akustik

python3 $DIR/files.py $src $temp/akustik

sort $temp/akustik/wav.scp -o $to/akustik/wav.scp
sort $temp/akustik/utt2spk -o $to/akustik/utt2spk
sort $temp/akustik/text -o $to/akustik/text

python3 $DIR/prep_lang.py $src $to


