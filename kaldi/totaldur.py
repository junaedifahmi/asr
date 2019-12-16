#!/usr/bin/env python
# coding: utf-8

# In[19]:


import sys


a = []
with open(sys.argv[1], 'r') as f:
    a = f.readlines()
    
dur = [ float(x.split()[1]) for x in a ]
print ( sum(dur)/60/60, " jam")


# In[ ]:




