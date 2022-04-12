import unittest
import copy
from cloud_generator_main import GUI

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.color_palette = {'bgColor' : '#404040', 
        'bgTBColor' : '#212121', 
        'buttonColor' : '#3D6DFF', 
        'buttonFTColor' : '#004A99', 
        'textboxColor' : '#515151', 
        'textboxFTColor' : '#2D2D2D'}
        self.newGUI = GUI(self.color_palette)

    def test_constructor_assigns_color_values_correctly(self):
        
        
        colors = [None]*6
        colors[0] = self.newGUI.bg_color
        colors[1] = self.newGUI.bg_tb_color
        colors[2] = self.newGUI.button_color
        colors[3] = self.newGUI.button_ft_color
        colors[4] = self.newGUI.textbox_color
        colors[5] = self.newGUI.textbox_ft_color
        compColors = []
        for i in self.color_palette:
            compColors.append(self.color_palette[i])
        self.assertEqual(colors, compColors)
    
    def test_create_frames_creates_correct_amount_frames_and_borders(self):
        results = []
        for i in range(0,2):
            if i == 0:
                page = 'creation_screen'
            else:
                page = 'editor_screen'

            temp = copy.copy(self.newGUI).create_frames(page)
            temp2 = []
            for b in temp[1]:
                if b != None:
                    temp2.append(b)
                
            temp[1] = temp2
            results.append([len(temp[0]), len(temp[1])])
            print(results)
        self.assertEqual(results, [[2,1], [3, 2]])