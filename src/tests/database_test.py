import unittest
import sqlite3
from database import Project
from generation_algorithm import Node

class Test_database(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect('project_data.db')
        self.cur = self.conn.cursor()
        self.table = []
        for _ in range(0, 20):
            self.table.append([None]*40)
        self.node = Node([11, 21],self.table)
        self.name = 'test_name'
            
        self.project = Project(self.name)
        
        self.projects_by_name = self.cur.execute("""SELECT * FROM projects WHERE name=?""", (self.name, )).fetchall()
    def test_initial_save_is_performed_on_project_creation(self):
        self.assertTrue(self.projects_by_name)
    def test_initial_save_stores_name_into_table_projects(self):
        self.assertEqual(self.projects_by_name[0][1], self.name)
    def test_initial_save_generates_both_id_and_timestamp_into_table_projects(self):
        if self.projects_by_name[0][0] and self.projects_by_name[0][2]:
            result = True
        else:
            result = False
        self.assertTrue(result)
    def doCleanups(self):
        self.cur.execute("""DELETE FROM projects WHERE name=?""", (self.name, ))
        self.conn.commit()

