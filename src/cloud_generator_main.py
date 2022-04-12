from graphical_user_interface import GUI


if __name__ == "__main__":
    color_palette = {'bgColor' : '#404040',
                'bgTBColor' : '#212121',
                'buttonColor' : '#3D6DFF',
                'buttonFTColor' : '#004A99',
                'textboxColor' : '#515151',
                'textboxFTColor' : '#2D2D2D'}
    newGUI = GUI(color_palette)
    window  = newGUI.create_gui(800)
    #initiation of mainloop
    window.mainloop()
