# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 20:28:51 2021

@author: Bennett
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr,f_oneway,lognorm,norm,normaltest
import re

datadf=pd.read_csv("cleaned_data.csv")
datadf.dropna(subset=["days"],axis=0,inplace=True)
datadf=datadf[datadf["days"]>0].copy()

"""
look at distribution of days
"""
sns.histplot(datadf["days"],kde=True,bins=25)
plt.annotate("Median time: {:.1f} days".format(datadf["days"].median()),(300,400))
plt.title("Days to ride 50 m")
plt.show()


#results are quite skewed. perhaps lognormal distribution will fit
logresults=np.log(datadf["days"])
k,p=normaltest(logresults)

sigresult=""
if p>.05:
    sigresult="not "
print("P= {:.3f}, lognormal distribution {}rejected".format(p,sigresult))
shape,loc,scale=lognorm.fit(datadf["days"])
print("fit: loc={}, scale={}, shape={}".format(loc,scale,shape))


"""
examining whether any variables show significant correlation with days to 
learn to unicycle
"""

#make Seaborn pairplot to look for obvious trends
numericdf=datadf[["Agen","diameter","crank_length","days","Gender"]]
#sns.pairplot(numericdf,hue="Gender",corner=True)
#plt.show()

#check correlation coefficients
indvars=['Agen', 'Year startedn', 'diameter', 'crank_length']

for v in indvars:
    reduceddf=datadf[["days",v]].copy()
    reduceddf.dropna(inplace=True)
    stat,p=pearsonr(reduceddf["days"],reduceddf[v])
    print("variable {}:".format(v))
    print("Pearson R: {:.4f}, p value: {:.4f}".format(stat,p))
    if p<0.05:
        print("possible correlation")
        
#evaluating the instruction column
"""
common values:
    youtube
    club
    circus
    web
    internet
    videos
    friend
    lessons
    society
    father
    girlfriend
    mother
    book
    brother
"""
familycode="father|mother|brother|girlfriend"

datadf["Youtube"]=0
datadf["Friend"]=0
datadf["Family"]=0
datadf["Book"]=0
datadf["Circus"]=0
datadf["Internet"]=0
datadf["Lessons"]=0
datadf["Club"]=0
for i in datadf.index:
    insttext=datadf["Instructions_en"][i]
    insttext=(re.sub("[\s\.,]","",insttext)).lower()
    if bool(re.search("youtube|videos",insttext)):
        datadf["Youtube"].loc[i]=1
    if bool(re.search(familycode,insttext)):
        datadf["Family"].loc[i]=1
    if bool(re.search("friend",insttext)):
        datadf["Friend"].loc[i]=1
    if bool(re.search("web|internet",insttext)):
        datadf["Internet"].loc[i]=1
    if bool(re.search("circus",insttext)):
        datadf["Circus"].loc[i]=1
    if bool(re.search("lesson",insttext)):
        datadf["Lessons"].loc[i]=1
    if bool(re.search("club",insttext)):
        datadf["Club"].loc[i]=1

  
youtube=datadf[datadf["Youtube"]==1]["days"]
family=datadf[datadf["Family"]==1]["days"]
friend=datadf[datadf["Friend"]==1]["days"]
internet=datadf[datadf["Internet"]==1]["days"]
circus=datadf[datadf["Circus"]==1]["days"]
lessons=datadf[datadf["Lessons"]==1]["days"]
club=datadf[datadf["Club"]==1]["days"]

violindata=[youtube,family,friend,internet,circus,lessons,club]
labels=["Youtube","family","friend","internet","circus","lessons","club"]
plt.figure()
ax=plt.subplot()
plt.boxplot(violindata)
ax.set_xticklabels(labels)
plt.title("Days to learn unicycle, by instruction method")
plt.ylabel("Days to ride 50 m")
plt.ylim(-10,200)
plt.show()

#medians do look distinct
stat,p=f_oneway(youtube,family,friend,internet,circus,lessons,club)
anovar=""
if p>0.05:
    anovar="not "
print("ANOVA results: p={:.3f}, H0 (single population) {}rejected".format(p,anovar))

#test the extremes: family vs. lessons
stat2,p2=f_oneway(family,lessons)
anovar2=""
if p>0.05:
    anovar2="not "
print("ANOVA results: p={:.3f}, H0 (single population) {}rejected".format(p2,anovar2))