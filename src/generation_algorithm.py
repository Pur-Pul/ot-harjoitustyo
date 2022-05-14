import random
import sys
#This class defines a signle node in the cloud to be generated. Each pixel is one node
class Node:
    """This class represents the nodes in a cloud.
    Each node has a chance to generate another node depending on their position and randomness.
    """
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
        table[coords[0]][coords[1]] = self
        self.neighbors = {}
        self.empty = []
        if parent:
            self.neighbors[str(parent.coords)] = parent
        if manual:
            return
        self.find_neighbors()
        if self.rec >= sys.getrecursionlimit()-800:
            return
        self.create_node()
        if parent:
            return
        for row in table:
            for node in row:
                if not node:
                    continue
                node.neighbors.clear()
                node.empty.clear()
                node.find_neighbors(single = True)

    def find_neighbors(self, rec = 1, single=False):
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
        coords, limit = (self.coords, self.limit)
        up = [coords[0]-1, coords[1]] # pylint: disable=invalid-name
        right = [coords[0], coords[1]+1]
        down = [coords[0]+1, coords[1]]
        left = [coords[0], coords[1]-1]
        neighbors,self.empty = (
            [up, down, left, right],
            [False, False, False, False]
            )
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
                if not single:
                    self.table[neighbor[0]][neighbor[1]].find_neighbors(rec+1, True)
            else:
                self.empty[neighbor_i] = True

    def create_node(self):
        """This function creates a new node in one of the empty adjecent spaces of the current node.
        Wether a node is created or not,
        is determined by the current node's distance to the limit and randomness.
        """
        middle_y, middle_x, y_dis, x_dis = (
            (-1 * (-self.limit[1]//2)),
            (-1 * (-self.limit[3]//2)),
            0,0)
        if self.coords[0] < middle_y:
            y_dis = self.coords[0]
        else:
            y_dis = self.limit[1] - self.coords[0]
        if self.coords[1] < middle_x:
            x_dis = self.coords[1]
        else:
            x_dis = self.limit[3] - self.coords[1]
        y_create, x_create = (False, False)
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
        if x_create:
            self.new_node('x', self.empty[2:4])
        if y_create:
            self.new_node('y', self.empty[0:2])
    def new_node(self, direction, empty):
        if empty[0] and empty[1]:
            ind = random.randrange(0, 2)
        else:
            for i, val in enumerate(empty):
                ind=None
                if val:
                    ind = i
                    break
        if ind is not None:
            diff = [-1,1][ind]
            new_coords = {
                'x':[self.coords[0],self.coords[1]+diff],
                'y':[self.coords[0]+diff,self.coords[1]]
                }
            self.neighbors[str(new_coords)] = Node(
                new_coords[direction],
                self.table,
                self,
                rec = self.rec+1
                )

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
