import face_recognition
import time
import numpy as np
from pathlib import Path

b=time.clock()
start = time.clock()
myface= Path("myface.npy")

if myface.exists():
    my_face_encoding=np.load("myface.npy")

else:
    picture_of_me = face_recognition.load_image_file("me.jpg")
    my_face_encoding = face_recognition.face_encodings(picture_of_me,num_jitters=2)[0]

    np.save("myface.npy",my_face_encoding)

start = time.clock()

unknown_picture = face_recognition.load_image_file("un2.jpeg")
# unknown_face_location=face_recognition.face_locations("un2.jpeg")
unknown_face_encoding = face_recognition.face_encodings(unknown_picture,num_jitters=2)[0]

results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding,0.5)
dis=face_recognition.api.face_distance( [my_face_encoding] , unknown_face_encoding )
print(results)
print(dis)
# print(results)

if results[0] == True:
    print("It's a picture of me!")
else:
    print("It's not a picture of me!")