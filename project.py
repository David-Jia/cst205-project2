# Names: Harrison Oglesby, Brandon Martinez, David Jia
# Trello: https://trello.com/b/BBmBhBGL/team-52-project-2-cst-205
# Github: https://github.com/HarrisonOg/cst205-project2
# Description: Description:  Face-blurring and eye-censoring program that uses Gaussian-style
# faceblurring to mask people's identity.
# If the user has a webcam, they are able to take pictures to perform face-blurring or eye-censoring on.

# Uses the OpenCV and Tkinter libraries in Python 2.7.

# import the necessary packages
import numpy as np
import cv2
from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import ImageTk, Image
import random
import os
import time
import datetime, time

# Countdown for when takepic() is used, counts 1, 2, 3, 4, 5 then takes the picture
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
#if webcam is detected, makes the background be what the connected webcam is showing
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
#Takes a picture with the connected webcam and saves the image
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
    file = "./result_" + str(int(random.random() * 1000)) + ".png"
    # A nice feature of the imwrite method is that it will automatically choose the
    # correct format based on the file extension you provide. Convenient!
    cv2.imwrite(file, camera_capture)
 
# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
    del(camera)

def donothing():
    print "hey"

# opens the resulting image after face blurring or eye censoring
def makepic():
   filewin = Toplevel(root)
   img = ImageTk.PhotoImage(Image.open("result.png"))
   panel = Label(filewin, image = img)
   panel.pack(side = "bottom", fill = "both", expand = "yes")
   filewin.mainloop()

# creates a sensor bar over the eyes
def censorbar():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    img = cv2.imread(filename) # reads the file
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # creates a grey version of the image to make the face 
    											 # recognition work a little better

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
     
    censorFileName = "./result_" + str(int(random.random() * 1000)) + ".png"
    cv2.imwrite(censorFileName, img)
    cv2.imshow(censorFileName, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    makepic()
    
# blurs the face
def blur():
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
        
    blurFileName = "./result_" + str(int(random.random() * 1000)) + ".png"
    cv2.imwrite(blurFileName, result_image)
    cv2.imshow(blurFileName, result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    makepic()

root = Tk()

lmain = Label(root)
lmain.pack()

# buttons the appear for the GUI
button = Button(text="Blur Face", command=blur)
button.place(x = 300, y = 100)
button2 = Button(text="Censor Bar", command=censorbar)
button2.place(x = 100, y = 100)
button2 = Button(text="Take Picture", command=takepic)
button2.place(x = 200, y = 200)
# runs showframe() if a webcam is detected
try:
	showframe()
# if a webcam is not detected, then changes the background to a default one, otter background
except:
	width, height = 550, 400
	root.minsize(width,height)
	root.maxsize(width,height)
	im = Image.open("otter.jpg")
	tkimage = ImageTk.PhotoImage(im)
	myvar = Label(root, image = tkimage)
	myvar.place(x=0,y=0,relwidth=1,relheight=1)
	myvar.lower()
root.wm_title("Face Blur")
root.mainloop()

