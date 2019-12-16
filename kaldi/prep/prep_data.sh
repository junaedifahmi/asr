DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo "Preparing data"
python3 $DIR/files.py $1
sort wav.scp -o wav.scp
sort utt2spk -o utt2spk
sort text -o text
