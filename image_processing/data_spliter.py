import os
import numpy as np
import shutil
from tqdm import tqdm


src = r'D:\2020-21\yolov5\YOLO_visualbot\image_processing\Green'

def list_files(directory, extension):
    """ To list the files of particular extensions """
    return (f for f in os.listdir(directory) if f.endswith('.' + extension))

test_ratio = 0.20

image = os.listdir(src)

files_jpg = set([i.split(".jpg")[0] for i in image if i.endswith('.jpg')])
files_xml = set([i.split(".xml")[0] for i in image if i.endswith('.xml')])
print("Files not annotated:\n",list(map(lambda orig_string: orig_string + '.jpg', list(files_jpg-files_xml))))
image=list(set(image)-set(list(map(lambda orig_string: orig_string + '.jpg', list(files_jpg-files_xml)))))
image=[i for i in image if i.endswith('.jpg')]
np.random.shuffle(image)
train_FileNames, test_FileNames = np.split(np.array(image),[int(len(image)* (1 - test_ratio))])
train_FileNames = [src+'/'+ name for name in train_FileNames.tolist()]
test_FileNames = [src+'/' + name for name in test_FileNames.tolist()]

print("*****************************")
print('Total images: ', len(image))
print('Training: ', len(train_FileNames))
print('Testing: ', len(test_FileNames))
print("*****************************")

if not os.path.exists(src +'/train/'): os.makedirs(src +'/train/')
for name in tqdm(train_FileNames):
    # try:
    shutil.move(name, src +'/train/')
    shutil.move(name.split(".")[0]+".xml", src +'/train/')
    # except:
    #     pass
  
# shutil.make_archive('train', 'zip', src +'/train/')
# shutil.rmtree(src +'/train/')

if not os.path.exists(src +'/test/'): os.makedirs(src +'/test/')
for name in tqdm(test_FileNames):
    # try:
    shutil.move(name, src +'/test/')
    shutil.move(name.split(".jpg")[0]+".xml", src +'/test/')
    # except:
    #     pass
    
# shutil.make_archive('test', 'zip', src +'/test/')
# shutil.rmtree(src +'/test/')

print("Copying Done!")

 
