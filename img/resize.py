import cv2
import os

img = cv2.imread("me.jpg", -1)
re=720/img.shape[1]
print('Original Dimensions : ', img.shape)

img2 = cv2.resize(img, (int(img.shape[1]*re), int(img.shape[0]*re)), interpolation = cv2.INTER_AREA)

print('Resized Dimensions : ', img2.shape)

cv2.imwrite("mere.jpg", img2)