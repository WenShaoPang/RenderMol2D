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
    for i in sequenceRing1:
        if i in sequenceRing2:
            matchElem.append(i)
    return matchElem

def AdjustRingSequence( sequence=[], commonElem=[] ):
    '''
    def AdjustSequence( sequence=[], index=0, reverse=False ):
        sequence = sequence[index:] + sequence[:index] 
        if reverse == True:
            sequence.reverse()
            sequence.insert( 0, sequence.pop() )
        return sequence

    reverse = False
    if sequence.index(commonElem[-1]) < sequence.index(commonElem[0]) or (
        abs( sequence.index(commonElem[-1]) - sequence.index(commonElem[0]) ) > 1
    ):
        reverse = True
    return AdjustSequence( sequence, sequence.index(commonElem[0]), reverse )
    '''
    visit, connect, queue =[], [], []
    new_sequence = []
    for i in range( len(sequence) ):
        if i ==  ( len(sequence) -1 ):
            connect.append(  [i-1, 0] )
        elif i == 0:
            connect.append( [1,-1] )
        else:
            connect.append( [i-1,i+1] )
            
    new_sequence.append( commonElem[0] )
    new_sequence.append( commonElem[1] )
    visit = [ commonElem[0], commonElem[1] ]
    queue.append( commonElem[1]  )
    
    while queue:
        elem = queue.pop(0)
        for i in connect[ sequence.index( elem ) ]:
            if sequence[i] not in visit:
                queue.append( sequence[i] )
                new_sequence.append( sequence[i] )
                visit.append( sequence[i] )
    return new_sequence

def PolygonDirect(ring_coordinate=[]):
    ''' 計算一個 Polygon 的方向, 順時針(CW) or 逆時針(CCW) '''
    direct, index = 'CCW', 0
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
    sequence2 =  AdjustRingSequence(ring_sequence2.copy(), attachAtoms)

    direct = PolygonDirect(ring_coordinate1)
    new_direct = ['CCW','CW'][direct=='CCW']
    ring2 = GenerationAttachFusedRing( sequence2, 
                                      ring_coordinate1[ring_sequence1.index(attachAtoms[0])],
                                      ring_coordinate1[ring_sequence1.index(attachAtoms[1])],
                                      new_direct
                                      )
    return ring2, sequence2

def RenderRingSystem(ring_system=[],init_ring_series=[],init_ring_coordinate=[]):
    '''
    import:
        ring_system : fused ring , [  [ring1], [ring2], [ring3],...  ]
        init_ring_series : fused ring 外的獨立 ring, 由此 ring 去延伸 fused ring
                        格式: [ sequence ]
        init_ring_coordinate : fused ring 外的獨立 ring 的各點座標, 格式 : [ coordinate(x,y), (x,y),... ]
    return coordinate:
        [  [ring1:(x,y),(x,y)...],  [ring2],  [ring3],...  ]
    '''
    # 暫存計算結果
    # 由於為了快速尋找一個ring全部頂點的座標, 故以ring為單位做儲存
    ring_coord_system = [ init_ring_coordinate.copy() ]  
    ring_sequence_system = [ init_ring_series.copy() ]
    ring_base_sequence = [ init_ring_series.copy() ]  

    # 紀錄已計算過之座標,用於確認是否有重複計算的頂點,以確保相同頂點卻有不同座標之情況
    # 同時也作為 output 結果
    sequence, coord = init_ring_series.copy(), init_ring_coordinate.copy()

    for base_ring, attach_ring in ring_system:
        base_ring_coord = ring_coord_system[ ring_base_sequence.index( base_ring ) ]

        ring2,seq = GenerateFusedRing( 
            ring_sequence_system[ ring_base_sequence.index( base_ring ) ].copy(), 
            base_ring_coord.copy(), attach_ring )
        # 檢查是否有重複計算的頂點
        count=0
        for i in seq:
            if i in sequence:
                # 若有已計算過的頂點, 則使用該座標
                ring2[ count ] = coord[ sequence.index(i) ]
            else:
                # 若為未被計算過的頂點, 則記錄起來
                sequence.append(i)
                coord.append( ring2[count] )
            count += 1
        # ----- 保存計算完畢之 ring 的結果 -----
        ring_sequence_system.append( seq.copy() )
        ring_coord_system.append( ring2.copy() )
        ring_base_sequence.append( attach_ring.copy() )
    return sequence, coord


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
    
        
    ring_coord_system = ring_coord_system + RenderRingSystem(ring_system, sequence1,ring1)[0]
    print( ring_coord_system )
    import matplotlib.pyplot as plt
    plt.figure()
    for ring in ring_coord_system:
        x,y=[],[]
        for elem in ring:
            x.append(elem[0])
            y.append(elem[1])
        plt.plot(x,y)
    plt.show()



# ----- ------ ------ 修改前版本 ------ ------ -----
"""
def RenderRingSystem(ring_system=[],init_ring_series=[],init_ring_coordinate=[]):
    '''
    import:
        ring_system : fused ring , [  [ring1], [ring2], [ring3],...  ]
        init_ring_series : fused ring 外的獨立 ring, 由此 ring 去延伸 fused ring
                        格式: [ sequence ]
        init_ring_coordinate : fused ring 外的獨立 ring 的各點座標, 格式 : [ coordinate(x,y), (x,y),... ]
    return coordinate:
        [  [ring1:(x,y),(x,y)...],  [ring2],  [ring3],...  ]
    '''
    ring_coord_system = []  # 存放座標計算結果
    ring_sequence_system = []

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
        ring_sequence_system.append( seq.copy() )
        
        base_sequence = seq.copy()
        base_ring_coordinate = ring2.copy()
    return [j for sub in ring_coord_system for j in sub], [j for sub in ring_sequence_system for j in sub]
"""