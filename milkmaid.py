# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 10:54:58 2023

@author: benne
"""


import numpy as np 
import matplotlib.pyplot as plt 
from scipy. optimize import minimize,differential_evolution,root,fsolve 
import numdifftools as nd 
from timeit import default_timer 

"""
Milkmaid Problem:
    
A milkmaid needs to travel from city A to city B, bringing a pail of water on
the way. If the river is defined on an x,y plane by the function f(x)=10/(1+x),
find the shortest path between A and B that touches the river

The problem is solved by finding the global minimum of the total distance
between A and (x,f(x)) plus the distance between (x,f(x)) and B.
"""

#function defining river 
def river(x): 
    return 10/(x+1) 

#distance function for total walk- this will be minimized 
def walk_function(x,A,B): 
    y=river(x) 
    leg1=((A[0]-x)**2+(A[1]-y)**2)**.5 
    
    leg2=((B[0]-x)**2+(B[1]-y)**2)**.5 
    return leg1+leg2
 
#perform the minimization with Scipy 
def calc_min(A,B): 
    sol=minimize(walk_function,x0=8,args=(A,B),method="TNC") 
    return sol,sol["x"][0],river(sol["x"][0]) 
""" 
Scipy Optimize Minimize doesn't always find the globabl minimum. Try all of the 
engines and note the solution time 
"""
#cycle through all applicable Scipy Optimize Minimize methods 
def calc_all(A,B): 
    sumtext=" Method\t\t\t\tSolution\tTime [s]" 
    methods=['Nelder-Mead' , 'Powell' , 'CG' , 'BFGS', 'L-BFGS-B' , 'TNC' , 
    'COBYLA', 'SLSQP' , "diff_evol"]
    for m in methods: 
        start=default_timer() 
        if m=="diff_evol": 
            bounds=[(-10,10)] 
            opt=differential_evolution(walk_function,args=(A,B),bounds=bounds) 
            #print(opt) 
        else: 
            opt=minimize(walk_function,x0=8,args=(A,B),method=m) 
     
        dist=float(opt["fun"]) 
        loc=float(opt["x"])
        time=default_timer()-start 
        #print(m,dist,time) 
        sumtext+=f"\n{m: ^{11}}\t{loc:.4}\t\t{dist:.4}\t\t{time:.4}"
    print(sumtext) 
    return sumtext 

"""
Investigate the gradients of the distance function. The Jacobian is the first 
derivative, which will be 0 at minima or maxima. The Hessian is the second 
derivative, which will be positive for minima, and negative for maxima. For 
multivariable optimizations, the inverse of the Hessian approximates the 
variance/ covariance matrix. Here, the Python Numdifftools module is used to 
numerically estimate derivatives. The fsolve function is used to find the roots 
of the Jacobian 
"""

def jacobian(x,A,B): 
    return float(nd.Jacobian(lambda x:walk_function(x,A,B))(x)) 

def hessian(x,A,B): 
    return float(nd.Hessian(lambda x:walk_function(x,A,B))(x)) 

def findroots(A,B): 
    roots=[] 
    for x in [0,1,2,3,4,5]:
        rout=fsolve(jacobian,x0=x,args=(A,B)) 
        roots.extend(np.round(rout,4)) 
        uniqueroots=set(roots) 
    return list(uniqueroots) 
"""
Plot the results- first the problem, then the distance, then the derivatives 
"""

def plotwalk(A,B,sol): 
    xvals=np.linspace(A[0]-2,B[0]+2) 
    riverp=[river(x) for x in xvals] 
    plt.plot(xvals,riverp,color="blue") 
    plt.scatter(A[0],A[1],color="Black") 
    plt.scatter(B[0],B[1],color="Black") 
    plt.plot([A[0],sol[0],B[0]],[A[1],sol[1],B[1]],ls=":",color="red") 
    plt.annotate("A",(A[0]+.2,A[1])) 
    plt.annotate("B",(B[0]+.2,B[1])) 
    plt.annotate("Priver\ny.10/(1+x)",(xvals[40],riverp[40]+.5)) 
    plt.title("Milkmaid Problem") 
    plt.xlabel("x") 
    plt.ylabel("y") 
    plt.show() 

def plotdist(A,B): 
    xvals=np.linspace(A[0]-2,B[0]+2) 
  
    distances=[walk_function(x,A,B) for x in xvals] 
    plt.plot(xvals,distances,label="distance") 
    plt.title("Distance") 
    plt.axvline(.5322597,color="black",ls=":") 
    plt.axvline(4.398814,color="black",ls=":") 
    plt.axvline(3.1608926,color="black",ls=":") 
    plt.axvline(8.0,color="black",ls="-.") 
    plt.annotate("start",xy=(8,13),xytext=(6,13.2),
                 arrowprops=dict(arrowstyle="->")) 
    plt.annotate("local\nminimum",xy=(findroots(A,B)[2],13),xytext=(4.7,12.2),
                 arrowprops=dict(arrowstyle="->")) 
    plt.annotate("global\nminimum",xy=(findroots(A,B)[0],13),xytext=(1.5,13.5), 
                                        arrowprops=dict(arrowstyle="->")) 
    plt.annotate("local\nmaximum",xy=(findroots(A,B)[1],13),xytext=(1.3,12), 
    arrowprops=dict(arrowstyle="->")) 
    plt.xlabel("x") 
    plt.ylabel("y")
    plt. show() 

def plot_derivatives(A,B): 
    xvals=np.linspace(A[0]-2,B[0]+2) 
    jac=[jacobian(x,A,B) for x in xvals] 
    plt.plot(xvals,jac,label="Jacobian") 
    hes=[hessian(x,A,B) for x in xvals] 
    plt.plot(xvals,hes,label="Hessian") 
    plt.title("Derivatives") 
    plt.legend() 
    plt.axhline(0,ls=":") 
    plt.ylim(-2,2) 
    plt.axvline(findroots(A,B)[0],color="black",ls=":") 
    plt.axvline(findroots(A,B)[1],color="black",ls=":") 
    plt.axvline(findroots(A,B)[2],color="black",ls=":") 
    plt.show() 

if __name__=="__main__": 
    A=[2,8] 
    B=[8,4] 
    sol=calc_min(A,B) 
    print(f"Minimum value found at x,y= {sol[1]:.4f},{river(sol[1]):.4f}") 
    print(f"Total distance traveled= {walk_function(sol[1],A,B):.4f}")
    print("\nTrying all Optimize Minimize engines") 
    calc_all(A,B) 
    plotwalk(A,B,(sol[1],sol[2])) 
    plotdist(A,B) 
    plot_derivatives(A,B)