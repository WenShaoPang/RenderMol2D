# -*- coding: utf-8 -*-
"""
Created on Mon May  6 21:13:24 2019

@author: gogho

reference:
    GeeksforGeeks : Bridges in a graph
    https://www.geeksforgeeks.org/bridge-in-a-graph/
    
    Tarjan's bridge-finding algorithm
    https://www.slideshare.net/TraianRebedea/algorithm-design-and-complexity-course-8

    Biconnected Components
    https://www.geeksforgeeks.org/biconnected-components/
    
    Articulation Points (or Cut Vertices) in a Graph
    https://www.geeksforgeeks.org/articulation-points-or-cut-vertices-in-a-graph/
"""




from collections import defaultdict 
   
#This class represents an undirected graph using adjacency list representation 
class Tarjan_Bridge: 
    def __init__(self, g=[]):
        self.graph = g
        self.Time = 0
        self.V = len(g)
        self.BridgeEdge=[]
        #--- 用於尋找 articulation
        self.articulation=[]
        #--- 用於建立 biconnected subgraph.---
        self.subgraph = []
        self.stack = []
        #--- 用於搜尋 back edges---
        self.backedges = []
    
    
    # A recursive function that finds and prints bridges 
    # using DFS traversal 
    # u --> The vertex to be visited next 
    # visited[] --> keeps tract of visited vertices 
    # disc[] --> Stores discovery times of visited vertices 
    # parent[] --> Stores parent vertices in DFS tree
    
    def bridgeUtil(self,u, visited, parent, low, disc): 
  
        # Mark the current node as visited and print it 
        visited[u]= True
  
        # Initialize discovery time and low value 
        disc[u] = self.Time 
        low[u] = self.Time 
        self.Time += 1
        
        connect_vertices = []
        for i in range( len(self.graph) ):
            if self.graph[u][i] == 1:
                connect_vertices.append(i)
        
        #Recur for all the vertices adjacent to this vertex 
        for v in connect_vertices: 
            # If v is not visited yet, then make it a child of u 
            # in DFS tree and recur for it 
            if visited[v] == False : 
                parent[v] = u 
                self.stack.append( (u,v) )
                self.bridgeUtil(v, visited, parent, low, disc) 
  
                # Check if the subtree rooted with v has a connection to 
                # one of the ancestors of u 
                low[u] = min(low[u], low[v]) 
  
  
                ''' If the lowest vertex reachable from subtree 
                under v is below u in DFS tree, then u-v is 
                a bridge'''
                if low[v] > disc[u]: 
                    self.BridgeEdge.append([u,v])
                    #print ("%d %d" %(u,v)) 
                if low[v] >= disc[u] and parent[u] != -1 :
                    self.articulation[u] = True
                    
                    w, temp = -1, []
                    while w != (u,v):
                        w = self.stack.pop()
                        temp.append( w )
                    self.subgraph.append( temp )
                      
            elif v != parent[u]: # Update low value of u for parent function calls. 
                low[u] = min(low[u], disc[v]) 
                if low[u] >= disc[v]:
                    self.stack.append( (u,v) )
                 
                # back edge
                if disc[u] == low[v]:
                    self.backedges.append( (u,v) )
  
  
    # DFS based function to find all bridges. It uses recursive 
    # function bridgeUtil() 
    def bridge(self): 
   
        # Mark all the vertices as not visited and Initialize parent and visited,  
        # and ap(articulation point) arrays 
        visited = [False] * (self.V) 
        disc = [float("Inf")] * (self.V) 
        low = [float("Inf")] * (self.V) 
        parent = [-1] * (self.V) 
        self.articulation = [False]*(self.V)
        # Call the recursive helper function to find bridges 
        # in DFS tree rooted with vertex 'i' 
        for i in range(self.V): 
            if visited[i] == False: 
                self.bridgeUtil(i, visited, parent, low, disc) 
                
            if self.stack:
                w, temp = -1, []
                while self.stack:
                    w = self.stack.pop()
                    temp.append( w )
                self.subgraph.append( temp )
                
          
def SearchBridgeEdge(g=[]):
    b = Tarjan_Bridge(g)
    b.bridge()
    return b.BridgeEdge

def SearchArticulationPoint( g=[] ):
    a = Tarjan_Bridge(g)
    a.bridge()
    return a.articulation

def SearchBiconnectedSubgraph( g = [] ):
    a = Tarjan_Bridge(g)
    a.bridge()
    return a.subgraph

def SearchBackEdges( g=[] ):
    a = Tarjan_Bridge(g)
    a.bridge()
    return a.backedges

if __name__ == '__main__':
    try:
        from modules.Graph.Graph import Graph, SaveGraph, OpenGraph
    except:
        import sys
        from os import path
        module_root = path.dirname(path.dirname( path.abspath(__file__)))
        sys.path.append( path.dirname(module_root) )
        from modules.Graph.Graph import Graph, SaveGraph, OpenGraph
    filepath = path.dirname(module_root) + '//sample//graph4.txt'
    
    g = Graph( OpenGraph(filepath) )
    print(g._graph)
    print( g.output_AdjacentMatrix() )
    answer = SearchBridgeEdge(g.output_AdjacentMatrix())
    for i in range( len(answer) ):
        print( 'Bridge Edge = ( {0},{1} )'.format( 
                list(g._graph.keys())[answer[i][0]], 
                list(g._graph.keys())[answer[i][1]] ) )
        
    ar = SearchArticulationPoint( g.output_AdjacentMatrix() )
    for i in range(len(ar)):
        if ar[i] == True:
            print( list(g._graph.keys())[ i ] ) 
            
    a = SearchBiconnectedSubgraph(g.output_AdjacentMatrix()  )
    print(a)
    print( SearchBackEdges( g.output_AdjacentMatrix() ) )
        
   