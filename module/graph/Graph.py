# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 21:19:41 2019

@author: gogho
"""
from collections import defaultdict

class Graph:
    '''
    Undirected Graph
    member:
        _graph : the data of graog
            dictionary of set
            ex : {
                    a : { b,c },
                    b : { a,c },
                    c : { a,b }
                }
    '''
    def __init__(self, connections=[()]):
        self._graph = defaultdict(set)
        self.add_connections( connections )
        
    def add_connections(self, connections=[()]):
        for node1, node2 in connections:
            self._graph[node1].add( node2 )
            self._graph[node2].add( node1 )
            
    def output_AdjacentMatrix(self):
        adj_matrix = []
        for i in self._graph.keys():
            temp = []
            for j in self._graph.keys():
                if i==j:
                    temp.append(0)
                elif j in self._graph[i]:
                    temp.append( 1 )
                else:
                    temp.append(0)
            adj_matrix.append( temp )
        return adj_matrix
    
    def get_edges(self):
        edges = []
        temp = []
        for node1 in self._graph.keys():
            for node2 in self._graph[ node1 ]:
                if {node1,node2} not in temp:
                    edges.append( (node1,node2) )
                    temp.append( {node1,node2} )
        return edges
    
    def add_vertex(self, node):
        if node not in self._graph.keys():
            self._graph[node] = set()
        
    def add_edge(self, node1, node2):
        if node1 not in self._graph[ node2 ]:
            self._graph[ node2 ].add( node1 )
        if node2 not in self._graph[ node1 ]:
            self._graph[ node1 ].add( node2 )
        
    def delete_vertex(self, node1 ):
        # delete node
        self._graph.pop( node1 )
        
        # delete edge
        for NODE in self._graph.keys():
            if node1 in self._graph[NODE]:
                self._graph[NODE].remove( node1 )
    
    def delete_edge(self, node1, node2):
        if node2 in self._graph[ node1 ]:
            self._graph[node1].remove( node2 )
        if node1 in self._graph[ node2 ]:
            self._graph[node2].remove( node1 )


#=====================================================================================



def SaveGraph( Graph=object, filepath = '' ):
    '''
    from os import path
    filepath = path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) )) 
    filepath = filepath + '\\sample\\' + filename +'.txt'
    '''
    graph_string = ''
    for node1 in Graph._graph.keys():
        s, count = '', 0
        for i in Graph._graph[ node1 ]:
            s += str( i )
            if count != len( Graph._graph[ node1 ] )-1:
                count += 1
                s += ','
        graph_string += ( str(node1) + ':' + s + '\n' )
    with open( filepath, 'w+' ) as f:
        f.write( graph_string )
        
def OpenGraph( filepath = '' ):
    '''
    from os import path
    filepath = path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) )) 
    filepath = filepath + '\\sample\\' + filename +'.txt'
    '''
    temp = []
    connections = []
    with open( filepath, 'r' ) as f:
        data = f.readlines()
        for line in data:
            line = line[ : len(line)-1 ] # delete '\n'
            a = line.split( ':' )
            node1 = a[0]
            nodes = a[1].split( ',' )
            for i in nodes:
                if { node1, i } not in temp:
                    temp.append(  {node1, i } )
                    connections.append( (node1, i) )
    return connections
                    
            


if __name__ == '__main__':
    
    connections = [ ( 'a','b' ),
                       ( 'b','c' ),
                       ( 'c','d' ),
                       ( 'd','e' ),
                       ( 'e','f' ),
                       ( 'b','g' ),
                       ( 'd','g' ),
                       ( 'e','g' ),
                       ( 'a','f' )
                       ]
    g = Graph( connections )
    print(g._graph)
    g.delete_vertex('b')
    print(g._graph)
    a = g._graph