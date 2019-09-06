import sys , os ,logger , random
import numpy as np
#np.set_printoptions(threshold=sys.maxsize)
from random import randrange
import cv2
import glob
import argparse
#from guppy import hpy
script_dir = os.path.dirname(__file__)

class iterator: 
    def __init__(self,seed): 
        self.seed = seed
        self.cv_img = []

    def __iter__(self): 
        return self

    def __next__(self,image):
            self.image=image
            if self.seed % 32 == 0:
                for value in self.__generator__():
                    print(value) 
                    #cv2.imshow('Image Patch' ,value)
                    #cv2.waitKey(0) 
            else:
                try:
                    img = cv2.imread(self.image)
                    height , width =  img.shape[:2] 
                    start=randrange(0,200)                   #Using fixed value because of inconsistent dataset
                    end=randrange(0,200)
                    frame = img[ start : 512+start , end : 512+end ]
                    self.cv_img.append(frame)
                except cv2.error as e:
                    print(e)
            self.seed += 1

    def __generator__(self):
        for patch in self.cv_img[:]:
            yield patch
        print(str(self.seed) + ' Images Batch Completed')
        self.cv_img.clear()
        self.seed = 1 

def Run(ext):
     path = script_dir + '/data/' 
     c1 = iterator(1)
     temp = len(os.listdir(path))
     
     if args.ForeverRun == 'Yes' and args.Order == 'Random' :
        while True:
            for i in range(temp):
                Image = random.choice(glob.glob(path + ext))
                c1.__next__(Image)
            i=0
            temp = len(os.listdir(path))                # Fetch directory Updates
            
     if args.ForeverRun == 'Yes' and args.Order == 'Sequential' :
        while True:
            for i in range(temp):
                for eachimg in glob.glob(path + ext):
                    c1.__next__(eachimg)
                i = 0    
                temp = len(os.listdir(path))    
                
     if args.ForeverRun == 'No' and args.Order == 'Sequential' :
        for eachimg in glob.glob(path + ext):
            c1.__next__(eachimg)
            
     if args.ForeverRun == 'No' and args.Order == 'Random' :
        for i in range(temp):
            Image = random.choice(glob.glob(path + ext))
            c1.__next__(Image)


if __name__ == '__main__' : 
    parser = argparse.ArgumentParser()
    parser.add_argument('-F' , '--ForeverRun' , default='No' ,  help = " Choose 'Yes' or 'No' ")
    parser.add_argument('-O' , '--Order', default='Sequential' , help = " Choose 'Random' or 'Sequential' ")
    args = parser.parse_args()
    #sys.stdout = open("log.out", 'w')
    Run('*.jpg')