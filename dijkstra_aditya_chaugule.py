import heapq as hq
import numpy as np
import cv2

exp_color = (255, 0, 0)

global idx 
idx = 1
def execute(canvas,start,goal):
    nodes = {}
    nodes[start] = (0,0,None)
    
    ol = []
    cl = set()

    def up(canvas, node, c2c):
        x,y = node
        x = x
        if y < canvas.shape[0]-1:
            y += 1
            c2c += 1
            new_node = (x,y)
            return (canvas,new_node,c2c)
        return (canvas,None, None)
        
    def upright(canvas, node, c2c):
        x,y = node
        if x < (canvas.shape[1]-1) and y < (canvas.shape[0]-1) :
            x += 1
            y += 1
            c2c += 1.4
            new_node = (x,y)
            return (canvas,new_node, c2c)
        return (canvas,None, None)

    def right(canvas, node, c2c):
        x,y = node
        y = y
        if x < (canvas.shape[1]-1):
            x += 1
            c2c += 1
            new_node = (x,y)
            return (canvas,new_node,c2c)
        return (canvas,None, None)

    def downright(canvas, node, c2c):
        x,y = node
        if x < (canvas.shape[1]-1) and y > 0 :
            x += 1
            y -= 1
            c2c += 1.4
            new_node = (x,y)
            return (canvas,new_node,c2c)
        return (canvas,None, None)

    def down(canvas, node, c2c):
        x,y = node
        x = x
        if y > 0 :
            y -= 1
            c2c += 1
            new_node = (x,y)
            return (canvas,new_node,c2c)
        return (canvas,None, None)

    def downleft(canvas, node, c2c):
        x,y = node
        if x > 0 and y > 0 :
            x -= 1
            y -= 1
            c2c += 1.4
            new_node = (x,y)
            return (canvas,new_node,c2c)
        return (canvas,None, None)

    def left(canvas, node, c2c):
        x,y = node
        y = y
        if x > 0:
            x -= 1
            c2c += 1
            new_node = (x,y)
            return (canvas,new_node,c2c)
        return (canvas,None, None)
    
    def upleft(canvas, node, c2c):
        x,y = node
        if x > 0 and y < canvas.shape[0]-1 :
            x -= 1
            y += 1
            c2c += 1.4
            new_node = (x,y)
            return (canvas,new_node,c2c)
        return (canvas,None,None)
    
    # Vision Space
    def vision(frame,node):
        x,y = node
        rad = 5

        # # Rectangular Mask
        # xmin = max(0, x - rad)
        # xmax = min(frame.shape[1], x + rad )
        # ymin = max(0, y - rad)
        # ymax = min(frame.shape[0], y + rad )
        # circ_mask = frame[ymin:ymax, xmin:xmax]

        # # Circular Mask
        # # Using Circular Mask increases run time but gives accurate representation of vision space clearance
        mask = np.zeros_like(frame)
        cv2.circle(mask, (x, y), rad, (255, 255, 255), -1)
        circ_mask = cv2.bitwise_and(frame, mask)
        
        return circ_mask
        
    def success():
        a,b = 400,400
        frame = np.zeros((a, b, 3), np.uint8)
        cv2.rectangle(frame, (0, 0), (a-1, b-1), (140, 0, 0), -1)
        cv2.rectangle(frame, (100, 100), (a-100, b-100), (255, 0, 0), -1)

        cv2.putText(frame, 'Goal Reached !', (30, 200), cv2.FONT_HERSHEY_COMPLEX,1.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.namedWindow('Goal Reached', cv2.WINDOW_NORMAL)
        cv2.imshow('Goal Reached', frame)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()

    def explore(canvas,node):
        parent = node
        p_c2c = nodes[node][0]
        for act in [up,upright,right,downright,down,downleft,left,upleft]:
            canvas,new_node,c2c = act(canvas,node, p_c2c)
            if new_node == None:
                continue
            (x,y)  = new_node
            y_up = (canvas.shape[0]-1)-y
            if new_node in cl:
                continue
            mask = vision(canvas,new_node)
            if np.any(mask[:,:,1]):
                continue

            if new_node not in nodes or c2c < nodes[new_node][0]:
                global idx
                idx += 1
                nodes[(x,y)] = (c2c, idx, parent)
                
                hq.heappush(ol, (c2c,(new_node)))
            if new_node == goal:
                break 


    def animate(canvas, nodes):
        parent_nodes = {}
        for node, (c2c, idx, parent) in nodes.items():
            if parent is not None:
                if parent not in parent_nodes:
                    parent_nodes[parent] = []
                parent_nodes[parent].append(node)

        color = (255,0,0)
        count = 0

        for parent, nodes_list in parent_nodes.items():
            shift = canvas.shape[0]-1
            node_coords = np.array([(shift-node[1], node[0]) for node in nodes_list]).transpose()
            canvas[node_coords[0], node_coords[1], :] = color
            count += len(nodes_list)
            if count % 100 == 0:
                cv2.imshow('Image', canvas)
                cv2.waitKey(1)

        success()

    def track_animate(canvas,track):
        for i in range(len(track)-1):
            node1 = track[i]
            node2 = track[i+1]
            cv2.line(canvas, (node1[0], node1[1]), (node2[0], node2[1]), (0, 255, 255), 1)

    def robot_animate(canvas,track):
        rad = 5
        color = (0, 255, 255)
        
        for node in track:
            x,y = node
            
            cv2.circle(canvas, (x,y), rad, color, 1)
            cv2.imshow("Canvas", canvas)
            cv2.waitKey(2)
            cv2.circle(canvas, (x,y), rad+1, (255,0,0), -1)
            cv2.imshow("Canvas", canvas)
            cv2.waitKey(1)

        cv2.waitKey(2000)
        cv2.destroyAllWindows()

    def tracking(nodes, start, goal):
        track = []      
        node = goal      
        while node != start:
            track.append(node)
            parent = nodes[node][2]
            node = parent
        track.append(start)
        track.reverse() 
        shift = canvas.shape[0]-1
        track_up = [((x,shift-y)) for (x,y) in track]
        return track_up
    
    hq.heappush(ol,(0,start))

    while ol:
        c2c, node = hq.heappop(ol)
        if node in cl:
            continue

        cl.add(node)
        if node == goal:
            print("Goal Reached\n\n")
            animate(canvas, nodes)
            track = tracking(nodes,start,goal)
            track_animate(canvas,track)
            robot_animate(canvas,track)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            return nodes

        if goal in ol:
            continue
        explore(canvas,node)