import unittest
import copy
from CloudGeneratorMain import GUI

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.colorPalette = {'bgColor' : '#404040', 
        'bgTBColor' : '#212121', 
        'buttonColor' : '#3D6DFF', 
        'buttonFTColor' : '#004A99', 
        'textboxColor' : '#515151', 
        'textboxFTColor' : '#2D2D2D'}
        self.newGUI = GUI(self.colorPalette)

    def test_constructor_assigns_color_values_correctly(self):
        
        
        colors = [None]*6
        colors[0] = self.newGUI.bgColor
        colors[1] = self.newGUI.bgTBColor
        colors[2] = self.newGUI.buttonColor
        colors[3] = self.newGUI.buttonFTColor
        colors[4] = self.newGUI.textboxColor
        colors[5] = self.newGUI.textboxFTColor
        compColors = []
        for i in self.colorPalette:
            compColors.append(self.colorPalette[i])
        self.assertEqual(colors, compColors)
    
    def test_createFrames_creates_correct_amount_frames_and_borders(self):
        results = []
        for i in range(1, 5):
            temp = copy.copy(self.newGUI).createFrames(i, None)
            results.append(len(temp[0], len(temp[1])))
        self.assertEqual(results, [[1,0], [2, 1], [3, 2], [4, 3]])