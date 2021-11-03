# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 20:24:32 2021

@author: Bennett
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 18:37:04 2021

@author: Bennett
"""

import pandas as pd
import re
from deep_translator import GoogleTranslator

"""
survey data from Bill Klaas, unicyclist@xs4all.nl
deep_translator documentation: https://github.com/nidhaloff/deep-translator#usage



"""
#codes for Google Translator API
langdict={"English":"en",
          "Dutch":"nl",
          "German":"de",
          "French":"fr",
          "Japanese":"ja",
          "Spanish":"es",
          "Korean":"ko"}

#read excel file
rawdf=pd.read_excel("agelearn_2021_anonymised_20211102.xlsx")
rawdf.drop(0,axis=0,inplace=True)
rawdf.drop(rawdf.index[1:5],axis=0,inplace=True)

#drop unneeded columns, strip partial cleans
rawdf.drop(["Unnamed: 0","Name","E-mail","Agree",'|', 'Date/time.1', 'Country.1', 'M=1', 'Age',
       'Year started.1', 'Hours.1', 'Days.1', 'Wheel size.1', 'Crank length.1',
       'Instructions.1', 'Other sports.1', 'Remarks.1'],axis=1,inplace=True)

#strip and save verbose questions
verboseqs=rawdf.loc[1].copy()

#initial cleaning
rawdf.drop(1,axis=0,inplace=True)
rawdf.reset_index(inplace=True,drop=True)
rawdf.drop(rawdf.index[783:],axis=0,inplace=True)
rawdf["Date/time"]=rawdf["Date/time"].apply(pd.to_datetime)
rawdf["lang code"]=rawdf["Language"].apply(lambda x: langdict[x])

#functions to convert numbers in text format to numeric
def make_numeric(s):
    if s=="Nine":
        return 9
    if s=="Twenty":
        return 20
    if s=="A los ":
        return 0   
    try:
        s=str(s)
        numberpattern="(\d{1,2})"
        strnum=re.search(numberpattern,s).group(0)
        return int(strnum)
    except:
        return s

def make_numericyr(s):
    
    try:
        s=str(s)
        numberpattern="(\d{4})"
        strnum=re.search(numberpattern,s).group(0)
        return int(strnum)
    except:
        return 2021
rawdf["Agen"]=rawdf["Age started"].apply(lambda x: int(make_numeric(x)))
rawdf["Year startedn"]=rawdf["Year started"].apply(lambda x: make_numericyr(x))

#translate non-English text 
#time-intensive, so pickle dataframe at this point for further work

textcols=["Country", 'Hours', 'Days', 'Wheel size',
       'Crank length',"Gender","Instructions","Other sports","Remarks"]
rawdf["Country_en"]=""
rawdf["Hours_en"]=""
rawdf["Days_en"]=""
rawdf["Wheel size_en"]=""
rawdf["Crank length_en"]=""
rawdf["Gender_en"]=""
rawdf["Instructions_en"]=""
rawdf["Other sports_en"]=""
rawdf["Remarks_en"]=""

for textcol in textcols:
    for i in rawdf.index:
        if rawdf["lang code"][i]=="en":
            pass
            rawdf[textcol+"_en"].loc[i]=rawdf[textcol][i]
        else:
            totranslate=str(rawdf[textcol][i])
            lang=rawdf["lang code"][i] 
            try:
                textout=GoogleTranslator(source=lang,target="en").translate(text=totranslate)
                rawdf[textcol+"_en"].loc[i]=textout
            except:
                rawdf[textcol+"_en"].loc[i]=totranslate
                
rawdf.to_pickle("rawdf.pkl")
rawdf.to_excel("translated.xlsx")
verboseqs.to_csv("verboseqs.csv") 
print("initial cleaning complete")           