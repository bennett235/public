# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 21:57:05 2021

@author: Bennett
"""

import pandas as pd
import numpy as np
import re

"""
first cleaning file includes translations. That takes significant time
this file picks up the pickled dataframe after translating to English
"""

rawdf=pd.read_pickle("rawdf.pkl")
rawdf.drop([ 'Country','Hours', 'Days', 'Wheel size','Crank length','Gender',
            'Age started','Year started','Instructions','Other sports', 
            'Remarks'],axis=1,inplace=True)

#standardize gender codes, including non-binary
gendict={'Male':"M",
         'Woman':"F", 
         'Female':"F", 
         'masculine':"M",
         'man':"M",
         'Prefer not to say':np.nan,
       'Other':"NB", 
       "I'd rather not say":np.nan, 
       'Feminine':"F", 
       'Man':"M", 
       'others':"NB",
       'Different':"NB", 
       'woman':"F",
       'I do not wish to specify it':np.nan}

rawdf["Gender"]=rawdf["Gender_en"].apply(lambda x: gendict[x])
rawdf.drop("Gender_en",axis=1,inplace=True)

#now code days, wheel diameter, crank length to numeric values
def make_numeric(s):
    #coarse pass at converting columns to numbers
    s=str(s)
    if re.match("week|month|year|yr",s):
        #pass over these, fix later
        return s
     
    try:
        
        numberpattern="(\d{1,3})"
        strnum=re.search(numberpattern,s).group(0)
        return int(strnum)
    except:
        return s
    
rawdf["days"]=rawdf["Days_en"].apply(lambda x: make_numeric(x))
rawdf["diameter"]=rawdf["Wheel size_en"].apply(lambda x: make_numeric(x))

#ok, fixing the rest...
tofix=[]
for i in rawdf.index:
    if not isinstance(rawdf["days"][i],int):
        tofix.append(rawdf["days"][i])
    if not isinstance(rawdf["diameter"][i],int):
        tofix.append(rawdf["diameter"][i])
tofix=set(tofix)        
        
#sort of cheating... but resorting to manual fixes
tofixdf=pd.DataFrame(tofix,columns=["unfixed"])
tofixdf.to_csv("tofix.csv",index=False)        
fixeddf=pd.read_csv("tofix_manual.csv") 
fixdict=dict(fixeddf.values)

for i in rawdf.index:
    if not isinstance(rawdf["days"][i],int):
        texttofix=rawdf["days"][i]
        rawdf["days"].loc[i]=fixdict[texttofix]
    if not isinstance(rawdf["diameter"][i],int):
        texttofix=rawdf["diameter"][i]
        rawdf["diameter"].loc[i]=fixdict[texttofix]

rawdf["days"]=rawdf["days"].apply(lambda x: float(make_numeric(x)))
rawdf["diameter"]=rawdf["diameter"].apply(lambda x: float(make_numeric(x)))

#ok, now make crank length numeric

def make_numeric_crank(s):
    #assume 1-digit is inches, 2 is cm, 3 is mm
    s=str(s)
    inchpattern="(\d{1}?)" 
    cmpattern="(\d{2}?)"
    mmpattern="(\d{3})"
    if re.match(mmpattern,s):
        lenstr=re.search(mmpattern,s).group(0)
        return float(lenstr)
    if re.match(cmpattern,s):
        lenstr=re.search(cmpattern,s).group(0)
        if float(lenstr)>80:
            return float(lenstr)
        else:
            return float(lenstr)*10
    if re.match(inchpattern,s):
        lenstr=re.search(inchpattern,s).group()
        return float(lenstr)*25.4
    

rawdf["crank_length"]=rawdf["Crank length_en"].apply(lambda x: make_numeric_crank(x))

rawdf["crank_length"].loc[11]=150
rawdf["crank_length"].loc[50]=145
rawdf["crank_length"].loc[91]=np.nan #don't believe this one
rawdf["crank_length"].loc[340]=np.nan #or this one
rawdf["crank_length"].loc[324]=np.nan #or this one


cleandf=rawdf[['Language', 'Date/time', 'lang code', 'Agen', 'Year startedn',
       'Country_en', 'Instructions_en', 'Other sports_en', 'Remarks_en', 'Gender', 'days',
       'diameter', 'crank_length']].copy()


cleandf.to_csv("cleaned_data.csv",index=False)


