def getMolCoordinate( mol:Molecule, mol_Info:MolInfo, bond_length=1 ):
    queue, direct = [], 'CCW'
    visitVertice = SequenceRecord() # 紀錄拜訪之 nodes
    graphCoordinate = [0] * ( len(mol.Atoms) ) 
    
    # ---------- 初始化位置 ----------
    ans, fused_ring = mol_Info.ifInFusedRing( mol.Atoms[0] )
    if ans :
        # ----- Fused Ring 的情況 -----
        # 在函式中, 會先計算一個初始 ring 的座標, 接著再跟著此 ring 向外延伸 Fused Ring
        # 回傳為一個 1D 序列與 1D 序列座標
        sequence, coord = InitialFusedRing( fused_ring.sortAttachRing() , bond_length )
    else:
        ans, ring = mol_Info.ifInRing( [0] )
        if ans:
            # ----- Ring 的情況下 -----
            sequence, coord = InitialDraw( ring, bond_length )
        else:
            # ------ 單一原子的情況下 -----
            sequence, coord = InitialDraw( [ 0 ], bond_length )
    testDraw(coord)
    
    # 紀錄已拜訪之頂點
    visitVertice.add(sequence, coord)
    
    graphCoordinate[0] = coord
    # 初始化向量, 若初始 sequence 為 ring 則向量為(0,0)
    if len(sequence) > 1:
        # 若遇到 從環開始延伸向量的情況, 則給向量為(0,0)
        # 環的情況會另外根據與那個頂點開始延伸來計算向量
        vector = (0,0)
        # 尋找相鄰點
        for node in sequence:
            for ad_node in mol.getAdjacency( node ):
                # 把與初始位置( 單點 or ring)相鄰的頂點放入 queue message 中
                # Qeueu_Message( base_index, next_index, edge, base_coord, vector, direct )
                queue.append( 
                    Queue_Message( node, ad_node, {node,ad_node}, coord, vector, direct ) 
                )
    else:
        # 若為單點延伸的情況, 
        # <<<<<<<<<<  有問題 待解決....   >>>>>>>>>
        # 需要重新定義
        bond_order = len( mol.getAdjacency( sequence[0] ) )
        # 預設初始角度
        angle = 60 *(3.14159/180)
        v = ( math.cos(angle)*bond_length, math.sin(angle)*bond_length )
        vector = ChainExtend( (0,0), v, direct, bond_order )

        count = 0
        for ad_node in mol.getAdjacency( sequence[0] ):
                # 把與初始位置( 單點 or ring)相鄰的頂點放入 queue message 中
                # Qeueu_Message( base_index, next_index, edge, base_coord, vector, direct )
                queue.append( 
                    Queue_Message( sequence[0], ad_node, {sequence[0],ad_node}, coord, v[count], direct ) 
                )
                count += 1

    print( vector )
    
    #
    #old version 
    for node in component_tree.edges[0]:
        queue.append( Queue_Message( 0, node[0], node[1], coord, vector, direct  ) )
    
    while queue:
        
        message = queue.pop()
        unit_1 = component_tree.Nodes[ message.base_index ]
        unit_2 = component_tree.Nodes[ message.next_index ]
        
        if len(unit_1) > 1 and len(unit_2) > 1:
            """ Fused rings 的情況 """
            """ 帶修改: 目前為單個環單個環的串接, 而非直接計算多環的FusedRinge的情況 """
            coord = RenderRingSystem( [unit_2], unit_1, message.base_coord )
            # 把 coord (2d) 轉換成 1D list
            temp = []
            for ring in coord:
                temp += ring
            visitVertice.add( unit_2, temp )
            coord = coord[0]
            graphCoordinate[ message.next_index ] = coord
        elif len(unit_1) > 1 and len(unit_2) == 1:
            """ ring 延伸碳鏈的情況 """
            # 尋找環上要延伸碳鏈的頂點
            index = 0
            for i in message.edge:
                if i in component_tree.Nodes[ message.base_index ]:
                    index = component_tree.Nodes[message.base_index].index( i )
            
            coord, vector = RingBlanch( message.base_coord, index )
            # 注意 [coord], 座標 list 化, 
            # 因為 graph.Nodes[message.next_index] 也是 list
            visitVertice.add( component_tree.Nodes[message.next_index], [coord] )
            graphCoordinate[ message.next_index ] = coord
        
        
        elif len(unit_1) == 1 and len( unit_2 ) ==1:
            """ 碳鏈延伸 """
            # 把 queue 中有相同 base_index者抓出來, 並同一處理
            temp = [ message ]
            for mes in queue:
                if mes.base_index == message.base_index:
                    temp.append( mes )
            # 去除 queue 中已取出的 mes
            for mes in temp:
                if mes in queue:
                    queue.remove(mes)
            # 計算往下延伸的向量
            # 注意 bond order 為 len(temp)+1
            vector_list = []
            vector_list, direct = ChainExtend( message.base_coord, vector, direct, len(temp)+1 )
            #  計算分支的座標
            # 待改善 : 給有較高分子量的支鏈特定的方向
            count = 0
            for mes in temp:
                vector = vector_list[count]
                if len( component_tree.Nodes[ mes.next_index ] ) == 1:
                    """ 一般碳鏈延伸 """
                    # 計算座標 : 舊座標 + 向量
                    coord = ( mes.base_coord[0]+vector[0], mes.base_coord[1]+vector[1] )
                    visitVertice.add( component_tree.Nodes[mes.next_index], [coord] )
                elif len( component_tree.Nodes[ mes.next_index ] ) > 1:
                    """ 碳鏈接環的情況下 """
                    # 找環的起始點
                    index = 0
                    for i in message.edge:
                        if i in component_tree.Nodes[ mes.next_index ]:
                            index = component_tree.Nodes[mes.next_index].index( i )
                    # 計算環的座標
                    coord, sequecne = buildCycle( vector, mes.base_coord, component_tree.Nodes[ mes.next_index ], index  )
                    visitVertice.add( sequecne, coord )
                # 於碳鏈的延伸之步驟, queue的加入  獨立出來處理
                for node in component_tree.edges[ mes.next_index ]:
                    # Queue_Message( base_index, next_index, edge, base_coord, vector, direct )
                    queue.append( 
                            Queue_Message( mes.next_index, node[0], node[1], coord, vector, direct  ) 
                            )
                count +=1
            continue
        else:
            pass
        # 把 unit_2 的 children node 加入 queue
        for node in component_tree.edges[ message.next_index ]:
            # Queue_Message( base_index, next_index, edge, base_coord, vector, direct )
            queue.append( 
                    Queue_Message( message.next_index, node[0], node[1], coord, vector, direct  ) 
                    )
   
    return visitVertice.sequenceList, visitVertice.coord_List