#!/usr/bin/env python
# coding: utf-8

# In[76]:


import glob
import sys
import os
import random
import sox
import logging
import argparse
import time

start_time = time.time()

parser = argparse.ArgumentParser(description="Dataset Creation for w2l")
parser.add_argument("--src", help="Folder data akustik dan text")
parser.add_argument("--to", help="Folder data untuk hasil")
parser.add_argument("--split",help="Split ke train dan test dalam persen",default=30)
parser.add_argument("--log", help="Simpan dimana lognya", default='./log/datapreparation')
args = parser.parse_args()

path = args.src
to = args.to + '/'
split = int(args.split)
os.makedirs(to, exist_ok=True)
logging.basicConfig(filename=args.log, filemode='w', format='[%(asctime)s] [%(levelname)s] [%(massage)s]')

#os.makedirs(to, exist_ok=True)

files = glob.glob(path+"/**/*.wav",recursive=True)
logging.info("Terdapat %i wav files ditemukan dari folder %s",len(files),path)


# In[70]:

def getname(filename):
    return os.path.basename(filename).split(".")[0]

def gettext(filename):
    filename = filename.replace('wav','txt')
    with open(filename, 'r') as f:
        txt = f.readline()
    return txt.replace('\n','')

def getabs(filename):
    return os.path.abspath(filename)

def writefile(filename,datas):
    with open(filename,'w') as f:
        for data in datas:
            f.write(getname(data))
            f.write("\t")
            f.write(getabs(data))
            f.write("\t")
            f.write(str(sox.file_info.duration(data)))
            f.write("\t")
            f.write(gettext(data))
            f.write("\n")
def cacah(text):
    txt = ""
    for c in text:
        if c not in list('abcdefghijklmnopqrstuvwxyz'):
            txt+='| '
        else:
            txt+=c+' '
            
    return txt+'|'
            


# In[82]:


os.makedirs(to+'/lists/', exist_ok=True)
if int(split) > 0 :
    k = int(split/100*len(files))
    test = random.sample(files,k)
    train = [ f for f in files if f not in test]
    writefile(to+'/lists/train.lst',train)
    writefile(to+'/lists/test.lst',test)
else:
    writefile(to+'/lists/train.lst',file)


# In[102]:


os.makedirs(to+'/txt/',exist_ok=True)

text = open(to+'/txt/text.txt','w')

lexicon = []
for f in files:
    lexicon.extend(gettext(f).split())
    text.writelines(gettext(f)+'\n')
text.close()


# In[110]:

lexicon = set(lexicon)

tokens = set()

with open( (to+"/txt/lexicon.txt"), 'w' ) as f:
    for l in lexicon:
        tokens |= set(cacah(l))
        print(l,cacah(l))
        f.writelines(l+" "+cacah(l)+"\n")
        
tokens.remove(' ')
with open ( (to+"/txt/tokens.txt")  , 'w' ) as f:
    for c in tokens:
        f.writelines(c+"\n")
    f.writelines("|")


elapsed_time = time.time() - start_time
logging.info("Proses selesai dengan waktu",elapsed_time/60,"menit")


