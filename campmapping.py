# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 11:28:44 2020

@author: Bennett
"""


import pandas as pd
import folium

nyparks=pd.read_csv("https://data.ny.gov/api/views/9uuk-x7vh/rows.csv")
nyforest1=pd.read_csv("https://data.ny.gov/api/views/5zxz-z3ci/rows.csv")
nyforest2=pd.read_csv("https://data.ny.gov/api/views/tnqf-vydw/rows.csv")

nyforest2.columns=['Name', 'County', 'Facility URL', 'Latitude', 'Longitude', 'Location']
nyparks=nyparks[nyparks["Camp"]=="Y"]

campgrounds=pd.concat([nyparks,nyforest1,nyforest2],ignore_index=True)
campgrounds.drop([ 'Region', 'Golf', 'Camp', 'Playground',  'Nature Center',  'Golf URL','Nature Center URL',  'Location'],axis=1,inplace=True)

campmap=folium.Map(location=[42.7675904,-73.9114415],  zoom_start=9)
   
for i,row in campgrounds.iterrows():
    popuplink=folium.Popup("<a href=" + row["Facility URL"] + ">" + row["Name"] +' </a>')
    folium.CircleMarker((row.Latitude,row.Longitude), popup=popuplink,radius=3, weight=2, color='red', fill_color='red', fill_opacity=.5).add_to(campmap)
  
campmap.save('camp.html')
