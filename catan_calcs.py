# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 09:55:44 2023

@author: benne
"""
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def binom(n,k):
    comb=math.factorial(n)/(math.factorial(k)*math.factorial(n-k))
    return comb

def roll_prob(x,n=6):
    return (n-abs(x-(n+1)))/n**2

def pipcalc(n):
    if n<7:
        return n-1
    if n>7:
        return 13-n
     
vals=list(range(2,13))
vals=[v for v in vals if v!=7]
valstr=vals[1:9]
valstr2=valstr.copy()
valstr2.extend([0])

corners=[]
for i in vals:
    for j in valstr:
        for k in valstr2:
            corners.extend([[i,j,k]])

celldf=pd.DataFrame(corners,columns=["A","B","C"])

celldf["pipsum"]=celldf.apply(lambda x: pipcalc(x["A"])+pipcalc(x["B"])+pipcalc(x["C"]),axis=1)
celldf["prob"]=celldf.apply(lambda x: roll_prob(x["A"])+roll_prob(x["B"])+roll_prob(x["C"]),axis=1)
celldf=celldf[celldf["pipsum"]<14].copy()
celldf.reset_index(inplace=True,drop=True)


xvals=list(np.linspace(2,13))
yvals=[x/36 for x in xvals]

plt.bar(vals,[roll_prob(v) for v in vals])
plt.xlabel("Total")
plt.ylabel("Probability")
plt.title("Sum of Two Dice Rolls")
plt.show()
    
plt.scatter(celldf["pipsum"],celldf["prob"])
plt.xlabel("Pip Sum")
plt.ylabel("Probability")
plt.title("Catan Probabilities")
plt.annotate("P= pip sum / 36",xy=(.25,.75),xycoords="axes fraction")
plt.xticks(np.linspace(2,13,12))
plt.plot(xvals,yvals,ls=":")
plt.show()
    