#!/bin/bash

#### Data prerpocessnig #####
src=$1
to=$2


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

temp=./data/prep

python3 $DIR/files.py $src $temp/akustik
sort $temp/akustik/wav.scp -o $temp/akustik/wav.scp
sort $temp/akustik/utt2spk -o $temp/akustik/utt2spk
sort $temp/akustik/text -o $temp/akustik/text

python3 prepare_lang.py $src $to


