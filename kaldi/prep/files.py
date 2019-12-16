#!/usr/bin/env python
# coding: utf-8

# # Make Text

# In[46]:


def get_name(x):
    return x.split("/")[-1].split(".")[0]


# In[25]:


import glob
import sys

all_dir = glob.glob(sys.argv[1]+"/**/*.txt",recursive=True)

txt = open('text','w')
txt_all = open('text_all', 'w')
for x in all_dir:    
    with open(x) as f:
        txt.writelines(get_name(x)+" "+f.readline()+"\n")
        txt_all.writelines(f.readline()+"\n")
txt.close()
txt_all.close()

# In[59]:


#get_name(all_dir[-1])


# # Make SCP

# In[36]:


all_wav = glob.glob(sys.argv[1]+"/**/*.wav", recursive=True)

wav = open('wav.scp','w')

for x in all_wav:
    wav.writelines( get_name(x)+" "+x+"\n")
wav.close()


# # Make utt2spk

# In[43]:


utt = open('utt2spk','w')

for x in all_wav:
    utt.writelines(get_name(x)+" "+get_name(x)+"\n")
utt.close()

