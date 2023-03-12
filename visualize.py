import cv2
import numpy as np

def display(frame):
    cv2.imshow('Canvas',frame)

def colorize(frame,node,color):
        x,y = node
        x = x
        y = (frame.shape[0]-1)-y
        color = np.array([255, 0, 0])
        frame[x][y] = color

def visualize(start,goal):

    def change_origin(frame,node):
        x,y = node
        x = x
        y = (frame.shape[0]-1)-y
        return (x,y)

    def indicate_start(frame,node):
        x,y = change_origin(frame,node)
        cv2.circle(frame,(x,y),5,(0,0,255),-1)
        return frame

    def indicate_goal(frame,node):
        x,y = change_origin(frame,node)
        cv2.circle(frame,(x,y),5,(0,0,255),-1)
        return frame
    
    obs_color = (0,255,0)
    
    def polygon(frame,sides, length, xc, yc,orient):
        xc = xc
        yc = (frame.shape[0]-1)-yc
        n = sides
        theta = 2*np.pi/n
        p = length*0.5/np.sin(theta/2)
        x = []
        y = []
        for i in range(n):
            x.append(xc + p*np.cos(theta*i + orient))
            y.append(yc + p*np.sin(theta*i + orient))

        pts = np.array([[int(x[i]), int(y[i])] for i in range(n)], dtype=np.int32)
        cv2.fillPoly(frame, [pts], obs_color)

        return frame

    def rectangle(frame, h,w,xc,yc):
        xc = xc
        yc = (frame.shape[0]-1)-yc

        h = h/2
        w = w/2
        pt1 = (int(xc + w), int(yc - h))
        pt2 = (int(xc - w), int(yc + h))

        cv2.rectangle(frame,pt1,pt2,obs_color,-1)
        return frame
    
    def triangle(frame, base, height, xc,yc, angle=0):
        xc = xc
        yc = (frame.shape[0]-1)-yc

        x1, y1 = xc+height, yc
        x2, y2 = xc, yc + base/2
        x3, y3 = xc, yc - base/2

        pts = np.array([[x1, y1], [x2, y2], [x3, y3]], dtype=np.int32)
        cv2.fillPoly(frame, [pts], obs_color)
        return frame

    height = 600
    width = 250
    canvas = np.zeros((width,height,3),np.uint8)
    canvas = rectangle(canvas,100,50,125,50)
    canvas = rectangle(canvas,100,50,125,200)
    canvas = polygon(canvas,6,75,300,125,np.pi/2)
    canvas = triangle(canvas,200,50,460,125)


    x,y = start
    yb = (canvas.shape[0]-1)-y
    if np.array_equal(canvas[yb, x], np.array([0, 255, 0])):
        raise ValueError("Start coordinate cannot be in obstacle space")
    
    x,y = goal
    yb = (canvas.shape[0]-1)-y
    if np.array_equal(canvas[yb, x], np.array([0, 255, 0])):
        raise ValueError("Goal coordinate cannot be in obstacle space")
    
    canvas = indicate_start(canvas,start)
    canvas = indicate_goal(canvas,goal)

    return canvas

