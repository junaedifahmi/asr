#!/usr/bin/env python
# coding: utf-8

# # Make Text

# In[46]:


def get_name(x):
    return x.split("/")[-1].split(".")[0]


# In[25]:


import glob
import sys
import os


if len(sys.argv) < 3 :
    print("Kurang argument")
    sys.exit()

all_dir = glob.glob(sys.argv[1]+"/**/*.txt",recursive=True)
to = sys.argv[2] + '/'

os.makedirs(to, exist_ok=True)


txt = open(to+'text','w')
for x in all_dir:    
    with open(x) as f:
        text = f.readline()+"\n"
        txt.writelines(get_name(x)+" "+text)
txt.close()

# In[59]:


#get_name(all_dir[-1])


# # Make SCP

# In[36]:


all_wav = glob.glob(sys.argv[1]+"/**/*.wav", recursive=True)

wav = open(to+'wav.scp','w')

for x in all_wav:
    wav.writelines( get_name(x)+" "+x+"\n")
wav.close()


# # Make utt2spk

# In[43]:


utt = open(to+'utt2spk','w')

for x in all_wav:
    utt.writelines(get_name(x)+" "+get_name(x)+"\n")
utt.close()

