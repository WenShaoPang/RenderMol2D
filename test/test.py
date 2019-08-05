# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:41:34 2019

@author: gogho
"""

import abc
import copy

class Atom:
    label=''
    charge=0
    # bond 所儲存之數值為 Molecule class 中 Bonds(list)的index
    bond=[]
    x, y, z=0.0, 0.0, 0.0
    def __init__(self,x,y,z,label):
        self.bond=[]
        self.x, self.y, self.z = x, y, z
        self.label=label
    
class Bond:
    order = 0
    # 表示幾何之描述, 0 -> cis, 1 -> trans, othor
    stereo = 0
    # connected_atom 所儲存之數值為Molecule class中 Atoms(list)的 index
    connected_atom=[]
    def __init__(self,connected1, connected2, order):
        self.connected_atom = [ connected1, connected2 ]
        self.order = order

class Ring:
    # ex : [ 2,3,4,5,6,7 ]  ( CW or CCW 按順序排列 )  
    sequence = []
    def __init__(self, seq):
        self.sequence = seq
        
    def ifInRing(self, num):
        if num in self.sequence:
            return True
        else:
            return False
        
class FusedRing:
    # ex : [[ 2,3,4,5,6,7 ], [......], [......]  
    # CW or CCW 按順序排列
    fused_ring = []
    def __init__(self, sequence_list):
        self.fused_ring = sequence_list
        
    def ifInRing(self, num):
        if num in self.sequence:
            return True
        else:
            return False
        

class Molecule:
    Atoms=[]
    Bonds=[]
    
    def __init__(self, atom_info=[], bond_info=[]):
        self.Atoms, self.Bonds=[],[]
        for info in atom_info:
            self.Atoms.append( Atom( info[0], info[1], info[2], info[3] ) )
        
        for info in bond_info:
            self.Bonds.append( Bond(info[0]-1, info[1]-1, info[2]) )
            
        count = 0
        for bond in self.Bonds:
            c1, c2 = bond.connected_atom[0], bond.connected_atom[1]
            if count not in self.Atoms[c1].bond:
                self.Atoms[c1].bond.append( count )
            if count not in self.Atoms[c2].bond:
                self.Atoms[c2].bond.append( count )
            count +=1
            
    def getAdjacency(self,atom_index):
        # 輸入 Atoms (list) 的 index, 則輸出該 atom 相鄰的atoms (list -> atoms(lsit) index)
        output_adjacency_atom = []
        bond_index_list = self.Atoms[ atom_index ].bond
        for bond_index in bond_index_list:
            adjacency_list = self.Bonds[ bond_index ].connected_atom
            for v in adjacency_list:
                if v != atom_index:
                    output_adjacency_atom.append( v )
        return output_adjacency_atom
            
    def outputAdjmatrix(self):
        
        adjmx = []
        for i in self.Atoms:
            temp=[]
            for j in self.Atoms:
                temp.append(0)
            adjmx.append(temp)
        for bond in self.Bonds:
            
            n1 = bond.connected_atom[0]
            n2 = bond.connected_atom[1]
            adjmx[n1][n2] = 1
            adjmx[n2][n1] = 1
        return adjmx
        
if __name__ == '__main__':
    pass