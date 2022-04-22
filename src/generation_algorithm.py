import random
import sys
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
        self.find_neighbors()
        self.create_node()

    def find_neighbors(self, rec = 1):
        if rec == sys.getrecursionlimit()-100:
            return
        #This function looks for neighboring nodes in the ajdecent spaces.
        #If a  new node is found,
        #it is saved as a neighbor and told to look for neighbors of it's own.
        coords = self.coords
        limit = self.limit
        up = [coords[0]-1, coords[1]] # pylint: disable=invalid-name
        right = [coords[0], coords[1]+1]
        down = [coords[0]+1, coords[1]]
        left = [coords[0], coords[1]-1]
        neighbors = [up, down, left, right]

        self.empty = [False, False, False, False]
        #print(coords, neighbors)
        for next, neighbor in enumerate(neighbors):
            in_range = (neighbors[next][0] <= limit[1] and
            neighbor[0] >= limit[0] and
            neighbor[1] <= limit[3] and
            neighbor[1] >= limit[2])
            if str(neighbor) in self.neighbors or not in_range:
                continue
            #print('pass', neighbors[n])
            if self.table[neighbor[0]][neighbor[1]]:
                self.neighbors[str(neighbor)] = self.table[neighbor[0]][neighbor[1]]
                self.table[neighbor[0]][neighbor[1]].find_neighbors(rec+1)
            else:
                self.empty[next] = True

    def create_node(self):
        #This function creates a new node in one of the empty adjecent spaces.
        #Wether a node is created or not
        #is determined by the current node's distance to the limit and random.
        middle_y = -1 * (-self.limit[1]//2)
        middle_x = -1 * (-self.limit[3]//2)
        y_dis = 0
        x_dis = 0
        if self.coords[0] < middle_y:
            y_dis = self.coords[0]
        else:
            y_dis = self.limit[1] - self.coords[0]
        if self.coords[1] < middle_x:
            x_dis = self.coords[1]
        else:
            x_dis = self.limit[3] - self.coords[1]
        #print(self.coords, yDis, xDis)
        y_create = False
        x_create = False
        for direction_index, direction in enumerate(self.empty):
            if direction: #[up, down, left, right]
                if (y_dis > 0 and direction_index in  (0, 1)
                and random.randrange(0, y_dis+1) < y_dis
                and random.randrange(0, x_dis+1) < x_dis):
                    y_create = True
                elif (x_dis > 0 and direction_index in (2, 3)
                and random.randrange(0, x_dis+1) < x_dis
                and random.randrange(0, y_dis+1) < y_dis):
                    x_create = True
        if y_create and (self.empty[0] or self.empty[1]):
            ind = random.randrange(0, 2)
            while not self.empty[ind]:
                if ind == 0:
                    ind = 1
                else:
                    ind = 0
            if ind == 0:
                diff = -1
            else:
                diff = 1
            new_coords = [self.coords[0]+diff,self.coords[1]]
            self.neighbors[str(new_coords)] = Node(new_coords, self.table, self)

        if x_create and (self.empty[2] or self.empty[3]):
            ind = random.randrange(2,4)
            while not self.empty[ind]:
                if ind == 3:
                    ind = 2
                else:
                    ind = 3
            if ind == 2:
                diff = -1
            else:
                diff = 1
            new_coords = [self.coords[0],self.coords[1]+diff]
            self.neighbors[str(new_coords)] = Node(new_coords, self.table, self)


if __name__ == "__main__": # pragma: no cover
    table = []
    for i in range(0, 20):
        table.append([None]*70)
    new_node = Node([(len(table)-1)//2,(len(table[0])-1)//2], table)
    art = []
    for row_index, row in enumerate(table):
        art.append('')
        for node_index, node in enumerate(row):
            if node:
                if len(node.neighbors) == 1:
                    art[row_index]+='░░'
                elif len(node.neighbors) == 2:
                    art[row_index]+='▒▒'
                elif len(node.neighbors) == 3:
                    art[row_index]+='▓▓'
                elif len(node.neighbors) == 4:
                    art[row_index]+='██'
            else:
                art[row_index]+='  '
    for i in art:
        print(i)
