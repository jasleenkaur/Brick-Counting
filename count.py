import cv2
import numpy as np
import argparse

# Construct argument parse to inline image with command
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
 
# load the image
img = cv2.imread(args["image"])

#unsharp masking
gaussian_3 = cv2.GaussianBlur(img, (9,9), 10.0)
unsharp_image = cv2.addWeighted(img, 1.5, gaussian_3, -0.5, 0, img)

# convert BGR TO HSV
hsv = cv2.cvtColor(unsharp_image ,cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(unsharp_image,cv2.COLOR_BGR2GRAY)
gray_hsv = cv2.cvtColor(hsv,cv2.COLOR_BGR2GRAY)

# Otsu Thresholding
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret, thresh_hsv = cv2.threshold(gray_hsv,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh_hsv,cv2.MORPH_OPEN,kernel, iterations = 1)

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=1)
opening[:]= 255-opening[:]
_, contours, _= cv2.findContours(sure_bg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#cv2.drawContours(sure_bg,contours,-1,(0,255,0),3)
idx =0 
for cnt in contours:
    idx += 1
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(sure_bg,(x,y),(x+w,y+h),(0,255,0),2)
print "total number of bricks: " + str(idx)
cv2.imshow("All keypoints",img)
cv2.imshow('opening',opening)
cv2.imshow('sure_bg',sure_bg)
cv2.imwrite('images/sure_bg.png',sure_bg)
cv2.imwrite('images/opening.png',sure_bg)

cv2.waitKey(0)
cv2.destroyAllWindows()
