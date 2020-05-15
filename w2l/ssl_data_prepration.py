import argparse
import re
import subprocess
import os
from tqdm import tqdm

# Argument definition
parser = argparse.ArgumentParser(description="Language model construction for wav2letter engine")
parser.add_argument("--labeled", help="source text files")
parser.add_argument("--unlabeled", help="kenlm root directory")
parser.add_argument("--outdir", help="output directori", default="./ssl")

args = parser.parse_args()

os.makedirs(args.outdir, exist_ok=True)

labeled = []
unlabeled = []

with open(args.labeled, 'r') as f:
    for line in f:
        labeled.append(line)


with open(args.unlabeled, 'r') as f:
    for line in f:
        unlabeled.append(line)

minlen = min(len(labeled), len(unlabeled))

if len(labeled) == minlen:
    unlabeled = unlabeled[0:minlen]
else:
    labeled = labeled[0:minlen]

for f in labeled:
    print(f.split('\t'))

flabel = open(args.outdir+"/labeled.lst", 'w')
funlabel = open(args.outdir+"/unlabeled.lst", 'w')
for i in range(0, minlen):
    flabel.writelines(labeled[i])
    unlabel = unlabeled[i].split('\t')
    # print(unlabel)
    unlabel = unlabel[0:-1]
    unlabel.append("<unk>")
    print(unlabel)
    unlabel = '\t'.join(unlabel)
    funlabel.writelines(unlabel)

print("Done")






