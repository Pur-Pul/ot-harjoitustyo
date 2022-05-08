import sqlite3
class Project:
    def __init__(self, name):
        """Initializes the base values for the class variables,
        connects to the database and calls create_tables and initial_save.

        Args:
            name (_type_): _description_
        """
        self.conn = sqlite3.connect('project_data.db')
        self.cur = self.conn.cursor()

        self.name = name
        self.id = None
        self.table_width = None
        self.table_height = None
        self.frame_count = None
        self.table = None

        self.create_tables()
        self.initial_save()

    def create_tables(self):
        """This function generates the tables in the database if they do not already exist.
        """
        #self.cur.execute('''DROP TABLE IF EXISTS projects''')
        self.cur.execute("""CREATE TABLE IF NOT EXISTS projects
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        time TIMESTAMP DEFAULT(datetime('now','localtime')))
        """)
        #self.cur.execute('''DROP TABLE IF EXISTS project_data''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS project_data
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_width INTEGER,
        table_height INTEGER,
        frame_count INTEGER)
        ''')
        #self.cur.execute('''DROP TABLE IF EXISTS cloud''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS cloud
        (id INTEGER,
        y INTEGER,
        x INTEGER,
        value INTEGER)
        ''')

    def initial_save(self):
        """This function saves the name of the current project into the database.
        An id and timestamp is also atomatically generated for each project.
        If a project with the same name already exists,
        said project is then instead loaded from the database.
        """
        self.id = self.cur.execute("""SELECT id FROM projects WHERE name=?""",
        (self.name,)).fetchone()
        if not self.id:
            self.cur.execute("""INSERT INTO projects (name) VALUES (?)""", (self.name,))
            self.conn.commit()
            self.id = self.cur.execute("""SELECT id FROM projects WHERE name=?""",
            (self.name,)).fetchone()[0]
        else:
            self.id = self.id[0]
            self.get_project_data()

    def save_project_data(self):
        """When this function is called, the relevant classvariables are saved into the database.
        This includes: The table, table width and height as well as the frame count.
        The table is saved by converting all node objects into 1's and all Nones into 0.
        """
        self.cur.execute("""SELECT * FROM project_data WHERE id = ?""", (self.id,))

        self.cur.execute("""INSERT OR REPLACE INTO project_data
        (id, table_width, table_height, frame_count) VALUES (?,?,?,?)""",
        (self.id, self.table_width, self.table_height, self.frame_count))

        self.cur.execute("""SELECT * FROM cloud WHERE id = ?""", (self.id,))
        if self.cur.fetchone():
            self.cur.execute("""DELETE FROM cloud WHERE id = ?""", (self.id,))

        for row_i, row in enumerate(self.table):
            for col_i, col in enumerate(row):
                if col:
                    value = 1
                else:
                    value = 0
                self.cur.execute("""INSERT INTO cloud
                (id, y, x, value) values(?,?,?,?) """,
                (self.id, row_i, col_i, value))
        self.conn.commit()


    def get_project_data(self):
        """This function retrieves the data of the current project from the database
        and assigns the data to the class variables.
        """
        data = self.cur.execute("""SELECT * FROM project_data WHERE id=?""",
        (self.id,)).fetchone()
        if data:
            self.table_width = data[1]
            self.table_height = data[2]
            self.frame_count = data[3]

            new_table = []
            for _ in range(0, self.table_height):
                new_table.append([None]*self.table_width)

            rows = self.cur.execute("""SELECT * FROM cloud WHERE id=?""",
            (self.id,)).fetchall()
            for row in rows:
                if not row[3]:
                    continue
                new_table[row[1]][row[2]] = row[3]
            self.table = new_table

def get_project_names():
    """This funtion retrieves all the names of the projects
    and returns them as a list

    Returns:
        project_names :This is a list containing all the names of projects in the database.
    """
    conn = sqlite3.connect('project_data.db')
    cur = conn.cursor()
    project_names = cur.execute("""SELECT name FROM projects""").fetchall()
    if project_names:
        for name_i, name in enumerate(project_names):
            project_names[name_i] = name[0]
    return project_names


if __name__ == "__main__": # pragma: no cover
    new_project = Project("test_7")
    #new_project.save_project_data()
    #new_project.get_project_data()