#!/bin/bash

source ./path.sh
source ./cmd.sh

musan=/root/data/musan
noise=/root/data
dsource=./data/train

./utils/data/get_reco2dur.sh --nj 80 --cmd "run.pl" $dsource 

./steps/data/make_musan.sh --sampling-rate 16000 --use-vocals false $musan $noise

./steps/data/augment_data_dir.py --utt-prefix "noise" --modify-spk-id "true" --fg-interval 1 --fg-snrs "15:10:5:0" --fg-noise-dir $noise/musan_noise ${dsource} ${dsource}_noise

./steps/data/augment_data_dir.py --utt-prefix "music" --modify-spk-id "true" --bg-snrs "15:10:8:5" --num-bg-noises 1 --bg-noise-dir  $noise/musan_music ${dsource} ${dsource}_music

./steps/data/augment_data_dir.py --utt-prefix "babble" --modify-spk-id "true" --bg-snrs "20:17:15:13" --num-bg-noise 1 --bg-noise-dir $noise/musan_noise ${dsource} ${dsource}_speech

./utils/copy_data_dir.sh $dsource ${dsource}_aug

./utils/combine_data.sh ${dsource}_aug ${dsource}_noise ${dsource}_music ${dsource}_speech

mfcc=${dsource}_mfcc_aug

./steps/make_mfcc.sh --cmd "$train_cmd" --nj $njobs ${dsource}_aug ./exp/make_mfcc/${dsource}_aug $mfcc
./steps/compute_cmvn_stats.sh ${dsource}_aug ./exp/make_mfcc/${dsource} $mfcc
./utils/fix_data_dir.sh ${dsource}_aug || exit 1;

## GET Subset Data
./utils/subset_data_dir.sh ${dsource}_aug 3000 ${dsource}_aug_3k
./utils/data/remove_dup_utts.sh 200 ${dsource}_aug_3k 


# Copy Ali So we Dont have to retrain from the scratch

ali=./exp/tri2b_ali
./steps/copy_ali_dir.sh --nj $njobs --cmd "$train_cmd" ${dsource}_aug $ali ./exp/aug/ali

./steps/train_lda_mllt.sh --cmd "$train_cmd" --num-iters 13 --splice-opts "--left-context=3 --right-context=3" 5500 90000 ${dsource}_aug data/lang ./exp/aug/ali ./exp/aug/lda

# make ivector extractor and feats
./steps/online/nnet2/train_diag_ubm.sh --cmd "$train_cmd" --nj $njobs --num-frames 200000 ${dsource}_aug_3k 512 ./exp/aug/lda ./exp/aug/ivector/ubm

./steps/online/nnet2/train_ivector_extractor.sh --cmd "$train_cmd" --nj $njobs ${dsource}_aug ./exp/aug/ivector/ubm ./exp/aug/ivector/extractor

./steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj $njobs ${dsource}_aug ./exp/aug/ivector/extractor ./exp/aug/ivector/feats


