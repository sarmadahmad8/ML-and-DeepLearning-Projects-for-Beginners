import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

brushThickness = 50 #select brush thickness
eraserThickness = 80 #select eraser thickness
folderPath = "Header" # not necessary but for customizing purposes
myList = os.listdir(folderPath) #put file names in header folder as elements of mylist
#print(myList)
overlayList = [] #put images in this list
for imPath in myList: #run loop for amount of elements in myList
    image = cv2.imread(f'{folderPath}/{imPath}') #read image and save in variable image
    overlayList.append(image) #add image to list
#print(len(overlayList))
header = overlayList[0] #default image to appear on display
drawColour = (0,0,255) #select draw colour

capture = cv2.VideoCapture(0) #start videocapture
capture.set (3,1280) #set width
capture.set (4,720) #set height

detector = htm.handDetector(detectionCon=0.85) # call handdetector method from module increase detection confidence to increase accuracy of drawing
xp,yp=0,0 #updated x and y position initialization
imgCanvas = np.zeros((720,1280,3),np.uint8) #initialize 720x1280x3 8 bit image to draw on
while True:
    #1. Import Image
    success, img = capture.read() #read video feed and save frame in img continuously
    img = cv2.flip(img,1) # x mirror image

    #2. Find Hand Landmarks
    img = detector.findHands(img) #get and draw landmarks on hands
    lmList, _ = detector.findPosition(img,draw=False) #get the position of landmarks

    if len(lmList)!=0: #if lmList is non-empty
        #print(lmList)

        #tip of index and middle fingers
        x1,y1 = lmList[8][1:] #get x and y position of index finger
        x2,y2 = lmList[12][1:] #get x and y position of middle finger

        #3. Check which fingers are up
        fingers = detector.fingersUp() #check which fingers are up
        print(fingers) #print 1 if finger is up, 0 for closed

        #4. If selection mode (Two fingers up)
        if fingers[1] and fingers[2]:
            xp,yp=0,0 #reset previous finger position

            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColour,cv2.FILLED) # draw a rectangle around two fingers to show selection mode
            print("Selection Mode")
            if y1<125: #pixel location y<125 to access header
                if 250<x1<450: #red colour selection is this pixel region
                    header=overlayList[0] #header image to show red selection
                    drawColour = (0,0,255) #red colour selection
                elif 550<x1<750: #blue colour selection is this pixel region
                    header=overlayList[1] #header image to show blue selection
                    drawColour = (255,0,0) #header image to show red selection
                elif 800<x1<950: #green colour selection is this pixel region
                    header=overlayList[2] #header image to show green selection
                    drawColour = (0,255,0) #green colour selection is this pixel region
                elif 1050<x1<1250: #eraser selection in this pixel region
                    header=overlayList[3] #header image to show eraser selection
                    drawColour = (0,0,0) #black erases the previous colours

        #5 If Drawing Mode (Index finger is up)
        if fingers[1] and fingers[2] == False: #if both fingers are not up
            xp,yp=0,0
            cv2.circle(img,(x1,y1),15,drawColour,cv2.FILLED) #draw circle around index finger
            print("Drawing Mode")
            if xp==0 and yp==0: 
                xp,yp=x1,y1 #set previous position to current position only if xp,yp=0
            if drawColour == (0,0,0):
                #cv2.line(img,(xp,yp),(x1,y1),drawColour, eraserThickness) #draw line from previous to current position of selected colour and thickness
                                                                            #line resets each time frame is refreshed
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColour, eraserThickness) #draw line from previous to current position of selected colour and thickness
            else:
                #cv2.line(img,(xp,yp),(x1,y1),drawColour, brushThickness) #draw line from previous to current position of selected colour and thickness
                                                                            #line resets each time frame is refreshed
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColour, brushThickness) #draw line from previous to current position of selected colour and thickness
            xp,yp = x1,y1 #set previos location to current location to keep drawing
    #6 lay the canvas on top of the camera feed
    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY) #convert to gray
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV) #Binary threshold to make the painted area black and the rest white
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR) #convert it back to bgr to make it integrate with cv2 operations
    img = cv2.bitwise_and(img,imgInv) #and both the frame and the canvas to make the painted region (0,0,0) in the img frame
    img = cv2.bitwise_or(img,imgCanvas) #or the canvas to make the empty region fill with the canvas paint
    img[0:200,0:1280] = header #lay header at the top of the image at the specified pixel locations
    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    img1 = imgCanvas #save canvas in img1
    cv2.imshow("Image", img) #show the resulting img
    #cv2.imshow("Canvas", imgCanvas)
    if cv2.waitKey(1) & 0xFF == ord('q'): #wait for q press to end feed
        for i in range(720):
            for j in range(1280):
                # img[i, j] is the RGB pixel at position (i, j)
                # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
                if img1[i, j].sum() == 0: #check if pixel is black
                    img1[i, j] = [255, 255, 255] #convert pixel to white
        cv2.imwrite("Drawing.jpg",img1) #save image
        break