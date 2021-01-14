# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 15:03:36 2020

@author: Bennett
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f,t, nct,ncf
from scipy.optimize import minimize
import pandas as pd

"""
Performs sample size and power calculation assuming the experimental effect
is a 1-dimensional shift in the mean with equal variance. Power is computed 
with inputted values for effect size, sigma, alpha, and sample size, and then 
the number of samples required to reach the target beta is computed.

alpha= probability of Type I error (false positive), where an effect is judged
to be real when it occurred by normal variability. Significance = 1-alpha

beta= probability of Type II error (false negative), where a real effect is
mistaken for normal variability. Power = 1-beta

Benchmarked against JMP calculations.
#https://www.jmp.com/content/dam/jmp/documents/en/technical-reports/powerAndSampleSize.pdf

JMP output (2-sided tests)
comdf=pd.DataFrame()
comdf["alpha"]=[.05]*9
comdf["sigma"]=[1,1,1,1,10,10,10,10,10]
comdf["delta"]=[.5,1,1.5,2,5,10,15,20,25]
comdf["n"]=[10,10,10,10,5,5,5,5,5]
comdf["JMP Power"]=[.2932,.8031,.9873,.9998,.1405,.4014,.7107,.9089,.9817]
comdf["Calculated Power"]=0
"""

print("\nCalculate Sample Size and Power")
print("Assumes equal variances")

mean_h0=0
mean_h1=1
alpha=.05 
betatarget=.05
sigma=1
n=16
sided=1

print("\nAssumed effect size= "+str(mean_h1))
print("Assumed standard deviation= "+str(sigma))

stderr=sigma/(n**.5)
alphas=alpha/sided
lam=(mean_h1-mean_h0)/stderr
dsr=mean_h1/sigma

#set up x axis for plotting
xmin=mean_h0-3*stderr
xmax=mean_h1+3*stderr
xs=np.linspace(xmin,xmax,200)

#define H0 distribution
h0pdf=t.pdf(xs,df=n-1,loc=mean_h0,scale=stderr)
alpha_xval=t.isf(alphas,df=n-1,loc=mean_h0,scale=stderr)
ymax=h0pdf.max()

#define H1 distribution
h1pdf=nct.pdf(xs,df=n-1,nc=lam,scale=stderr)
betah=nct.cdf(alpha_xval,df=n-1,nc=lam,scale=stderr)
if sided==1.2:
    betal=nct.cdf(-alpha_xval,df=n-1,nc=lam)
    betacalc=betah-betal
else:
    betacalc=betah

#plot results
plt.plot(xs,h0pdf,label="H0")
plt.plot(xs,h1pdf,label="H1")
plt.axvline(alpha_xval,ls="--",color="blue")
if sided==2:
    plt.fill_between(xs,0,h0pdf,where=(xs>alpha_xval)|(xs<-alpha_xval),color="blue",alpha=.2,
                     label="alpha")
    plt.fill_between(xs,0,h1pdf,where=(xs<alpha_xval)&(xs>-alpha_xval),color="orange",alpha=.2,
                     label="beta")
if sided==1:
    plt.fill_between(xs,0,h0pdf,where=(xs>alpha_xval),color="blue",alpha=.2,
                     label="alpha")
    plt.fill_between(xs,0,h1pdf,where=(xs<alpha_xval),color="orange",alpha=.2,
                     label="beta")
plt.annotate("alpha= "+str(sided) +"* "+str(alphas),(mean_h1-stderr,.1*ymax))
plt.annotate("beta= "+str(np.round(betacalc,3)),(mean_h0-stderr,.1*ymax))
plt.annotate("n= "+str(n),(alpha_xval+stderr/2,.2*ymax))
plt.legend(loc=1)
plt.xlabel("Effect Size")
plt.ylabel("Probability")
plt.title("Sample Size and Power Calculation")
plt.show()

#optimize beta to desired value
print("Power of test as entered (n={})= {:.2f}%".format(n,100*(1-betacalc)))
print("[nct power= {:.2f}%]".format((1-betacalc)*100))

#compute F dist power :
fcrit=f.ppf(1-alpha*sided,1,n-1)
dsr=mean_h1/sigma
betacalc_f=ncf.cdf(fcrit,1,n-1,n*dsr**2)  
print("[fct power= {:.2f}%]".format((1-betacalc_f)*100))

def opt_n(n):
    stderr_n=sigma/n**.5
    lam_n=(mean_h1-mean_h0)/stderr_n
    alpha_xval_n=t.isf(alphas,df=n-1,scale=stderr_n)
    betah_n=nct.cdf(alpha_xval_n,df=n-1,nc=lam_n,scale=stderr_n)
    if sided==2:
        betal_n=nct.cdf(-alpha_xval_n,df=n-1,nc=lam_n)
        betacalc_n=betah_n-betal_n
    else:
        betacalc_n=betah_n
    
    return betacalc_n


optex=minimize(lambda x: abs(opt_n(x)-betatarget),n,tol=.00001,method="bfgs")
n_solved=math.ceil(optex["x"][0])


print("Optimized sample size for desired power of {:.0f}% = {}"\
      .format(100*(1-betatarget),n_solved))
