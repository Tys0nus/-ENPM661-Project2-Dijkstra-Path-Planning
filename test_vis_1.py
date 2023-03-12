import cv2
import numpy as np

# Create a black image
img = np.zeros((512,512,3), np.uint8)

# Define top-left and bottom-right points
# pt1 = (100+3, 100)
# pt2 = (400, 400)

# Draw a rectangle on the image

def colorize(frame,node):
    for i in img:
        x0 = 512/2
        y0 = 512/2
        x1 = x0 + 10
        y1 = y0 + 10
        
        img[x0:x1,y0:y1] = (255,0,0)
    
    return node


# canvas = 

# cv2.rectangle(img, pt1, pt2, (0,255,0), 2)

# Show the image
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
