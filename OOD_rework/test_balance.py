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
from assets import StaticScreens
import ai

class BalanceTest(unittest.TestCase):
    
    def test_main_loop_runs_and_breaks(self):
        with patch('datamanager.DataManager.take_control') as myDM:
            myDM.return_value = None
            game = Balance()
            game.run()
            myDM.assert_called_once()
                
class DMTest(unittest.TestCase):
    
    def test_dm_activity_loop(self):
        with patch('datamanager.DataManager._screen') as screen:
            screen.get_command.return_value = ai.STARTER_QUIT_GAME
            dm = DataManager.get_starting_dm()
            result = dm.take_control()
            screen.load_template.assert_called()
            screen.get_command.assert_called()
            screen.present.assert_called()
            assert result == None

class ScreenTest(unittest.TestCase):
    
    def test_load_template(self):
        screen = Screen()
        screen.load_template(**StaticScreens.tester)
        self._check_pixels(screen,[(0,0,'a',176)])
        
    def test_present(self):
        assert 1==0
        
    def test_get_command(self):
        assert 1==0
    
    def test_calls_console(self):
        assert 1==0
        
    def test_calls_console_only_for_changes(self):
        assert 1==0
        
    def test_does_not_call_console_when_no_changes(self):
        assert 1==0
    
    def test_set_pixel(self):
        screen = Screen()
        screen.load_template(**StaticScreens.tester)
        ## Full call test
        screen.set_pixel(x=0,y=0,char='z',fore='b',back='m')
        self._check_pixels(screen,[(0,0,'z',193)])
        ## New pixel test
        screen.set_pixel(x=1,y=0,char='a')
        self._check_pixels(screen,[(0,0,'z',193),(1,0,'a',
                                                  Screen._default_fore+ \
                                                  16*Screen._default_back)],
                            check_size=2)
        ## Exceptions test
        with self.assertRaises(ValueError):
            screen.set_pixel(x=0,char='z',fore='b',back='m')
        with self.assertRaises(ValueError):
            screen.set_pixel(y=0,char='z',fore='b',back='m')
        with self.assertRaises(ValueError):
            screen.set_pixel(x=0,y=0,char='z',fore='z',back='m')
        with self.assertRaises(ValueError):
            screen.set_pixel(x=0,y=0,char='z',fore='a',back='z')
        ## Test set fore only
        screen.set_pixel(x=0,y=0,fore='c')
        self._check_pixels(screen,[(0,0,'z',194)])
        ## Test set back only
        screen.set_pixel(x=0,y=0,back='n')
        self._check_pixels(screen,[(0,0,'z',210)])
        ## Test set char only
        screen.set_pixel(x=0,y=0,char='B')
        self._check_pixels(screen,[(0,0,'B',210)])
        ## Test delete pixel
        screen.set_pixel(x=0,y=0)
        self._check_pixels(screen,[(1,0,'a',
                                    Screen._default_fore+ \
                                    16*Screen._default_back)])
        
    def _check_pixels(self,screen,expected,check_size=1):
        pixels = []
        stream = screen._get_pixels()
        for i in range(check_size):
            pixels.append(next(stream))
        assert pixels == expected
        
    def test_raise_on_bad_input(self):
        screen = Screen()
        screen.load_template(chars='\n'*24)
        assert isinstance(screen,Screen)
        with self.assertRaises(ValueError):
            screen.load_template(chars='\n'*25)
        screen.load_template(chars='a'*79)
        assert isinstance(screen,Screen)
        with self.assertRaises(ValueError):
            screen.load_template(chars='a'*80)
        with self.assertRaises(ValueError):
            screen.load_template(fores='pq')
        with self.assertRaises(ValueError):
            screen.load_template(fores='-')
        with self.assertRaises(ValueError):
            screen.load_template(backs='pq')
        with self.assertRaises(ValueError):
            screen.load_template(backs='-')
        

class GameDataTest(unittest.TestCase):
    pass

class GameObjectTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
