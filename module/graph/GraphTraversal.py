# -*- coding: utf-8 -*-
"""
Created on Fri May 10 15:47:52 2019

@author: gogho
"""


def BFS_path( graph, start, goal ):    
    queue = [(start, [start])]
    while queue:  
        (vertex, path) = queue.pop(0)
        for node in (graph[vertex] - set(path) ):
            if node == goal:
                return path + [node]
            else:
                queue.append((node, path + [node]))
    return -1

def BFS_path_adjmx( graph, start, goal ):    
    queue = [(start, [start])]
    while queue:  
        (vertex, path) = queue.pop(0)
        for i in range(len(graph[vertex])):
            if graph[vertex][i] == 0: 
                continue
            if i == goal and graph[vertex][i] ==1 :
                return path + [i]
            else:
                queue.append((i, path + [i]))
    return 1

    
if __name__ == '__main__':
    
    import sys
    from os import path
    module_root = path.dirname(path.dirname( path.abspath(__file__)))
    sys.path.append( path.dirname(module_root) )
    from modules.Graph.Graph import Graph, SaveGraph, OpenGraph
    filepath = path.dirname(module_root) + '//sample//graph4.txt'
    
    filepath = path.dirname(module_root) + '//sample//graph4.txt'
    g = Graph( OpenGraph(filepath) )
    print(g._graph)
    print( BFS_path( g._graph, 'c', 'e' ) )
    
    print(BFS_path_adjmx(g.output_AdjacentMatrix(),0,4))