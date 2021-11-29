# encoding:utf-8
import requests
import base64

# client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id='6ieHyjIspHNtcX9g79twV4sT'
client_secret = 'G0X3zK8ZpQ6WmdeiXhlR8q5DBs1tjBVa'
access_token=''
img_path='./me.jpg'

def imgdata(img_path):
    
    f=open(r'%s' % file1path,'rb') 
    pic1=base64.b64encode(f.read()) 
    f.close()
    #将图片信息格式化为可提交信息，这里需要注意str参数设置
    params = {"images":str(pic1,'utf-8')}
    return params


def get_token():
    global access_token
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(client_id,client_secret)
    response = requests.get(host)
    if response:
        access_token=response.json()["access_token"]
        print(access_token)
    else:
        print('access_token:error')
        exit(0)
get_token()

request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

params = "{\"image\":img,\"image_type\":\"FACE_TOKEN\",\"face_field\":\"faceshape,facetype\"}"
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/json'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())


