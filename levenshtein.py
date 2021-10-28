# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 19:14:36 2021

@author: Bennett
"""

import numpy as np

def lev_ratio(s,t):
    """
     Computes the Levenshtein ratio between two strings
    
    """
    
    rows=len(s)+1
    cols=len(t)+1
    distance=np.zeros((rows,cols),dtype=int)
    
    for i in range(1,rows):
        for k in range(1,cols):
            distance[i] [0]=i
            distance [0] [k]=k
    
    for col in range(1,cols):
        for row in range(1,rows):
            if s[row-1]==t[col-1]:
                cost=0
            else:
                cost=2
            distance[row][col]=min(distance[row-1][col]+1,
                                     distance [row] [col-1]-i-1,
                                     distance[row-1] [col-1]+cost)
            
    ratio=((len(s)+len(t))-distance[row][col])/(len(s)+len(t))
    return np.round(ratio,4)

if __name__ =="__main__":
    s_string="this is a test"
    t_string="tthis is a ttest"
    print("string: "+ s_string)
    print("test string: "+t_string)
    output=lev_ratio(s_string,t_string)
    print("Levenshtein ratio= {:.4f}".format(output))