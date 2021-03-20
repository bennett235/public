# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:29:05 2021

@author: Bennett
"""

"""
plots a Bardsley's fern. Based on Python Programmer YouTube video

"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

m1=np.array([[0,0],[0,.16]])
m2=np.array([[.85,.04],[-.04,.85]])
m3=np.array([[.2,-.26],[.23,.22]])
m4=np.array([[-.15,.28],[.26,.24]])
ms=[m1,m2,m3,m4]

b1=np.array([[0],[0]])
b2=np.array([[0],[1.6]])
b3=np.array([[0],[1.6]])
b4=np.array([[0],[.44]])
bs=[b1,b2,b3,b4]

def plotpoint(x,y):
    point=np.array([[x],[y]])
    pval=np.random.choice([0,1,2,3],p=[.01,.85,.07,.07])
    m=ms[pval]
    b=bs[pval]
    #newpoint=np.dot(m,point)+b
    newpoint=m@point + b
    return float(newpoint[0]),float(newpoint[1])

points=100000
x,y=0,0
xs=[]
ys=[]
for i in range(points):
    xs.append(x)
    ys.append(y)
    x,y=plotpoint(x,y)
     
plt.figure()
plt.scatter(xs,ys,s=.2,c="green")
plt.plot()

plt.figure()   
sns.scatterplot(x=xs,y=ys,marker=".",color="green")    
plt.plot()    
