import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

img = cv2.imread('test.jpg')
result = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#keeps track of how many eyes detected
eyecount = 0

faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255))
    alt_face = img[y:y+h, x:x+w]
    alt_face = cv2.GaussianBlur(alt_face,(23, 23), 30)
    
    result[y:y+alt_face.shape[0], x:x+alt_face.shape[1]] = alt_face
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        eyecount+=1
        #takes the top left point of the first eye
        if (eyecount % 2 == 1):
        	topLeftX = ex
        	topLeftY = ey
        #takes the bottom right point of the second eye and draws a censor rectangle between the
        #two points
        if (eyecount % 2 == 0):
        	cv2.rectangle(roi_color,(topLeftX,topLeftY),(ex+ew,ey+eh),(0,0,0),-1)

        	

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
