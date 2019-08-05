# -*- coding: utf-8 -*-
"""
Created on Fri May  3 09:41:01 2019

@author: gogho
"""
import time
# =================================================================
# =================================================================
from os import path
import sys
from module.Molecule import openMDL
from module.MolInfo import MolInfo
from module.RenderMol import getMolCoordinate 

import math

t0 = time.clock()
filepath = path.dirname( path.abspath( __file__ ))
sys.path.append(filepath)
print( filepath )

# ----- MDL File ------
#filepath = filepath + '//Mol Model//Caffeine.mol'
#filepath = filepath + '//Mol Model//mol1.mol'
filepath = filepath + '//Mol Model//mol8.mol'
mol = openMDL(filepath)


info = MolInfo(mol)
info.RingPerception()
print( 'Ring : ', [  ring.sequence for ring in info.rings] )
print( 'Fused Ring : ', [ fusedring.fused_ring for fusedring in info.fused_rings] )  


print('-----Test----')
#print( info.fused_rings[0].sortAttachRing() )
coord = []
coord = getMolCoordinate( mol,info, BOND_LENGTH = 1 )
'''
try:
    import matplotlib.pyplot as plt 
    plt.figure()
    x,y = [], []
    count = 0
    for c in coord:
        if mol.Atoms[count].label == 'H':
            continue
        x.append( c[0] )
        y.append( c[1] )
        count += 1

    plt.scatter(x,y)

    line_x, line_y = [], []
    for bond in mol.Bonds:
        if (mol.Atoms[ bond.connected_atom[0] ].label == 'H') or (
            mol.Atoms[ bond.connected_atom[1] ].label == 'H'):
            continue 
        coord1 = coord[ bond.connected_atom[0] ]
        coord2 = coord[ bond.connected_atom[1] ]
        line_x = [ coord1[0], coord2[0] ]
        line_y = [ coord1[1], coord2[1] ]
        plt.plot(line_x, line_y)
    plt.xlim(-8,8)
    plt.ylim(-8,8)
    print( 'time : ', time.clock() - t0 )
    plt.show()
except:
    pass
'''
# =======================
from tkinter import *
root = Tk()
root.wm_minsize(800, 600)
cv = Canvas(root,bg = 'white', width = 800,height = 600)

new_coord = [0] * len(coord)
min_x, min_y = coord[0][0], coord[0][1]
sum_x, sum_y = 0, 0
count = 0
for i in range( len(coord) ):
    if coord[i] == 0:
        continue
    new_coord[i] =  (coord[i][0]*40, coord[i][1]*40)
    sum_x += new_coord[i][0]
    sum_y += new_coord[i][1]
    count += 1
    if coord[i][0] < min_x:
        min_x = new_coord[i][0]
    if coord[i][1] < min_y:
        min_y = new_coord[i][1]

for i in range( len(new_coord) ):
    if new_coord[i] == 0:
        # 通常為 C-H 的情況
        continue
    new_coord[i] =  (new_coord[i][0] + (400 - sum_x/count), new_coord[i][1] + ( 300 - sum_y/count) )
    
stack, visit =[ 0 ], []
while stack:
    index = stack.pop()
    visit.append( index )

    for bond_index in mol.Atoms[index].bond:
        for next_atom_index in mol.Bonds[bond_index].connected_atom:
            if new_coord[next_atom_index] == 0:
                # 通常為 C-H 的情況
                continue
            if next_atom_index in visit:
                continue
            else:
                cv.create_line( 
                    new_coord[index][0], new_coord[index][1], 
                    new_coord[next_atom_index][0], new_coord[next_atom_index][1],width=2 )
                stack.append(next_atom_index)

                if mol.Bonds[ bond_index ].order == 2:
                    # ----- 畫雙鍵 -----
                    coord = [ new_coord[index][0], new_coord[index][1], 
                            new_coord[next_atom_index][0], new_coord[next_atom_index][1]
                             ]
                    vector = [  new_coord[next_atom_index][0] - new_coord[index][0],
                                new_coord[next_atom_index][1] - new_coord[index][1]
                            ]
                    const = 5
                    x_const = math.cos(math.pi/2)*vector[0] - math.sin( math.pi/2 )*vector[1]
                    y_const = math.sin(math.pi/2)*vector[0] + math.cos( math.pi/2 )*vector[1]
                    x_const = x_const/ abs(x_const)
                    y_const = y_const/abs(y_const)
                    
                    
                    nc = [ coord[0] + const*x_const + vector[0]*0.1, 
                                coord[1] + const*y_const + vector[1]*0.1,
                                coord[2] + const*x_const - vector[0]*0.1, 
                                coord[3] + const*y_const - vector[1]*0.1]
                    cv.create_line( nc[0], nc[1], nc[2], nc[3], width=2 )

size, color=15, 'black'
count = -1
for atom in mol.Atoms:
    count += 1
    if atom.label != 'C'  :
        if new_coord[count] == 0:
            continue
        cv.create_oval( new_coord[count][0]-size, new_coord[count][1]-size, 
                           new_coord[count][0]+size, new_coord[count][1]+size,
                           fill='white', outline='white' )
        if atom.label == 'O':
            color = 'red'
        elif atom.label == 'N':
            color = 'blue'
        else:
            color = 'black'
        cv.create_text( new_coord[count][0], new_coord[count][1], 
                           text = atom.label, font=("Purisa", 14, 'bold'), fill=color )
    

cv.pack()
root.mainloop()




