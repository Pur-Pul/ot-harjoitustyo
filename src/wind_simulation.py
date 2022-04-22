from generation_algorithm import Node
import copy
import math
class simulator:
    def __init__(self, table):
        #initializes the old table and an empty new table
        self.old_table = table
        self.new_table = []
        for i in range(0, len(self.old_table)):
            self.new_table.append([None]*len(self.old_table[0]))
    
    def simulate(self):
        old_table = self.old_table
        new_table = self.new_table
        for row_i, row in enumerate(old_table):
            for col_i, col in enumerate(row):
                if col:
                    empty = col.empty
                    up_free = empty[0]
                    down_free = empty[1]
                    left_free = empty[2]
                    right_free = empty[3]
                    '''
                    if row_i == 0:
                        up_free = False
                    if row_i == len(old_table)-1:
                        down_free = False
                    if col_i == 0:
                        left_free = False
                    if col_i == len(row)-1:
                        right_free = False'''
                    
                    y_move = 0
                    x_move = 0

                    x_dif = col_i
                    if len(row)-1 - col_i < col_i:
                        x_dif = len(row)-1 - col_i
                    
                    y_dif = row_i
                    if len(old_table)-1 - row_i < row_i:
                        y_dif = len(old_table)-1 - row_i
                    left_side = col_i < len(row)//2
                    up_side = row_i < len(old_table)//2

                    if (up_side and x_dif > y_dif) or (up_side and not left_side and x_dif == y_dif):
                        x_move = -1

                    if (not up_side and x_dif > y_dif) or (not up_side and left_side and x_dif == y_dif):
                        x_move = 1
                    if (left_side and x_dif < y_dif) or (up_side and left_side and x_dif == y_dif):
                        y_move = 1
                    if (not left_side and x_dif < y_dif) or ( not up_side and not left_side and x_dif == y_dif):
                        y_move = -1
                    

                    '''
                    if not up_free and not down_free:
                        x_move = -1
                    elif left_free and right_free:
                        x_move = 1
                    elif up_free and left_free and not right_free and row_i<len(old_table)/2:
                        y_move = -1
                    elif down_free and left_free and not right_free and row_i>=len(old_table)/2:
                        y_move = 1
                    else:
                        x_move = -1'''


                    new_y = row_i + y_move
                    new_x = col_i + x_move
                    col.table = new_table
                    col.coords = [new_y,new_x]
                    col.neighbors.clear()
                    #print([new_y, new_x],[y_move, x_move])
                    new_table[new_y][new_x] = col
        
        for row_i, row in enumerate(new_table):
            for col_i, col in enumerate(row):
                if col:
                    col.find_neighbors()
        return new_table

def print_table(table):
    art = []
    for row_index, row in enumerate(table):
        art.append('')
        for node_index, node in enumerate(row):
            if node:
                if len(node.neighbors) <= 1:
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

if __name__ == "__main__": # pragma: no cover
    table_1 = []
    for i in range(0, 20):
        table_1.append([None]*50)
    new_node = Node([(len(table_1)-1)//2,(len(table_1[0])-1)//2], table_1)
    
    print_table(table_1)
    for _ in range(0, 5000):
        new_table = []
        for i in range(0, len(table_1)):
            new_table.append(copy.copy(table_1[i]))
        new_simulation = simulator(new_table)
        table_1 = new_simulation.simulate()
        print_table(table_1)
    #print_table(table_1)
    


