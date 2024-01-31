# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 09:22:13 2024

@author: benne
"""

import cv2
import os

def make_vid(frompath,topath,name):
    name=os.path.join(topath,name)
    images = [img for img in os.listdir(frompath) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(frompath, images[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(name+".mp4", fourcc, 10, (width,height))
    
    for image in images:
        video.write(cv2.imread(os.path.join(frompath, image)))
    
    cv2.destroyAllWindows()
    video.release()
    
def cleardir(path):
    for f in os.listdir(path):
        os.remove(os.path.join(path,f))