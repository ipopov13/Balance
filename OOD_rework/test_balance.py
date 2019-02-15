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
import view
import datamanager

class BalanceTest(unittest.TestCase):
    
    def test_main_loop_runs_and_breaks(self):
        with patch('view.StarterView.take_control') as myVC:
            myVC.return_value = datamanager.END_GAME
            game = Balance()
            run = game.run()
            myVC.assert_called_once()
            assert run == datamanager.END_GAME
                
    
class ViewTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        class TestView(view.View):
            
            def _post_init(self):
                self._getter_message = 'testing view'
                self._dm = datamanager.DataManager()
        
            def _update_screen(self,game_data):
                pass
        
        cls.test_view = TestView()
        
    @classmethod
    def tearDownClass(cls):
        del(cls.test_view)
    
    def test_returns_message(self):
        message = self.test_view.take_control(None)
        assert message == datamanager.END_GAME
        
    def test_calls_console(self):
        with patch('view.View._console') as myConsole:
            self.test_view.take_control(None)
            assert myConsole.method_calls != []
            
    def test_calls_dm_update_data(self):
        with patch('datamanager.DataManager.update_data') as myDM:
            myDM.return_value = datamanager.END_GAME
            self.test_view.take_control(None)
            myDM.assert_called_once()
        
    ## TODO: Test subclasses conform to View interface
    
class DMTest(unittest.TestCase):
    pass
## TODO: test starting dms (load and new game) fully init game data?
    #It's probably gameData's responsibility
    ## TODO: Test dms raise an error when no commands (None?)are received
    ## TODO: Test dms return the correct view code when asked
    ## TODO: this doesnt change game data ^^^
    ## TODO: Test that any other message changes game data in some way

if __name__ == '__main__':
    unittest.main()
