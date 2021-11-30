# encoding:utf-8
import time
import requests
import base64
import cv2
import os
from pykeyboard import PyKeyboard
from requests.models import requote_uri

client_id='6ieHyjIspHNtcX9g79twV4sT'
client_secret = 'G0X3zK8ZpQ6WmdeiXhlR8q5DBs1tjBVa'
access_token=''
img_path='./img_44e2695e-91ac-43bb-9b71-cfe50155bd1l.jpeg'
myface_token="774e76a9c092ab8c5a3e4c8c5f6eec35"
noface_token=""
camera = cv2.VideoCapture(1)

def pid_pri():                #升级线程优先级
    import  psutil
    for proc in psutil.process_iter():
        if (proc.name()=='python'):
            os.system("sudo renice 1 %s "%(proc.pid))

def notify(title,message):
    os.environ.setdefault('DISPLAY', ':0.0')
    os.system('notify-send -i "notification-message-IM" "'+title+'" "'+message+'"')


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
        print(response.json())
        if response.json()['error_msg'] == 'SUCCESS':   #检测到存在人脸
            face_token=response.json()['result']['face_list'][0]['face_token']
            face_exsit=True
            noface_token=face_token
            # print(face_token)
        elif response.json()['error_msg'] ==  'pic not has face':   #检测到没有存在人脸
            face_exsit=False
    return face_exsit

get_token()
base=str(base64.b64encode(cv2.imencode('.jpg',cv2.imread("./me.jpg"))[1]))[2:-1]
face_info(base)