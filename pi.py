# -*- coding: utf-8 -*-
"""
Compare various pi estimation algorithms

@author: Bennett
"""
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

maxsteps=1000
convtol=1E-8
pi=chr(960)
#set up dataframe to store results
index=range(500)
pidf=pd.DataFrame(index=index,columns=["Euler","Leibniz","Nilakantha", 
                                       "Madhava","Ramanujan","Chudnovsky",
                                       "Rational"])
pd.set_option("display.precision", 8)

def conv_check(x):
    if abs(x-np.pi)<convtol:
        return True
    else:
        return False

convmessage=pi+" estimation to {}, max of {} iterations:\n".format(convtol,maxsteps)        
#########################################################
#Chudnovsky algoritm, gives 15 digits with each iteration
pisinv=0.0
for i in range(maxsteps):
    num=(-1)**i*math.factorial(6*i)*(545140134*i+13591409)
    den=math.factorial(3*i)*(math.factorial(i))**3*640320**(3*i+3/2)
    pisinv+=num/den

    pis=1/(12*pisinv)
    pidf.loc[i,"Chudnovsky"]=pis
    if conv_check(pis):
        cmessage=("Chudnovsky converged in {} steps\n".format(i+1))
        break
    
pidf["Chudnovsky"].fillna(pis,inplace=True)    
if not conv_check(pis):
    cmessage=("Chudnovsky did not converge\n")  
convmessage+=cmessage

#######################################################
#Ramanujan
piriter=0
for i in range(maxsteps):
    piriter+=(math.factorial(4*i) *(1103+26390*i))/((math.factorial(i))**4*396**(4*i))
    pir=1/(piriter*(2*2**.5)/9801)
    pidf.loc[i,"Ramanujan"]=pir
    
    if conv_check(pir):
        rmessage=("Ramanujan converged in {} steps\n".format(i+1))
        break
if not conv_check(pir):
    rmessage=("Ramanujan did not converge\n")  

pidf["Ramanujan"].fillna(pir,inplace=True) 
convmessage+=rmessage  

#######################################################
#Madhava
pimiter=0
for i in range(maxsteps):
    pimiter+=((-3)**(-i))/(2*i+1)
    pim=(12**.5)*pimiter
    pidf.loc[i,"Madhava"]=pim
    
    if conv_check(pim):
        mmessage=("Madhava converged in {} steps\n".format(i+1))
        break
if not conv_check(pim):
    mmessage=("Madhava did not converge\n")  
    
pidf["Madhava"].fillna(pim,inplace=True)     
convmessage+=mmessage    

########################################################    
#Euler-Newton
pieiter=0
for i in range(maxsteps):
    pieiter+=((2**i)*(math.factorial(i))**2)/(math.factorial(2*i+1))
    pie=2*pieiter
    pidf.loc[i,"Euler"]=pie
    
    if conv_check(pie):
        emessage=("Euler converged in {} steps\n".format(i+1))
        break
if not conv_check(pie):
    emessage=("Euler did not converge\n")  
    
pidf["Euler"].fillna(pie,inplace=True) 
convmessage+=emessage


#######################################################
#Nilakantha

pin=3
dterm=2
sign=-1
pidf.loc[0,"Nilakantha"]=pin

for i in range(1,maxsteps):
    dterm+=2
    sign=-sign
    pin+=sign*4/(dterm*(dterm-1)*(dterm-2))
    pidf.loc[i,"Nilakantha"]=pin
    if conv_check(pin):
        nmessage=("Nilakantha converged in {} steps\n".format(i+1))
        break
if not conv_check(pin):
    nmessage=("Nilakantha did not converge, error={:.2E}\n".format(1-pin/np.pi))  
    
pidf["Nilakantha"].fillna(pin,inplace=True)   

convmessage+=nmessage

#########################################################
#Leibniz algorithm, very slow to converge
den=1
sign=1
pil=0
piliter=0
for i in range(maxsteps):
    piliter+=sign*1/den
    pil=piliter*4
    pidf.loc[i,"Leibniz"]=pil
    sign=-sign
    den+=2
    if conv_check(pil):
        lmessage=("Leibniz converged in {} steps\n".format(i-1))
        break
if not conv_check(pil):
    lmessage=("Leibniz did not converge, error={:.2E}\n".format(1-pil/np.pi))  
convmessage+=lmessage  
  
   

seed=pis
##############################################################

whole=math.floor(seed)
remain=seed-whole
start=(0,1,1,1)

def update(fracts,val):
    a,b,c,d=fracts
    mid=(a+c)/(b+d)
    if val<mid:
        anew=a
        bnew=b
        cnew=a+c
        dnew=b+d
    elif val>mid:
        anew=a+c
        bnew=b+d
        cnew=c
        dnew=d
    else:
        print('exact')
        return a,b,c,d
    return anew,bnew,cnew,dnew

vals=start
error=10
ri=0        
while error>convtol:
    vals=update(vals,remain)  
    a,b,c,d=vals
    highval=whole+c/d
    lowval=whole +a/b
    error =min(abs(highval-seed),abs(lowval-seed))
        
    if abs(highval-seed)<abs(lowval-seed):     
        pidf.loc[ri,"Rational"]=highval
    else:
        pidf.loc[ri,"Rational"]=lowval
    ri+=1   

if abs(highval-seed)>abs(lowval-seed):
    ratio=("{}/{}".format(a+whole*b,b))
else:
    ratio="{}/{}".format(c+whole*d,d)

convmessage+="Rational estimate: "+ratio+ ",converged in {} steps".format(ri)    
#########################################################
#Plot results 
plotdf=pidf.loc[0:50].copy()
#plotdf.drop("Rational",inplace=True,axis=1)
for col in plotdf.columns:
    plt.plot(plotdf.index,plotdf[col],label=col)
plt.legend(bbox_to_anchor=(1.3,1),ncol=1)
plt.ylim((2.5,3.5))
plt.annotate(convmessage,(5,2.55))
plt.title("Estimating "+pi)
plt.xlabel("Iteration")
plt.ylabel("Value")
plt.show()
errors=(1-pidf.loc[199]/math.pi)

print(convmessage)