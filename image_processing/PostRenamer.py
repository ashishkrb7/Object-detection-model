import os
from tqdm import tqdm

def main(path,extension,alias):
   """ Function to rename multiple files """
   i = 0
   image=[j for j in os.listdir(path) if j.endswith(extension)]
   for filename in tqdm(image):
      my_dest =alias + str(i) + extension
      my_source =path + filename
      my_dest =path + my_dest
      os.rename(my_source, my_dest)
      i += 1

# Driver Code
if __name__ == '__main__':
    path=r"C:\Users\css120804\Desktop\EthernetCable_Annotated_final/"
    extension=".jpg"
    alias="ethernetcable_"
    main(path,extension,alias)
    extension=".xml"
    main(path,extension,alias)