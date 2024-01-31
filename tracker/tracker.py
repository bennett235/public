# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 09:26:44 2024

@author: benne
"""
import cv2
import os
import shutil
from auxfuncts import cleardir,make_vid
import pandas as pd
import re
from PIL import Image,ImageDraw, ImageChops
import cv2
import matplotlib.pyplot as plt
import numpy as np

class Tracker():
    def __init__(self,movie,startframe,endframe,clipped=True,threshold=70,
                 scale=31.667):
        self.movie=movie
        self.threshold=threshold
        self.scale=scale
        self.vidcap=cv2.VideoCapture(self.movie)
        self.framerate=self.vidcap.get(5)
        self.rootpath=movie.split(".")[0]
        if os.path.exists(self.rootpath):
            shutil.rmtree(self.rootpath)
        os.mkdir(self.rootpath)
        shutil.copy(self.movie,os.path.join(self.rootpath,self.movie))
        os.mkdir(os.path.join(self.rootpath,"frames"))
        os.mkdir(os.path.join(self.rootpath,"diffs"))
        os.mkdir(os.path.join(self.rootpath,"blobs"))
        os.mkdir(os.path.join(self.rootpath,"path_add"))
        self.startframe=startframe
        self.endframe=endframe
        
    def framegrab(self):
        print(f"Framegrabbing from {self.movie} from frame {self.startframe} to {self.endframe}")
        cleardir(os.path.join(self.rootpath,"frames"))        
        count=1        
        success=True
        while success:
            success,image=self.vidcap.read()
            if count>=self.startframe and count<=self.endframe:
                cv2.imwrite(self.rootpath+"\\frames\\frame-"+f"{count:03d}"+".jpg",image)
            count+=1
    
    def set_startstop(self):
        print("Select starting and ending frame number to truncate video\n")
        self.startframe=input("Starting frame?")
        self.endframe=input("Ending frame?")
                
    def timestamps(self):
        print(f"Applying timestamps with framerate= {self.framerate}")
        frames=os.listdir(os.path.join(self.rootpath,"frames"))
        framedf=pd.DataFrame(columns=["frame","id","time"])
        framedf["frame"]=frames
        framedf["id"]=framedf["frame"].apply(lambda x:  int(re.search(r"-(\d+)",x).group(1)))
        start=framedf["id"].min()
        framedf["time"]=framedf["id"].apply(lambda x: (x-start)*1/self.framerate)
        framedf.sort_values("time",inplace=True)
        framedf.reset_index(drop=True,inplace=True)
        framedf.to_csv(os.path.join(self.rootpath,"timestamps.csv"),index=False)
        return framedf

    def calibrate(self):
        firstframe=os.listdir(os.path.join(self.rootpath,"frames"))[0]
        frame=Image.open(os.path.join(self.rootpath,"frames",firstframe))       
        width,height = frame.size
        xstart=50
        xend=50
        ystart=350
        yend=1490
        draw=ImageDraw.Draw(frame)
        draw.line((xstart,ystart,xend,yend),fill=(128,128,0),width=7)
        frame.show()
        
        self.scale=(yend-ystart)/36
        
        print(f"scale is {self.scale:.4f} pixels/in")
        frame.save(os.path.join(self.rootpath,"dimcal.jpg"),"JPEG")

    def find_diffs(self):
        print("Finding ball with sequential pixel differences")
        cleardir(os.path.join(self.rootpath,"diffs"))
        
        framedf=pd.read_csv(os.path.join(self.rootpath,"timestamps.csv"))
        imlist=framedf["frame"]
      
        for i in range(1,len(imlist)):
            frameid=re.search("(\d+)",imlist[i]).group(0)
            img1=Image.open(os.path.join(self.rootpath,"frames",imlist[i-1]))
            img2=Image.open(os.path.join(self.rootpath,"frames",imlist[i])) 
            diff = ImageChops.difference(img1, img2) 
            diff.save(os.path.join(self.rootpath,"diffs","diff_"+frameid+".jpg"),"JPEG")        
        make_vid(os.path.join(self.rootpath,"diffs"),self.rootpath,"diffs")
     
    def centroids(self):
        print("finding centroids of difference blobs")
        diffs=os.listdir(os.path.join(self.rootpath,"diffs"))
        trackdf=pd.DataFrame(columns=["frame","x","y"])
        
        cleardir(os.path.join(self.rootpath,"blobs"))
        
        for d in diffs:
            frame=re.search("(\d+)",d).group()
            img=cv2.imread(os.path.join(self.rootpath,"diffs",d))
            # convert image to grayscale image
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
             
            # convert the grayscale image to binary image
            ret,thresh = cv2.threshold(gray_image,70,255,0)
             
            # calculate moments of binary image
            M = cv2.moments(thresh)
             
            # calculate x,y coordinate of center
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
             
            # put text and highlight the center
            cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
            cv2.putText(img, "ball center", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
             
            cv2.imwrite(os.path.join(self.rootpath,"blobs","blob"+frame+".jpg"),img)
            trackdf.loc[len(trackdf)]=[frame,cX,cY]
        
        
        trackdf.to_csv(os.path.join(self.rootpath,"blobtrack.csv"))
        
        make_vid(os.path.join(self.rootpath,"blobs"),self.rootpath,"blobs")
        return trackdf


    def build_track(self):
        print("Defining track in real and pixel coordinates")
        print(f"scale= {self.scale} pixels/inch")
        timestamps=pd.read_csv(os.path.join(self.rootpath,"timestamps.csv"))
        blobdf=pd.read_csv(os.path.join(self.rootpath,"blobtrack.csv"))
        
        outdf=pd.merge(timestamps,blobdf,left_on="id",right_on="frame")
        outdf.drop(["Unnamed: 0","frame_y"],inplace=True,axis=1)
        outdf["x_real"]=(outdf["x"]-outdf["x"][0])/self.scale
        outdf["y_real"]=-(outdf["y"]-outdf["y"][0])/self.scale
        outdf.to_csv(os.path.join(self.rootpath,"track.csv"),index=False)
        
       
        
        fig,(ax1,ax2)=plt.subplots(2,sharex=True)
        fig.suptitle("Ball Track")
        ax1.plot(outdf["time"],outdf["x_real"],marker="o")
        ax2.plot(outdf["time"],outdf["y_real"],marker="o")
        
        
        plt.xlabel("Time [s]")
        ax1.set_ylabel("X Position [in")
        ax2.set_ylabel("Y Position [in]")
        
        plt.savefig(os.path.join(self.rootpath,"track.png"),dpi=300)
        plt.show()
        return outdf


    def draw_curve(self):
        cleardir(os.path.join(self.rootpath,"path_add"))
        
        track=pd.read_csv(os.path.join(self.rootpath,"track.csv"))
        
        x0=int(track["x"][0])
        y0=int(track["y"][0])
        locs=(x0,y0)
        
        for i in track.index:
            filename=track.loc[i]["frame_x"]
            image=Image.open(os.path.join(self.rootpath,"frames",filename))
            locs=locs+(track.loc[i]["x"],track.loc[i]["y"],)
            
            draw=ImageDraw.Draw(image)
            draw.line(locs,fill=(255,255,0),width=18)
            image.save(os.path.join(self.rootpath,"path_add",filename))
        
        make_vid(os.path.join(self.rootpath,"path_add"),self.rootpath,"wpath")
    
    def build_output(self):
        self.framegrab()
        self.timestamps()
        framedf=self.timestamps()
        self.find_diffs()
        trackdf=self.centroids()
        outdf=self.build_track()
        self.draw_curve()
        output={}
        output["framedf"]=framedf
        output["trackdf"]=trackdf
        output["outdf"]=outdf
        return output
        
if __name__=="__main__":
    moviefile="toss.mp4"
    track=Tracker(moviefile,8,43)
    outfiles=track.build_output()
  