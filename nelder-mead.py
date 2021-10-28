# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 18:43:27 2021

@author: Bennett
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

verbose=True
if verbose:
    tol=.01
else:
    tol=1e-10

 #define arbitrary 2D function
def funct(x,y):
    coefs=[2, 1, -5, 0, -7, -4, 2]
    f=coefs[6]
    f+=coefs[0]/100*x+coefs[1]/100*y+coefs[2]/1000*x*y
    #f+=10*coefs[4]*np.sin(x/np.pi/10)+10*coefs[5]*np.sin(y/np.pi/10)
    f+=10*coefs[4]*np.sin(x/np.pi/5)+10*coefs[5]*np.sin(y/np.pi/5)
    return f

xvals=np.linspace(0,100,200)
yvals=np.linspace(0,100,200)
xvals,yvals=np.meshgrid(xvals,yvals)
zplot=funct(xvals,yvals)

#return worst (maximum) response from a 2D simplex
def worst_result(p):
    f0=funct(*p[0])
    f1=funct(*p[1])
    f2=funct(*p[2])
    return max(f0,f1,f2)

#update 2D simplex per Nelder-Mead algorithm
def simplex_update(simplex):
    s0=funct(*simplex[0])
    s1=funct(*simplex[1])
    s2=funct(*simplex[2])
    initresponse=[s0,s1,s2]
    pbest=np.argmin(initresponse)
    pworst=np.argmax(initresponse)
    pmiddle=[0,1,2]
    pmiddle.remove(pbest)
    pmiddle.remove(pworst)
    pmiddle=pmiddle[0]
    centroid=((simplex[pbest][0]+simplex[pmiddle] [0])/2,
              (simplex[pbest][1]+simplex[pmiddle] [1])/2)
    
    pr=(2*centroid[0]-simplex[pworst][0],2*centroid[1]-simplex[pworst][1])
    ex=(2*pr[0]-centroid[0],2*pr[1]-centroid[1])
    pco=(.5*centroid[0]+.5*pr[0],.5*centroid[1]+.5*pr[1])
    pci=(.5*centroid[0]+.5*simplex[pworst] [0],.5*centroid[1]+.5*simplex[pworst] [1])
    pshr3=(.5*simplex[pbest][0]+.5*simplex[pworst] [0],
           .5*simplex[pbest][1]+.5*simplex[pworst] [1])
    shrresult=min(funct(*simplex[pbest]),funct(*centroid),funct(*pshr3))
    
    if verbose:
        print("original simplex {}, function= {:.3f}".format(simplex,\
                                                             funct(*simplex[pbest])))
        print("reflection result {}, function = {:.5f}".format(pr,funct(*pr)))
        print("expansion result {}, function = {:.5f}".format(ex,funct(*ex)))
        print("contraction (outside) result {}, function ={:.5f}".format(pco,funct(*pco)))
        print("contraction (inside) result {}, function ={:.5f}".format(pci,funct(*pci)))
        print("shrink result, function = {:.5f}".format(shrresult))

    #reflection
    if funct(*pr)>= funct(*simplex[pmiddle]) and funct(*pr)<funct(*simplex[pbest]):
        if verbose:
            print("\naction: reflection")
        return [simplex[pbest],simplex[pmiddle],pr]

    #expand
    if funct(*ex) < funct (*pr):
        if verbose:
            print("\naction: expansion")
        return [simplex[pbest],simplex[pmiddle],ex]

    #contract
    if funct(*simplex[pbest]) <= funct(*pr) and funct(*pr) < funct(*simplex[pworst]):
        if verbose:
            print("\naction: contract- outside")
        return [simplex[pbest],simplex[pmiddle],pco]
    if funct(*pr) >= funct(*simplex[pworst]):
        if verbose:
            print("\naction: contract- inside")
        return [simplex[pbest],simplex[pmiddle],pci]

    if verbose:
        print("\naction: shrink")
    return [simplex[pbest],centroid,pshr3]

triangle=[(60,60),(60,65),(65,60)]
simplex=triangle
i=0
delta=100

while delta > tol:
    funstart=worst_result(simplex)
    simplex=simplex_update(simplex)
    funend=worst_result(simplex)
    delta=abs(funend-funstart)
    print("iteration {}".format(i))
    print("new simplex: "+str(simplex))
    i+=1
    
    if verbose:
        #plot result on surface
        fig=plt.figure()
        ax=plt.axes(projection="3d")
        ax.plot_surface(xvals,yvals,zplot,linewidth=0,alpha=.5)

        ax.scatter(triangle[0][0] ,triangle[0][1],funct(*triangle[0]),
                   label="minima",marker="o",color="red")

        ax.scatter(simplex[0][0],simplex[0] [1],funct(*simplex[0]),
                   label="minima",marker="o",color="black")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Minimization with Nelder-Mead Algorithm")
        plt.show()
        _=input("press any key")

print("\n\nfinal result {}, function = {:.8f}".format(simplex[0],funct(*simplex[0])))
print(str(i)+" iterations for a tolerance of {:.0e}".format(tol))
print("\n\nScipy Optimize Minimize says:")
 
def functone(p):
    return funct(p[0],p[1])

opt=minimize(functone,[10,10],method="Nelder-Mead")
print (opt)

#plot final result
fig=plt.figure()
ax=plt.axes(projection="3d")
ax.plot_surface(xvals,yvals,zplot,linewidth=0,alpha=.5)
ax.scatter(triangle[0][0],triangle[0][1],funct(*triangle[0]),label="minima",
           marker="o",color="red")
ax.scatter(simplex[0][0] ,simplex[0][1],funct(*simplex[0]),label="minima",
                       marker="o",color="black")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Final Result: Nelder-Mead Simplex Minimization")
plt.show()