import cv2
import numpy as np

img = cv2.imread('Software/Vision/Images/2016-01-23 16-06-42.285.jpg',cv2.IMREAD_COLOR)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_green = np.array([75,70,70])
upper_green = np.array([95,255,255])

mask = cv2.inRange(hsv, lower_green, upper_green)

res = cv2.bitwise_and(img, img, mask = mask)

#se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
#se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
#mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, se1)
#mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

#mask = np.dstack([mask, mask, mask]) / 255
#out = img * mask

edges = cv2.Canny(mask,100,200)

gray = np.float32(mask)
dst = cv2.cornerHarris(gray,2,3,0.04)
dst = cv2.dilate(dst,None)
ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

# define the criteria to stop and refine the corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

# Now draw them
res = np.hstack((centroids,corners))
res = np.int0(res)
img[res[:,1],res[:,0]]=[0,0,255]
img[res[:,3],res[:,2]] = [0,255,0]

cv2.imwrite('image',img)