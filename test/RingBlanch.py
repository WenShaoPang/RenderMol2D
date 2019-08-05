# -*- coding: utf-8 -*-
"""
Created on Mon May 27 16:05:50 2019

@author: gogho
"""
import math
def RingBlanch(ring_coordinate=[], ring_index=0, bond_length=1):
    center_x, center_y = 0, 0
    for vertex in ring_coordinate:
        center_x += vertex[0]
        center_y += vertex[1]
    center_x /= len(ring_coordinate)
    center_y /= len(ring_coordinate)
    vector = ( ring_coordinate[ring_index][0] - center_x,
              ring_coordinate[ring_index][1] - center_y)
    vector = ( vector[0]*bond_length/math.sqrt( vector[0]**2 + vector[1]**2 ),
              vector[1]*bond_length/math.sqrt( vector[0]**2 + vector[1]**2 ))
    new_vertex = ( ring_coordinate[ring_index][0] + vector[0],
                  ring_coordinate[ring_index][1] + vector[1])
    return new_vertex




if __name__ == '__main__':
    ring1 = [(0.851, 0), (0.263, 0.809), (-0.688, 0.5), 
         (-0.688, -0.5), (0.263, -0.809)]
    index = 0
    vertex = RingBlanch( ring1, index )
    
    print(vertex)
    
    import matplotlib.pyplot as plt
    plt.figure()
    ring1.append( ring1[0] )
    
    x, y =[], []
    for node in ring1:
        x.append( node[0] )
        y.append( node[1] )
    plt.plot(x,y)
    plt.plot( [ring1[index][0],vertex[0]], [ring1[index][1],vertex[1]] )
    plt.xlim((-2,2))
    plt.ylim((-2,2))
    plt.show()