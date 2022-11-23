import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import os

def nothing (x):
    pass


folder_dir = "/Users/nishantnagururu/Documents/Nishant/OrchardRoboticsCodingProject" #my local path for the directory - needs to be changed to new local path to run properly
files = os.listdir(folder_dir)
images = []
for el in files:
    if(el.endswith(".jpeg")): #pulls out all the .jpeg files which are all the images
        images.append(el)

images = sorted(images) #sorts all the images so that the corresponding stereo images are next to each other in the list
i =0
while(i<len(images)-1):
    imgL = np.array(cv.imread(images[i],0)) #pulls the corresponding stereo images one pair at a time.
    imgR = np.array(cv.imread(images[i+1],0))
    stereo = cv.StereoBM_create()  #creates StereoBM object and sets its properties
    stereo.setNumDisparities(16)
    stereo.setBlockSize(15)
    stereo.setSpeckleRange(16)
    # stereo.setSpeckleWindowSize(8)
    disparity = stereo.compute(imgL, imgR) #creates disparity map
    disparity = np.array(disparity)
    depth = np.zeros([np.shape(disparity)[0],np.shape(disparity)[1]]) #creates depth map with same dimensions as disparity map
    for x in range(np.shape(disparity)[0]):
        for y in range(np.shape(disparity)[1]):
            if disparity[x,y] == 0: #prevents ZeroDivisionError
                depth[x,y] = 0
            else:
                depth[x,y] = 120/disparity[x,y] # converting disparity to depth. uses 120 mm disparity given in the project details.
    plt.imshow(depth,'gray') #creates depth plot
    plt.axis('off') # removes axes because its a relative plot
    plt.savefig("depth" +images[i][0:13]+".png") #saves image to local directory and includes the number identifier for the stereo pair in the file name
    i+=2


