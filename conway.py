"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

#import sys, argparse
from datetime import date
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]
global num_generations, width, height, live_cells, total

# Define all patterns for counting

block = np.array([[0,     0,   0,   0],
                  [0,   255, 255,   0],
                  [0,   255, 255,   0],
                  [0,     0,   0,   0]])
beehive = np.array([[0,     0,   0,   0,   0,   0],
                    [0,     0, 255, 255,  0,    0],
                    [0,   255,   0,   0, 255,   0],
                    [0,     0, 255, 255,   0,   0],
                    [0,     0,   0,   0,   0,   0]])
loaf = np.array([[0,     0,   0,   0,   0,   0],
                 [0,     0, 255, 255,   0,   0],
                 [0,   255,   0,   0, 255,   0],
                 [0,     0, 255,   0, 255,   0],
                 [0,     0,   0, 255,   0,   0],
                 [0,     0,   0,   0,   0,   0]])
boat = np.array([[0,     0,   0,   0,   0],
                 [0,   255, 255,   0,   0],
                 [0,   255,   0, 255,   0],
                 [0,     0, 255,   0,   0],
                 [0,     0,   0,   0,   0]])
tub = np.array([[0,     0,   0,   0,   0],
                [0,     0, 255,   0,   0],
                [0,   255,   0, 255,   0],
                [0,     0, 255,   0,   0],
                [0,     0,   0,   0,   0]])
blinker1 = np.array([[0,     0,   0,   0,   0],
                     [0,     0, 255,   0,   0],
                     [0,     0, 255,   0,   0],
                     [0,     0, 255,   0,   0],
                     [0,     0,   0,   0,   0]])
blinker2 = np.array([[0,     0,   0,   0,   0],
                     [0,     0,   0,   0,   0],
                     [0,   255, 255, 255,   0],
                     [0,     0,   0,   0,   0],
                     [0,     0,   0,   0,   0]])
toad1 = np.array([[0,     0,   0,   0,   0,   0],
                  [0,     0,   0, 255,   0,   0],
                  [0,   255,   0,   0, 255,   0],
                  [0,   255,   0,   0, 255,   0],
                  [0,     0, 255,   0,   0,   0],
                  [0,     0,   0,   0,   0,   0]])
toad2 = np.array([[0,     0,   0,   0,   0,   0],
                  [0,     0, 255, 255, 255,   0],
                  [0,   255, 255, 255,   0,   0],
                  [0,     0,   0,   0,   0,   0]])
beacon1 = np.array([[0,     0,   0,   0,   0,   0],
                    [0,   255, 255,   0,   0,   0],
                    [0,   255, 255,   0,   0,   0],
                    [0,     0,   0, 255, 255,   0],
                    [0,     0,   0, 255, 255,   0],
                    [0,     0,   0,   0,   0,   0]])
beacon2 = np.array([[0,     0,   0,   0,   0,   0],
                    [0,   255, 255,   0,   0,   0],
                    [0,   255,   0,   0,   0,   0],
                    [0,     0,   0,   0, 255,   0],
                    [0,     0,   0, 255, 255,   0],
                    [0,     0,   0,   0,   0,   0]])
glider1 = np.array([[0,   255,   0],
                    [0,     0, 255],
                    [255, 255, 255]])
glider2 = np.array([[255,   0, 255],
                    [0,   255, 255],
                    [0,   255,   0]])
glider3 = np.array([[0,     0, 255],
                    [255,   0, 255],
                    [0,   255, 255]])
glider4 = np.array([[255,   0,   0],
                    [0,   255, 255],
                    [255, 255,   0]])
lwss1 = np.array([[255,   0,   0, 255,   0],
                  [0,     0,   0,   0, 255],
                  [255,   0,   0,   0, 255],
                  [0,   255, 255, 255, 255]])
lwss2 = np.array([[0,     0, 255, 255,   0],
                  [255, 255,   0, 255, 255],
                  [255, 255, 255, 255,   0],
                  [0,   255, 255,   0,   0]])
lwss3 = np.array([[0,   255, 255, 255, 255],
                  [255,   0,   0,   0, 255],
                  [0,     0,   0,   0, 255],
                  [255,   0,   0, 255,   0]])
lwss4 = np.array([[0,   255, 255,   0,   0],
                  [255, 255, 255, 255,   0],
                  [255, 255,   0, 255, 255],
                  [0,     0, 255, 255,   0]])


def readConfigFile():
    global live_cells, width, height, num_generations
    live_cells = []
    # reads file named "input.txt" according to given specifications
    file = open("input.txt", "r")

    for index, line in enumerate(file):
        # Width and height from first line
        if (index==0):
            width, height = line.split(" ")
            width = int(width)
            height = int(height)
        # get number of generations from second line
        if (index==1):
            num_generations = int(line)
        # get live cells from rest of file
        if (index>1):
            x, y = line.split(" ")
            live_cells.append((int(x),int(y)))

def setCells(grid):
    newGrid = grid.copy()
    for cell in live_cells:
        x,y = cell
        newGrid[y,x] = ON

    return newGrid

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def countPatterns(grid, pattern):
    count = 0
    height, width = pattern.shape

    for i in range(grid.shape[0] - height + 1):
        for j in range(grid.shape[1] - width + 1):
            if (np.all(grid[i:i+height,j:j+width] == pattern)):
                count+=1
    return count

def allPatterns(grid):
    global total

    blockCount = countPatterns(grid,block)
    beehiveCount = countPatterns(grid,beehive)
    loafCount = countPatterns(grid,loaf)
    boatCount = countPatterns(grid,boat)
    tubCount = countPatterns(grid,tub)
    blinkerCount = countPatterns(grid,blinker1) + countPatterns(grid,blinker2)
    toadCount = countPatterns(grid,toad1) + countPatterns(grid,toad2)
    beaconCount = countPatterns(grid,beacon1) + countPatterns(grid,beacon2)
    gliderCount = countPatterns(grid,glider1) + countPatterns(grid,glider2) + countPatterns(grid,glider3) + countPatterns(grid,glider4)
    shipCount = countPatterns(grid,lwss1) + countPatterns(grid,lwss2) + countPatterns(grid,lwss3) + countPatterns(grid,lwss4)
    total = blockCount + beehiveCount + loafCount + boatCount + tubCount + blinkerCount + toadCount + beaconCount + gliderCount + shipCount
    counters = [blockCount, beehiveCount, loafCount, boatCount, tubCount, blinkerCount, toadCount, beaconCount, gliderCount, shipCount]

    return counters

def generateReport(grid, frameNum):
    global total
    
    file = open("output.txt", "a")
    count = allPatterns(grid)
    file.write("Iteration: " + str(frameNum)+"\n")
    file.write("---------------------------------\n")
    file.write("              | Count | Percent |\n")
    file.write(" Block        |  " + str(count[0]) + "    |  " + str(percent(count[0])) + "      |\n")
    file.write(" Beehive      |  " + str(count[1]) + "    |  " + str(percent(count[1])) + "      |\n")
    file.write(" Loaf         |  " + str(count[2]) + "    |  " + str(percent(count[2])) + "      |\n")
    file.write(" Boat         |  " + str(count[3]) + "    |  " + str(percent(count[3])) + "      |\n")
    file.write(" Tub          |  " + str(count[4]) + "    |  " + str(percent(count[4])) + "      |\n")
    file.write(" Blinker      |  " + str(count[5]) + "    |  " + str(percent(count[5])) + "      |\n")
    file.write(" Toad         |  " + str(count[6]) + "    |  " + str(percent(count[6])) + "      |\n")
    file.write(" Beacon       |  " + str(count[7]) + "    |  " + str(percent(count[7])) + "      |\n")
    file.write(" Glider       |  " + str(count[8]) + "    |  " + str(percent(count[8])) + "      |\n")
    file.write(" LW spaceship |  " + str(count[9]) + "    |  " + str(percent(count[9])) + "      |\n")
    file.write("---------------------------------\n")
    file.write(" TOTAL        |  " + str(total) + "    |         |\n")
    file.write("---------------------------------\n")
    file.write("\n")
    file.close()

def percent(num):
    global total

    if (total == 0):
        return 0
    return int(num/(total/100))


'''
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
'''
    
def update(frameNum, img, grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    # Rules of Conway's Game of Life
    #height, width = newGrid.shape

    for i in range(height):
        for j in range(width):
            live_neighbours =   (grid[(i-1)%height, (j-1)%width] + grid[(i-1)%height, j] + grid[(i-1)%height, (j+1)%width] +
                                grid[i, (j-1)%width]              + grid[i, (j+1)%width] +
                                grid[(i+1)%height, (j-1)%width] + grid[(i+1)%height, j] + grid[(i+1)%height, (j+1)%width])/255
            if grid[i,j] == ON:
                newGrid[i,j] = OFF if ((live_neighbours < 2) or (live_neighbours > 3)) else ON
            else:
                newGrid[i,j] = ON if live_neighbours == 3 else OFF


    # update data on report on all frames except first
    if (frameNum < num_generations and frameNum != 0):
        generateReport(newGrid, frameNum)

    # pause animation on max generations
    #crashes for unknown reasons
    if frameNum == num_generations-1:
        print("Report generated!")
        plt.pause(100)
        exit()

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    #parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    #global width, height

    global total
    # set grid size
    N = 100
    readConfigFile()
        
    # set animation update interval
    updateInterval = 1

    # manual set for generations, preferably >= 200
    #num_generations = 200

    # declare grid
    grid = np.array([])


    # populate grid with random on/off - more off than on
    #grid = randomGrid(N)
    # populate grid
    grid = np.random.choice(vals, width*height, p=[0.2, 0.8]).reshape(height, width)
    grid = np.zeros(height*height).reshape(height, width)
    grid = setCells(grid)

    #addGlider(1, 1, grid)
    #addLWSpaceship(10, 10, grid)
    #addBlinker(20,0,grid)
    #addBeacon(0,20,grid)
    #addToad(20,20,grid)

    # create report file with initial values        
    file = open("output.txt", "w")    
    count = allPatterns(grid)
    today = date.today()
    day = today.strftime("%Y/%m/%d")
    file.write("Simulation at " + str(today) + "\n")
    file.write("Universe size " + str(width) + " x " + str(height) + "\n\n")
    file.write("Iteration: 0\n")
    file.write("---------------------------------\n")
    file.write("              | Count | Percent |\n")
    file.write(" Block        |  " + str(count[0]) + "    |  " + str(percent(count[0])) + "      |\n")
    file.write(" Beehive      |  " + str(count[1]) + "    |  " + str(percent(count[1])) + "      |\n")
    file.write(" Loaf         |  " + str(count[2]) + "    |  " + str(percent(count[2])) + "      |\n")
    file.write(" Boat         |  " + str(count[3]) + "    |  " + str(percent(count[3])) + "      |\n")
    file.write(" Tub          |  " + str(count[4]) + "    |  " + str(percent(count[4])) + "      |\n")
    file.write(" Blinker      |  " + str(count[5]) + "    |  " + str(percent(count[5])) + "      |\n")
    file.write(" Toad         |  " + str(count[6]) + "    |  " + str(percent(count[6])) + "      |\n")
    file.write(" Beacon       |  " + str(count[7]) + "    |  " + str(percent(count[7])) + "      |\n")
    file.write(" Glider       |  " + str(count[8]) + "    |  " + str(percent(count[8])) + "      |\n")
    file.write(" LW spaceship |  " + str(count[9]) + "    |  " + str(percent(count[9])) + "      |\n")
    file.write("---------------------------------\n")
    file.write(" TOTAL        |  " + str(total) + "    |         |\n")
    file.write("---------------------------------\n")
    file.write("\n")
    file.close()

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