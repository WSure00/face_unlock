#coding=utf-8

import threading
import face_recognition
import time
import numpy as np
from pathlib import Path

global my_face_encoding
global unknown_face_encoding
myface= Path("myface.npy")
start = time.clock()

def me_recognition():
    global my_face_encoding

    if myface.exists():
        my_face_encoding=np.load("myface.npy")
        print("my_face_encoding: ",time.clock()-start)
        return
    else:
        picture_of_me = face_recognition.load_image_file("me.jpg")
        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
        print("my_face_encoding: ",time.clock()-start)
        np.save("myface.npy",my_face_encoding)

def unknown():
    unknown_picture = face_recognition.load_image_file("re.jpg")
    global unknown_face_encoding
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
    print("unknown_face_encoding: ",time.clock()-start) 


def main():  
    b=time.clock()

    threads = []
    t1 = threading.Thread(target=me_recognition)
    threads.append(t1)
    t2 = threading.Thread(target=unknown)
    threads.append(t2)

    print("thread_before: ",time.clock()-start)
    for t in threads:
        t.start()
    print("thread_start: ",time.clock()-start)
    for t in threads:
            t.join()
    print("thread_end: ",time.clock()-start)
    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

    print("total : ",time.clock()-start)
    if results[0] == True:
        print("It's a picture of me!")
    else:
        print("It's not a picture of me!")


if __name__ == '__main__':
    main()