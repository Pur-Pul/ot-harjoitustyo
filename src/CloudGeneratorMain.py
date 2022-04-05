import tkinter as tk

'''
    Color values
    Background color: #404040
    Background text and border color: #212121
    Button color: #3D6DFF
    Button frame and text color: #004A99
    Textbox color: #515151
    Textbox frame and text color #2D2D2D
'''

def createGUI(frameCount, windowSize):
    #creation of main window, frame and border
    window = tk.Tk()
    window.geometry(str(windowSize)+'x'+str(windowSize)) 
    borderFrame = tk.Frame(window, bg='#212121')
    mainFrame = tk.Frame(borderFrame, bg='#404040')

    '''
    #configure grid
    tk.Grid.rowconfigure(mainFrame,0,weight=1)
    for i in range(0, frameCount):
        if i==0:
            tk.Grid.columnconfigure(mainFrame,i,weight=1)

        else:
            tk.Grid.columnconfigure(mainFrame,i,weight=3)'''
    
    #creation of frames and borders
    frames = []
    borders = []
    for i in range(0, frameCount):
        borders.append(None)
        if i!=0:
            borders[i]=(tk.Frame(mainFrame, bg="#212121", width=3))
            borders[i].pack(side='left', fill='y')
            frames.append(tk.Frame(mainFrame, bg="#404040"))
            frames[i].pack(side='left', expand=True,  fill='both')
        else:
            frames.append(tk.Frame(mainFrame, bg="#404040", width=150))
            frames[i].pack(side='left', fill='y')
    #Creation of labels
    labels=[]
    for i in range(0, len(frames)):
        labels.append([])
        if i == 0:
            label = tk.Label(frames[i], fg = '#212121', bg='#404040', text = 'Projects', font=('calibri', 20))
            label.place(anchor='n', relx=0.5, rely=0)
            labels[i].append(label)
        if i == 1:
            label = tk.Label(frames[i], fg = '#212121', bg='#404040', text = 'CloudGenerator', font=('calibri', 50))
            label.place(x=100, y=50)
            labels[i].append(label)
    
    #Creation of textbox
    textBoxes=[]
    for i in range(0, len(frames)):
        textBoxes.append([])
        if i == 1:
            textBox = tk.Entry(frames[i], fg = '#004A99', bg='#3D6DFF', highlightcolor='#004A99', font=('calibri', 25), width=50, exportselection = 0, bd=0)
            textBox.place( anchor='s', x=885, y=400)
            textBoxes[i].append(textBox)
    #initiation of mainloop
    mainFrame.pack(fill='both', expand=True, padx=3,pady=3)
    borderFrame.pack(fill='both', expand=True)
    window.mainloop()

createGUI(2, 500)
