import tkinter as tk
from generation_algorithm import Node
from wind_simulation import simulator
from wind_simulation import print_table

import copy
import time
class GUI:
    def __init__(self, color_palette):
        #Color values
        self.bg_color = color_palette['bgColor']
        self.bg_tb_color = color_palette['bgTBColor']
        self.button_color = color_palette['buttonColor']
        self.button_ft_color = color_palette['buttonFTColor']
        self.textbox_color = color_palette['textboxColor']
        self.textbox_ft_color = color_palette['textboxFTColor']
        self.done=False
        self.table = []
        self.cloud = None

        self.pages = {'creation_screen' :
        {'frame_count' : 2,
            'main_frame' : None},
            'editor_screen' :
        {'frame_count' : 3,
            'main_frame' : None}}

    def create_frames(self, page):
        frame_count = self.pages[page]['frame_count']
        main_frame = self.pages[page]['main_frame']
        #creation of frames and borders
        frames = []
        borders = []
        for i in range(0, frame_count):
            borders.append(None)
            if i!=0:
                borders[i]=(tk.Frame(main_frame, bg=self.bg_tb_color, width=3))
                borders[i].pack(side='left', fill='y')
                if frame_count==3 and i ==1:
                    frames.append(tk.Frame(main_frame, bg=self.bg_color, width = 800))
                else:
                    frames.append(tk.Frame(main_frame, bg=self.bg_color))
                frames[i].pack(side='left', expand=True,  fill='both')
            else:
                frames.append(tk.Frame(main_frame, bg=self.bg_color, width=150))
                frames[i].pack(side='left', fill='y')
        return [frames,borders]

    def create_labels(self, page):
        frames = self.pages[page]['frames']
        #Creation of labels
        labels=[]
        for i, frame in enumerate(frames):
            labels.append([])
            if i == 0:
                label = tk.Label(frame,
                                fg = self.bg_tb_color,
                                bg=self.bg_color,
                                text = 'Projects',
                                font=('calibri', 20))
                label.place(anchor='n',relx=0.5, rely=0)
                labels[i].append(label)
            if i == 1 and page == 'creation_screen':
                label = tk.Label(frame,
                                fg = self.bg_tb_color,
                                bg=self.bg_color,
                                text = 'CloudGenerator',
                                font=('calibri', 50))
                label.place(x=100, y=50)
                labels[i].append(label)
        return labels

    def create_textboxes(self, page):
        frames = self.pages[page]['frames']
        #Creation of textbox
        textboxes=[]
        if page == 'creation_screen':
            for i, frame in enumerate(frames):
                textboxes.append([])
                if i == 1:
                    strv = tk.StringVar(value = 'Enter name of project...')
                    textbox = tk.Entry(frame,
                    fg = self.bg_tb_color,
                    bg=self.textbox_color,
                    highlightcolor=self.textbox_ft_color,
                    highlightbackground = self.textbox_ft_color,
                    highlightthickness = 3,
                    font=('calibri', 25),
                    width=50,
                    exportselection = 0,
                    textvariable = strv)
                    strv.trace("w",
                                lambda name,
                                index,
                                mode,
                                strv=strv: self.clear_textbox(textbox))
                    textbox.place( anchor='s', x=885, y=400)
                    textboxes[i].append(textbox)
        return textboxes
    def create_buttons(self, page):
        frames = self.pages[page]['frames']
        buttons = []
        if page == 'creation_screen':
            buttons.append(tk.Button(frames[1],
                                    command = lambda: self.show('editor_screen'),
                                    text = 'create'))
            buttons[-1].place(anchor='s', x=885, y=500)
        if page == 'editor_screen':
            #Create button
            buttons.append(tk.Button(frames[2],
                                    command = lambda: self.draw_cloud(),
                                    text = 'Generate new cloud'))
            buttons[-1].place(anchor='s', relx=0.5, rely=0.5)
            #Animate button
            buttons.append(tk.Button(frames[2],
                                    command = lambda: self.animate_cloud(20),
                                    text = 'Animate cloud'))
            buttons[-1].place(anchor='s', relx=0.5, rely=0.6)

        return buttons

    def create_canvas(self, page):
        #This is the canvas where the cloud is drawn.
        frames = self.pages[page]['frames']
        canvas = []
        if page == 'editor_screen':
            canvas.append(tk.Canvas(frames[1],
                                    bg=self.button_color,
                                    highlightbackground=self.bg_color,
                                    highlightthickness=10))
            canvas[-1].place(relwidth=1, relheight=1)
        return canvas

    def create_gui(self, window_size):
        pages = self.pages
        #creation of main window, frame and border
        window = tk.Tk()
        self.window = window
        window.geometry(str(window_size)+'x'+str(window_size))
        pages['creation_screen']['main_frame'] = tk.Frame(window,
                                                        bg=self.bg_color,
                                                        highlightbackground=self.bg_tb_color,
                                                        highlightthickness=3)
        pages['editor_screen']['main_frame'] = tk.Frame(window,
                                                        bg=self.bg_color,
                                                        highlightbackground=self.bg_tb_color,
                                                        highlightthickness=3)
        for key, page in pages.items():
            frames_and_borders = self.create_frames(key)
            frames = frames_and_borders[0]
            page['frames'] = frames
            borders = frames_and_borders[1]
            page['borders'] = borders
            labels = self.create_labels(key)
            page['labels'] = labels
            textboxes = self.create_textboxes(key)
            page['textboxes'] = textboxes
            buttons = self.create_buttons(key)
            page['buttons'] = buttons
            canvas = self.create_canvas(key)
            page['canvas'] = canvas
        self.draw_cloud()
        pages['editor_screen']['main_frame'].place(relwidth=1, relheight=1)
        pages['creation_screen']['main_frame'].place(relwidth=1, relheight=1)
        pages['creation_screen']['main_frame'].lift()
        return window

    def show(self, page):
        #Lifts the specified page to the front.
        self.pages[page]['main_frame'].lift()
    def clear_textbox(self, textbox):
        text = textbox.get()
        print('here')
        if 'Enter name of project...' in text and not self.done:
            self.done=True
            textbox.delete(0, 'end')
            text = text.replace('Enter name of project...','')
            print('newtext', text)
            textbox.insert(0, text)

    def animate_cloud(self, frame_count):
        original = self.table
        frame_1 = copy.copy(original)
        window = self.window
        
        for _ in range(0, frame_count):
            new_table = []
            for i in range(0, len(frame_1)):
                new_table.append(copy.copy(frame_1[i]))
            
            new_simulation = simulator(new_table)
            frame_1 = new_simulation.simulate()
            
            self.draw_cloud(frame_1)
            window.update()
            time.sleep(0.01)
        self.draw_cloud(original)
        window.update()
            
            

    
    def draw_cloud(self, table=None):
        if not table:
            
            table = []
            for _ in range(0, 15):
                table.append([None]*40)
            self.cloud = Node([6,11],table)
        canvas = self.pages['editor_screen']['canvas'][-1]
        canvas.delete("all")
        for row_index, row in enumerate(table):
            for node_index, node in enumerate(row):
                if node:
                    outline='white'
                    fill='white'
                    if len(node.neighbors) == 1:
                        outline="#A9A9A9"
                        fill="#A9A9A9"
                    elif len(node.neighbors) == 2:
                        outline="#D3D3D3"
                        fill="#D3D3D3"
                    elif len(node.neighbors) == 3:
                        outline="#E5E4E2"
                        fill="#E5E4E2"
                    elif len(node.neighbors) == 4:
                        outline="white"
                        fill="white"
                    polygon = canvas.create_rectangle( # pylint: disable=unused-variable
                    (node_index+1)*10, (row_index+1)*10, (node_index+2)*10, (row_index+2)*10, outline=outline,
                    fill=fill)

                    

                    
        self.table = table
                    