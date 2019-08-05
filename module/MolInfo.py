# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 11:50:23 2019

@author: gogho
"""
from os import path
import sys
filepath = path.dirname( path.abspath( __file__ ))
sys.path.append(filepath)

from Molecule import Molecule, Atom 
from graph.SearchBridgeEdges import (SearchBiconnectedSubgraph, 
                                            SearchBackEdges)
from molStructure.molStructure import molCycleSearch
from graph.Graph import Graph

class Ring:
    # ex : [ 2,3,4,5,6,7 ]  ( CW or CCW 按順序排列 )  
    sequence = []
    def __init__(self, seq):
        self.sequence = seq
        
    def ifInRing(self, num):
        return num in self.sequence
        
class FusedRing:
    # ex : [[ 2,3,4,5,6,7 ], [......], [......]  
    # CW or CCW 按順序排列
    fused_ring = []
    def __init__(self, sequence_list):
        self.fused_ring = sequence_list
        
    def ifInRing(self, num):
        for ring in self.fused_ring:
            if num in ring:
                return True
        return False

    def sortAttachRing(self, index=0):
        '''
        尋找 Fused Ring 中互相連接的Ring
        輸出結果:
            [ ( ring1, ring2 ), (ring2, ring3), (ring2, rin3),... ]
            () 內表示兩個ring是貼合的狀況
        '''
        temp_fused_ring = self.fused_ring.copy()
        queue = [ temp_fused_ring.pop(index) ]
        answer = []

        # 每次迴圈都會搜尋 temp_fused_ring 中是否有與 base_ring相連的ring
        # 若有相連, 則把結果儲存, 並把找到的 ring 加入倒queue中
        # 每次迴圈都會使 temp_fused_ring 變短
        # 注意 fused ring 中的每個ring 必定會至少與其中一個ring相連
        while queue:
            new_fused_ring = []
            base_ring = queue.pop()
            for ring in temp_fused_ring:
                # 尋找是否有 ring 與 base_ring 相連
                if self.__ifAttachRing( ring, base_ring ):
                    # 若有相連, 則儲存結果
                    answer.append( ( base_ring, ring ) )
                    queue.append(ring)
                else:
                    new_fused_ring.append( ring )
            # 把未被配對的 ring 做下次迴圈的搜尋
            temp_fused_ring = new_fused_ring.copy() 
        return answer


    def __ifAttachRing(self, sequence, base_sequence):
        for i in sequence:
            if self.__inRing( i, base_sequence ):
                return True
        return False

    def __inRing(self, num, sequence):
        return num in sequence


class MolInfo:
    '''
    目的 : 使用 Molecule class,並對其結構進行操作
    功能 : 
        1. RingPerception : 解析 Molecule 中的環系統, 並分為 Ring & Fused Ring
    '''
    molecule = None # 儲存 Melocule class
    rings = [] # 儲存 Ring class 
    fused_rings = [] # 儲存 Fused Ring class
    
    def __init__(self, mol:Molecule ):
        # 匯入分子結構 ( Molecule class ) & 參數初始化
        self.molecule = mol
        self.rings = []
        self.fused_rings = []

    def ifInRing( self, atom:Atom ):
        '''
        檢查該原子是否於 Ring 系統中, 回傳T/F & 所在 Ring( if exist )
        注意Ring & Fused Ring 需分開檢查
        '''
        count = 0
        for a in self.molecule.Atoms:
            if a == atom:
                break
            count += 1
        for r in self.rings:
            if r.ifInRing(count):
                return True, r
        return False, 0

    def ifInFusedRing(self, atom:Atom):
        '''
        檢查該原子是否於 Fused Ring 系統中, 回傳T/F & 所在 Fused Ring( if exist )
        注意Ring & Fused Ring 需分開檢查
        '''
        count = 0
        for a in self.molecule.Atoms:
            if a == atom:
                break
            count += 1
        for r in self.fused_rings:
            if r.ifInRing(count):
                return True, r
        return False, 0
    
    def getComponent(self, atom:Atom):
        '''
        目的 : 輸入Atom class, 判斷該atom位於何者系統(Ring or FusedRing)中, 並輸出其系統
        '''
        index = self.molecule.Atoms.index( atom )
        for fr in self.fused_rings:
            for ring in fr.fused_ring:
                if index in ring:
                    return fr
        for r in self.rings:
            if index in r.sequence:
                return r
        return self.molecule.Atoms[index]

    def getNeiborComponent(self, component):
        '''
        目的 : 輸入系統, 並輸出與該系統相鄰的系統
        '''
        connect_component=[]
        if type(component).__name__ == 'Atom':
            # bond_list 為 molecule.Bonds(list) 的 index
            bond_list = component.bond
            for bond_index in bond_list:
                # Bond.connected_atom 的輸出結果為 molecule,Atoms(list)的 index
                for connect_atom_index in self.molecule.Bonds[ bond_index ].connected_atom:
                    # 判斷連接 atom 是否就是自己
                    if self.molecule.Atoms[connect_atom_index] != component:
                        # 利用 Mol_Info.getComponent() 找 atom 位於何者系統中
                        connect_component.append( 
                            self.getComponent( self.molecule.Atoms[connect_atom_index] ) )
        elif type(component).__name__ == 'Ring':
            # Ring.sequence(list) 中的數值為 Molecule.Atoms 的 index
            for index in component.sequence:
                bond_list = self.molecule.Atoms[index].bond
                for bond_index in bond_list:
                    for connect_atom_index in self.molecule.Bonds[ bond_index ].connected_atom:
                        if connect_atom_index not in component.sequence:
                            connect_component.append( 
                            self.getComponent( self.molecule.Atoms[connect_atom_index] ) )
        elif type(component).__name__ == 'FusedRing':
            # 把 fused ring(2D list) 轉成 1d list
            sequence = [ i for ring in component.fused_ring for i in ring ]
            for index in sequence:
                bond_list = self.molecule.Atoms[index].bond
                for bond_index in bond_list:
                    for connect_atom_index in self.molecule.Bonds[ bond_index ].connected_atom:
                        if connect_atom_index not in sequence:
                            connect_component.append( 
                            self.getComponent( self.molecule.Atoms[connect_atom_index] ) )
        else:
            print( 'Mol_INfo.getNeiborComponent() Function "component" Error' )
            print( '---> component : ',component )
            print( '---> type( component ) : ', type( component ) )
            print( '---> type( component ).__name__ : ', type( component ).__name__ )
        return connect_component


    def RingPerception(self):
        # ---------- 從 Molecule (Graph) 結構中尋找 "環(Ring)" ----------
        # 其中被找到的 Ring System,被分成 Ring 與 Fused Ring, 並分別儲存
        subgraphlist, ringSystem, sub_edges = [], [], []
        subgraphlist = SearchBiconnectedSubgraph( self.molecule.outputAdjmatrix() )
        # ----------- search rings sysytem and not ring edges
        for subgraph in subgraphlist:
            if len(subgraph) > 1:
                ringSystem.append(subgraph)
            else:
                sub_edges.append(subgraph)
        # ringSystem 參數以"邊"的形式儲存 Graph 結構
        # 後續演算法之建立, 皆於 Sequence 序列的形式, 故使用時需要轉換
        # Ex : [[6, 3, 10, 5, 7], [6, 7, 2, 9, 4, 8]]
        # 轉換的方式, 使用 module 中 Graph class
       
        # ---------- ring perception ------------------     
        temp = []        
        for rings in ringSystem:
            # 先把 ring 轉成 Graph, 再轉成 adjacency matrix
            # 接著使用 adjacency matrix 來尋找最小單位元
            # 注意: 此時的 output 為 index, 故需要與原本資料(ring)進行對照,並轉成ring資料中的labe
            g = Graph(rings)
            adjmx = g.output_AdjacentMatrix()
            temp = molCycleSearch( adjmx )
            # 把 index 換成 ring的資料
            # temp 可能的格式如下 :
            #   +-- 單一 ring : [ [0, 2, 3, 4, 5, 1] ]
            #   +-- Fused Rings : [ [0, 2, 3, 4, 5, 6], [6, 5, 7, 8, 9] ]
            if len(temp) > 1:
                # ----- 為 Fused Rings 的情況 -----
                for i in range(len(temp)):
                    for j in range(len(temp[i])):
                        temp[i][j] = list( g._graph.keys() )[ temp[i][j] ]
                self.fused_rings.append(FusedRing(temp))
            elif len(temp) == 1:
                # ----- 為單一Ring 的情況 -----
                temp = temp[0]  # 2D list 轉成 1D list
                for i in range( len(temp) ):
                    temp[i] = list( g._graph.keys() )[ temp[i] ]
                self.rings.append(Ring(temp))
            else:
                # len(temp) == 0,  empty的情況, 意味著 molCycleSearch 函式找不到Cycle
                pass
            # ----- ----- ------ ------ ------ ------ ------
        # --------------------------------------------------------
        
if __name__ == '__main__':
    pass
        