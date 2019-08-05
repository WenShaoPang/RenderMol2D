# -*- coding: utf-8 -*-
"""
Created on Fri May 31 15:21:38 2019

@author: gogho
"""
from os import path
import sys
filepath = path.dirname( path.abspath( __file__ ))
sys.path.append(filepath)

import math
from PutFusedRing import RenderRingSystem

def InitialDraw(Sequence=[], bond_length=1):
    coordinate_list = []
    if len(Sequence) == 1:
        # ---- 單一原子的狀況下 -----
        coordinate_list.append( (0,0) )
    else:
        # ----- 為 ring 的狀況下 -----
        rot_angle = 360 /len(Sequence) *(3.14159/180)
        radius = 0.5*bond_length/math.sin( 0.5*rot_angle )
        angle = 0
        for i in Sequence:
            coordinate = ( radius*math.cos(angle), radius*math.sin(angle) )
            coordinate_list.append( coordinate )
            angle += rot_angle
    return Sequence, coordinate_list

def InitialFusedRing( fused_ring=[], bond_length=1 ):
    '''
    fused ring 格式:
           [ ( ring1, ring2 ), (ring2, ring3),... ] 
    ( rin1,rin2 ), 括弧內表示兩個 ring 互相 attach

    '''
    # ----- 選擇第一個先被計算的 ring
    first_ring = fused_ring[0][0]

    # ----- 首先計算第一個 初始 ring的座標 -----
    ring_sequence, coord_list = InitialDraw( first_ring, bond_length )
    # ------ 利用已被計算的初始 ring , 開始擴展 fused ring ------
    # 注意 : 輸出結果已包含第一個 ring 的座標與序列
    seq, coord = RenderRingSystem(fused_ring, ring_sequence, coord_list)
    return seq, coord


if __name__ == '__main__':
    s, c = InitialDraw([1,2,3,4,5])
    
    import matplotlib.pyplot as plt
    plt.figure()
    x, y = [], []
    for i in c:
        x.append( i[0] )
        y.append( i[1] )
    plt.plot(x,y)
    plt.show()