import os
from tqdm import tqdm

def main():
   """ Function to rename multiple files """
   i = 0
   path=r"D:\2020-21\yolov5\YOLO_visualbot\image_processing\Green/"
   image=[j for j in os.listdir(path) if j.endswith('.jpg')]
   for filename in tqdm(image):
      my_dest ="GreenPart2_" + str(i) + ".jpg"
      my_source =path + filename
      my_dest =path + my_dest
      os.rename(my_source, my_dest)
      i += 1
# Driver Code
if __name__ == '__main__':
   main()