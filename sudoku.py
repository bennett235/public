# -*- coding: utf-8 -*-
"""
Created on Sun May 24 18:03:55 2020

@author: Bennett
"""


import numpy as np
#Arthur Benjamin YouTube video, 2119226 calls
grid=[[0,0,0,0,4,0,0,2,0],
      [0,5,0,9,0,0,0,0,0],
      [0,1,0,0,0,0,0,0,0],
      [0,0,0,8,0,0,1,0,5],
      [2,0,0,0,3,0,0,0,0],
      [0,0,0,0,0,0,9,0,0],
      [4,9,0,0,0,2,0,0,0],
      [3,0,0,0,0,0,0,6,0],
      [0,0,0,1,0,0,0,0,0]]

#Saturday TU puzzle, rated as 5: 11045 calls
grid1=[[0,0,0,0,7,0,4,0,0],
      [0,0,2,0,1,5,7,0,8],
      [0,0,0,8,0,0,0,5,2],
      [7,0,0,0,9,0,0,6,0],
      [4,0,0,0,5,0,0,0,1],
      [0,9,0,0,2,0,0,0,3],
      [5,1,0,0,0,7,0,0,0],
      [2,0,8,5,4,0,3,0,0],
      [0,0,4,0,8,0,0,0,0]]

#Monday TU puzzle, rated as easy: 123 calls
grid2=[[0,0,0,4,2,7,0,8,0],
      [0,5,2,1,6,8,4,0,7],
      [0,4,7,3,0,0,0,0,0],
      [5,0,6,0,3,0,9,0,0],
      [7,0,0,0,9,0,0,0,1],
      [0,0,3,0,7,0,6,0,8],
      [0,0,0,0,0,3,2,1,0],
      [6,0,8,5,4,2,7,9,0],
      [0,3,0,7,1,6,0,0,0]]

#Sunday TU puzzle: 7634 calls
grid3=[[0,0,2,0,5,9,0,0,8],
      [0,9,1,0,4,0,0,0,0],
      [0,0,0,0,7,8,0,1,0],
      [4,0,0,0,2,7,0,5,0],
      [0,0,0,0,6,0,0,0,0],
      [0,5,0,8,3,0,0,0,2],
      [0,2,0,3,1,0,0,0,0],
      [0,0,0,0,8,0,4,2,0],
      [5,0,0,7,9,0,8,0,0]]
print("starting puzzle:")
print(np.matrix(grid))

#check whether number n is already present in column y, row x, or 3x3 box
def fits(y,x,n):
    for i in range(0,9):
        if grid[y][i]==n:
            return False
    for i in range (0,9):
        if grid[i][x]==n:
            return False
    y0=(y//3)*3
    x0=(x//3)*3
    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+i][x0+j]==n:
                return False
    return True

#iteratively solve all grid locations
r=0 #check number of recursive calls needed
def solve():
    global r    
    for y in range(0,9):
        for x in range(0,9):
            if grid[y][x]==0:                
                for n in range(1,10):                    
                    if fits(y,x,n):
                        grid[y][x]=n                                               
                        r+=1
                        solve()
                        grid[y][x]=0
                return None
                
    print("\n Solved:")
    print("{} Recursive calls".format(r))
    print(np.matrix(grid))
   
    
solve()

