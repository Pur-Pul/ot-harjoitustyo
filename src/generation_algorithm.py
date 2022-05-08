import random
import sys
#This class defines a signle node in the cloud to be generated. Each pixel is one node
class Node:
    def __init__(self, coords, table, parent = None, manual = False, rec = 1):
        """Assigns base values for the class variables.

        Args:
            coords: This is the coordinates for the node in the table.

            table: The table the cloud is generated into.

            parent (_type_, optional): The partent node of the current node. Defaults to None.

            manual (bool, optional): If this is True, nodes will manually be place into the table,
            which means that there will be no randomly placed nodes.
            This is used to generate the tables that are read from the database. Defaults to False.
        """
        self.rec = rec
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
        if not manual:
            self.find_neighbors()
            self.create_node()

    def find_neighbors(self, rec = 1):
        """This function looks for neighboring nodes in the adjecent spaces.
        If a new node is found,
        it is saved as a neighbor and told to look for neighbors of it's own.

        Args:
            rec: This variable keeps track of the current recursion depth.
            If it gets within 100 recursions from the recursion limit,
            The recursion will stop. Defaults to 1.
        """
        if rec == 1:
            rec = self.rec
        if rec >= sys.getrecursionlimit()-500:
            return
        coords = self.coords
        limit = self.limit
        up = [coords[0]-1, coords[1]] # pylint: disable=invalid-name
        right = [coords[0], coords[1]+1]
        down = [coords[0]+1, coords[1]]
        left = [coords[0], coords[1]-1]
        neighbors = [up, down, left, right]

        self.empty = [False, False, False, False]
        #print(coords, neighbors)
        for neighbor_i, neighbor in enumerate(neighbors):
            in_range = (neighbors[neighbor_i][0] <= limit[1] and
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
                self.empty[neighbor_i] = True

    def create_node(self):
        """This function creates a new node in one of the empty adjecent spaces of the current node.
        Wether a node is created or not,
        is determined by the current node's distance to the limit and randomness.
        """
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

        if self.rec >= sys.getrecursionlimit()-700:
            y_create = False
            x_create = False
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
            self.neighbors[str(new_coords)] = Node(new_coords, self.table, self, rec = self.rec+1)
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
            self.neighbors[str(new_coords)] = Node(new_coords, self.table, self, rec = self.rec+1)

        

def print_table(table): # pragma: no cover
    art = []
    for row_index, row in enumerate(table):
        art.append('')
        for _, node in enumerate(row):
            if not node:
                art[row_index]+='  '
                continue
            if len(node.neighbors) <= 1:
                art[row_index]+='░░'
            elif len(node.neighbors) == 2:
                art[row_index]+='▒▒'
            elif len(node.neighbors) == 3:
                art[row_index]+='▓▓'
            elif len(node.neighbors) == 4:
                art[row_index]+='██'

    for i in art:
        print(i)

if __name__ == "__main__": # pragma: no cover
    main_table = []
    for _ in range(0, 50):
        main_table.append([None]*50)
    new_node = Node([(len(main_table)-1)//2,(len(main_table[0])-1)//2], main_table)
    print_table(main_table)
