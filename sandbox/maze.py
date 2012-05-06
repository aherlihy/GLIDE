#!usr/bin/python

# This method generates a random maze that guarentees that every room is accessible
# The output is to a file named "level6"
# The values to print are determined by generating a binary number based on which walls are visible. The binary number is then converted to hex and added to the output.
# (The binary numbers are actually in decimal since it's easier to convert to hex). The binary strings are just for funsiez.

# @author aherlihy

import random
import sys
# Direction enum
class dir:
    NORTH=[0,-1]
    SOUTH=[0,1]
    WEST=[-1,0]
    EAST=[1,0]
# Structure to keep track of each wall
class room:
    def __init__(self):
        self.northWall = 'N'
        self.southWall = 'N'
        self.eastWall = 'N'
        self.westWall = 'N'
        self.isGoal = False
        self.isStart = False
    def set_wall(self, dirc, component):
        if(dirc == dir.NORTH):
            self.northWall=component
        elif(dirc == dir.SOUTH):
            self.southWall=component
        elif(dirc == dir.EAST):
            self.eastWall=component
        elif(dirc == dir.WEST):
            self.westWall=component
    def get_opposite_wall(self, dirc):
        if(dirc == dir.NORTH):
            return self.southWall
        elif(dirc == dir.SOUTH):
            return self.northWall
        elif(dirc == dir.EAST):
            return self.westWall
        elif(dirc == dir.WEST):
            return self.eastWall

#Generates an array of the 4 direction enums in a (pseudo)random order.
def randomizeDirections():
    directions = [dir.NORTH, dir.SOUTH, dir.EAST, dir.WEST]
    for i in range(0,10):
        index1 = random.randint(0,3)
        index2 = random.randint(0,3)
        temp = directions[index1]
        directions[index1]=directions[index2]
        directions[index2]=temp
    return directions
def drunkenWalk(rooms, x, y):
    xMax = 26
    yMax = 10
    rooms[x][y] = room()
    directions = randomizeDirections()
    for d in directions:
        x_offset = d[0]
        y_offset = d[1]
        neighbor_x = x+x_offset
        neighbor_y = y+y_offset
        if(neighbor_x>=len(rooms) or neighbor_x<0):
            rooms[x][y].set_wall(d, 'W')
        elif(neighbor_y>=len(rooms[x]) or neighbor_y<0):
            rooms[x][y].set_wall(d, 'W')
        elif(rooms[neighbor_x][neighbor_y]==None):
            #make an open connection
            rooms[x][y].set_wall(d, 'A')
            #recurse on empty neighbor
            drunkenWalk(rooms, neighbor_x, neighbor_y)
        #if neighbor exists, and a connection does not exist for the opposite end
        elif(rooms[neighbor_x][neighbor_y].get_opposite_wall(d) == 'N'):
            #create random connection in x,y
            r = random.randint(0,10)
            if(r<=10):
                rooms[x][y].set_wall(d, 'W')
                #print "wall"
            else:
               # print "open"
                rooms[x][y].set_wall(d, 'A')
#            rooms[x][y].set_wall(d, 'W')
       #if neighbor exists, and a connection exists for the opposite end
        else:
            #set the connection in x,y to match
            rooms[x][y].set_wall(d, rooms[neighbor_x][neighbor_y].get_opposite_wall(d))
    return rooms
#Generate 10X24 array
def genMaze():
    rooms = []
    for x in range(0,26):
        rooms.append([])
        for y in range(0, 10):
            rooms[x].append(None)
    return rooms
def printMaze(rooms):
#The binary notation for each combination for a room is:
    # 0000 (0) All open
    # 0001 (1) North Wall
    # 0010 (2) South Wall
    # 0100 (4) West Wall
    # 1000 (8) East Wall
    file=open("../support/levels/level6", "w")
    for i in range(0, 10):
        for j in range(0,26):
            bin=""
            val=0
            rm = rooms[j][i]
            if(rm.eastWall == 'W'):
                bin = bin+"1"
                val = val+8
            else:
                bin = bin+"0"
            if(rm.westWall == 'W'):
                bin = bin+"1"
                val = val+4
            else:
                bin = bin+"0"

            if(rm.southWall == 'W'):
                bin = bin+"1"
                val = val+2
            else:
                bin = bin+"0"

            if(rm.northWall == 'W'):
                bin = bin+"1"
                val = val+1
            else:
                bin = bin+"0"
#            if(i==0 and j==0):
#                file.write('P')
#            elif(i==24 and j==9):
#                file.write('G')
#            else: 
            file.write(hex(val)[2:])
        file.write("\n")
    file.close()
#main
def create_maze():
    rooms = genMaze()
    rooms=drunkenWalk(rooms, 0, 0)
    printMaze(rooms)

if __name__ == '__main__':
    create_maze()
