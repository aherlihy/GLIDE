#!usr/bin/python

# This method generates a random maze and prints the output to a file named "level6"
# Throwback from CS15
import random
import sys
class dir:
    NORTH=[0,-1]
    SOUTH=[0,1]
    WEST=[-1,0]
    EAST=[1,0]
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
#            print ("making north wall")
            self.northWall=component
        elif(dirc == dir.SOUTH):
            self.southWall=component
        elif(dirc == dir.EAST):
#            print "making a west wall"
            self.eastWall=component
        elif(dirc == dir.WEST):
#            if(component == 'W'):
#                print "making an west wall"
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

def randomizeDirections():
    #rooms[x][y] = room()
    directions = [dir.NORTH, dir.SOUTH, dir.EAST, dir.WEST]
    for i in range(0,10):
        index1 = random.randint(0,3)
        index2 = random.randint(0,3)
        temp = directions[index1]
        directions[index1]=directions[index2]
        directions[index2]=temp
    return directions
def drunkenWalk(rooms, x, y):
    xMax = 12
    yMax = 4
#    file = open("output.py", 'w')
#    file.write("size of maze:("+ str(len(rooms))+","+ str(len(rooms[x]))+ ") index to:("+ str(x)+", "+ str(y)+ ")")
    rooms[x][y] = room()
    directions = randomizeDirections()
    count = 0
    for d in directions:
        count=count+1
        x_offset = d[0]
        y_offset = d[1]
        neighbor_x = x+x_offset
        neighbor_y = y+y_offset
        if(neighbor_x>=len(rooms) or neighbor_x<0):
#            print "room X out of range ", neighbor_x
#            print "making at", x, y
            if(d==dir.WEST):
                print "making west wall because oob at ", x, y
            if(d==dir.EAST):
                print "making east wall because oob at ", x, y
            rooms[x][y].set_wall(d, 'W')
        elif(neighbor_y>=len(rooms[x]) or neighbor_y<0):
#            print "room Y out of range ", neighbor_y
#            if(d==dir.WEST):
#                print "making west wall because oob at ", x, y
#            if(d==dir.EAST):
#                print "making east wall because oob at ", x, y
            rooms[x][y].set_wall(d, 'W')
        elif(rooms[neighbor_x][neighbor_y]==None):
            #make an open connection
#            print "neighbor room is null. recurse on ", neighbor_x, neighbor_y
            rooms[x][y].set_wall(d, 'A')
            #recurse on empty neighbor
            drunkenWalk(rooms, neighbor_x, neighbor_y)
        #if neighbor exists, and a connection does not exist for the opposite end
        elif(rooms[neighbor_x][neighbor_y].get_opposite_wall(d) == 'N'):
#            print "room exists, no connection"
            #create random connection in x,y
            r = random.randint(0,1)
            if(r==0):
                rooms[x][y].set_wall(d, 'W')
            else:
                rooms[x][y].set_wall(d, 'W')
       #if neighbor exists, and a connection exists for the opposite end
        else:
            #set the connection in x,y to match
#            print "room exists, connection"
            rooms[x][y].set_wall(d, rooms[neighbor_x][neighbor_y].get_opposite_wall(d))
#    print count
    return rooms
#Generate 10X24 array
def genMaze():
    rooms = []
    for x in range(0,12):
        rooms.append([])
        for y in range(0, 4):
            rooms[x].append(None)
    return rooms
def printMaze(rooms):
    file=open("level3", "w")
    #write the north wall (twice)
    for i in range(0,4):
        for j in range(0, 12):
            file.write(rooms[j][i].northWall + rooms[j][i].northWall)
        file.write('W'  + '\n')
        for j in range(0,12):
            if(j==0 and i==0):
                file.write(rooms[j][i].westWall + 'P')
            elif(j==10 and i==3):
                file.write(rooms[j][i].westWall + 'G')
            else:
                file.write(rooms[j][i].westWall + 'A')
        file.write(rooms[11][i].eastWall + "\n")
    for i in range(0, 12):
        file.write(rooms[i][3].southWall+rooms[i][3].southWall)
    file.write("W"+"\n")
    for i in range(0, 12):
        file.write(rooms[i][3].southWall+rooms[i][3].southWall)
    file.write("W" + "\n")
    
#main script
rooms = genMaze()
count=0
rooms=drunkenWalk(rooms, 0, 0)
for i in range(0,12):
    for j in range(0, 4):
        count=count+1
        if(rooms[i][j]==None):
            print "Null room at ", i, ", ", j
#rooms = drunkenWalk(rooms, 0,0)
print count
printMaze(rooms)
for i in range(0, 4):
    sys.stdout.write(' north '+rooms[0][i].northWall)
    sys.stdout.write(' south '+rooms[0][i].southWall)
    sys.stdout.write(' east ' + rooms[0][i].eastWall)
    sys.stdout.write(' west ' + rooms[0][i].westWall)
    sys.stdout.write('\n')
print "EASTSIDE"
for i in range(0,4):
    sys.stdout.write(' north '+rooms[10][i].northWall)
    sys.stdout.write(' south '+rooms[10][i].southWall)
    sys.stdout.write(' east ' + rooms[10][i].eastWall)
    sys.stdout.write(' west ' + rooms[10][i].westWall)
    sys.stdout.write('\n')
