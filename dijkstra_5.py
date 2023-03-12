import heapq as hq
import numpy as np
import vis_2 as vis
import cv2

exp_color = (255, 0, 0)

global idx 
idx = 1
def execute(canvas,start,goal):
    print(canvas.shape)
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

        xmin = max(0, x - rad)
        xmax = min(frame.shape[1], x + rad + 1)
        ymin = max(0, y - rad)
        ymax = min(frame.shape[0], y + rad + 1)
        circ_mask = frame[ymin:ymax, xmin:xmax]

        return circ_mask
            # if np.all(canvas[y_up][x] == [0,255,0]): 
            #     continue   
    def explore(canvas,node):
        parent = node
        p_c2c = nodes[node][0]
        for act in [up,upright,right,downright,down,downleft,left,upleft]:
            canvas,new_node,c2c = act(canvas,node, p_c2c)
            if new_node == None:
                continue
            # print(new_node)
            (x,y)  = new_node
            y_up = (canvas.shape[0]-1)-y
            if new_node in cl:
                continue
            mask = vision(canvas,new_node)
            if np.any(mask[:,:,1]):
                print("Masking")
                continue

            if new_node not in nodes or c2c < nodes[new_node][0]:
                global idx
                idx += 1
                nodes[(x,y)] = (c2c, idx, parent)
                
                hq.heappush(ol, (c2c,(new_node)))
            if new_node == goal:
                break 
        # print(nodes)

            # cv2.imshow("Exploring", canvas)
            # cv2.waitKey(0.001)

    def animate(canvas, nodes):
        # Batch the nodes that have the same parent and draw them together
        parent_nodes = {}
        for node, (c2c, idx, parent) in nodes.items():
            if parent is not None:
                if parent not in parent_nodes:
                    parent_nodes[parent] = []
                parent_nodes[parent].append(node)
        
        print("Parent nodes: ", len(parent_nodes))

        color = (255,0,0)
        count = 0
        # Draw all the nodes with the same parent in one batch
        for parent, nodes_list in parent_nodes.items():
            shift = canvas.shape[0]-1
            node_coords = np.array([(shift-node[1], node[0]) for node in nodes_list]).transpose()
            canvas[node_coords[0], node_coords[1], :] = color
            count += len(nodes_list)
            if count % 1000 == 0:
                cv2.imshow('Image', canvas)
                cv2.waitKey(1)

        # Show the final canvas
        canvas = cv2.putText(canvas, 'Goal Reached !',(200,125), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Image', canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def track_animate(canvas,track):
        for i in range(len(track)-1):
            node1 = track[i]
            node2 = track[i+1]
            print(node1[1], node1[0])
            print(node2[1], node2[0])
            cv2.line(canvas, (node1[0], node1[1]), (node2[0], node2[1]), (0, 255, 255), 1)

    def animate_robot(canvas,track):
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

        cv2.waitKey(0)
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
            print(len(nodes))
            print("Goal Reached")
            animate(canvas, nodes)
            track = tracking(nodes,start,goal)
            # print(track)
            track_animate(canvas,track)
            animate_robot(canvas,track)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return nodes

        if goal in ol:
            continue
        explore(canvas,node)
    
    

