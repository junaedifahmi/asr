#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sys

def plot_wer(data,title):
    plt.figure()
    plt.plot(data)
    plt.suptitle(title, fontsize=20)
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("WER", fontsize=12)
    plt.savefig(title+'.svg')
    
def plot_loss(data, title):
    plt.figure()
    plt.plot(data)
    plt.suptitle(title, fontsize=20)
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("Loss", fontsize=12)
    plt.savefig(title+'.svg')


# In[2]:


path = sys.argv[1]

df = pd.read_csv(path+'/001_perf',comment='#',delim_whitespace=True,header=None)


# In[3]:


plot_wer(df[13],path+"/train_wer")
plot_wer(df[17],path+"/test_wer")
plot_loss(df[14],path+"/loss")


# In[28]:


min_wer = df[df[17] == df[17].min()][17].to_list()

text = '#'*20+"\nHasil terbaik diperoleh dengan Word Error Rate sebesar "+str(min_wer)+" percent"
print(text, file=open(path+'/summary','a'))


# In[29]:


a = df.iloc[[0, -1]][1].to_list()
FMT = '%H:%M:%S'
tdelta = datetime.strptime(a[1], FMT) - datetime.strptime(a[0], FMT)
ttraining = str(tdelta.total_seconds()/60/60)

text = '#'*20+"\nDengan waktu training yang dibutuhkan sebesar ["+ttraining+"] jam."
print(text, file=open(path+'/summary','a'))


# In[30]:


hrs = list(df[21].unique())

text = '#'*20+"\nData latih dan data validasi yang digunakan berjumlah "+ str(hrs) + " jam"
print(text, file=open(path+'/summary','a'))

