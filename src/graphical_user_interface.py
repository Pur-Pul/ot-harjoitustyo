import tkinter as tk
import copy
from generation_algorithm import Node
from wind_simulation import WindSimulator
from database import Project, get_project_names

class GUI:
    """This class is the base of the graphical user interface.
    It generates and displays all the graphical elements of the application using tkinter.
    """
    def __init__(self, color_palette):
        """Assigns the base values for the class variables.

        Args:
            color_palette: This is the color palette used in the user interface.
        """
        self.done = False
        self.window = None
        self.frame_update = True
        #project options
        self.project_options = {
            'table' : [],
            'current_project' : None
        }
        #cloud options
        self.cloud_options = {}
        #animation options
        self.animation_options = {
            'canvas_frames' : ['first'],
            'animating' : False,
            'loading_text' : None,
            'color' : '#ffffff'
        }
        self.widget = Widget(color_palette)

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
            frames.append(self.widget.frame(main_frame))
            if i!=0:
                borders[i]=self.widget.border(main_frame)
                if frame_count==3 and i ==1:
                    frames[i].configure(width = 800)
                frames[i].pack(side='left', expand=True,  fill='both')
            else:
                frames[i].configure(width=150)
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
                label = self.widget.label(frame, 'Recent projects:', 16)
                label.pack()
                labels[i].append(label)
                for name in get_project_names():
                    label = self.widget.link(frame, name, self)
                    label.pack()
                    labels[i].append(label)
            elif i == 1 and page == 'creation_screen':
                label = self.widget.label(frame, 'CloudGenerator', 50)
                label.place(x=100, y=50)
                labels[i].append(label)
            elif i == 2 and page == 'editor_screen':
                option_labels=['Frames:', 'Width:', 'Height:', 'FPS:', 'Red', 'Green', 'Blue']
                for text_i, text in enumerate(option_labels):
                    label = self.widget.label(frame, text)
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
        frames, textboxes = (self.pages[page]['frames'],[])
        #Creation of textbox
        for i, frame in enumerate(frames):
            if page == 'creation_screen' and i == 1:
                textbox,strv = (
                    self.widget.textbox(frame),
                    tk.StringVar(value = 'Enter name of project...')
                    )
                textbox.configure(
                    font=('calibri', 25),
                    width=50,
                    textvariable = strv
                    )
                strv.trace(
                    "w",
                    lambda *args,
                    textbox=textbox,
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
                option_textboxes = []
                for option,value in self.cloud_options.items():
                    option_textboxes.append([value, option])
                for textbox_i, textbox_value in enumerate(option_textboxes):
                    strv = textbox_value[0]
                    textbox = self.widget.textbox(frame)
                    textbox.configure(
                        font=('calibri', 16),
                        width=4,
                        textvariable = strv
                        )
                    if textbox_i < 4:
                        strv.trace(
                            "w",
                            lambda *args,
                            strv=strv:
                            self.textbox_update(strv)
                            )
                    else:
                        strv.trace(
                            "w",
                            lambda *args,
                            strv=strv,
                            textbox_i=textbox_i:
                            self.color_values(strv, (textbox_i-4)*2)
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
                button = self.widget.button(
                    frame,
                    'create',
                    20,
                    lambda: self.save_project(self.pages[page]['textboxes'][0].get())
                    )
                button.place(
                    anchor='s',
                    x=885,
                    y=500
                    )
                buttons.append(button)
            if page == 'editor_screen' and i == 2:
                #Create button
                button = self.widget.button(
                    frame,
                    'Generate new cloud',
                    command = lambda: self.draw_cloud() # pylint: disable=unnecessary-lambda
                    )
                button.place(
                    anchor='s',
                    relx=0.5,
                    rely=0.5
                    )
                buttons.append(button)
                #Animate button
                button = self.widget.button(
                    frame,
                    'Animate cloud',
                    command = lambda: self.animate_cloud(int(self.cloud_options['frames'].get())) # pylint: disable=unnecessary-lambda
                    )
                button.place(
                    anchor='s',
                    relx=0.5,
                    rely=0.6
                    )
                buttons.append(button)
                #Save project to database
                button = self.widget.button(
                    frame,
                    'Save project',
                    command = lambda: self.save_project() # pylint: disable=unnecessary-lambda
                    )
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
        self.cloud_options = {
            'frames' : tk.StringVar(value=1),
            'width' : tk.StringVar(value=40),
            'height' : tk.StringVar(value=15),
            'fps' : tk.StringVar(value=12),
            'red' : tk.StringVar(value=255),
            'green' : tk.StringVar(value=255),
            'blue' : tk.StringVar(value=255)
            }
        self.window.geometry(str(window_size*2)+'x'+str(window_size))
        self.pages['creation_screen']['main_frame'] = self.widget.frame(self.window)
        self.pages['editor_screen']['main_frame'] = self.widget.frame(self.window)
        for key, page in self.pages.items():
            frames_and_borders = self.create_frames(key)
            page['frames'] = frames_and_borders[0]
            page['borders'] = frames_and_borders[1]
            page['labels'] = self.create_labels(key)
            page['textboxes'] = self.create_textboxes(key)
            page['buttons'] = self.create_buttons(key)
            page['canvas'] = self.create_canvas(key)
        self.draw_cloud()
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
            new_project = Project(name)
            if new_project.table:
                self.project_options['table'] = self.reconstruct_table(new_project.table)
                if new_project.table_options['height']:
                    self.cloud_options['height'].set(new_project.table_options['height'])
                if new_project.table_options['width']:
                    self.cloud_options['width'].set(new_project.table_options['width'])
                if new_project.table_options['frame_count']:
                    self.cloud_options['frames'].set(new_project.table_options['frame_count'])
                if new_project.fps:
                    self.cloud_options['fps'].set(new_project.fps)
                if new_project.color:
                    self.cloud_options['red'].set(new_project.color['red'])
                    self.cloud_options['green'].set(new_project.color['green'])
                    self.cloud_options['blue'].set(new_project.color['blue'])

                self.draw_cloud(self.project_options['table'])
            self.show('editor_screen')
            self.project_options['current_project'] = new_project
        else:
            project = self.project_options['current_project']
            project.table = self.project_options['table']
            (
                project.table_options['height'],
                project.table_options['width'],
                project.table_options['frame_count'],
                project.fps,
                project.color
                ) = (
                len(self.project_options['table']),
                len(self.project_options['table'][0]),
                self.cloud_options['frames'].get(),
                self.cloud_options['fps'].get(),
                {
                    'red' : self.cloud_options['red'].get(),
                    'green': self.cloud_options['green'].get(),
                    'blue' : self.cloud_options['blue'].get()
                    }
                )
            project.save_project_data()

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
        if not self.done:
            self.done=True
            template = 'Enter name of project...'
            if len(text) < len(template):
                strv.set('')
                return
            for i, letter in enumerate(template):
                if text[i] != letter:
                    strv.set(text[i])
                    return
            strv.set(text[-1])

    def animate_cloud(self, frame_count):
        """This function animates the cloud
        by switching between a specified number frames generated by the WindSimulator class.
        The frames are represented as items on the canvas,
        which can be manipulated using a tag in the format 'cloud_<number>'.

        Args:
            frame_count: the number of frames to be used in the animation.
        """
        if self.animation_options['animating']:
            return
        for textbox in self.pages['editor_screen']['textboxes']:
            textbox.configure(state='disabled')
        self.animation_options['animating'], frame_1, canvas, canvas_frames = (
            True,
            copy.copy(self.project_options['table']),
            self.pages['editor_screen']['canvas'][-1],
            self.animation_options['canvas_frames']
            )
        while self.frame_update and len(canvas_frames)>1:
            canvas.delete(canvas_frames.pop())

        for i in range(0, frame_count):
            new_table = []
            if self.frame_update:
                for row in frame_1:
                    new_table.append(copy.copy(row))
                frame_1 = WindSimulator(new_table).simulate()
                self.draw_cloud(frame_1,'cloud_'+str(i))
                canvas_frames.append('cloud_'+str(i))
                canvas.itemconfigure(canvas_frames[-2], state='hidden')
                self.window.update()
            else:
                canvas.itemconfigure('all', state='hidden')
                canvas.itemconfigure(canvas_frames[i], state='normal')
                self.window.after(
                    1000//int(self.cloud_options['fps'].get()),
                    self.window.update()
                    )
        canvas.itemconfigure('all', state='hidden')
        canvas.itemconfigure(canvas_frames[0], state='normal')
        self.window.update()
        self.animation_options['animating'], self.frame_update = (False, False)
        for textbox in self.pages['editor_screen']['textboxes']:
            textbox.configure(state='normal')

    def textbox_update(self, strv):
        """Function that validates the input written into the textboxes.

        Args:
            strv: StringVariable of the updated textbox.
        """
        text = strv.get()
        new_text=''
        for i in text:
            if i.isdigit():
                new_text+=i
        while len(new_text) > 0 and new_text[0] == '0':
            new_text = new_text[1:]
        if len(new_text) == 0:
            new_text='1'
        strv.set(new_text)
        self.frame_update=True

    def color_values(self, strv, color_index):
        """This function validates and converts the RGB values into hexadecimal.

        Args:
            strv (_type_): The StringVariable that contains the input.
            color_index (_type_): An index that determines
            which part of the hexadecimal the value belongs to
        """
        print(color_index)
        text = strv.get()
        new_text=''
        for i in text:
            if i.isdigit():
                new_text+=i
        if len(new_text) == 0:
            new_text='0'
        if int(new_text)>255:
            new_text = '255'
        strv.set(new_text)
        hex_color = hex(int(new_text)).replace('0x','')
        print(hex_color)
        if len(hex_color) == 1:
            hex_color = '0'+hex_color
        self.animation_options['color'] = (
            self.animation_options['color'][:color_index+1]+
            hex_color+
            self.animation_options['color'][color_index+3:]
            )
        print(self.animation_options['color'])
        self.frame_update=True
        self.draw_cloud(self.project_options['table'])

    def darken_color(self, color_code, level):
        """This function darkens the specified color value depending on the specified level.

        Args:
            color_code (_type_): The color value to darken.
            level (_type_): The lower level, the darker.

        Returns:
            color_code: The darkened color value.
        """
        red = int('0x'+color_code[1:3],16) - (4-level)*30
        blue = int('0x'+color_code[3:5],16) - (4-level)*30
        green = int('0x'+color_code[5:7],16) - (4-level)*30
        red = max(red, 0)
        blue = max(blue, 0)
        green = max(green, 0)
        red = hex(red).replace('0x', '')
        blue = hex(blue).replace('0x', '')
        green = hex(green).replace('0x', '')
        if len(red) == 1:
            red = '0'+red
        if len(blue) == 1:
            blue = '0'+blue
        if len(green) == 1:
            green = '0'+green
        return '#'+red+blue+green


    def draw_cloud(self, table=None, cloud_tag='first'):
        """Generates a cloud using the Node class and draws it onto the previously generated canvas.

        Args:
            table (_type_, optional): If a cloud table is given,
            the function draws the specified cloud onto the canvas instead of generating a new one.
            Defaults to None.
        """
        canvas, neighbor_color, self.animation_options['loading_text'], scale = (
            self.pages['editor_screen']['canvas'][-1],
            {
                1: self.darken_color(self.animation_options['color'], 1),
                2 : self.darken_color(self.animation_options['color'], 2),
                3 : self.darken_color(self.animation_options['color'], 3)
                },
            None,
            [int(self.cloud_options['height'].get()),int(self.cloud_options['width'].get())]
            )
        if not table:
            table, self.frame_update = ([], True)
            for _ in range(0,int(self.cloud_options['height'].get())):
                table.append([None]*int(self.cloud_options['width'].get()))
            Node(
                [int(self.cloud_options['height'].get())//2,
                int(self.cloud_options['width'].get())//2],
                table
                )
        scale.sort()
        if cloud_tag == 'first':
            canvas.delete('all')
            self.project_options['table'] = table
        for row_index, row in enumerate(table):
            for node_index, node in enumerate(row):
                if not node:
                    continue
                if len(node.neighbors) not in neighbor_color:
                    cloud_color=self.animation_options['color']
                else:
                    cloud_color=neighbor_color[len(node.neighbors)]
                canvas.create_rectangle(
                    (node_index+1)*800//scale[1],
                    (row_index+1)*800//scale[1],
                    (node_index+2)*800//scale[1],
                    (row_index+2)*800//scale[1],
                    outline=cloud_color,
                    fill=cloud_color,
                    tags = cloud_tag
                    )
        if cloud_tag != 'first' and self.frame_update:
            self.animation_options['loading_text'] = canvas.create_text(
                    100,
                    100,
                    font=("calibri", 16),
                    text="Generating frames..."
                    )
            canvas.tag_raise(self.animation_options['loading_text'])


class Widget:
    """This class is used to simplify the creation of widgets for the GUI
    """
    def __init__(self, palette):
        """Initializes the color palette used in the GUI

        Args:
            palette: A python dictionary containing colorvalues as hex form.
        """
        self.palette = palette
    def textbox(self,frame):
        """This function is used to generate an entry widget with predefined attributes.

        Args:
            frame: The master frame of the entry widget.

        Returns:
            textbox: The created entry widget.
        """
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
    def label(self,frame, text, size = 15):
        """This function is used to generate a label widget with predefined attributes.

        Args:
            frame: The master frame of the label widget.
            text: The text the label will display.
            size (int, optional): The font size. Defaults to 15.

        Returns:
            label: The generated label.
        """
        label = tk.Label(
            frame,
            fg = self.palette['bg_tb_color'],
            bg = self.palette['bg_color'],
            text = text,
            font=('calibri', size)
            )
        return label
    def button(self,frame,text=None,size=15,command=None):
        """This function generates a button widget with predefiend attributes.

        Args:
            frame: The master frame of the generated button.
            text: (optional) The text displayed on the button. Defaults to None
            size (int, optional): The font size. Defaults to 15.
            command (optional): The command executen when the button is pressed. Defaults to None.

        Returns:
            button: The generated button.
        """
        button = tk.Button(
            frame,
            padx=2,
            fg = self.palette['button_ft_color'],
            bg = self.palette['button_color'],
            activeforeground = self.palette['button_color'],
            activebackground = self.palette['button_ft_color'],
            font=('calibri', size),
            text = text,
            command = command
            )
        return button
    def canvas(self,frame=None):
        """This function is used to generate canvas widget with predefined attributes.

        Args:
            frame (_type_, optional): The master frame of the generated widget. Defaults to None.

        Returns:
            canvas: The generated canvas.
        """
        canvas = tk.Canvas(
            frame,
            bg=self.palette['button_color']
            )
        canvas.pack(
            expand = True,
            fill = 'both'
            )
        return canvas
    def border(self, main_frame):
        """This function uses predefined attributes to generates a frame widget,
        which acts as a cosmetic border.

        Args:
            main_frame: The master frame of the generated widget.

        Returns:
            border: The generated border
        """
        border = tk.Frame(
            main_frame,
            bg=self.palette['bg_tb_color'],
            width=3)
        border.pack(side='left', fill='y')
        return border
    def frame(self, main_frame):
        """This function generates a frame widget with predefined attributes

        Args:
            main_frame: The master frame of the widget

        Returns:
            frame: The generated frame
        """
        frame = tk.Frame(
            main_frame,
            bg=self.palette['bg_color']
            )
        return frame
    def link(self,frame, text, gui, size = 15):
        """This function is used to generate a button widget, which functions as a link.

        Args:
            frame: The master frame of the label widget.
            text: The text the label will display.
            gui: The GUI object, used to access the save_project function.
            size (int, optional): The font size. Defaults to 15.

        Returns:
            label: The generated label.
        """
        label = tk.Button(
            frame,
            fg = self.palette['bg_tb_color'],
            bg = self.palette['bg_color'],
            activebackground=self.palette['bg_color'],
            activeforeground=self.palette['button_color'],
            bd = 0,
            highlightthickness= 0,
            text = text,
            font=('calibri', size),
            wraplength=150,
            command= lambda: gui.save_project(text)
            )
        return label
