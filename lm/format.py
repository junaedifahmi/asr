#!/usr/bin/env python
# coding: utf-8

# In[36]:


n2t = {
    '1' : "satu",
    '2' : "dua",
    '3' : "tiga",
    '4' : "empat",
    '5' : "lima",
    '6' : "enam",
    '7' : "tujuh",
    '8' : "delapan",
    '9' : "sembilan",
    '0' : "nol",
}

def rep_number(num):
    txt = []
    for n in num:
        txt.append(n2t[n])
    return ' '.join(txt)

def to_lower(txt):
    txt = txt.lower()
    return txt


import re
def num2txt(txt):
    txt = re.sub(r'\d+',lambda x: rep_number(x.group()),txt)
    return txt


import string
def punc(txt):
    txt = txt.translate(str.maketrans("","", string.punctuation))
    return txt


# In[40]:


type(punc("siaa asp,,las"))


# In[ ]:


import argparse
import os

parser = argparse.ArgumentParser(description="Cleaning ")
parser.add_argument("--src", help="Folder data kotor text", nargs='+')
parser.add_argument("--to", help="Folder data untuk hasil", default=".")

args = parser.parse_args()

paths = args.src
to = args.to + '/'
os.makedirs(to, exist_ok=True)



hasil = open(to+"clean",'w')
for path in paths:
    with open(path,'r') as f:
        for line in f:
            line = to_lower(line)
            line = num2txt(line)
            line = punc(line)
            hasil.write(line)
            
hasil.close()

