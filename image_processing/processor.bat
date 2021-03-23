@echo off
SET LOGFILE="%~dp0\logs\processor.log"
(echo====================================================================================================== >> %LOGFILE%)
(echo Script Start Running at - ^ %date% %time% >> %LOGFILE%)
call 
python "%~dp0\Videos2Images.py" --filename "PP.mp4" --fps 0.5 --imageExt .jpg --OutputName V2I
python "%~dp0\resize_images.py" --raw-dir "D:/2020-21/yolov5/YOLO_visualbot/image_processing/OutputDump" --save-dir "D:/2020-21/yolov5/YOLO_visualbot/image_processing/images" --ext jpg --target-size "(800, 600)"
(echo Script Successfully Executed at - ^ %date% %time% >> %LOGFILE%)
(echo====================================================================================================== >> %LOGFILE%)