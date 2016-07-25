import cv2
import numpy as np
import argparse

# Construct argument parse to inline image with command
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
 
# load the image
img = cv2.imread(args["image"])

#noise removal by blurring coloured image
blur = cv2.GaussianBlur(img,(9,9),10.0)

# convert BGR TO HSV
hsv = cv2.cvtColor(img ,cv2.COLOR_BGR2HSV)
gray_hsv = cv2.cvtColor(hsv,cv2.COLOR_BGR2GRAY)

# Otsu Thresholding
ret, thresh_hsv = cv2.threshold(gray_hsv,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imwrite("thresh_hsv.jpg",thresh_hsv)

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh_hsv,cv2.MORPH_OPEN,kernel, iterations = 2)
opening_image = opening
#cv2.imshow("opening_image.jpg",opening_image)
#closing = cv2.morphologyEx(thresh_hsv,cv2.MORPH_CLOSE,kernel, iterations = 1)
#cv2.imwrite("closing.jpg",closing)

_, contours, hierarchy= cv2.findContours(opening, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
idx =0
count = 0 
for cnt in contours:
    idx += 1
    area = cv2.contourArea(cnt)
    print str(idx) +"="+ str(area)
    if area <70:  # percentile should be here
        continue
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.drawContours( img, cnt,-1, (0,255,0),2) 
    count=count+1
print "total number of bricks: " +  str(idx) +"  count  =" +str(count)
    #idx += 1
    #x,y,w,h = cv2.boundingRect(cnt)
    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
#draw conours are better to draw a boundary
#cv2.drawContours( img, contours,-1, (0,255,0),2)    
#print "total number of bricks: " +  str(idx)
#cv2.imshow("image with contours",img)
cv2.imwrite("imageCONTOURS.jpg",img)
#cv2.imshow('opening',opening)
cv2.waitKey(0)
