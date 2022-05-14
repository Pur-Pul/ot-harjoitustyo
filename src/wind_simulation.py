import copy
from generation_algorithm import Node
from generation_algorithm import print_table
class WindSimulator:
    def __init__(self, table):
        """initializes the old table and an empty new table

        Args:
            table: This is the previous frame of the cloud animation.
        """
        self.old_table = table
        self.new_table = []
        for _ in range(0, len(self.old_table)):
            self.new_table.append([None]*len(self.old_table[0]))

    def find_new_coords(self, col_i, row_i, row):
        """This function find the new coordinates of a node
        based on the give previous coordinates

        Args:
            col_i : The x coordinate of node in the previous frame.
            row_i : The y coordinate of node in the previous frame.
            row : The current row in the previous frame.

        Returns:
            _type_: _description_
        """
        y_move,x_move,x_difs,y_difs=(
            0,0,
            [col_i,len(row)-1 - col_i],
            [row_i,len(self.old_table)-1 - row_i]
            )
        x_difs.sort()
        y_difs.sort()
        y_dif,x_dif = (y_difs[0], x_difs[0])

        left_side = col_i < len(row)//2
        up_side = row_i < len(self.old_table)//2

        if not(
            abs(len(self.old_table)-1 - row_i) == row_i
            and x_dif>=y_dif
            ):
            if ((up_side and x_dif > y_dif) or
            (up_side and not left_side and x_dif == y_dif)):
                x_move = -1
            if ((not up_side and x_dif > y_dif) or
            (not up_side and left_side and x_dif == y_dif)):
                x_move = 1
            if ((left_side and x_dif < y_dif) or
            (up_side and left_side and x_dif == y_dif)):
                y_move = 1
            if ((not left_side and x_dif < y_dif) or
            ( not up_side and not left_side and x_dif == y_dif)):
                y_move = -1
        return [row_i + y_move, col_i + x_move]

    def simulate(self):
        """This function uses find_new_coords for every node to create the new frame.

        Returns:
            new_table: This is the newly generated frame of the animation.
        """
        for row_i, row in enumerate(self.old_table):
            for col_i, col in enumerate(row):
                if not col:
                    continue
                new_coords = self.find_new_coords(col_i, row_i, row)
                col.table = self.new_table
                col.coords = new_coords
                col.neighbors.clear()
                self.new_table[new_coords[0]][new_coords[1]] = col
        for row_i, row in enumerate(self.new_table):
            for col_i, col in enumerate(row):
                if not col:
                    continue
                col.find_neighbors(single=True)

        return self.new_table


if __name__ == "__main__": # pragma: no cover
    table_1 = []
    frames=[]
    N = 20
    M = 40
    for _ in range(0, N):
        table_1.append([None]*M)
    new_node = Node([(len(table_1)-1)//2,(len(table_1[0])-1)//2], table_1)

    frames.append(copy.copy(table_1))
    print_table(table_1)

    for _ in range(0, 10):
        n_table = []
        for row_1 in table_1:
            n_table.append(copy.copy(row_1))
        new_simulation = WindSimulator(n_table)
        table_1 = new_simulation.simulate()
        print_table(table_1)
        frames.append(copy.copy(table_1))
    print_table(frames[0])
    print_table(frames[-1])
