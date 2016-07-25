import cv2
import numpy as np
img = cv2.imread('images/sample17.jpg',0)
ret,thresh = cv2.threshold(img,127,255,0)
edged = cv2.Canny(img, 75, 200)
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(edged, cv2.MORPH_OPEN, kernel)
# show the original image and the edge detected image
print "STEP 1: Edge Detection"
cv2.imshow("Image", thresh)
cv2.imshow("Edged", edged)
cv2.imshow("Openeing", opening)
cv2.waitKey(0) &0xff
