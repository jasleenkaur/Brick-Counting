import cv2
import numpy as np
import argparse
import time
from matplotlib import pyplot as plt
# Construct argument parse to inline image with command
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
t1 = time.time() 
# load the image
img = cv2.imread(args["image"])
#noise removal by blurring coloured image
blur = cv2.GaussianBlur(img,(9,9),10.0)

# convert BGR TO HSV
hsv = cv2.cvtColor(img ,cv2.COLOR_BGR2HSV)
gray_hsv = cv2.cvtColor(hsv,cv2.COLOR_BGR2GRAY)
# Otsu Thresholding
ret, thresh_hsv = cv2.threshold(gray_hsv,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# noise removal
kernel = np.ones((5,5),np.uint8)

opening = cv2.morphologyEx(thresh_hsv,cv2.MORPH_OPEN,kernel, iterations = 2)
#erosion = cv2.erode(thresh_hsv,kernel,iterations = 1)
#cv2.imshow("erosion",erosion)
cv2.imwrite("opening.jpg",opening)
_, contours, hierarchy= cv2.findContours(opening, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    cv2.drawContours(opening,[cnt],0,255,-1)

_, contours1, hierarchy= cv2.findContours(opening, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
idx =0
count = 0 
for cnt in contours1:
    cv2.drawContours(opening,[cnt],0,255,-1)
    idx += 1
    area = cv2.contourArea(cnt)
    print str(idx) +"="+ str(area)
    if area <30:  # percentile should be here
        continue
    x,y,w,h = cv2.boundingRect(cnt)
    count=count+1
print "total number of bricks: " +  str(idx) +"  count  =" +str(count)
    #idx += 1
    #x,y,w,h = cv2.boundingRect(cnt)
    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
#draw conours are better to draw a boundary
#cv2.drawContours( img, contours,-1, (0,255,0),2)    
#print "total number of bricks: " +  str(idx)

t2 = time.time() -t1
print "time taken(seconds): " + str(t2)
'''
plt.hist(gray_hsv.ravel(),256,[0,256]); plt.show()

titles = ['Original Image', 'hsv image', 'Thresholding',
            'erosion','opening' ]
images = [img, hsv, thresh_hsv, erosion,opening]
for i in xrange(5):
    plt.subplot(3,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
'''
cv2.waitKey(0)
