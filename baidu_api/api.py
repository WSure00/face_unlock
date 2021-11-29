# encoding:utf-8
import requests
import base64
import cv2
import os


# client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id='6ieHyjIspHNtcX9g79twV4sT'
client_secret = 'G0X3zK8ZpQ6WmdeiXhlR8q5DBs1tjBVa'
access_token=''
img_path='./img_44e2695e-91ac-43bb-9b71-cfe50155bd1l.jpeg'
camera = cv2.VideoCapture(0)

def revert(img):
    # image=cv2.transpose(img)          #图像转置
    new_img = cv2.flip(img, 0)         #图像横置
    return new_img

def imgdata(img): 
    return str(base64.b64encode(img)[2:-1])


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

while True:

    success,img=camera.read()
    img_new=revert(img)
    get_token()
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    base=imgdata(img_new)
    params = {"image":base,"image_type":"BASE64","face_field":"age,beauty,face_shape,gender"}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        face_exsit=int(response.json()['result']['face_num'])
        face_token=response.json()['result']['face_list'][0]['face_token']
        print(face_token,face_exsit)
    cv2.imshow('face', img_new)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()


