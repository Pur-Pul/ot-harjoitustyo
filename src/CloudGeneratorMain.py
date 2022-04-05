import tkinter as tk


class GUI:
    def __init__(self, colorPalette):
        #Color values
        self.bgColor = colorPalette['bgColor']
        self.bgTBColor = colorPalette['bgTBColor']
        self.buttonColor = colorPalette['buttonColor']
        self.buttonFTColor = colorPalette['buttonFTColor']
        self.textboxColor = colorPalette['textboxColor']
        self.textboxFTColor = colorPalette['textboxFTColor']

    def createFrames(self, frameCount, mainFrame):
        #creation of frames and borders
        frames = []
        borders = []
        for i in range(0, frameCount):
            borders.append(None)
            if i!=0:
                borders[i]=(tk.Frame(mainFrame, bg=self.bgTBColor, width=3))
                borders[i].pack(side='left', fill='y')
                frames.append(tk.Frame(mainFrame, bg=self.bgColor))
                frames[i].pack(side='left', expand=True,  fill='both')
            else:
                frames.append(tk.Frame(mainFrame, bg=self.bgColor, width=150))
                frames[i].pack(side='left', fill='y')
        return [frames,borders]

    def createLabels(self, frames):
        #Creation of labels
        labels=[]
        for i in range(0, len(frames)):
            labels.append([])
            if i == 0:
                label = tk.Label(frames[i], fg = self.bgTBColor, bg=self.bgColor, text = 'Projects', font=('calibri', 20))
                label.place(anchor='n', relx=0.5, rely=0)
                labels[i].append(label)
            if i == 1:
                label = tk.Label(frames[i], fg = self.bgTBColor, bg=self.bgColor, text = 'CloudGenerator', font=('calibri', 50))
                label.place(x=100, y=50)
                labels[i].append(label)
        return labels

    def createTextBoxes(self, frames):
        #Creation of textbox
        textBoxes=[]
        for i in range(0, len(frames)):
            textBoxes.append([])
            if i == 1:
                textBox = tk.Entry(frames[i], fg = self.buttonFTColor, bg=self.buttonColor, highlightcolor=self.buttonFTColor, font=('calibri', 25), width=50, exportselection = 0, bd=0)
                textBox.place( anchor='s', x=885, y=400)
                textBoxes[i].append(textBox)
        return textBoxes

    def createGUI(self, frameCount, windowSize):
        #creation of main window, frame and border
        window = tk.Tk()
        window.geometry(str(windowSize)+'x'+str(windowSize)) 
        borderFrame = tk.Frame(window, bg=self.bgTBColor)
        mainFrame = tk.Frame(borderFrame, bg=self.bgColor)
        
        fb = self.createFrames(frameCount, mainFrame)
        frames = fb[0]
        borders = fb[1]
        labels = self.createLabels(frames)
        textBoxes = self.createTextBoxes(frames)
        
        mainFrame.pack(fill='both', expand=True, padx=3,pady=3)
        borderFrame.pack(fill='both', expand=True)
        return window


if __name__ == "__main__":
    colorPalette = {'bgColor' : '#404040',
                'bgTBColor' : '#212121',
                'buttonColor' : '#3D6DFF',
                'buttonFTColor' : '#004A99',
                'textboxColor' : '#515151',
                'textboxFTColor' : '#2D2D2D'}
    newGUI = GUI(colorPalette)
    window  = newGUI.createGUI(2, 500)

    #initiation of mainloop
    window.mainloop()
