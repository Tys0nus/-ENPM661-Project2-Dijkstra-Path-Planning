import dijkstra_aditya_chaugule as djk
import visualize as vis
import time
if __name__ == "__main__":


    start_time = time.time()
    print("-----------------------")
    print("Path Planning: Dijkstra")
    print("-----------------------")
    x, y = [int(x) for x in input("Enter the Start Coordinates: ").split()] 
    
    if not (0 <= x < 600) or not (0 <= y < 250):
        raise ValueError("Start coordinates are not acceptable")

    start = (x,y)

    x, y = [int(x) for x in input("Enter the Goal Coordinates: ").split()] 
    if not (0 <= x < 600) or not (0 <= y < 250):
        raise ValueError("Goal coordinates are not acceptable")
    goal = (x,y)

    canvas = vis.visualize(start,goal)
    djk.execute(canvas,start,goal)

    end_time = time.time()
    runtime = end_time - start_time
    print("Runtime: {:.4f} seconds".format(runtime),"\n\n")

