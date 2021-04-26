# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 12:58:26 2020

@author: Jing
"""
#SRPT算法要再想想
#用HEAP的性質讓計算變快

#比較runtime跟visit的Node數(算一次lb就+1)
#去想有什麼方法能讓runtime快一點e.g.同node長出來的樹Cmax不用重複算
#srpt要更有彈性e.g. walk:1,2 Cmax=17，remain:3,4,5,6 時讓開始時間在17
#LB_OLD改成UB_OLD
#UB_OLD更新後，把HEAP中可以砍的砍掉

import time
jobs=[1,2,3,4,5,6]
rj = [0,2,2,6,7,9]
pj = [6,2,3,2,5,2]

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

# past_time = 0 

def recursive(h,remain_time,cur_time):
    #h:等待排列的job,rt:idle time,cur_time:目前時間
    #global past_time 
    
    #沒空閒時間or沒工作在排隊
    if remain_time == 0 or len(h)==0: 
        return cur_time
    else:
        if h[0]>remain_time: #最短工作比cpu idle時間長
            h[0] -= remain_time
            cur_time += remain_time  
            remain_time = 0
        else: #最短工作比cpu idle時間短
            cur_time += h[0]
            remain_time -= h[0]
            
            if remain_time>0 and len(h)==0: #cpu還有idle time但已經沒job在排隊
                cur_time += remain_time
            #cpu還有idle time且有job在排隊
            recursive(h,remain_time,cur_time)
        return cur_time

       
def srpt(remain_job): #remain_job: list  
    heap=[] #比較剩餘時間
    cur_time = 0
    for i in remain_job:
        index = 0 #current index
        heap.append(pj[i-1])
        adjust(heap)
        #最後一個工作進來前
        if i!=remain_job[-1]:
            remain_time = rj[remain_job[index+1]-1]-rj[remain_job[index]-1] 
            #print(heap,'pt',past_time,'rt',remain_time)
            index += 1
            cur_time += recursive(heap,remain_time,cur_time)
                 
        else:
        #最後一個工作進來時
            for j in range(len(heap)):
                cur_time += heap[j] #剩下的工作不用管順序，全加到pt
    return cur_time


#Cmax
def completeTime(jobs):
    totalt = 0 # sum of completion time
    currt = 0 #current time
    for i in range(len(jobs)):
        if currt < rj[jobs[i]-1]: #if current time is smaller than job arrival time
            currt = rj[jobs[i]-1] 
        # totalt += (currt + pj[jobs[i]-1]) - rj[jobs[i]-1]
        totalt += (currt + pj[jobs[i]-1])
        currt += pj[jobs[i]-1]  
    return totalt

bestLB=999
def BFS(heap):
    all_seq = [1,2,3,4,5,6]
    global bestLB
    #每一層的第一個seq
    first=True
    for i in heap:
        #問題:heap中會有int與list type
        if type(i)==int:
            walked_seq = [i]
        else:
            walked_seq = i
        # print('walk',walked_seq)
        remain_seq = [x for x in all_seq if x not in walked_seq]
        # print('remain',remain_seq)
        Cmax = completeTime(walked_seq)
        LB = Cmax + srpt(remain_seq)
        
        # print(LB)
        if first==True:
            bestLB = LB
            #紀錄LB最小的seq
            seq_chosen = walked_seq
        first=False
        if LB<bestLB:
            bestLB = LB
            seq_chosen = walked_seq
            
    # perm = seq_chosen + remain_seq 
    # print('Cmax: ', Cmax)
    # print('srpt: ', srpt(remain_seq))
    print('BESTLB',bestLB,'BESTSEQ',seq_chosen) 
    
    #產生下一層的heap
    next_heap = heap 
    if len(seq_chosen)==1:
        #避免出錯
        next_heap.remove(seq_chosen[0])
    else:
        next_heap.remove(seq_chosen)
        
    temp_seq = [x for x in all_seq if x not in seq_chosen]
    for seq in temp_seq:
        x = seq_chosen.copy()
        x.append(seq)
        next_heap.append(x)
    # print('NEXTHEAP',next_heap)
    #終止條件
    if len(seq_chosen)==6:
        print('Objected value:',bestLB,'\nbest permutation:',seq_chosen) 
        return bestLB,seq_chosen
    else:
        BFS(next_heap)
        
st = time.time()
BFS(jobs)
run_time = time.time()-st
print('runtime:',run_time)
# print('Ans:',BFS(jobs))
    
    
    
    