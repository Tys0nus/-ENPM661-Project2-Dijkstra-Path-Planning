#Process nodes in this code and visuals in another
import heapq as hq
import numpy as np
import vis_basic_1 as vis

# Node structure: dict{(x,y):(c2c,idx,parent)}
start = (100,100)
# goal = (599,249)
goal = (101,102)

nodes = {}
nodes[start] = (0,0,None)
idx = 1

ol = []
cl = set()

# obs_space = (0,255,0)

def up(frame, node, c2c):
    x,y = node
    x = x
    if y < frame.shape[1]-1:
        y += 1
        c2c += 1
        new_node = (x,y)
        vis.colorize(frame,new_node)
        return (frame,new_node,c2c)
    return (frame,None, None)
    
def upright(frame, node, c2c):
    x,y = node
    if x < (frame.shape[0]-1) and y < (frame.shape[1]-1) :
        x += 1
        y += 1
        c2c += 1.4
        new_node = (x,y)
        vis.colorize(frame,new_node)
        return (frame,new_node, c2c)
    return (frame,None, None)

def right(frame, node, c2c):
    x,y = node
    y = y
    if x < (frame.shape[0]-1):
        x += 1
        c2c += 1
        new_node = (x,y)
        vis.colorize(frame,new_node)
        return (frame,new_node,c2c)
    return (frame,None, None)

def downright(frame, node, c2c):
    x,y = node
    if x < (frame.shape[0]-1) and y > 0 :
        x += 1
        y -= 1
        c2c += 1.4
        new_node = (x,y)
        vis.colorize(frame,new_node)
        return (frame,new_node,c2c)
    return (frame,None, None)

def down(frame, node, c2c):
    x,y = node
    x = x
    if y > 0 :
        y -= 1
        c2c += 1
        new_node = (x,y)
        vis.colorize(frame,new_node)
        return (frame,new_node,c2c)
    return (frame,None, None)

def downleft(frame, node, c2c):
    x,y = node
    if x > 0 and y > 0 :
        x -= 1
        y -= 1
        c2c += 1.4
        new_node = (x,y)
        vis.colorize(frame,new_node)
        return (frame,new_node,c2c)
    return (frame,None, None)

def left(frame, node, c2c):
    x,y = node
    y = y
    if x > 0:
        x -= 1
        c2c += 1
        new_node = (x,y)
        vis.colorize(frame,new_node)
        return (frame,new_node,c2c)
    return (frame,None, None)
  
def upleft(frame, node, c2c):
    x,y = node
    if x > 0 and y < frame.shape[1]-1 :
        x -= 1
        y += 1
        c2c += 1.4
        new_node = (x,y)
        vis.colorize(frame,new_node)
        return (frame,new_node,c2c)
    return (frame,None,None)

# # Vision Space
# def vision(frame,node):
#     x,y = node
#     rad = 5

#     xmin = max(0, x - rad)
#     xmax = min(frame.shape[1], x + rad + 1)
#     ymin = max(0, y - rad)
#     ymax = min(frame.shape[0], y + rad + 1)
#     circ_mask = frame[ymin:ymax, xmin:xmax]

#     return circ_mask

def explore(frame,node):
    parent = node
    p_c2c = nodes[node][0]
    for act in [up,upright,right,downright,down,downleft,left,upleft]:
        frame,new_node,c2c = act(frame,node, p_c2c)
        # mask =vision(frame,new_node)
        # if np.any(mask == ()):
        #     continue
        if new_node == None:
            continue
        if new_node in cl:
            continue
        if new_node not in nodes or c2c < nodes[new_node][0]:
            global idx
            idx += 1
            nodes[new_node] = (c2c, idx, parent)
            hq.heappush(ol, (c2c,(new_node)))
        if new_node == goal:
            break 

frame = np.zeros((600,250))
hq.heappush(ol,(0,start))

while ol:
    c2c, node = hq.heappop(ol)
    if node in cl:
        continue

    cl.add(node)
    if goal in nodes:
        print("Goal Reached")
        break
    c2c, idx, parent = nodes[node]
    explore(frame,node)
    # print("Popped: ",node)
    # print(nodes)



def tracking(nodes, start, goal):
    track = []
    
    node = goal
    
    while node != start:
        track.append(node)
        parent = nodes[node][2]
        node = parent
    track.append(start)
    track.reverse()
    
    return track

track = tracking(nodes,start,goal)
print(track)