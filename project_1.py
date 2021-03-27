import cv2
import numpy as np


video = cv2.VideoCapture(0)   ##0--> default webcam
video.set(3,600)  #id number 3 ---> width
video.set(4,400)   #id 4 -->height
video.set(10,150)   #id 10--> brightness

myPoints =  []  ## [x , y , colorId ]

### this list defines which all colors to be detected
myColors = [["Orange",5,107,0,19,255,255],   # orange
            ["Purple",133,56,0,159,156,255],  #purple
            ["Green",57,76,0,100,255,255],   #green
            ["Blue",90,48,0,118,255,255]]

myColorValues = [[51,153,255],          ## BGR found from online
                 [255,0,255],
                 [0,255,0],
                 [255,0,0]]

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  ##find external contours more precisely
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)   ### contour areas
        #print(area)
        if area>800:   ### threshold  depends on pixel amount within the contour
            #cv2.drawContours(imageResult, cnt, -1, (255, 0, 0), 3)  ### -1---> all contours , blue, thickness
            ### above code gives blue outline around the shapes
            peri = cv2.arcLength(cnt,True)
            #acr length of all shapes
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)  ## determines number of corner points, True--> closed images
            ##bounding rectangle cordinnates to place it around shapes
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

### a function to find min max values for all colors
def find_color(img, myColors, myColorValues):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        count = 0
        newPoints=[]   ###every time execution
        for color in myColors:
            lower = np.array(color[1:4])  ### min array
            upper = np.array(color[4:7])  ### max array
            mask = cv2.inRange(imgHSV,lower,upper)
            x, y = getContours(mask)
            if x!=0 or y!=0:
                cv2.circle(imageResult,(x,y),10,myColorValues[count],cv2.FILLED)
                newPoints.append([x,y,count])   ### to find the new points every time we change position
                count +=1
                #cv2.imshow(color[0], mask)    ##name that is changing
        return newPoints

def drawOnCanvas(myPoints,myColorValues):   ### printing a list of newpoints
    for point in myPoints:
        cv2.circle(imageResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = video.read()
    imageResult=img.copy()
    newPoints = find_color(img, myColors,myColorValues)
    if len(newPoints)!=0:
        for new in newPoints:
            myPoints.append(new)   ### not list within list
    if len(myPoints) != 0:
            drawOnCanvas(myPoints, myColorValues)
    cv2.imshow("Webcam", imageResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break