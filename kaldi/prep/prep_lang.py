#!/usr/bin/env python
# coding: utf-8

# In[2]:


import glob
import sys
text = []

all_dir = glob.glob(sys.argv[1]+"/**/*.txt", recursive=True)

for x in all_dir:    
    with open(x) as f:
        text.extend(f.readline().split())


# In[3]:


settext = set(text)


# In[4]:


print(len(text))


# In[5]:


print(len(settext))


# In[127]:


def lexiconize(kata):
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
        except:
            pass
    x = [c for c in x if c != '#']
    
    return ' '.join(x)


# In[128]:


import re
ex = r"(<|\[)\w*(>|\])"

silence_phone = open('silence_phone.txt','w')
lexicon = open('lexicon.txt', 'w')

for x in settext:
    if re.match(ex, x):
        print(x)
        silence_phone.write(x+'\n')
    else:
        lexicon.write(x+" "+lexiconize(x)+'\n')
        
silence_phone.close()
lexicon.close()


# In[130]:


phone= []
with open('lexicon.txt','r') as f:
    for x in f:
        y = x.split()
        y.pop(0)
        phone.extend(y)

phone = set(phone)

phonef = open('nonsilence_phones.txt','w')
for c in phone:
    phonef.write(c+'\n')
    
phonef.close()
