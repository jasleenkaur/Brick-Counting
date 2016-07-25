import cv2
import numpy as np
import argparse

# Construct argument parse to inline image with command
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
 
# load the image
img = cv2.imread(args["image"])
# median filter gives bad result : blur = cv2.medianBlur(img,5)

#unsharp masking
#gaussain is beter in this case than median
blur = cv2.GaussianBlur(img,(5,5),0)
'''
gaussian_3 = cv2.GaussianBlur(img, (9,9), 10.0)
unsharp_image = cv2.addWeighted(img, 1.5, gaussian_3, -0.5, 0, img)
'''
# convert BGR TO HSV
hsv = cv2.cvtColor(blur ,cv2.COLOR_BGR2HSV)

gray_hsv = cv2.cvtColor(hsv,cv2.COLOR_BGR2GRAY)

# Otsu Thresholding
ret, thresh_hsv = cv2.threshold(gray_hsv,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imwrite("thresh-hsv.jpg", thresh_hsv)
# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh_hsv,cv2.MORPH_OPEN,kernel, iterations = 1)

# sure background area
#sure_bg = cv2.dilate(opening,kernel,iterations=1)
_, contours, hierarchy= cv2.findContours(opening, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
idx =0 
count=0
for cnt in contours:
    idx += 1
    area = cv2.contourArea(cnt)
    print str(idx) +"="+ str(area)
    if area < 20:  # percentile should be here
        continue
    print " area = " + str(area) 
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.drawContours( img, cnt,-1, (0,255,0),2) 
    count=count+1
    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
#draw conours are better to draw a boundary
#cv2.drawContours( img, contours,-1, (0,255,0),2)    
print "total number of bricks: " +  str(idx) +"  count  =" +str(count)
cv2.imshow("All keypoints",img)
cv2.imwrite("keypoints.jpg",img)
cv2.imshow('opening',opening)

cv2.waitKey(0)
