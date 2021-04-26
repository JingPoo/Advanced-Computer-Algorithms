# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 20:48:10 2020

@author: Jing
"""
#SRPT算法要再想想
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

#past_time = 0 


timelist=[]
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
        totalt += (currt + pj[jobs[i]-1])
        currt += pj[jobs[i]-1]  
    return totalt

LB_old = 9999
best_perm=[]
branch_list=[]
bound_list=[]
def DFS(remain_seq, walked_seq): 
    #未排工作,已排工作
    #init: [1,2,3,4,5,6], []
    all_seq=[1,2,3,4,5,6]
    global LB_old, best_perm, LB, past_time

    #判斷是否為該層第一個node
    first=True
    for i in remain_seq: 
       # print('i=',i)
        if first==False:
            walked_seq = walked_seq[:len(walked_seq)-1]
        
        walked_seq = walked_seq.copy()+[i] 
        remain_seq = [x for x in all_seq if x not in walked_seq]
        
        Cmax = completeTime(walked_seq)
        LB = Cmax + srpt(remain_seq)
        
        # print('w',walked_seq)
        # print('r',remain_seq)
        # print('Cmax',Cmax)
        # print('srpt',srpt(remain_seq))
        # print('LB',LB)
        first=False  
        
        # Bound
        if LB<=LB_old:
            #continue find
            DFS(remain_seq, walked_seq)
        if len(walked_seq)==6:
            if LB<=LB_old:
                cur_perm = walked_seq + remain_seq
                branch_list.append(cur_perm)
                # print('cur_perm:',cur_perm,'LB:',LB,'v')
                LB_old = LB
                best_perm = cur_perm
            else:
                cur_perm = walked_seq + remain_seq
                bound_list.append(cur_perm)
                # print('cur_perm:',cur_perm,'LB:',LB)
         
    return LB_old,best_perm

def DFS_withoutBB(remain_seq, walked_seq): 
    #未排工作,已排工作
    #init: [1,2,3,4,5,6], []
    all_seq=[1,2,3,4,5,6]
    global LB_old, best_perm, LB, past_time

    #判斷是否為該層第一個node
    first=True
    for i in remain_seq: 
       # print('i=',i)
        if first==False:
            walked_seq = walked_seq[:len(walked_seq)-1]
        
        walked_seq = walked_seq.copy()+[i] 
        remain_seq = [x for x in all_seq if x not in walked_seq]
        
        Cmax = completeTime(walked_seq)
        LB = Cmax + srpt(remain_seq)
        
        # print('w',walked_seq)
        # print('r',remain_seq)
        # print('Cmax',Cmax)
        # print('srpt',srpt(remain_seq))
        # print('LB',LB)
        first=False  
        
        DFS_withoutBB(remain_seq, walked_seq)
        if len(walked_seq)==6:
            if LB<=LB_old:
                cur_perm = walked_seq + remain_seq
                # print('cur_perm:',cur_perm,'LB:',LB,'v')
                LB_old = LB
                best_perm = cur_perm
            else:
                cur_perm = walked_seq + remain_seq
                # print('cur_perm:',cur_perm,'LB:',LB)
         
    return LB_old,best_perm


# def DFS2(jobs,l,r):
#     global LB_old
#     global best_perm
#     global LB
#     walked_seq=jobs[:l+1]
#     remain_seq=jobs[l+1:]
   
#     Cmax = completeTime(walked_seq)
#     LB = Cmax + srpt(remain_seq)
#     if l==r:
#         print(jobs)
#         if LB<=LB_old:
#             LB_old = LB
#             cur_perm = jobs.copy() #把現在最佳解copy一份(避免reference回最初jobs)
#             #print('cur_perm:',cur_perm,'LB:',LB)
#     for i in range(l,r+1):
#         walked_seq=jobs[:l+1]
#         remain_seq=jobs[l+1:]
#         #swapping
#         jobs[i],jobs[l] = jobs[l],jobs[i]
#         #calling permutation function
#         #by keeping the element at the index start fixed
#         if LB<=LB_old:
#             DFS2(jobs,l+1,r)
#         else:
#             pass
#         #restoring the array
#         jobs[i],jobs[l] = jobs[l],jobs[i]
#     return LB_old,best_perm
  
  

st1 = time.time()
print('---with BB---')
print('Objected value:',DFS(jobs,[])[0],'\nbest permutation:',DFS(jobs,[])[1])
run_time1 = time.time()-st1
print('runtime:',run_time1)
print('branch_list:\n',branch_list)
print('bound_list:\n',bound_list)
st2 = time.time()
print('\n---without BB---')
print('Objected value:',DFS_withoutBB(jobs,[])[0],'\nbest permutation:',DFS_withoutBB(jobs,[])[1])
run_time2 = time.time()-st2
print('runtime:',run_time2)
# print(timelist)


