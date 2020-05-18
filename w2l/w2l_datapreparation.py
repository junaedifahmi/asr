#!/usr/bin/env python
# coding: utf-8

# In[76]:


import re
import glob
import sys
import os
import random
import sox
import logging
import argparse
import time
import re
import string

start_time = time.time()

parser = argparse.ArgumentParser(description="Dataset Creation for w2l")
parser.add_argument("--src", help="Folder data akustik dan text", nargs='+')
parser.add_argument("--to", help="Folder data untuk hasil")
parser.add_argument(
    "--split", help="Split ke train dan test dalam persen", default=10)
parser.add_argument("--log", help="Simpan dimana lognya",
                    default='info.log')
args = parser.parse_args()

if len(sys.argv) < 3 :
    parser.print_help()
    exit()

paths = args.src
to = args.to + '/'
log = args.log
split = int(args.split)
os.makedirs(to, exist_ok=True)


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(to+log, mode='w'),
        logging.StreamHandler()
    ]
)

logging.info("Data diambil dari %s", paths)
files = []
for path in paths:
    files.extend(glob.glob(path + "/**/*.wav", recursive=True))
    logging.info("Terdapat %i wav files ditemukan dari folder %s",
                 len(files), path)

files_filtered = []
for file in files:
    if os.path.exists(file.replace('wav', 'txt')):
        files_filtered.append(file)
    elif os.path.exists(file.replace('wav', 'lab')):
        files_filtered.append(file)
    else:
        logging.warn("%s tidak memiliki transkrip file, dihapus", file)

# In[70]:


def getname(filename):
    return os.path.basename(filename).split(".")[0]


def gettext(filename):
    if os.path.exists(filename.replace('wav', 'txt')):
        filename = filename.replace('wav', 'txt')
    else:
        filename = filename.replace('wav', 'lab')

    with open(filename, 'r') as f:
        txt = f.readline()
    txt = txt.lower()
    txt = re.sub(r'\d+','',txt)
    txt = re.sub(r'(\[\w+\]?|<\w+>?)', '', txt) # Remove tag (silphone)
    txt = re.sub(r'-', '|', txt) # Remove dashline (keep the repetitif words)
    txt = txt.translate(str.maketrans('','',string.punctuation))    # Remove punctuation
    return txt.replace('\n', '')


def getabs(filename):
    return os.path.abspath(filename)


totaldur = []


def writefile(filename, datas):
    with open(filename, 'w') as f:
        for data in datas:
            f.write(getname(data))
            f.write("\t")
            f.write(getabs(data))
            f.write("\t")
            dur = sox.file_info.duration(data) * 1000
            totaldur.append(dur)
            f.write(str(dur))
            f.write("\t")
            f.write(gettext(data))
            f.write("\n")


def cacah(kata):
    x = [c for c in kata]
    for i in range(len(x)):
        try:
            y = x[i+1]

            if x[i] == 'n' and y == 'y':
                x[i] = 'ny'
                x[i+1] = '#'
            elif x[i] == 'n' and y == 'g':
                x[i] = 'ng'
                x[i+1] = '#'
            elif x[i] == 's' and y == 'y':
                x[i] = 'sy'
                x[i+1] = '#'
            elif x[i] == 'k' and y == 'h':
                x[i] = 'kh'
                x[i+1] = '#'
            elif x[i] == 't' and y == 'h':
                x[i] = 'th'
                x[i+1] = '#'
            elif x[i] not in list('abcdefghijklmnopqrstuvwxyz') and x[i] != '#':
                x[i] = '|'
        except:
            pass
    x = [c for c in x if c != '#']

    return x


# In[82]:

os.makedirs(to+'/lists/', exist_ok=True)
if int(split) > 0:
    k = int(split/100*len(files_filtered))
    test = random.sample(files_filtered, k)
    train = [f for f in files_filtered if f not in test]
    totaldur = []
    writefile(to + '/lists/train.lst', train)
    logging.info("Total data latih %.2f jam", sum(totaldur)/1000/60/60)
    totaldur = []
    writefile(to + '/lists/test.lst', test)
    logging.info("Total data uji %.2f jam", sum(totaldur)/1000/60/60)
else:
    writefile(to + '/lists/train.lst', files)
    logging.info("Total data latih %.2f jam", sum(totaldur)/1000/60/60)

logging.info("Telah dibuat file list di %s", to+'/lists/')

# In[102]:
os.makedirs(to+'/txt/', exist_ok=True)

text = open(to+'/txt/text.txt', 'w')

lexicon = []
for f in files_filtered:
    lexicon.extend(gettext(f).split())
    text.writelines(gettext(f)+'\n')
text.close()
logging.info("Telah dibuat file text di %s", to+'/txt/text.txt')

# In[110]:

lexicon = sorted(set(lexicon))
tokens = set()


# Write Lexicon file "<word> <spelling>" format
with open((to+"/txt/lexicon.txt"), 'w') as f:
    for l in lexicon:
        ch = cacah(l)
        tokens |= set(ch)
        f.writelines(l+"\t"+' '.join(ch)+" |\n")

logging.info("Telah dibuat file lexicon di %s", to + "/txt/lexicon.txt")
logging.info("Terdapat %d lexicon unik", len(lexicon))
try:
    tokens.remove(' ')
except:
    pass

# Write tokens list
with open((to+"/txt/tokens.txt"), 'w') as f:
    tokens.add("|")
    tokens = sorted(tokens)
    for c in tokens:
        f.writelines(c+"\n")
logging.info("Token dibuat di %s", to+"/txt/tokens.txt")

elapsed_time = time.time() - start_time
logging.info("Proses selesai dengan waktu %.2f menit", elapsed_time/60)
print("DONEEEEE")
