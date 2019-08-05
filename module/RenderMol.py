# -*- coding: utf-8 -*-
"""
Created on Thu May 30 08:56:56 2019

@author: gogho
"""
from os import path
import sys
filepath = path.dirname( path.abspath( __file__ ))
sys.path.append(filepath)

from module.graph.SearchBridgeEdges import (SearchBiconnectedSubgraph, 
                                            SearchBackEdges)
from Molecule import Molecule, Atom, Bond
from MolInfo import MolInfo, Ring, FusedRing

from module.DrawMol.InitialCoord import InitialDraw, InitialFusedRing
from module.DrawMol.CarbonChain import ChainExtend
from module.DrawMol.PutFusedRing import RenderRingSystem
from module.DrawMol.RingBlanch import RingBlanch
from module.DrawMol.PutRing import buildCycle

import math

# ----------------------------------------------------------------
def GetInitialCoord( component, mol:Molecule, bond_length=1 ):
    """
    初始化第一個Component座標

    type( component ).__name__ 問題參考資料 : 
        https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance
    """
    """
    Debug Log:
        1.type( component ).__name__  :
            由於其結果 print 出 <class 'module.MolInfo.FusedRing'> , 
            導致 type( component ) != Atom or Ring or FusedRing Class, 故多新增 __name__
    待改善:
        1. 輸出結果(座標)是否直接匯入 Atom 物件中
    190725:
        1. GetInitialCoord( mol:Molecule, mol_info:MolInfo, index=0, bond_length=1 )
        ==> GetInitialCoord( component, mol:Molecule, bond_length=1 )

    """
    sequence, coord = [], []
    #component = mol_info.getComponent( mol.Atoms[index] )
    #print( type( component ) )
    if type( component ).__name__ == 'FusedRing':
        # ----- Fused Ring 情況的處理 ------
        # 在函式中, 會先計算一個初始 ring 的座標, 接著再跟著此 ring 向外延伸 Fused Ring
        # 回傳為一個 1D 序列與 1D 序列座標
        # 注意 Fused Ring 再匯入函式前, 需要先 sort
        sequence, coord = InitialFusedRing( component.sortAttachRing() , bond_length )
    elif type( component ).__name__ == 'Ring':
        # ----- Ring 的情況下 -----
        sequence, coord = InitialDraw( component.sequence , bond_length )
    elif type( component ).__name__ == 'Atom':
        # ------ 單一原子的情況下 -----
        sequence, coord = InitialDraw( [  mol.Atoms.index(component)  ], bond_length )
    else:
        # ----- 顯示錯誤訊息 -----
        print( 'GetInitialCoord Function "component" Error' )
        print( '---> component : ',component )
        print( '---> type( component ) : ', type( component ) )
        print( '---> type( component ).__name__ : ', type( component ).__name__ )
    return sequence, coord,component

def Atom_BFS_Sort(mol:Molecule, atomBeforeAtom:list, start_index=0):
    queue = [ start_index ]
    visit = [start_index]
    while queue:
        index = queue.pop(0)
        visit.append( index )
        for bond_index in mol.Atoms[index].bond:
            for atom in mol.Bonds[bond_index].connected_atom:
                if atom not in visit:
                    # 此處 atom 為 mol.Atom 的List
                    queue.append( atom )
                    atomBeforeAtom[ atom ] = index

def getMolCoordinate( mol:Molecule, mol_Info:MolInfo, BOND_LENGTH=1, start_index = 0 ):
    queue, direct, vector = [], 'CCW', (0,0)

    BOND_LENGTH = 1

    atomCoordTable = [0]* len(mol.Atoms)
    atomInterVector = [0]* len(mol.Atoms)
    atomInterDirect = [0]* len(mol.Atoms)
    atomBeforeAtom = [None]*len(mol.Atoms)
    visit = []

    Atom_BFS_Sort( mol, atomBeforeAtom, 0 )

    # ----- 建立初始座標 -----
    sequence, coord, component = GetInitialCoord( 
        mol_Info.getComponent( mol.Atoms[start_index] ), mol, BOND_LENGTH
        )
    visit = sequence.copy()
    # ----- 紀錄座標 ------
    count = 0
    for atom_index in sequence:
        atomCoordTable[atom_index] = coord[count]
        count += 1

    # ----- 尋找相鄰原子 ------
    baseType = type(component).__name__
    count = 0 
    for i in sequence:
        # ----------  尋找與該原子相鄰且未拜訪過之原子  ----------
        temp = [] # 暫存 next atom的編號
        for bond_index in mol.Atoms[ i ].bond:
            count += 1
            for next_atom_index in mol.Bonds[ bond_index ].connected_atom:
                if next_atom_index not in visit :
                    if mol.Atoms[i].label == 'C' and mol.Atoms[next_atom_index].label == 'H':
                        continue
                    
                    temp.append(next_atom_index)
                    if next_atom_index not in queue:
                        queue.append(next_atom_index)
        
        # ----------  設定相鄰原子的 vector, direct, atomBeforeAtom  ----------
        if baseType == 'Atom':
            # 使用temp 而非真的鍵結數目, 使得可以屏蔽 H atom 的鍵結的計算
            bond_order = len( temp ) 
            angle = 60 *(3.14159/180)
            v = ( math.cos(angle)*BOND_LENGTH, math.sin(angle)*BOND_LENGTH ) # 為初始向量
            vector, direct = ChainExtend( (0,0), v, direct, bond_order )  # vector 為list 
            
            # 紀錄 next atom 的 inter vector與旋轉方向
            for i in range( len(temp) ):
                next_atom_index = temp[i]
                atomInterDirect[ next_atom_index ] = direct
                atomBeforeAtom[ next_atom_index ] = atom_index
                if i >= 3:
                    i=3
                atomInterVector[ next_atom_index ] = vector[i]
        elif baseType == 'Ring':
            for next_atom_index in temp:
                #  以 BFS Table的結果來找在ring上的連接點
                index = sequence.index( atomBeforeAtom[ next_atom_index ] )
                new_coord, vector = RingBlanch( coord, index, BOND_LENGTH )
                atomInterDirect[next_atom_index] = direct
                atomInterVector[next_atom_index] = vector
                atomCoordTable[next_atom_index] = new_coord
        elif baseType == 'FusedRing':
            for next_atom_index in temp:
                # ------ 尋找Fused Ring中的哪個ring要連接出去 ------
                for ring in component.fused_ring:
                    if atomBeforeAtom[ next_atom_index ] in ring:
                        blanchRingSequence = ring.copy()
                        break
                index = blanchRingSequence.index( atomBeforeAtom[ next_atom_index ] )
                # ------ if blanchRingSequence 為空, 則有錯誤 ------
                if  blanchRingSequence == []:
                    print( 'Fused Ring Error' )
                # ------ 取得該 Ring 的座標系統 ------
                ringCoord = []
                for i in blanchRingSequence:
                    ringCoord.append( atomCoordTable[i] )
                # 計算座標, 向量
                new_coord, vector = RingBlanch( ringCoord, index, BOND_LENGTH )
                atomInterDirect[next_atom_index] = direct
                atomInterVector[next_atom_index] = vector
                atomCoordTable[next_atom_index] = new_coord
            
        else:
            # ----- Show Error -----
            pass
    #====================================================================================
    while queue:
        atom_index = queue.pop(0)
        sequence = []
        if atom_index in visit:
            continue
        else:
            visit.append(atom_index)
        component = mol_Info.getComponent( mol.Atoms[atom_index] )
        direct = atomInterDirect[ atom_index ]
        if type(component).__name__ == 'Atom':
            #  計算當前位址座標
            beforeAtomIndex = atomBeforeAtom[ atom_index ]
            atomCoordTable[atom_index] = ( atomCoordTable[ beforeAtomIndex ][0] + atomInterVector[atom_index][0],
                atomCoordTable[ beforeAtomIndex ][1] + atomInterVector[atom_index][1])
            sequence.append(atom_index)
        elif type(component).__name__ == 'Ring':
            beforeAtomIndex = atomBeforeAtom[ atom_index ]
            atomCoordTable[atom_index] = ( atomCoordTable[ beforeAtomIndex ][0] + atomInterVector[atom_index][0],
                atomCoordTable[ beforeAtomIndex ][1] + atomInterVector[atom_index][1])
            coord, sequence = buildCycle( 
                atomInterVector[atom_index], atomCoordTable[atom_index], 
                component.sequence, component.sequence.index( atom_index ), BOND_LENGTH  )
            count = 0
            # 紀錄座標
            for i in sequence:
                atomCoordTable[i] = coord[count]
                count += 1
        elif type(component).__name__ == 'FusedRing':
            beforeAtomIndex = atomBeforeAtom[ atom_index ]
            init_ring, ring_index, count = [], 0, 0
            for ring in component.fused_ring:
                if atom_index in ring:
                    init_ring = ring
                    ring_index = count
                count += 1

            atomCoordTable[atom_index] = ( atomCoordTable[ beforeAtomIndex ][0] + atomInterVector[atom_index][0],
                atomCoordTable[ beforeAtomIndex ][1] + atomInterVector[atom_index][1])
            coord, sequence = buildCycle( 
                atomInterVector[atom_index], atomCoordTable[atom_index], 
                init_ring, init_ring.index( atom_index ) , BOND_LENGTH  )

            ring_system = component.sortAttachRing(ring_index)
            ring_system[0] = ( sequence.copy(), ring_system[0][1] )
            sequence, coord = RenderRingSystem(ring_system, sequence, coord )
            count = 0
            for i in sequence:
                atomCoordTable[i] = coord[count]
                count += 1

        else:
            pass

        for i in sequence:
            if i not in visit:
                visit.append(i)
        # ----- 尋找相鄰原子 ------
        baseType = type(component).__name__
        for i in sequence:
            # ----------  尋找與該原子相鄰且未拜訪過之原子  ----------
            temp = [] # 暫存 next atom的編號
            for bond_index in mol.Atoms[ i ].bond:
                for next_atom_index in mol.Bonds[ bond_index ].connected_atom:
                    if next_atom_index not in visit :
                        if mol.Atoms[i].label == 'C' and mol.Atoms[next_atom_index].label == 'H':
                            continue
                        
                        temp.append(next_atom_index)
                        if next_atom_index not in queue:
                            queue.append(next_atom_index)
            
            # ----------  設定相鄰原子的 vector, direct, atomBeforeAtom  ----------
            if baseType == 'Atom':
                bond_order = len(temp)
                vector, direct = ChainExtend( 
                    (0,0), atomInterVector[atom_index] , direct, bond_order )  # vector 為list 
                
                for i in range( len( temp ) ):
                    next_atom_index = temp[i]
                    atomInterDirect[ next_atom_index ] = direct
                    atomBeforeAtom[ next_atom_index ] = atom_index
                    if i >= 3:
                        i=3
                    atomInterVector[ next_atom_index ] = vector[i]
                i=1
            elif baseType == 'Ring':
                for next_atom_index in temp:
                    #  以 BFS Table的結果來找在ring上的連接點
                    index = sequence.index( atomBeforeAtom[ next_atom_index ] )
                    new_coord, vector = RingBlanch( coord, index, BOND_LENGTH )
                    atomInterDirect[next_atom_index] = direct
                    atomInterVector[next_atom_index] = vector
                    atomCoordTable[next_atom_index] = new_coord
            elif baseType == 'FusedRing':
                for next_atom_index in temp:
                    # ------ 尋找Fused Ring中的哪個ring要連接出去 ------
                    for ring in component.fused_ring:
                        if atomBeforeAtom[ next_atom_index ] in ring:
                            blanchRingSequence = ring.copy()
                            break
                    index = blanchRingSequence.index( atomBeforeAtom[ next_atom_index ] )
                    # ------ if blanchRingSequence 為空, 則有錯誤 ------
                    if  blanchRingSequence == []:
                        print( 'Fused Ring Error' )
                    # ------ 取得該 Ring 的座標系統 ------
                    ringCoord = []
                    for i in blanchRingSequence:
                        ringCoord.append( atomCoordTable[i] )
                    # 計算座標, 向量
                    new_coord, vector = RingBlanch( ringCoord, index, BOND_LENGTH )
                    atomInterDirect[next_atom_index] = direct
                    atomInterVector[next_atom_index] = vector
                    atomCoordTable[next_atom_index] = new_coord
                
            else:
                # ----- Show Error -----
                pass
    return atomCoordTable

    
# ====================================================
if __name__ == '__main__':
    structure = FragmentTree()
    structure.Nodes.append([1,2,3,4,5])
    structure.Nodes.append( [2,3,9,8,7,6] )
    structure.Nodes.append( [10] )
    structure.Nodes.append( [11] )
    structure.Nodes.append( [12] )
    structure.Nodes.append( [13] )
    structure.Nodes.append( [14] )

    structure.edges.append([ [1, {2,3}] ])
    structure.edges.append([[2, {8,10}],
                            [5, {7,13}] ])
    structure.edges.append([[3, {10,11}],
                            [4, {10,12}] ])
    structure.edges.append([ ])
    structure.edges.append([ ])
    structure.edges.append([ [6, {13, 14}] ])
    structure.edges.append([ ])

    sequence, coord = getMolCoordinate(structure)



    import matplotlib.pyplot as plt

    edges=[(1,2),(2,3),(3,4),(4,5),(5,1),(3,9),(9,8),(8,7),(7,6),(6,2),
        (8,10),(7,13),(10,11),(10,12),(13,14)
        ]
    plt.figure()
    for e in edges:
        n1_coord = coord[ sequence.index( e[0] ) ]
        n2_coord = coord[ sequence.index( e[1] ) ]
        plt.plot( [n1_coord[0], n2_coord[0] ],[n1_coord[1], n2_coord[1] ],color='black' )
    plt.xlim( [-3,5] )
    plt.ylim( [-3,5] )
    plt.show()

#===================================================================================
