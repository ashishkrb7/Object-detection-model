# Import libraries
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from models.experimental import *
from utils.datasetsCustom import *
from utils.utils import *
import time
import uuid
import json

# Configuration
path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")).replace("\\","/")
speech = json.load(open(path+"/setting/setting.json", "r")) # Installation instruction

# Methods
def VisualBot(INFERENCE_IMAGE_PATH_INPUT,conf_thres,iou_thres,out,model,save_img=True):
    """ Virtual bot inference method """

    item = dict()
    item["threshold"]=conf_thres
    item["name"]="CSS Corp Visual bot"

    # Run inference
    t0 = time.time()

    imgsz = check_img_size(640, s=model.stride.max())
    img, im0s = LoadImages(INFERENCE_IMAGE_PATH_INPUT, img_size=imgsz)
    # img = torch.zeros((1, 3, imgsz, imgsz), device='cpu')  # init img

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

    BoundingBox=[]

    img = torch.from_numpy(img).to('cpu')
    
    img = img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    t1 = torch_utils.time_synchronized()
    pred = model(img)[0]
    # Apply NMS
    pred = non_max_suppression(pred, conf_thres, iou_thres)#, classes=classes, agnostic=agnostic_nms)
    t2 = torch_utils.time_synchronized()

    # Process detections
    for _, det in enumerate(pred):  # detections per image

        s, im0 = '', im0s

        save_path = out+'/'+str(uuid.uuid4())+".jpg"

        s += '%gx%g ' % img.shape[2:]  # print string
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        if det is not None and len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class
                s += '%g %ss, ' % (n, names[int(c)])  # add to string

            # Write results
            for *xyxy, conf, cls in det:
                xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                corr=canvas(xywh,im0)
                corr.update({"score":str(conf.detach().numpy())})
                corr.update({"class_name":names[int(cls)]})
                corr.update({"name":speech[str(names[int(c)])]}) #{"name":"%s detected" % (names[int(c)])}
                BoundingBox.append(corr)
                del corr
                # print(xywh)

                # Save results (image with detections)
                if save_img:
                    label = '%s %.2f' % (names[int(cls)], conf)
                    plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)
                    cv2.imwrite(save_path, im0)
            
        # Print time (inference + NMS)
        print('%sDone. (%.3fs)' % (s, t2 - t1))
    item["numObjects"]=str(len(BoundingBox))
    BoundingBox.append(item)
    return(json.dumps(BoundingBox))

def canvas(normalized_coordinates,img0):
    """ Coordinate for canvas """
    key_name=["height","width","y","x"]
    x1, y1, w_size, h_size=normalized_coordinates[0], normalized_coordinates[1], normalized_coordinates[2],normalized_coordinates[3]
    x_start = round((x1 - (w_size/2))*img0.shape[1])
    y_start = round((y1 - (h_size/2))*img0.shape[0])    
    x_end = round((x_start + w_size*img0.shape[1]))
    y_end = round((y_start + h_size*img0.shape[0]))
    coordinates=[str((y_end-y_start)/img0.shape[0]),str((x_end-x_start)/img0.shape[1]),str(y_start/img0.shape[0]),str(x_start/img0.shape[1])]
    return(dict(zip(key_name,coordinates)))

# def speech(item):
#     """ Installation instruction """
#     itemlist = json.load(open(path+"/setting/setting.json", "r"))
#     # itemlist=dict()
#     # itemlist["Router"]="Router Identified. Show ethernet cable in front of the camera."
#     # itemlist["Ethernet cable"]="Ethernet cable identified. Show Power cable in front of the camera"
#     # itemlist["Power cable"]="Power cable identified. Show router back side"
#     # itemlist["Power port"]="Power port identified. Insert power chord to the power port on router"
#     # itemlist["Ethernet port"]="Ethernet port identified, Insert one end of ethernet cable to ethernet port"
#     # itemlist["Switch button"]="Switch button identified. Turn on the switch to start router"
#     return(itemlist.get(item))

