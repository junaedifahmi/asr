#!/usr/bin/env python
# coding: utf-8

# # Make Text

# In[46]:


def get_name(x):
    return x.split("/")[-1].split(".")[0]


# In[25]:


import glob


all_dir = glob.glob("Call/*/*/*.txt")

txt = open('text','w')
for x in all_dir:    
    with open(x) as f:
        txt.writelines(get_name(x)+" "+f.readline()+"\n")
txt.close()


# In[59]:


get_name(all_dir[-1])


# # Make SCP

# In[36]:


all_wav = glob.glob("Call/*/*/*.wav")

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

