"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider

def addLWSpaceship(i,j,grid):
    lwSpaceship = np.array([[255,   0,   0, 255,   0],
                            [0,     0,   0,   0, 255],
                            [255,   0,   0,   0, 255],
                            [0,   255, 255, 255, 255]])
    grid[i:i+4, j:j+5] = lwSpaceship

def addBlinker(i,j,grid):
    blinker = np.array([[0, 255, 0], 
                        [0, 255, 0], 
                        [0, 255, 0]])
    grid[i:i+3, j:j+3] = blinker

def addToad(i,j,grid):
    toad = np.array([[0,     0, 255,   0],
                     [255,   0,   0, 255],
                     [255,   0,   0, 255],
                     [0,   255,   0,   0]])
    grid[i:i+4, j:j+4] = toad

def addBeacon(i,j,grid):
    beacon = np.array([[255, 255,   0,   0],
                       [255, 255,   0,   0],
                       [0,     0, 255, 255],
                       [0,     0, 255, 255]])
    grid[i:i+4, j:j+4] = beacon

def update(frameNum, img, grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    # Rules of Conway's Game of Life
    height, width = newGrid.shape

    for i in range(height):
        for j in range(width):
            live_neighbours =   (grid[(i-1)%height, (j-1)%width] + grid[(i-1)%height, j] + grid[(i-1)%height, (j+1)%width] +
                                grid[i, (j-1)%width]              + grid[i, (j+1)%width] +
                                grid[(i+1)%height, (j-1)%width] + grid[(i+1)%height, j] + grid[(i+1)%height, (j+1)%width])/255
            if grid[i,j] == ON:
                newGrid[i,j] = OFF if ((live_neighbours < 2) or (live_neighbours > 3)) else ON
                '''
                if ((live_neighbours < 2) or (live_neighbours > 3)):
                    newGrid[i,j] = OFF
                else:
                    newGrid[i,j] = ON
                '''
            else:
                newGrid[i,j] = ON if live_neighbours == 3 else OFF




    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments



    
    # set grid size
    N = 100
        
    # set animation update interval
    updateInterval = 1

    # set generations, preferably >= 200
    global num_generations
    num_generations = 200

    # declare grid
    grid = np.array([])


    # populate grid with random on/off - more off than on
    #grid = randomGrid(N)
    # Uncomment lines to see the "glider" demo
    grid = np.zeros(N*N).reshape(N, N)
    addGlider(1, 1, grid)
    addLWSpaceship(10, 10, grid)
    #addBlinker(20,0,grid)
    #addBeacon(0,20,grid)
    addToad(20,20,grid)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames = num_generations,
                                  interval=updateInterval,
                                  save_count=200)

    plt.show()

# call main
if __name__ == '__main__':
    main()