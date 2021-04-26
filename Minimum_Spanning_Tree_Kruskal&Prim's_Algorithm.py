# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 21:23:56 2020

@author: Jing
"""

import pandas as pd
import numpy as np

am = pd.read_excel('MST data.xlsx')
# transform to  50*50
am = am.iloc[:,1:]
# df to array
am = am.to_numpy()
print(am)
print('------------------------------------------')
INF = float('inf')

# given num of nodes and a matrix, output upperright_matrix and lowerleft_matrix
def matrix(num_nodes,adjacency_matrix):
    global INF
    upperright_matrix = np.zeros((num_nodes,num_nodes))
    lowerleft_matrix = np.zeros((num_nodes,num_nodes))
    for i in range(num_nodes):
        for j in range(i+1,num_nodes):
            upperright_matrix[i][j] = adjacency_matrix[i][j]
            upperright_matrix[j][i] = upperright_matrix[i][j]
        for j in range(num_nodes):
            # don't count '0' weight edge
            if upperright_matrix[i][j]==0:
                upperright_matrix[i][j]=INF
            # # count '0' weight edge
            # if i==j:
            #     upperright_matrix[i][j]=INF
 
    for i in range(num_nodes):
        for j in range(i+1,num_nodes):
            lowerleft_matrix[j][i] = adjacency_matrix[j][i]
            lowerleft_matrix[i][j] = lowerleft_matrix[j][i]
        for j in range(num_nodes):
            # don't count '0' weight edge
            if lowerleft_matrix[i][j]==0:
                lowerleft_matrix[i][j]=INF
            # # count '0' weight edge
            # if i==j:
            #     upperright_matrix[i][j]=INF
            
    return upperright_matrix,lowerleft_matrix
#--------------------------------------------------------
# Kruskal's algorithm

# Find set of vertex i 
def find(i): 
    while parent[i] != i:
        i = parent[i]
    return i 

# Does union of i and j. It returns 
# false if i and j are already in same 
# set. 
def union(i, j): 
    a = find(i) 
    b = find(j) 
    parent[a] = b 

# Finds MST using Kruskal's algorithm 
def kruskalMST(cost): 
    mincost = 0 # Cost of min MST 

 	# Initialize sets of disjoint sets 
    for i in range(V): 
        parent[i] = i 

 	# Include minimum weight edges one by one 
    edge_count = 0
    while edge_count < V - 1: 
        min = INF
        a = -1
        b = -1
        for i in range(V): 
            for j in range(V): 
                if find(i) != find(j) and cost[i][j] < min: 
                    min = cost[i][j] 
                    a = i
                    b = j 
        union(a, b)
        # print('Edge {}:({}, {}) cost:{}'.format(edge_count, a, b, min)) 
        edge_count += 1
        mincost += min

    return mincost
#--------------------------------------------------------
# Prim's algorithm

# Returns true if edge u-v is a valid edge to be 
# include in MST. An edge is valid if one end is 
# already included in MST and other is not in MST. 
def isValidEdge(u, v, inMST): 
 	if u == v: 
         return False
 	if inMST[u] == False and inMST[v] == False: 
         return False
 	elif inMST[u] == True and inMST[v] == True: 
         return False
 	return True

def primMST(cost): 
    inMST = [False] * V 

 	# Include first vertex in MST 
    inMST[0] = True

 	# Keep adding edges while number of included 
 	# edges does not become V-1. 
    edge_count = 0
    mincost = 0
    while edge_count < V - 1: 

		# Find minimum weight valid edge. 
        minn = INF
        a = -1
        b = -1
        for i in range(V): 
            for j in range(V): 
                if cost[i][j] < minn: 
                    if isValidEdge(i, j, inMST): 
                        minn = cost[i][j] 
                        a = i 
                        b = j 

        if a != -1 and b != -1: 
            # print("Edge %d: (%d, %d) cost: %d" %(edge_count, a, b, minn)) 
            edge_count += 1
            mincost += minn 
            inMST[b] = inMST[a] = True

    return mincost
#--------------------------------------------------------
# Main
kruskal=[] #save the result of kruskal
prim=[] #save the result of prim
for i in [10,20,30,40,50]:
    V = i #num of nodes
    parent = [i for i in range(V)]
    am1,am2 = matrix(i, am)
    # print(am1)
    # print(am2)
    kruskal.append([i,kruskalMST(am1),kruskalMST(am2)])
    prim.append([i,primMST(am1),primMST(am2)])

print('kruskal\'s algorithm:(# of nodes, '
      'min cost of u-r triangle, l-l triangle)\n',kruskal)
print('------------------------------------------')
print('prim\'s algorithm:(# of nodes, '
      'min cost of u-r triangle, l-l triangle)\n',prim)