# encoding:utf-8
import time
import requests
import base64
import cv2
import os
from pykeyboard import PyKeyboard
from requests.models import requote_uri

import  psutil
for proc in psutil.process_iter():
    if (proc.name()=='python'):
        os.system("sudo renice 1 %s "%(proc.pid))

client_id='6ieHyjIspHNtcX9g79twV4sT'
client_secret = 'G0X3zK8ZpQ6WmdeiXhlR8q5DBs1tjBVa'
access_token=''
img_path='./img_44e2695e-91ac-43bb-9b71-cfe50155bd1l.jpeg'
myface_token="774e76a9c092ab8c5a3e4c8c5f6eec35"
noface_token=""
camera = cv2.VideoCapture(1)

def revert(img):
    # image=cv2.transpose(img)          #图像转置
    new_img = cv2.flip(img, 0)         #图像横置
    return new_img

def img_base(img): 
    img_np=cv2.imwrite("./io.jpg",img)
    img_base=cv2.imread("./io.jpg")
    return str(base64.b64encode(cv2.imencode('.jpg',img_base)[1]))[2:-1]


def get_token():
    global access_token
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(client_id,client_secret)
    response = requests.get(host)
    if response:
        access_token=response.json()["access_token"]
        # print(access_token)
    else:
        print('access_token:error')
        exit(0)

def face_info(base):
    global noface_token
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params = {"image":base,"image_type":"BASE64"}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        # print(response.json())
        if response.json()['error_msg'] == 'SUCCESS':   #检测到存在人脸
            face_token=response.json()['result']['face_list'][0]['face_token']
            face_exsit=True
            noface_token=face_token
            # print(face_token)
        elif response.json()['error_msg'] ==  'pic not has face':   #检测到没有存在人脸
            face_exsit=False
    return face_exsit

def face_compare():
    
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
    params =  [{"image": myface_token, "image_type": "FACE_TOKEN", "face_type": "LIVE", "quality_control": "LOW"},
    {"image":noface_token, "image_type": "FACE_TOKEN", "face_type": "LIVE", "quality_control": "LOW"}]      #   %(myface_token,noface_token)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, json=params, headers=headers)
    # if response:
    #     print (response.json())
    if response.json()["error_msg"] == 'SUCCESS':
        result=int(response.json()['result']['score'])
    else:
        result=0
        print("face_compare: error ")
    return result

get_token()

while True:
    time.sleep(0.5)
    os.system('/opt/vc/bin/tvservice -p')
    #  检测摄像头读出的图片
    success,img=camera.read()
    img_new=revert(img)
    base=img_base(img_new)
    # base=str(base64.b64encode(cv2.imencode('.jpg',cv2.imread("./me.jpg"))[1]))[2:-1]  #检测单张图片
    if face_info(base) :
        print("ok")
        # print(noface_token)
        result=face_compare()
        if result >=80:
            if  os.system('gnome-screensaver-command -q | grep in') :
                k=PyKeyboard()
                k.tap_key(k.enter_key)
                os.system('gnome-screensaver-command -d')
        # else:
        #     os.system('gnome-screensaver-command -l')
    else:
        os.system('gnome-screensaver-command -l')
        print("no")
    
    # cv2.imshow('face', img_new)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
camera.release()
# cv2.destroyAllWindows()


