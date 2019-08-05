# -*- coding: utf-8 -*-
"""
Created on Mon May 27 21:49:05 2019

@author: gogho
"""
import math

def buildCycle(pre_direct='CCW', inter_vector=(1,0), start_coordinate=(0,0), 
               ring_sequence=[], index=0, bond_length=1):
    x, y = start_coordinate[0], start_coordinate[1]
    ring_coordinate = [start_coordinate]
    rot_angle = 360 / len(ring_sequence) *(3.14159/180)
    
    first_rot_angle = (3.14159 - rot_angle)/2
    # the secondary vertex
    new_vector = ( math.cos(first_rot_angle)*inter_vector[0] - math.sin(first_rot_angle)*inter_vector[1],
                  math.sin(first_rot_angle)*inter_vector[0] + math.cos(first_rot_angle)*inter_vector[1])
    x , y = x + new_vector[0], y + new_vector[1]
    ring_coordinate.append( ( x, y ) )
    
    for i in range(len(ring_sequence)-2):
        new_vector = ( math.cos(-rot_angle)*new_vector[0] - math.sin(-rot_angle)*new_vector[1],
                  math.sin(-rot_angle)*new_vector[0] + math.cos(-rot_angle)*new_vector[1])
        x , y = x + new_vector[0], y + new_vector[1]
        ring_coordinate.append( ( x, y ) )
        
    # return the coordinate of ring and return the sequence of ring adjusted
    return ring_coordinate, ring_sequence[index:]+ring_sequence[:index]
    

if __name__ == '__main__':
    start=(0,0)
    in_vector = (1,1)
    ring_coordinate,sequecne = buildCycle( inter_vector=in_vector, ring_sequence=[1,2,3,4,5],
                                 start_coordinate=( start[0]+in_vector[0], start[1]+in_vector[1] )
                                 )
    
    
    import matplotlib.pyplot as plt
    plt.figure()
    x , y = [], []
    for node in ring_coordinate:
        x.append( node[0] )
        y.append( node[1] )
    x.append( ring_coordinate[0][0] )
    y.append( ring_coordinate[0][1] )
    plt.plot( [start[0], start[0]+in_vector[0]], [start[1],start[1]+in_vector[1]] )
    plt.plot(x,y)
    plt.xlim( (-3,3) )
    plt.ylim( (-3,3) )
    plt.show()