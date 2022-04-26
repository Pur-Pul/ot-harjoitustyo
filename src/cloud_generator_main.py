from graphical_user_interface import GUI


if __name__ == "__main__":
    color_palette = {'bg_color' : '#404040',
                'bg_tb_color' : '#212121',
                'button_color' : '#3D6DFF',
                'button_ft_color' : '#004A99',
                'textbox_color' : '#515151',
                'textbox_ft_color' : '#2D2D2D'}
    newGUI = GUI(color_palette)
    window  = newGUI.create_gui(800)
    #initiation of mainloop
    window.mainloop()
