import unittest
from wind_simulation import WindSimulator
from generation_algorithm import Node
import copy

class Test_WindSimulator(unittest.TestCase):
    def setUp(self):
        self.table = []
        for _ in range(0, 20):
            self.table.append([None]*40)
        self.node = Node([11, 21],self.table)
    def test_the_nodes_in_the_new_table_know_their_new_neighbors(self):
        sim = WindSimulator(self.table)
        self.table = sim.simulate()
        print(self.table)
        test_table=[]
        for _ in range(0, 20):
            test_table.append([None]*40)
        for row_index, row in enumerate(self.table):
            for node_index, node in enumerate(row):
                up=[row_index-1, node_index]
                down=[row_index+1, node_index]
                left=[row_index,node_index-1]
                right=[row_index,node_index+1]
                if node:
                    if row_index != 0 and str(up) in node.neighbors:
                        test_table[row_index-1][node_index]=node.neighbors[str(up)]
                    if node_index != 0 and str(left) in node.neighbors:
                        test_table[row_index][node_index-1]=node.neighbors[str(left)]
                    if row_index != len(self.table)-1 and str(down) in node.neighbors:
                        test_table[row_index+1][node_index]=node.neighbors[str(down)]
                    if node_index != len(row)-1 and str(right) in node.neighbors:
                        test_table[row_index][node_index+1]=node.neighbors[str(right)]
        self.assertEqual(self.table, test_table)