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
    # 紀錄座標 ----- 尚未用到....
    coord = None
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

class Molecule:
    # the list of Atom class
    Atoms=[]
    # the list of Bond class
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
            
    def getAdjacency(self, atom_index):
        # 輸入 Atoms (list) 的 index, 
        # 輸出該 atom 相鄰的atoms (list : atoms(list) index)
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
        
def openMDL(filepath):
    with open( filepath, 'r' ) as f:
        data = f.readlines()
        # 去除前三行
        data = data[3:] 
        # 把首行字串轉成 list, 並取出 原子數量 bond數量等資訊 
        # ex: "24 25  0     0  0  0  0  0  0999 V2000" ->字串, 需要轉成 list
        # 第一個數字為原子數量, 第二個數字為bond數量
        # 因為使用 split 後有可能出現" "or"  "的情況, 因此加入 if (i != '' and i !=' ') 去除
        temp =  [i for i in ( data[0].split(' ') ) if (i != '' and i !=' ')]
        atom_n, bond_n = int( temp[0] ), int( temp[1] )
        
        atom_info=[]
        for i in range(atom_n ):
            temp =  [i for i in data[ 1 +i ].split(' ') if (i != '' and i !=' ')]
            atom_info.append( [ float(temp[0]), float(temp[1]), float(temp[2]), temp[3] ] )
        
        bond_info=[]
        for i in range( bond_n ):
            temp =  [i for i in data[ 1+atom_n +i ].split(' ') if (i != '' and i !=' ')]
            # 遇到結束語句
            if temp[0] == 'M' and temp[1] == 'END':
                break
            bond_info.append( [ int(temp[0]), int(temp[1]), int(temp[2]) ] )
        
    return Molecule( atom_info, bond_info )   


if __name__ == '__main__':
    pass