# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 10:10:43 2020

@author: Jing
"""

#Implementation of the SRPT rule

import time
import pandas as pd

df = pd.read_excel('test instance.xlsx',header=None)
p = df.iloc[0,1:].values.tolist() #p_j
print('p_j:',p)
r = df.iloc[1,1:].values.tolist() #r_j
print('r_j:',r)

def min_heapify(h,i):
    smallest = i
    left = 2*i+1 #because array start at 0
    right = 2*i+2
    length = len(h)
    
    if left<length and h[i]>h[left]:
        smallest = left
    if right<length and h[smallest]>h[right]:
        smallest = right
    if smallest != i:
        h[i],h[smallest] = h[smallest],h[i]
        min_heapify(h,smallest)

def adjust(h):
    length = len(h)
    for i in range(length//2-1,-1,-1):
        min_heapify(h,i)
      
def pop(h):
    length = len(h)
    if length == 0:
        return 0
    else:
        min = h[0]
        del h[0]
        return min

  
past_time = 0 
heap=[] #比較剩餘時間

def recursive(h,rt):
    global past_time 
    if rt == 0 or len(h)==0:
        return
    else:
        if h[0]>rt: #最短工作比cpu idle時間長
            h[0] -= rt
            past_time += rt  
            rt = 0
        else: #最短工作比cpu idle時間短
            past_time += h[0]
            rt -= h[0]
            pop(h)
            if rt>0 and len(h)==0: #cpu還有idle time但已經沒job在排隊
                past_time += rt
            recursive(h,rt)
            
st = time.time() 
        
x=100 #number of jobs
for i in range(x):   
    heap.append(p[i])
    adjust(heap)
    if i<(x-1):
        remain_time = r[i+1]-r[i] 
        print(heap,'pt',past_time,'rt',remain_time)
        recursive(heap,remain_time)
    else:
    #最後一個工作進來時
        for j in range(len(heap)):
            past_time += heap[j] #剩下的工作不用管順序，全加到pt
   
elapsed_run_time = time.time()-st
print('number of jobs:',x)         
print('elapsed run time:',elapsed_run_time)
print('sum of job completion times:',past_time)
        
'''
    20:166
    40:367
    60:567
    80:804
    100:1012
'''   
        



    
    
