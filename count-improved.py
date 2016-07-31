import cv2
import numpy as np
import argparse
import time
from matplotlib import pyplot as plt
# Construct argument parse to inline image with command
parser = argparse.ArgumentParser(description="-----Brick Counting algorithm to count number of bricks from an image.-----")
parser.add_argument("-i", "--image", help = "path to the image")
args = vars(parser.parse_args())

# time module to observe time taken
t1 = time.time() 

# load the image
img = cv2.imread(args["image"])
print "Image Datatype:  " + str(img.dtype)
print "Image Shape:  " + str(img.shape)
print "Total number of pixels in image:  " + str(img.size)
# need to load this to show original image in matplotlib as RGB
im= cv2.imread(args["image"])
b,g,r = cv2.split(img)
im=cv2.merge([r,g,b])

#noise removal by blurring coloured image
blur = cv2.GaussianBlur(img,(9,9),10.0)

# convert BGR TO HSV
hsv = cv2.cvtColor(img ,cv2.COLOR_BGR2HSV)
gray_hsv = cv2.cvtColor(hsv,cv2.COLOR_BGR2GRAY)

# Otsu Thresholding
ret, thresh_hsv = cv2.threshold(gray_hsv,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Morphological Opening to remove all white distortions around bricks
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh_hsv,cv2.MORPH_OPEN,kernel, iterations = 2)

# Contour and filling to fill holes
_, contours, hierarchy = cv2.findContours(opening, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    cv2.drawContours(opening,[cnt],0,255,-1)

# Contour detection to count it
_, contours1, hierarchy = cv2.findContours(opening, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

idx =0           #count id of every contour detected
count = 0        #counter to count actual number of contours(bricks) ignoring noise
for cnt in contours1:
    cv2.drawContours(opening,[cnt],0,255,-1)
    idx += 1
    area = cv2.contourArea(cnt)       #area is number of pixels a contour have
    #print str(idx) +"="+ str(area)
    sizeOfnoise = 30                  #percentile should be here    
    if area <sizeOfnoise:             #ignore noises of size less than 30 pixel area 
        continue
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.drawContours( img, contours,-1, (0,255,0),2) 
    count=count+1

t2 = time.time() -t1
print "Total Time Taken(in seconds): " + str(t2)
print "Threshold value taken by OTSU Thresholding: " + str(ret )
print "Total number of Bricks detected including noise: " +  str(idx) 
print "Total number of actual Bricks detected: " +str(count)

#ploting histogram of image
plt.hist(gray_hsv.ravel(),256,[0,256]); plt.show()

# Displaying all images
titles = ['Original Image', 'hsv image', 'Thresholding',
            'After opening and Contour Filling ' ]
images = [im, hsv, thresh_hsv, opening]
for i in xrange(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

# write total count of Bricks on Image
font = cv2.FONT_HERSHEY_SIMPLEX
if img.size >100000:
    img = cv2.putText(img,'Bricks Detected:'+ str(count),(50,50), font, 2,(255,255,255),2,cv2.LINE_AA)
else:
    img = cv2.putText(img,'Bricks Detected:'+ str(count),(50,50), font, 1,(255,255,255),2,cv2.LINE_AA)
cv2.namedWindow("Image with Bricks detected",cv2.WINDOW_NORMAL)
cv2.imshow("Image with Bricks detected",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
