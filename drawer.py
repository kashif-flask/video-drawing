import cv2
import numpy as np
colorpro=[[0,120,55,20,207,194],[91,99,128,179,205,255]] #orange and sky  blue
colorval=[(0,165,255),(235,206,135)]
def getcontour(imgerode):
    contours,hierarchy=cv2.findContours(imgerode,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    high=0
    x,y,w,h=0,0,0,0
    biggest=np.array([])
    for cnt in contours:
        area=cv2.contourArea(cnt)
        
        #cv2.drawContours(img2,cnt,-1,(0,255,0),3)
        if area>500:
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            if approx.size>0:
                x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y
    
 
def drawline(points):
    if len(points)>0:
        for p in points:
            c=colorval[p[2]]
            #print(c)
            cv2.circle(img,(p[0],p[1]),10,c,cv2.FILLED)
        
def empty(a):
    pass

cv2.namedWindow("trackbar")
cv2.resizeWindow("trackbar",640,240)
cv2.createTrackbar("hue min","trackbar",0,179,empty)
cv2.createTrackbar("hue max","trackbar",179,179,empty)
cv2.createTrackbar("sat min","trackbar",0,255,empty)
cv2.createTrackbar("sat max","trackbar",255,255,empty)
cv2.createTrackbar("val min","trackbar",0,255,empty)
cv2.createTrackbar("val max","trackbar",255,255,empty)
cap=cv2.VideoCapture(0)
points=[]
mypoints=[]
while True:
    success,img=cap.read()
    #img=cv2.resize(img,(0,0),None,0.6,0.6)
    imghsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #hmin=cv2.getTrackbarPos("hue min","trackbar")
    #hmax=cv2.getTrackbarPos("hue max","trackbar")
    #smin=cv2.getTrackbarPos("sat min","trackbar")
    #smax=cv2.getTrackbarPos("sat max","trackbar")
    #vmin=cv2.getTrackbarPos("val min","trackbar")
    #vmax=cv2.getTrackbarPos("val max","trackbar")

    
    count=0
    for pro in colorpro:
        lower=np.array(pro[0:3])
        upper=np.array(pro[3:6])
        mask=cv2.inRange(imghsv,lower,upper)
        #cv2.imshow("mask",mask)
        #newimg=cv2.bitwise_and(img,img,mask=mask)
        
        x,y=getcontour(mask)
        if x!=0 and y!=0:
            cv2.circle(img,(x,y),10,colorval[count],cv2.FILLED)
            points.append([x,y,count])
        count=count+1
    if len(points)!=0:
        for newp in points:
            mypoints.append(newp)
    if len(mypoints)!=0:
        drawline(mypoints)
    #cv2.imshow("mask",mask)
    #cv2.imshow("maskedimg",newimg)
    #cv2.imshow("imghsv",imghsv)
    cv2.imshow("car",img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
