"""
Created on Wed Feb  6 09:41:53 2019

Tests for the Balance rogue-like RPG

@author: IvanPopov
"""
import unittest
from unittest import mock
from unittest.mock import patch

#from module import function/object
from balance import Balance
from datamanager import DataManager
from screen import Screen

class BalanceTest(unittest.TestCase):
    
    def test_main_loop_runs_and_breaks(self):
        with patch('datamanager.DataManager.take_control') as myDM:
            myDM.return_value = None
            game = Balance()
            game.run()
            myDM.assert_called_once()
                
class DMTest(unittest.TestCase):
    
    def test_dm_activity_loop(self):
        with patch('datamanager.DataManager._console') as console:
            command = 'command'
            console.getchar.return_value = command
            dm = DataManager.get_starting_dm()
            result = dm.take_control()
            console.text.assert_called()
            assert result == command

class ScreenTest(unittest.TestCase):
    
    def test_set_pixel(self):
        screen = Screen(chars='asd',fores='abcd',backs='lmnop')
        screen.set_pixel(x=0,y=0,char='z',fore='b',back='m')
        stream = screen.get_pixels()
        pixels = next(stream)
        assert pixels == (0,0,'z',193)
        
    def test_get_pixels(self):
        ## Test longer style strings
        screen = Screen(chars='asd',fores='abcd',backs='lmnop')
        stream = screen.get_pixels()
        pixels = []
        for i in range(6):
            pixels.append(next(stream))
        assert pixels == [(0,0,'a',176),(1,0,'s',193),(2,0,'d',210),
                          (3,0,' ',227),(4,0,' ',240),(5,0,' ',0)]
        ## Test longer char strings
        screen = Screen(chars='asdfgh',fores='abcd',backs='lmn')
        stream = screen.get_pixels()
        pixels = []
        for i in range(6):
            pixels.append(next(stream))
        assert pixels == [(0,0,'a',176),(1,0,'s',193),(2,0,'d',210),
                          (3,0,'f',3),(4,0,'g',0),(5,0,'h',0)]
        
    def test_raise_on_bad_input(self):
        screen = Screen(chars='\n'*24)
        assert isinstance(screen,Screen)
        with self.assertRaises(ValueError):
            screen = Screen(chars='\n'*25)
        screen = Screen(chars='a'*79)
        assert isinstance(screen,Screen)
        with self.assertRaises(ValueError):
            screen = Screen(chars='a'*80)
        with self.assertRaises(ValueError):
            screen = Screen(fores='pq')
        with self.assertRaises(ValueError):
            screen = Screen(fores='-')
        with self.assertRaises(ValueError):
            screen = Screen(backs='pq')
        with self.assertRaises(ValueError):
            screen = Screen(backs='-')
        

class GameDataTest(unittest.TestCase):
    pass

class GameObjectTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
