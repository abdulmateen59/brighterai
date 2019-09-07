#!/usr/bin/python3
'''
    todo:
        
        
'''

import sys , os , random
import numpy as np
#np.set_printoptions(threshold = sys.maxsize)
from random import randrange
import cv2
import glob
import argparse
#from guppy import hpy


class iterator: 
    def __init__(self,size): 
        self.seed = 1
        self.size = size
        self.cv_img = []

    def __iter__(self): 
        return self

    def __next__(self,image):
            if self.seed-1  == self.size:
                for value in self.__generator__():
                    print(value)
                    #cv2.imshow('Image Patch' , value)                          #Uncomment these 3 lines to see the 512*512 images 
                    #cv2.waitKey(1000)
                    #cv2.destroyAllWindows()
            else:
                try:
                    img = cv2.imread(image)
                    height , width =  img.shape[:2] 
                    start = randrange(0,200)                                    #Using fixed value because of inconsistent dataset
                    end = randrange(0,200)
                    frame = img[ start : 512+start , end : 512+end ]
                    self.cv_img.append(frame)
                    self.seed += 1
                except cv2.error as e:
                    print(e)
            

    def __generator__(self):
        for patch in self.cv_img[:]:
            yield patch
        print('#' * 25 + '   ' + str((self.seed)-1)+ '   Images Batch Completed   ' + '#' * 25)
        self.cv_img *= 0
        #self.cv_img.clear()                 #For Latest Python version use this method for clearing
        self.seed = 1                       #Avoiding Seed Overflow

def run(dsDir,ext):
     path = (os.path.dirname(os.path.abspath(__file__)) + os.sep + dsDir + os.sep)
     itr = iterator(32)
     temp = len(os.listdir(path))
     
     if args.ForeverRun == 'Yes' and args.Order == 'Random' :
        while True:
            for i in range(temp):
                Image = random.choice(glob.glob(path + ext))
                itr.__next__(Image)
            i=0
            temp = len(os.listdir(path))                                         #Fetch directory Updates

     elif args.ForeverRun == 'Yes' and args.Order == 'Sequential' :
        while True:
            for i in range(temp):
                for eachimg in glob.glob(path + ext):
                    itr.__next__(eachimg)
                i=0    
                temp = len(os.listdir(path))

     elif args.ForeverRun == 'No' and args.Order == 'Sequential' :
        for eachimg in glob.glob(path + ext):
            itr.__next__(eachimg)
            
     elif args.ForeverRun == 'No' and args.Order == 'Random' :
        for i in range(temp):
            Image = random.choice(glob.glob(path + ext))
            itr.__next__(Image)
     else:
        print('~' * 50 + " Invalid Parameters " + '~' * 70)


if __name__ == '__main__' : 
    parser = argparse.ArgumentParser()
    parser.add_argument('-F' , '--ForeverRun' , default = 'No' ,  help = " Choose 'Yes' or 'No' ")
    parser.add_argument('-O' , '--Order', default = 'Sequential' , help = " Choose 'Random' or 'Sequential' ")
    args = parser.parse_args()
    #sys.stdout = open("log.out", 'w')
    dsDir = 'data'
    run(dsDir,'*.jpg')
