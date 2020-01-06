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


start_time = time.time()

parser = argparse.ArgumentParser(description="Dataset Creation for w2l")
parser.add_argument("--src", help="Folder data akustik dan text", nargs='+')
parser.add_argument("--to", help="Folder data untuk hasil")
parser.add_argument(
    "--split", help="Split ke train dan test dalam persen", default=30)
parser.add_argument("--log", help="Simpan dimana lognya",
                    default='./log_datapreparation')
args = parser.parse_args()

paths = args.src
to = args.to + '/'
split = int(args.split)
os.makedirs(to, exist_ok=True)
logging.basicConfig(filename=args.log,
                    format='[%(asctime)s] [%(levelname)s] [%(massage)s]')
logger = logging.getLogger()
#os.makedirs(to, exist_ok=True)


print(paths)
files = []
for path in paths:
    files.extend(glob.glob(path + "/**/*.wav", recursive=True))
    logger.info("Terdapat %i wav files ditemukan dari folder %s",
                len(files), path)

print(len(files))
for file in files:
    if not os.path.exists(file.replace('wav', 'txt')):
        files.remove(file)
        logger.info("%s tidak memiliki txt file, dihapus", file)
print(len(files))

# In[70]:


def getname(filename):
    return os.path.basename(filename).split(".")[0]


def gettext(filename):
    filename = filename.replace('wav', 'txt')
    with open(filename, 'r') as f:
        txt = f.readline()
    txt = re.sub(r'(\[\w+\]|<\w+>)', '', txt)
    return txt.replace('\n', '')


def getabs(filename):
    return os.path.abspath(filename)


def writefile(filename, datas):
    with open(filename, 'w') as f:
        for data in datas:
            f.write(getname(data))
            f.write("\t")
            f.write(getabs(data))
            f.write("\t")
            f.write(str(sox.file_info.duration(data)))
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
    k = int(split/100*len(files))
    test = random.sample(files, k)
    train = [f for f in files if f not in test]
    writefile(to+'/lists/train.lst', train)
    writefile(to+'/lists/test.lst', test)
else:
    writefile(to + '/lists/train.lst', files)

logger.info("Telah dibuat file list di %s", to+'/lists/')

# In[102]:
os.makedirs(to+'/txt/', exist_ok=True)

text = open(to+'/txt/text.txt', 'w')

lexicon = []
for f in files:
    lexicon.extend(gettext(f).split())
    text.writelines(gettext(f)+'\n')
text.close()
logger.info("Telah dibuat file text di %s", text)

# In[110]:

lexicon = set(lexicon)

tokens = set()


# Write Lexicon file "<word> <spelling>" format
with open((to+"/txt/lexicon.txt"), 'w') as f:
    for l in lexicon:
        ch = cacah(l)
        tokens |= set(ch)
        print(l, ' '.join(ch))
        f.writelines(l+" "+' '.join(ch)+"\n")

logger.info("Telah dibuat file lexicon di %s", to+"/txt/lexicon.txt")
try:
    tokens.remove(' ')
except:
    pass

# Write tokens list
with open((to+"/txt/tokens.txt"), 'w') as f:
    tokens.add("|")
    for c in tokens:
        f.writelines(c+"\n")
logger.info("Token dibuat di %s", to+"/txt/tokens.txt")

elapsed_time = time.time() - start_time
logger.info("Proses selesai dengan waktu %s menit", elapsed_time/60)
