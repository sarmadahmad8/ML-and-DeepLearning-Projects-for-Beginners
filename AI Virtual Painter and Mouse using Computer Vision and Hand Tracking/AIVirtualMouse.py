import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
#initializations
wScreen,hScreen = autopy.screen.size() #get screen size
wCam=1280 #set cam width
hCam=720 #set cam height
cTime=0 #current time
pTime=0 #previous time
RFrame=150 #reduced pixels from frame
smoothen=5 #smoothening level
xp,yp=0,0 #previous position of index
xc,yc=0,0 #new position of index

capture = cv2.VideoCapture(0) #initialize videofeed
capture.set(3,wCam) #set can width
capture.set(4,hCam) #set cam height
detector = htm.handDetector(maxHands=1) #initialize hand detection
while True:
    # 1. Find hand landmarks
    success,img = capture.read() #store frame from feed in img
    img = detector.findHands(img) #draw hand landmarks and connections
    lmList, bbox = detector.findPosition(img) #find the position of landmarks and bounding box of hand

    # 2. Get the tip of the index and middle fingers
    if len(lmList)!=0: #if lmList is non-empty
        #print(lmList)

        #tip of index and middle fingers
        x1,y1 = lmList[8][1:] #get x and y position of index finger
        x2,y2 = lmList[12][1:] #get x and y position of middle finger

        #3. Check which fingers are up
        fingers = detector.fingersUp() #check which fingers are up
        print(fingers) #print 1 if finger is up, 0 for closed
        cv2.rectangle(img,(RFrame,RFrame),(wCam-RFrame,hCam-RFrame),(255,0,255),2) #draw rectangle of usable frame
        #4 check if in moving mode
        if fingers[1]==1 and fingers[2]==0: # if index is up andmiddleis down

            # 5. convert coordinates to screen size
            x3 = np.interp(x1, (RFrame,wCam-RFrame),(0,wScreen)) # map working frame width onto screen width
            y3 = np.interp( y1, (RFrame,hCam-RFrame),(0,hScreen)) # map working frame height onto screen height
            #6. make movement more smooth
            xc=xp+(x3-xp)/smoothen #smoothen x travel
            yc=yp+(y3-yp)/smoothen #smoothen y travel
            # 7. moving the mouse
            autopy.mouse.move(wScreen-xc,yc) # move mouse mirrored
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED) #draw circle on index
            xp,yp=xc,yc #set previous position to current
            #8.Clicking Mode
        if fingers[1]==1 and fingers[2]==1: # if bothindex and middle are up 
            length,img, linfo =detector.findDistance(8,12,img) #find distance between index and middle
            # 9. Find distance between fingers
            if length<40: # ifdistance is less than 40
                cv2.circle(img,(linfo[4],linfo[5]),15,(0,255,0),cv2.FILLED) # draw green circle in middle point
            #10. click mouse of distance is short
                autopy.mouse.click() # click mouse
    #11. Frame rate
    cTime=time.time() # set current time
    fps = 1/(cTime-pTime) #calculate fps
    pTime=cTime #set previous time to current time
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255)) #put fps text in feed
    #12. Display
    cv2.imshow("image",img) # show feed
    if cv2.waitKey(1) & 0xFF == ord('q'): #wait for q press to end feed
        break