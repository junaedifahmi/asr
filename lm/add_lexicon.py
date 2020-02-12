#!/usr/bin/env python
# coding: utf-8

# In[9]:


# Arguments declaration
import logging
import argparse
import os

parser = argparse.ArgumentParser(description="Cleaning ")
parser.add_argument("--src", help="The lexicon file")
parser.add_argument("--add", help="Additional file(s)", nargs="+")
parser.add_argument("--logdir", help="Logging file", default=".")
args = parser.parse_args()
flexicon = args.src
fbaru = args.add
log = args.log

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log+"addlexicon.log", mode='w'),
        logging.StreamHandler()
    ]
)

# In[38]:


lexicon = set()

with open(flexicon, 'r+') as lex:
    for line in lex:
        lama = line.split()[0]
        lexicon.add(lama)

leng = len(lexicon)

logging.info(f"Diambil lexicon dari {flexicon}")
logging.info(f"Ada {leng} buah lexicon")


for file in fbaru:
    with open(file, 'r') as f:
        lexicon |= set(f.read().split())
    logging.info(f"Ditambahkan {len(lexicon)-leng} buah lexicon dari {file}")

lexicon = sorted(lexicon)


# In[40]:


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


with open(flexicon, 'w') as f:
    for lexi in lexicon:
        print(f"{lexi}\t{' '.join(cacah(lexi))+' |'}", file=f)

logging.info(f"Total lexicon baru berjumlah {len(lexicon)}")
