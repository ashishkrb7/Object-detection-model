""" 
        +-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-+
        |o||b||j||e||c||t||-||d||e||t||e||c||t||i||o||n||-||m||o||d||e||l|
        +-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-+
Developed by: Ashish Kumar
"""
print(__doc__)

#  Import dependencies
from src.engine import *
import logging
import os
from datetime import date,datetime
from flask import Flask,request, jsonify, make_response, Response
from cheroot import wsgi
import argparse
import json
import sys

# App initialization
app=Flask(__name__)

@app.after_request
def after_request(response):
    """ Cross Origin Resource Sharing """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST') # Put any other methods you need here
    return response

@app.route('/')
def index():
    """ To check the app is working or not """
    return Response('Your web services are working, Available endpoints are ./local, ./test, ./visualbot/router')
    
@app.route('/test')
def test():
    """ Testing image on folder """
    try:
        ip_address = request.remote_addr
        
        output=VisualBot(INFERENCE_IMAGE_PATH_INPUT,conf_thres,iou_thres,INFERENCE_IMAGE_PATH_OUTPUT,model_router,save_img)
        print(f"Testing successfully at {str(datetime.utcnow())}")
        logging.info(f"Execution Successful for {ip_address}")
        
        Result=jsonify(output),200,{"Content-Type":"application/json"}
        return (Result)
    except:
        error = "Oops! " + str(sys.exc_info()) + " occured."
        Result=jsonify(error),404,{"Content-Type":"application/json"}
        logging.error("ERROR occured", exc_info=True)   
        return(Result)

@app.route('/local')
def local():
    """ Activate webrtc """
    return Response(open('./static/local.html').read(), mimetype="text/html")

@app.route('/visualbot/router', methods = ['POST'])
# @token_required
def GetRouter():
    """ To get router """
    try:
        ip_address = request.remote_addr

        image_file = request.files['image']
        conf_thres=float(request.form.get('threshold'))

        output=VisualBot(image_file,conf_thres,iou_thres,INFERENCE_IMAGE_PATH_OUTPUT,model_router,save_img)

        print(f"Scanned successfully at {str(datetime.utcnow())}")
        logging.info(f"Execution Successful for {ip_address}")
        Result=jsonify(output),200,{"Content-Type":"application/json"}
        return (Result)

    except:
        error = "Oops! " + str(sys.exc_info()) + " occured."
        Result=jsonify(error),404,{"Content-Type":"application/json"}
        logging.error("ERROR occured", exc_info=True)   
        return(Result)

if __name__=='__main__':

    # Logging API hits
    logging.basicConfig(level=logging.DEBUG,
                        handlers=[logging.FileHandler(f'./logs/app_{date.today().isoformat()}.log', 'a', 'utf-8')],
                        format="%(asctime)s %(levelname)-6s - %(funcName)-8s - %(filename)s - %(lineno)-3d - %(message)s",
                        datefmt="[%Y-%m-%d] %H:%M:%S - ",
                        )
                        
    # Configuration
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./.")).replace("\\","/")

    model_path=speech = json.load(open(path+"/setting/model.json", "r")) # Installation instruction

    # INFERENCE_IMAGE_PATH_INPUT=path+"/inference/images"
    INFERENCE_IMAGE_PATH_INPUT=path+"/inference/images/router.jpg"

    INFERENCE_IMAGE_PATH_OUTPUT=path+"/inference/output"

    if not os.path.exists(INFERENCE_IMAGE_PATH_OUTPUT):os.makedirs(INFERENCE_IMAGE_PATH_OUTPUT)  

    ROUTER_MODEL_PATH=path+model_path["ROUTER_MODEL_PATH"] # Only detect Router in image

    conf_thres=0.7
    iou_thres=0.5
    save_img=True
    device='cpu'

    # Load models in workspace
    print("Model loaded successfully")
    model_router = attempt_load(ROUTER_MODEL_PATH, map_location=device)  # load FP32 model

    if not os.path.exists(INFERENCE_IMAGE_PATH_OUTPUT):os.makedirs(INFERENCE_IMAGE_PATH_OUTPUT)  

    parser=argparse.ArgumentParser()
    parser.add_argument('-p',"--port",type=int,help='Port of the server',default=5003)
    parser.add_argument('-e',"--env",type=str,help='Server environment',default="dev")
    args=parser.parse_args()
    if args.env=="dev":
        """ Development server """
        app.run(host='0.0.0.0', port= args.port,debug=True,threaded=True,processes=1)
    elif args.env=="prod":
        """ Production server """
        server = wsgi.Server(bind_addr=('0.0.0.0', int(args.port)), wsgi_app=app, numthreads=100,)
        server.start()