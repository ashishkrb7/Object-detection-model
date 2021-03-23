import os 
import cv2
from tqdm import tqdm
import numpy as np
path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".")).replace("\\", "/") # To get current working path

def main(): 
    # path of the folder containing the raw images 
    inPath =path+"/OutputDump"
  
    # path of the folder that will contain the modified image 
    outPath =path+"/rotated"
    if not os.path.exists(outPath): os.makedirs(outPath)
  
    for imagePath in tqdm(os.listdir(inPath)): 
        # imagePath contains name of the image  
        inputPath = os.path.join(inPath, imagePath) 
  
        # inputPath contains the full directory name 
        img = cv2.imread(inputPath)
        imgrot = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)

        fullOutPath = os.path.join(outPath, 'rotated_'+imagePath) 

        cv2.imwrite(fullOutPath, imgrot)
  
# Driver Function 
if __name__ == '__main__': 
    main() 