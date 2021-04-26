# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 11:17:03 2020

@author: Jing
"""

def completeTime(jobs):
    totalt = 0 # sum of completion time
    currt = 0 #current time
    for i in range(len(jobs)):
        if currt < rj[jobs[i]-1]: #if current time is smaller than job arrival time
            currt = rj[jobs[i]-1] 
        totalt += (currt + pj[jobs[i]-1]) - rj[jobs[i]-1]
        currt += pj[jobs[i]-1]  
    return totalt

perm_count = 0
best_time = 1000
def perm(jobs,l,r):
    global perm_count
    global best_time
    global best_perm
    
    if l==r:
        print(jobs,completeTime(jobs))
        perm_count += 1 
        if completeTime(jobs) < best_time:
            best_time = completeTime(jobs)
            best_perm = jobs.copy() #把現在最佳解copy一份(避免reference回最初jobs)
            print('bp',best_perm,'t',best_time)

    for i in range(l,r+1):
        #swapping
        jobs[i],jobs[l] = jobs[l],jobs[i]
        #calling permutation function
        #by keeping the element at the index start fixed
        perm(jobs,l+1,r)
        #restoring the array
        jobs[i],jobs[l] = jobs[l],jobs[i]
    
    
jobs=[1,2,3,4,5,6]
rj = [0,2,2,6,7,9]
pj = [6,2,3,2,5,2]
perm(jobs,0,5)
print('total perm.:',perm_count)
print('best perm.:',best_perm)
print('best time:',best_time)




