# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:17:38 2019

@author: gogho
"""

def molCycleSearch( graph=[[]], start=0):
    # 尋找 graph 結構中全部的最小單位環
    # ----- Breadth-First Search -----
    queue = [(start, [start])]
    visit = [False]*len(graph)
    visit[start] = True
    bfs_path = [[]]*len(graph)
    while queue:
        (vertex, path) = queue.pop(0)
        for i in range(len(graph[vertex])):
            if graph[vertex][i] == 0: 
                continue
            if visit[i]==False and graph[vertex][i] ==1 :
                visit[i] = True
                queue.append((i, path + [i]))
                bfs_path[i] = path+[i]
                
    # ----- Genrate Connection tabel ------
    temp, edges = [], []
    for i in range( len(graph) ):
        for j in range( len(graph) ):
            if i == j:
                continue
            if graph[i][j] == 1 and {i,j} not in temp:
                temp.append( {i,j} )
                edges.append( (i,j) )
    # ----- Search Cycle -----
    temp = []
    for e in edges:
        if bfs_path[e[0]] == [] or bfs_path[e[1]] == []:
            continue
        if (bfs_path[e[0]][-1] not in bfs_path[e[1]] and 
            bfs_path[e[1]][-1] not in bfs_path[e[0]] ):
            i,j = 1,1
            while (bfs_path[e[0]][-i] not in bfs_path[e[1]] or 
            bfs_path[e[1]][-j] not in bfs_path[e[0]] ):
                if (bfs_path[e[0]][-i] not in bfs_path[e[1]]):
                    i += 1
                if (bfs_path[e[1]][-j] not in bfs_path[e[0]] ):
                    j += 1
                if bfs_path[e[0]][-i] == bfs_path[e[1]][-j] :
                    break
            back_list = (bfs_path[e[1]][-j+1:])
            back_list.reverse()
            temp.append( bfs_path[e[0]][-i:] + back_list)
                
    return temp