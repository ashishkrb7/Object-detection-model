# Image processor

## Introduction
Python package to extract the images from the videos and for image preprocessing works like rotation, resizing. In addition tothat converting xml to YOLO data format

## Directory architecture
```
        D:.
        │   data_spliter.py
        │   PostRenamer.py
        │   Readme.md
        │   renamer.py
        │   requirements.txt
        │   resize_images.py
        │   rotation.py
        │   Videos2Images.py
        │   xml2yolo.py
        │   xml_to_csv.py
        │
        └───SourceDump
```
- SourceDump        : Put your videos here
- requirements.txt  : Requirements for python module

## Command to run 
*For help use*
```python
python Videos2Images.py -h
python resize_images.py -h
```
*Example*
```bash
python Videos2Images.py --filename VID20210308074805.mp4 --fps 0.5 --imageExt .jpg --OutputName Router

python resize_images.py --raw-dir "C:/Users/css120804/Desktop/Video/Videos to images/pc" --save-dir "C:/Users/css120804/Desktop/images" --ext jpg --target-size "(800, 600)"
```

# Author
Ashish Kumar

For any clarification on code, please feel free to drop an email to **Ashish.Kashyap@csscorp.com**

Made with ❤️ in India
