# ENPM661-Project2-Dijkstra-Path-Planning
This project is a Planning implementation for a point robot using Dijkstra algorithm

Dijkstra's Algorithm for Path Planning
======================================

This repository contains a Python implementation of Dijkstra's Algorithm for path planning in robotics.

Requirements
------------

-   Python 3.x
-   OpenCV (`cv2`)
-   NumPy

Usage
-----

1.  Clone the repository:

    bashCopy code

    `git clone https://github.com/aditya-chaugule/dijkstra-path-planning.git
    cd dijkstra-path-planning`

2.  Import the `dijkstra_aditya_chaugule` module:

    pythonCopy code
`python main.py`

3.  Input the start and goal coordinates:

    pythonCopy code

    `x, y = [int(x) for x in input("Enter the Start Coordinates: ").split()]

    if not (0 <= x < 600) or not (0 <= y < 250):
        raise ValueError("Start coordinates are not acceptable")

    start = (x,y)

    x, y = [int(x) for x in input("Enter the Goal Coordinates: ").split()]

    if not (0 <= x < 600) or not (0 <= y < 250):
        raise ValueError("Goal coordinates are not acceptable")

    goal = (x,y)`

4.  Visualize the start and goal points on the canvas:

    pythonCopy code

    `canvas = vis.visualize(start,goal)`

5.  Execute Dijkstra's Algorithm on the canvas:

    pythonCopy code

    `djk.execute(canvas,start,goal)`

License
-------

This project is licensed under the MIT License - see the [LICENSE](https://chat.openai.com/LICENSE) file for details.
