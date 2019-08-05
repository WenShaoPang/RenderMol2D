# -*- coding: utf-8 -*-
"""
Created on Fri May 24 08:38:45 2019

@author: gogho

基本條件:
    1. fuse ring
    2. 至少有一個相鄰邊
    3. ring 至少有三個點
    4. attachAtom list 之序列於 ring 1 中必為正序列
    
待修改:
    1. 若fusering中, 有頂點已給定座標(除了計算時所用之相鄰邊的頂點), 則使用該座標
        避免多重稠合ring之圖形未能相鄰

"""
import math

def SearchAttachAtom(sequenceRing1=[],sequenceRing2=[]):
    matchElem = []
    for i in sequenceRing2:
        if i in sequenceRing1:
            matchElem.append(i)
    return matchElem

def AdjustSequence( sequence=[], index=0, reverse=False ):
    sequence = sequence[index:] + sequence[:index] 
    if reverse == True:
        sequence.reverse()
        sequence.insert( 0, sequence.pop() )
    return sequence

def AdjustRingSequence( sequence=[], commonElem=[] ):
    reverse = False
    if sequence.index(commonElem[-1]) < sequence.index(commonElem[0]):
        reverse = True
    return AdjustSequence( sequence, sequence.index(commonElem[0]), reverse )

def PolygonDirect(ring_coordinate=[]):
    direct = 'CCW'
    index=0
    lowest_y = ring_coordinate[0][1]
    for i in range(len(ring_coordinate)):
        if ring_coordinate[i][1] < lowest_y:
            lowest_y = ring_coordinate[i][1]
            index = i
    
    if index+1 >= len(ring_coordinate):
        next_index = 0
    else:
        next_index = index +1
    direct = ['CCW','CW'][ring_coordinate[next_index][0] <= ring_coordinate[index][0]]
    
    return direct

def GenerationAttachFusedRing( sequence=[], point1=(0,0), point2=(0,0), direct='CW' ):
    rot_angle = 360/len(sequence) * (3.14159/180)
    if direct == 'CW':
        rot_angle *= -1
    ring_coordinate = [ point1, point2 ]
    vector_x, vector_y = point2[0]-point1[0], point2[1]-point1[1]
    x, y = point2[0], point2[1]
    for i in range( len(sequence)-2):
        new_vector_x = math.cos(rot_angle)*vector_x - math.sin( rot_angle )*vector_y
        new_vector_y = math.sin(rot_angle)*vector_x + math.cos( rot_angle )*vector_y
        x += new_vector_x
        y += new_vector_y
        vector_x = new_vector_x
        vector_y = new_vector_y
        ring_coordinate.append( (x,y) )
    return ring_coordinate
    
def GenerateFusedRing( ring_sequence1=[], ring_coordinate1=[], 
                      ring_sequence2=[] ):
    '''
    ring 1 : the base ring that had been built in coordination
    ring 2 : the ring that will fuse with ring 1
    ring_sequence1 : the sequence of ring 1 ( label )
    ring_coordinate1 : the coordinates of vertice of ring 1
    ring_sequence2 : the sequence of ring 2 ( label )
    '''
    attachAtoms = SearchAttachAtom(ring_sequence1, ring_sequence2)
    #print('attachAtoms  ', attachAtoms)
    sequence2 =  AdjustRingSequence(ring_sequence2.copy(), attachAtoms)
    #print('ring_sequence1 ',ring_sequence1)
    #print( ring_coordinate1 )
    
    direct = PolygonDirect(ring_coordinate1)
    new_direct = ['CCW','CW'][direct=='CCW']
    ring2 = GenerationAttachFusedRing( sequence2, 
                                      ring_coordinate1[ring_sequence1.index(attachAtoms[0])],
                                      ring_coordinate1[ring_sequence1.index(attachAtoms[1])],
                                      new_direct
                                      )
    return ring2, sequence2

def RenderRingSystem(ring_system=[],init_ring_series=[],init_ring_coordinate=[]):
    ring_coord_system = []  # 存放座標計算結果
    
    base_sequence = init_ring_series.copy()
    base_ring_coordinate = init_ring_coordinate.copy()
    
    #用於確認是否有相同頂點, 卻不同座標之情況
    sequence, coord = base_sequence.copy(), base_ring_coordinate.copy()
    
    seq = [] # 暫存 ring的 sequence 序列
    for ring in ring_system:
        ring2,seq = GenerateFusedRing(base_sequence,base_ring_coordinate,ring)
        ring2.append( ring2[0] )
        
        # 處理重複頂點, 重新設定為已給定之座標
        count=0
        for i in seq:
            if i in sequence:
                ring2[ count ] = coord[ sequence.index(i) ]
            else:
                sequence.append(i)
                coord.append( ring2[count] )
            count += 1
        # 存放已計算之座標
        ring_coord_system.append(ring2.copy())
        
        base_sequence = seq.copy()
        base_ring_coordinate = ring2.copy()
    return ring_coord_system


if __name__ == '__main__':
    ring1 = [(0.851, 0), (0.263, 0.809), (-0.688, 0.5), 
         (-0.688, -0.5), (0.263, -0.809)]
    sequence1 = [1,2,3,4,5]

    sequence2 = [8,9,10,1,2,7]
    
    
    ring_system = [sequence2.copy()]
    ring_system.append( [ 9,10,11,12,13,14 ] )
    ring_system.append( [13,14,15,16,17,18] )
    ring_system.append( [14,15,19,20,8,9] )
    
    ring_coord_system = [ring1.copy()]
    ring_coord_system[0].append( ring_coord_system[0][0] )
    
        
    ring_coord_system = ring_coord_system + RenderRingSystem(ring_system, sequence1,ring1)
    
    import matplotlib.pyplot as plt
    plt.figure()
    for ring in ring_coord_system:
        x,y=[],[]
        for elem in ring:
            x.append(elem[0])
            y.append(elem[1])
        plt.plot(x,y)
    plt.show()


