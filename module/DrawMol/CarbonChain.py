# -*- coding: utf-8 -*-
"""
Created on Tue May 28 15:29:37 2019

@author: gogho
"""
import math
def ChainExtend(base_coordinate=(0,0), inter_vector=(0,0), inter_direct='CCW', bond_order=2):
    
    direct = ['CW','CCW'][ inter_direct == 'CW' ]
    rot_angle = [ [60,-120, -120],[90,-90,-90, -90] ][ bond_order == 4 ] 
    rot_angle = [ angle*(3.14159/180) for angle in rot_angle  ]
    
    # first vector
    di = [1,-1][ direct == 'CCW' ]
    '''
    vector = ( math.cos(rot_angle[0]*di)*inter_vector[0]-math.sin(rot_angle[0]*di)*inter_vector[1],
                    math.sin(rot_angle[0]*di)*inter_vector[0] + math.cos(rot_angle[0]*di)*inter_vector[1])
    vector_list = [vector]
    # second & othor vector
    
    new_direct = ['CW','CCW'][ direct == 'CW' ]
    di = [1,-1][ new_direct == 'CCW' ]
    '''
    
    vector = inter_vector
    vector_list = []
    for angle in rot_angle:
        vector = ( math.cos(angle*di)*vector[0]-math.sin(angle*di)*vector[1],
                    math.sin(angle*di)*vector[0] + math.cos(angle*di)*vector[1])
        vector_list.append(vector)
    return vector_list, direct
    

if __name__=='__main__':
    vector = (2,3)
    coordinate = (0,0)
    vector_list, direct = ChainExtend(coordinate,vector,'CW',4)
    print(direct)
    coordinate_list=[]
    for i in vector_list:
        coordinate_list.append( (coordinate[0]+i[0], coordinate[1]+i[1]) )
    
    import matplotlib.pyplot as plt
    plt.figure()
    
    for i in range(len(vector_list)):
        plt.plot( [coordinate[0],coordinate_list[i][0]], [coordinate[1],coordinate_list[i][1]] )
    plt.show()
    
    
    