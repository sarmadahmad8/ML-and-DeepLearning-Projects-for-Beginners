#Hand Tracking Module
#the prints can be uncommented to see what is being stored in variables for better understanding
import cv2
import mediapipe as mp
import time
import math
# make a hand detector class based on the mediapipe hand object
class handDetector():
    #parameters are same as that in the hand.py file for mediapipe hand object
    # this is used to get information of the position as well as landmarks of the hand on the screen
    def __init__(self, 
                 mode=False, #treat it as a video file and not static unrelated images
                 maxHands = 2,  #only detect two hands
                 detectionCon=0.5, #only show output if confidence for hand being on screen is greater than 50%
                 trackCon=0.5): #only stop tracking the hand when the confidence for hand being on screen drops below 50%
        self.mode = mode
        self.maxHands= maxHands
        self.detectionCon=detectionCon
        self.trackCon = trackCon
        self.mpHands=mp.solutions.hands #contains all the pretrained files for hand detection
        self.hands = self.mpHands.Hands() #get the information for the hand
        self.mpDraw = mp.solutions.drawing_utils #containes all the pretrained files to draw connections on hands

        self.tipIds = [4, 8, 12, 16, 20]
    def findHands(self, img, draw=True):
    
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #convert BGR image into RGB
        self.results=self.hands.process(imgRGB) #feed image into the hand detection algorith and store results
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks: #if its non empty
            for handLms in self.results.multi_hand_landmarks: #for number of hand landmarks in result
                if draw: # if draw=True
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) # draw connections
                                       
        return img #return the image
    

    def findPosition(self, img, handNo=0, draw= True): #to find position of hand 
        xList= [] #list of x positions
        yList=[] #list of y positions
        bbox=[] #bounding box size
        self.lmList = [] # list for storing of position
        if self.results.multi_hand_landmarks: # if results is non empty
            myHand = self.results.multi_hand_landmarks[handNo]  # store the landmark position for hand in myHand
            #print(myHand)
            for id, lm in enumerate(myHand.landmark): #loop as long as myHands has values
                #print(id,lm)
                h,w,c=img.shape # defining image height, width and channel
                cx,cy =int(lm.x*w),int(lm.y*h) #lm positions exist in ratios so multilying them with height and 
                                                #width gives pixel locations of the points on screen
                xList.append(cx) #append x position 
                yList.append(cy) #append y position
                #print (id,cx,cy)
                self.lmList.append([id,cx,cy]) #store id with its posiition in lmList
                #print(self.lmList)
                if draw: #if draw=True
                    cv2.circle(img ,(cx,cy), 5, (255,0,255),cv2.FILLED) #highlight the landmark with a 15 size circle


            xmin,xmax = min(xList),max(xList) #find minimum and maximum of x
            ymin,ymax=min(yList),max(yList) #find minimum and maximum of y
            bbox = xmin,ymin,xmax,ymax #save in bbox

            if draw:
                cv2.rectangle(img, (xmin-20,ymin-20),(xmax+20,ymax+20),(0,255,0),2) #draw rectangle to make bounding box

        return self.lmList, bbox #return LmList & bbox
    
    def fingersUp(self):
        fingers=[] #array to show if fingers are open or closed
        #left hand 
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[4]][1]: #check if pinky finger is on left side of thumb to detect if hand is left
            #Thumb
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]: #check if thumb is open or closed
                fingers.append(1) #show 1 when thumb is open
            else:
                fingers.append(0) #show 0 when thumb is close
        else:
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]: #check if pinky finger is on right side of thumb to detect if hand is right
                fingers.append(1) #show 1 when thumb is open
            else:
                fingers.append(0) #show 0 when thumb is closed
        
        #4 fingers
        for id in range(1,5):  # for checking fingers
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]: #check if fingers are open or closed
                fingers.append(1) #show 1 if open
            else:
                fingers.append(0) #show 0 if closed
        return fingers #return the list
    
    def findDistance(self,p1,p2,img,draw=True,r=15,t=3): # find distance between choosen fingers
        x1,y1 = self.lmList[p1][1:] #position of finger landmark p1
        x2,y2=self.lmList[p2][1:] #position of finger landmark p2
        cx,cy=(x1+x2)//2,(y1+y2)//2 #position of midpoint of p1 and p2
        if draw: #if true
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),t) # draw line between p1 and p2
            cv2.circle(img,(x1,y1),r,(255,0,255),cv2.FILLED) #draw circle on p1
            cv2.circle(img,(x2,y2),r,(255,0,255),cv2.FILLED) #draw circle on p2
            cv2.circle(img,(cx,cy),r,(0,0,255),cv2.FILLED) #draw circle on midpoint
        length=math.hypot(x2-x1,y2-y1) #calculate distance between p1 and p2

        return length, img, [x1,y1,x2,y2,cx,cy] # return info

def main():
    pTime=0 #previous time
    cTime=0 #current time

    capture = cv2.VideoCapture(0) #initialise an object of type VideoCapture
    detector = handDetector() #make an object of type handDetector
    while True:
        success, img = capture.read() #read capture and store frame data in img
        img = detector.findHands(img) # find, track and draw landmarks on hand
        lmList = detector.findPosition(img) #calculate and store position in lmList
        #if len(lmList)!=0: #if lmList is non empty
            #print(lmList[4]) #print the position of the thumb only which is id=4, can be changed for any landmark
        cTime=time.time() #stores current time in cTime
        fps=1/(cTime-pTime) #calculate fps
        pTime=cTime #renew previous time to current time for next calculation

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3) #put fps text with position,font,colour,size etc
        cv2.imshow("Image",img) #show videocamera feed
        if cv2.waitKey(1) & 0xFF == ord('q'): #close videocamera when q key is pressed
            break



if __name__ == "__main__": #call main
    main()