# import the necessary packages
import numpy as np
import cv2
from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import ImageTk, Image
import os
import time
import datetime, time

def secondCount():    
    a = 0
    while a < 1:
        for minutes in range(0, 1):
            for seconds in range(0, 6):
                 time.sleep(1)
                 print(seconds)
                 if seconds == 5:
                     a=3
def show_frame():
#Code below is a piece from http://kieleth.blogspot.com/2014/05/webcam-with-opencv-and-tkinter.html
#implemented to work with our project
    width, height = 550, 400
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
    
def takepic():
#Code below is from https://codeplasma.com/2012/12/03/getting-webcam-images-with-python-and-opencv-2-for-real-this-time/
#implemented to work with our project
    secondCount()
    # Camera 0 is the integrated web cam on my netbook
    camera_port = 0
 
    #Number of frames to throw away while the camera adjusts to light levels
    ramp_frames = 30
 
    # Now we can initialize the camera capture object with the cv2.VideoCapture class.
    # All it needs is the index to a camera port.
    camera = cv2.VideoCapture(camera_port)
 
     # Captures a single image from the camera and returns it in PIL format
    
        # read is the easiest way to get a full image out of a VideoCapture object.
    retval, im = camera.read()

 
    # Ramp the camera - these frames will be discarded and are only used to allow v4l2
    # to adjust light levels, if necessary

    print("Taking image...")
    # Take the actual image we want to keep
    camera_capture = im
    file = "test_image.png"
    # A nice feature of the imwrite method is that it will automatically choose the
    # correct format based on the file extension you provide. Convenient!
    cv2.imwrite(file, camera_capture)
 
# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
    del(camera)
def donothing():
    print "hey"
def makepic():
   filewin = Toplevel(root)
   img = ImageTk.PhotoImage(Image.open("result.png"))
   panel = Label(filewin, image = img)
   panel.pack(side = "bottom", fill = "both", expand = "yes")
   filewin.mainloop()
def censorbar():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:

		#keeps track of how many eyes detected
        eyecount=0
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
        	elif (eyecount % 2 == 0):
        		cv2.rectangle(roi_color,(topLeftX,topLeftY),(ex+ew,ey+eh),(0,0,0),-1)
     
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("./result.png", result_image)
    makepic()
def pickfile():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    image = cv2.imread(filename)
    result_image = image.copy()

    # Specify the trained cascade classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    #Preprocess the image
    grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayimg = cv2.equalizeHist(grayimg)

    #Run the classifiers
    flags=cv2.CASCADE_SCALE_IMAGE
    faces = face_cascade.detectMultiScale(grayimg, 1.1, 2, 0| cv2.CASCADE_SCALE_IMAGE, (30, 30))


    if len(faces) != 0:         # If there are faces in the images
        print "Faces detected"
        for f in faces:         # For each face in the image

            # Get the origin co-ordinates and the length and width till where the face extends
            x, y, w, h = [ v for v in f ]

            # get the rectangle img around all the faces
            cv2.rectangle(image, (x,y), (x+w,y+h), (255,255,0), 0)
            sub_face = image[y:y+h, x:x+w]
            # apply a gaussian blur on this new recangle image
            sub_face = cv2.GaussianBlur(sub_face,(45, 45), 45)
            # merge this blurry rectangle to our final image
            result_image[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face
            face_file_name = "./face_" + str(y) + ".jpg"
            cv2.imwrite(face_file_name, sub_face)
        

    #cv2.imshow("Detected face", result_image)
    cv2.imwrite("./result.png", result_image)
    makepic()

root = Tk()

lmain = Label(root)
lmain.pack()


#root.config(menu=menubar)
root.wm_title("Face Blur")


button = Button(text="Blur Face", command=pickfile)
button.place(x = 300, y = 100)
button2 = Button(text="Censor Bar", command=censorbar)
button2.place(x = 100, y = 100)
button2 = Button(text="Take Picture", command=takepic)
button2.place(x = 200, y = 200)
# runs showframe() if a webcam is detected
try:
	showframe()
# if a webcam is not detected, then changes the background to a default one
except:
	width, height = 550, 400
	root.minsize(width,height)
	root.maxsize(width,height)
	root.configure(background="black")
root.wm_title("Face Blur")
root.mainloop()

