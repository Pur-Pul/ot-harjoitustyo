import random
#This class defines a signle node in the cloud to be generated. Each pixel is one node
class Node:
    def __init__(self, coords, table, parent = None):
        self.coords = coords
        self.limit = [0, len(table)-1, 0, len(table[0])-1] #[up, down, left right]
        self.table = table
        #Place self in table
        #print(coords)
        table[coords[0]][coords[1]] = self
        self.neighbors = {}
        self.empty = []
        if parent:
            self.neighbors[str(parent.coords)] = parent
        
        self.findNeighbors()
        self.createNode()

    def findNeighbors(self):
        #This function looks for neighboring nodes in the ajdecent spaces. 
        #If a  new node is found, it is saved as a neighbor and told to look for neighbors of it's own.
        coords = self.coords
        limit = self.limit
        up = [coords[0]-1, coords[1]]
        right = [coords[0], coords[1]+1]
        down = [coords[0]+1, coords[1]]
        left = [coords[0], coords[1]-1]
        neighbors = [up, down, left, right]

        self.empty = [False, False, False, False]
        #print(coords, neighbors)
        for n in range(0, len(neighbors)):
            inRange = neighbors[n][0] <= limit[1] and neighbors[n][0] >= limit[0] and neighbors[n][1] <= limit[3] and neighbors[n][1] >= limit[2]
            if str(neighbors[n]) in self.neighbors or not inRange:
                continue
            #print('pass', neighbors[n])
            if self.table[neighbors[n][0]][neighbors[n][1]]:
                self.neighbors[str(neighbors[n])] = self.table[neighbors[n][0]][neighbors[n][1]]
                self.table[neighbors[n][0]][neighbors[n][1]].findNeighbors()
            else:
                self.empty[n] = True

    def createNode(self):
        #This function creates a new node in one of the empty adjecent spaces.
        #Wether a node is created or not is determined by the current node's distance to the limit and random.
        middleY = -1 * (-self.limit[1]//2)
        middleX = -1 * (-self.limit[3]//2)
        
        yDis = 0
        xDis = 0
        if self.coords[0] < middleY:
            yDis = self.coords[0]
        else:
            yDis = self.limit[1] - self.coords[0]
        if self.coords[1] < middleX:
            xDis = self.coords[1]
        else:
            xDis = self.limit[3] - self.coords[1]
        print(self.coords, yDis, xDis)
        
        yCreate = False
        xCreate = False
        for e in range(0, len(self.empty)):
            if self.empty[e]: #[up, down, left, right]
                if yDis >0 and (e == 0 or e == 1) and random.randrange(0, yDis+1) < yDis and random.randrange(0, xDis+1) < xDis:
                    yCreate = True
                elif xDis >0 and (e == 2 or e == 3) and random.randrange(0, xDis+1) < xDis and random.randrange(0, yDis+1) < yDis:
                    xCreate = True
        if yCreate and (self.empty[0] or self.empty[1]):
            ind = random.randrange(0, 2)
            while(not self.empty[ind]):
                if ind == 0:
                    ind = 1
                else:
                    ind = 0
            if ind == 0:
                diff = -1
            else:
                diff = 1
            newCoords = [self.coords[0]+diff,self.coords[1]]
            self.neighbors[str(newCoords)] = Node(newCoords, self.table, self)

        if xCreate and (self.empty[2] or self.empty[3]):
            ind = random.randrange(2,4)
            while(not self.empty[ind]):
                if ind == 3:
                    ind = 2
                else:
                    ind = 3
            if ind == 2:
                diff = -1
            else:
                diff = 1
            newCoords = [self.coords[0],self.coords[1]+diff]
            self.neighbors[str(newCoords)] = Node(newCoords, self.table, self)


if __name__ == "__main__":
    table = []
    for i in range(0, 12):
        table.append([None]*30)
    newNode = Node([(len(table)-1)//2,(len(table[0])-1)//2], table)
    art = []
    for row in range(0, len(table)):
        art.append('')
        for col in range(0, len(table[row])):
            if table[row][col]:
                if len(table[row][col].neighbors) == 1:
                    art[row]+='░░'
                elif len(table[row][col].neighbors) == 2:
                    art[row]+='▒▒'
                elif len(table[row][col].neighbors) == 3:
                    art[row]+='▓▓' 
                elif len(table[row][col].neighbors) == 4:
                    art[row]+='██'
            else:
                art[row]+='  ' 
    for i in art:
        print(i)



