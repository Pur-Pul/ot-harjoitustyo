import tkinter as tk
import copy
import time
from generation_algorithm import Node
from wind_simulation import WindSimulator
from database import Project, get_project_names

class GUI:
    def __init__(self, color_palette):
        """Assigns the base values for the class variables.

        Args:
            color_palette: This is the color palette used in the user interface
        """
        self.palette = color_palette
        self.done=False
        self.table = []
        self.cloud = None
        self.window = None
        self.project_name = None
        self.current_project = None
        self.frame_update = True
        self.canvas_frames = []
        self.first_canvas_frame = None
        self.animating = False
        self.loading_text = []

        #cloud options
        self.cloud_frames = 1
        self.cloud_width = 40
        self.cloud_height = 15

        self.widget = Widget(self.palette)

        self.pages = {'creation_screen' :
        {'frame_count' : 2,
            'main_frame' : None},
            'editor_screen' :
        {'frame_count' : 3,
            'main_frame' : None}}

    def create_frames(self, page):
        """Creates the frames for the specified page.

        Args:
            page: This is the parent page of the frames to be generated.

        Returns:
            A list object containing the generated frames and borders.
        """
        frame_count = self.pages[page]['frame_count']
        main_frame = self.pages[page]['main_frame']
        #creation of frames and borders
        frames = []
        borders = []
        for i in range(0, frame_count):
            borders.append(None)
            if i!=0:
                borders[i]=(tk.Frame(main_frame, bg=self.palette['bg_tb_color'], width=3))
                borders[i].pack(side='left', fill='y')
                if frame_count==3 and i ==1:
                    frames.append(tk.Frame(main_frame, bg=self.palette['bg_color'], width = 800))
                else:
                    frames.append(tk.Frame(main_frame, bg=self.palette['bg_color']))
                frames[i].pack(side='left', expand=True,  fill='both')
            else:
                frames.append(tk.Frame(main_frame, bg=self.palette['bg_color'], width=150))
                frames[i].pack(side='left', fill='y')
        return [frames,borders]

    def create_labels(self, page):
        """Generates the labels for the specified page.

        Args:
            page: The parent page of the labels

        Returns:
            labels: A list containg all the generated labels
        """
        frames = self.pages[page]['frames']
        #Creation of labels
        labels=[]
        for i, frame in enumerate(frames):
            labels.append([])
            if i == 0:
                label = self.widget.label(frame)
                label.configure(
                    text = 'Recent projects:',
                    font=('calibri', 16)
                )
                label.place(
                    anchor='n',
                    relx=0.5,
                    rely=0
                    )
                labels[i].append(label)
                project_names = get_project_names()
                for name_i, name in enumerate(project_names):
                    label_y=float(name_i+2)/30
                    label = self.widget.label(frame)
                    label.configure(
                        text = name,
                        font=('calibri', 15)
                        )
                    label.place(
                        anchor='n',
                        relx=0.5,
                        rely=label_y
                        )
                    labels[i].append(label)
            elif i == 1 and page == 'creation_screen':
                label = self.widget.label(frame)
                label.configure(
                    text = 'CloudGenerator',
                    font=('calibri', 50)
                    )
                label.place(x=100, y=50)
                labels[i].append(label)
            elif i == 2 and page == 'editor_screen':
                option_labels=['Frames:', 'Width:', 'Height:']
                for text_i, text in enumerate(option_labels):
                    label = self.widget.label(frame)
                    label.configure(
                        text = text,
                        font=('calibri', 15)
                        )
                    label.place(
                        anchor = 'n',
                        relx = 0.15,
                        rely = 0.05 + text_i/20
                        )
                    labels[i].append(label)
        return labels

    def create_textboxes(self, page):
        """Generates the entry/textboxes for the specified page.

        Args:
            page: The parent page of the generated textboxes.

        Returns:
            textboxes: a list containing all the generated textboxes.
        """
        frames = self.pages[page]['frames']
        #Creation of textbox
        textboxes=[]
        for i, frame in enumerate(frames):
            if page == 'creation_screen' and i == 1:
                textbox = self.widget.textbox(frame)
                strv = tk.StringVar(value = 'Enter name of project...')
                textbox.configure(
                    font=('calibri', 25),
                    width=50,
                    textvariable = strv
                    )
                strv.trace(
                    "w",
                    lambda *args,
                    strv=strv:
                    self.clear_textbox(textbox, strv)
                    )
                textbox.place(
                    anchor='s',
                    x=885,
                    y=400
                    )
                textboxes.append(textbox)
            elif page == 'editor_screen' and i == 2:
                option_textboxes=[[self.cloud_frames, 'frames'], [self.cloud_width, 'width'], [self.cloud_height, 'height']]
                for textbox_i, textbox_value in enumerate(option_textboxes):
                    strv = tk.StringVar(value = textbox_value[0])
                    textbox = self.widget.textbox(frame)
                    textbox.configure(
                        font=('calibri', 16),
                        width=4,
                        textvariable = strv
                        )
                    strv.trace(
                        "w", 
                        lambda *args,
                        strv=strv,
                        textbox=textbox,
                        option=textbox_value[1]:
                        self.textbox_update(textbox, option, strv)
                        )
                    textbox.place(
                        anchor='nw',
                        relx = 0.30,
                        rely = 0.05 +textbox_i/20
                        )
                    textboxes.append(textbox)
        return textboxes
    def create_buttons(self, page):
        """Generates buttons for the specified page.

        Args:
            page: The parent page of the buttons to be generated.

        Returns:
            buttons: a list containing all the generated buttons.
        """
        frames = self.pages[page]['frames']
        buttons = []
        for i, frame in enumerate(frames):
            if page == 'creation_screen' and i == 1:
                button = self.widget.button(frame)
                button.configure(
                    command = lambda: self.save_project(self.pages[page]['textboxes'][0].get()),
                    text = 'create',
                    font=('calibri', 20)
                    )
                button.place(
                    anchor='s',
                    x=885,
                    y=500
                    )
                buttons.append(button)
            if page == 'editor_screen' and i == 2:
                #Create button
                button = self.widget.button(frame)
                button.configure(
                    command = lambda: self.draw_cloud(),
                    text = 'Generate new cloud'
                    )
                button.place(
                    anchor='s',
                    relx=0.5,
                    rely=0.5
                    )
                buttons.append(button)
                #Animate button
                button = self.widget.button(frame)
                button.configure(
                    command = lambda: self.animate_cloud(self.cloud_frames),
                    text = 'Animate cloud')
                button.place(
                    anchor='s',
                    relx=0.5,
                    rely=0.6
                    )
                buttons.append(button)
                #Save project to database
                button = self.widget.button(frame)
                button.configure(
                    command = lambda: self.save_project(),
                    text = 'Save project')
                button.place(
                    anchor='s',
                    relx=0.5,
                    rely=0.7
                    )
                buttons.append(button)

        return buttons

    def create_canvas(self, page):
        """Generates the canvas, which is used to draw the clouds on.

        Args:
            page: The parent page of the generated canvas.

        Returns:
            canvas: a list containing all the generated canvases.
        """
        frames = self.pages[page]['frames']
        canvases = []
        if page == 'editor_screen':
            canvas = self.widget.canvas(frames[1])
            canvases.append(canvas)
        return canvases

    def create_gui(self, window_size):
        """creation of main window, frame and border

        Args:
            window_size: The size of the window to be generated.

        Returns:
            _type_: _description_
        """
        self.window = tk.Tk()
        self.window.geometry(str(window_size*2)+'x'+str(window_size))
        self.pages['creation_screen']['main_frame'] = tk.Frame(self.window,
        bg=self.palette['bg_color'],
        highlightbackground=self.palette['bg_tb_color'],
        highlightthickness=3)
        self.pages['editor_screen']['main_frame'] = tk.Frame(self.window,
        bg=self.palette['bg_color'],
        highlightbackground=self.palette['bg_tb_color'],
        highlightthickness=3)
        for key, page in self.pages.items():
            frames_and_borders = self.create_frames(key)
            page['frames'] = frames_and_borders[0]
            page['borders'] = frames_and_borders[1]
            page['labels'] = self.create_labels(key)
            page['textboxes'] = self.create_textboxes(key)
            page['buttons'] = self.create_buttons(key)
            page['canvas'] = self.create_canvas(key)
        self.first_canvas_frame = self.draw_cloud()
        self.pages['editor_screen']['main_frame'].place(relwidth=1, relheight=1)
        self.pages['creation_screen']['main_frame'].place(relwidth=1, relheight=1)
        self.pages['creation_screen']['main_frame'].lift()
        return self.window

    def save_project(self, name=None):
        """This function handles the saving of the project to the database.
        As well as loading previously created projects from the database.

        Args:
            name (_type_, optional): This variable is name of the project to save.
            If no name is given, the function uses the stored project object. Defaults to None.
        """
        if name:
            print(name)
            self.project_name = name
            self.current_project = Project(name)
            if self.current_project.table:
                self.table = self.reconstruct_table(self.current_project.table)
                if self.current_project.table_height:
                    self.cloud_height = self.current_project.table_height
                if self.current_project.table_width:
                    self.cloud_width = self.current_project.table_width
                if self.current_project.frame_count:
                    self.cloud_frames = self.current_project.frame_count
                self.draw_cloud(self.table)
            self.show('editor_screen')
        else:
            self.current_project.table = self.table
            self.current_project.table_height = len(self.table)
            self.current_project.table_width = len(self.table[0])
            self.current_project.save_project_data()

    def reconstruct_table(self, table):
        """This function reconstructs a cloud table from the table stored in the database.

        Args:
            table: This is the table taken from the database.
            Nodes are represented as the number 1 in this table.

        Returns:
            a cloud table: This table has node objects in the place the 1's in the previous table.
        """
        height = len(table)
        width = len(table[0])
        new_table = []
        for _ in range(0, height):
            new_table.append([None]*width)

        for row_i, row in enumerate(table):
            for col_i, col in enumerate(row):
                if col:
                    col = Node([row_i,col_i],new_table,manual=True)
                    col.find_neighbors()
                new_table[row_i][col_i] = col
        return new_table

    def show(self, page):
        """Lifts the specified page to the front.

        Args:
            page: The page to lift.
        """
        self.pages[page]['main_frame'].lift()
    def clear_textbox(self, textbox, strv):
        """This function clears the textbox of the preset text the first time it is triggered.

        Args:
            textbox: The textbox to clear.
        """
        text = textbox.get()
        if 'Enter name of project...' in text and not self.done:
            self.done=True
            text = text.replace('Enter name of project...','')
            strv.set(text)
        print(textbox.get())

    def animate_cloud(self, frame_count):
        """This function animates the cloud
        by switching between a specified number frames generated by the WindSimulator class.

        Args:
            frame_count: the number of frames to be used in the animation.
        """
        if self.animating:
            return 
        self.animating = True
        original = self.table
        frame_1 = copy.copy(original)
        canvas = self.pages['editor_screen']['canvas'][-1]
        self.first_canvas_frame = canvas
        master = canvas.master
        if self.frame_update:
            for i in self.canvas_frames:
                i.destroy()
            self.canvas_frames.clear()

        for i in range(0, frame_count):
            canvas.pack_forget()
            new_table = []
            if self.frame_update:
                for row in frame_1:
                    new_table.append(copy.copy(row))
                new_simulation = WindSimulator(new_table)
                frame_1 = new_simulation.simulate()

                self.pages['editor_screen']['canvas'][-1] = self.widget.canvas(master)
                canvas = self.pages['editor_screen']['canvas'][-1]
                self.draw_cloud(frame_1)
                self.loading_text.append(canvas.create_text(100,100,font=("calibri", 16),
                        text="Generating frames..."))
                self.canvas_frames.append(canvas)
            else:
                #print(self.canvas_frames[i])
                canvas = self.canvas_frames[i]
                if self.loading_text:
                    canvas.delete(self.loading_text[i])
                self.widget.canvas(canvas=canvas)

            self.window.update()
            time.sleep(0.01)
        canvas.pack_forget()
        self.pages['editor_screen']['canvas'][-1] = self.first_canvas_frame
        self.widget.canvas(canvas=self.pages['editor_screen']['canvas'][-1])
        if not self.frame_update:
            self.loading_text = []
        self.frame_update = False
        self.window.update()
        self.animating = False
        self.table = original

    def textbox_update(self, textbox, option, strv):
        text = textbox.get()
        print(text, option)
        try:
            if option == 'frames':
                self.cloud_frames = int(text)
            elif option == 'width':
                self.cloud_width = int(text)
            elif option == 'height':
                self.cloud_height = int(text)
            self.frame_update = True
        except ValueError:
            newtext=''
            for i in text:
                if i.isdigit():
                    newtext+=i
            strv.set(newtext)

    def draw_cloud(self, table=None):
        """Generates a cloud using the Node class and draws it onto the previously generated canvas.

        Args:
            table (_type_, optional): If a cloud table is given,
            the function draws the specified cloud onto the canvas instead of generating a new one.
            Defaults to None.
        """
        canvas = self.pages['editor_screen']['canvas'][-1]
        if not table:
            table=[]
            for _ in range(0,self.cloud_height):
                table.append([None]*self.cloud_width)
            self.cloud = Node([self.cloud_height//2, self.cloud_width//2],table)
            self.frame_update = True

        canvas.itemconfig('all',state='hidden')
        for row_index, row in enumerate(table):
            for node_index, node in enumerate(row):
                if not node:
                    continue
                if len(node.neighbors) == 1:
                    cloud_color="#A9A9A9"
                elif len(node.neighbors) == 2:
                    cloud_color="#D3D3D3"
                elif len(node.neighbors) == 3:
                    cloud_color="#E5E4E2"
                else:
                    cloud_color="white"
                canvas.create_rectangle(
                    (node_index+1)*10,
                    (row_index+1)*10,
                    (node_index+2)*10,
                    (row_index+2)*10,
                    outline=cloud_color,
                    fill=cloud_color
                    )
        self.table = table

class Widget:
    def __init__(self, palette):
        self.palette = palette
    def textbox(self,frame):
        textbox = tk.Entry(
            frame,
            fg = self.palette['bg_tb_color'],
            bg=self.palette['textbox_color'],
            highlightcolor=self.palette['textbox_ft_color'],
            highlightbackground = self.palette['textbox_ft_color'],
            highlightthickness = 3,
            exportselection = 0
            )
        return textbox
    def label(self,frame):
        label = tk.Label(
            frame,
            fg = self.palette['bg_tb_color'],
            bg=self.palette['bg_color']
            )
        return label
    def button(self,frame):
        button = tk.Button(
            frame,
            padx=2,
            fg = self.palette['button_ft_color'],
            bg = self.palette['button_color'],
            activeforeground = self.palette['button_color'],
            activebackground = self.palette['button_ft_color'],
            font=('calibri', 15)
            )
        return button
    def canvas(self,frame=None,canvas=None):
        if not canvas:
            canvas = tk.Canvas(
                frame,
                bg=self.palette['button_color'],
                highlightbackground=self.palette['bg_color'],
                highlightthickness=10
                )
        canvas.pack(
            fill='both',
            expand=True,
            anchor='n'
            )
        return canvas
