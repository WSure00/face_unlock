import cv2
#引入库

cap = cv2.VideoCapture(1)

def revert(img):
    # image=cv2.transpose(img)
    image = cv2.flip(img, 0)
    return image

while True:
    ret, frame = cap.read()
    img=revert(frame)
    cv2.imshow("Video", img)
#读取内容
    if cv2.waitKey(10) == ord("q"):
        break
        
#随时准备按q退出
cap.release()
cv2.destroyAllWindows()