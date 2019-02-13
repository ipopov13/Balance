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

class BalanceTest(unittest.TestCase):
    
    def test_main_loop_runs_and_breaks(self):
        with patch('view.SceneView.take_control') as myVC:
            with patch('balanceui.UserInterface.present') as myUI:
                myVC.return_value = view.END_GAME
                myUI.return_value = view.GET_DEFAULT_VIEW
                game = Balance()
                run = game.run()
                myVC.assert_called_once()
                assert run == view.END_GAME
                
    
class ViewTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        class TestView(view.View):
            
            def _post_init(self):
                self._getter_message = 'testing view'
    
            def _update_data(self,*,data={},command=''):
                pass
        
            def _update_screen(self,game_data):
                pass
        
        cls.myUI = mock.Mock()
        cls.myUI.present.return_value = view.END_GAME
        cls.test_view = TestView(cls.myUI)
        
    @classmethod
    def tearDownClass(cls):
        del(cls.test_view)
    
    def test_take_control_calls_UI(self):
        self.test_view.take_control(None)
        self.myUI.present.assert_called_with([])
    
    def test_returns_message(self):
        message = self.test_view.take_control(None)
        assert message ==view.END_GAME
        
    ## TODO: Test subclasses conform to View interface

if __name__ == '__main__':
    unittest.main()
