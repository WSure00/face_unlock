# -*- coding: utf-8 -*-

import face_recognition
import cv2
import os
import time
import numpy as np
from pathlib import Path
from pykeyboard import PyKeyboard

import  psutil
for proc in psutil.process_iter():
    if (proc.name()=='python'):
        os.system("sudo renice 1 %s "%(proc.pid))


myface= Path("myface.npy")
camera = cv2.VideoCapture(1)
n=0
queue=[]
verify=4
faceon=True

def revert(img):
    # image=cv2.transpose(img)          #图像转置
    new_img = cv2.flip(img, 0)         #图像横置
    return new_img

def unlock(i):
    global queue
    global faceon
    flag=True
    if len(queue)>=i:
        for index in range(i):
            flag=queue[index] and flag

        queue.pop(0)
        if(flag):
            print ("====unlock===")
            if  os.system('gnome-screensaver-command -q | grep in') :
                k=PyKeyboard()
                k.tap_key(k.enter_key)
                os.system('gnome-screensaver-command -d')
                faceon=True
            
        else :
            faceon=False
            os.system('gnome-screensaver-command -l')
        return flag

if myface.exists():
    my_face_encoding=np.load("myface.npy")
    # print("my_face_encoding: ",time.clock()-start)
else:
    picture_of_me = face_recognition.load_image_file("me.jpg")
    my_face_encoding = face_recognition.face_encodings(picture_of_me,num_jitters=2,model='large')[0]
    # print("my_face_encoding: ",time.clock()-start)
    np.save("myface.npy",my_face_encoding)

while True:
    # start=time.clock()
    success,img=camera.read()
    img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    img_new=revert(img)
    marks = face_recognition.face_locations(img_new)
    if len(marks)!=0:
        if faceon :
            faceon=True
            print("sleep")
            time.sleep(1)
        
        else:
            flag=False
            # codings = face_recognition.face_encodings(img_new, known_face_locations=marks)
            # for coding in codings:
            coding = face_recognition.face_encodings(img_new,num_jitters=2,model='large')[0]
            result = face_recognition.compare_faces([my_face_encoding],coding,tolerance=0.4)
            flag=result[0]
            queue.append(flag)
            n+=1
            # print(queue)
            unlock(verify)
            print("flag: ",flag,n)
        
            
            # if result :
            #     os.popen('gnome-screensaver-command -d && xdotool key Return')
    else :
        faceon=False
        os.system('gnome-screensaver-command -l')
    # cv2.imshow('face', img_new)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
camera.release()
# cv2.destroyAllWindows()
