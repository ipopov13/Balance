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

class ViewTest(unittest.TestCase):
    
    def test_take_control_calls_UI(self):
        myUI = mock.Mock()
        myUI.present.return_value = view.END_GAME
        current_view = view.View(myUI)
        current_view.take_control(None)
        myUI.present.assert_called_once_with([])
    
    def test_returns_message(self):
        myUI = mock.Mock()
        myUI.present.return_value = view.END_GAME
        current_view = view.View(myUI)
        message = current_view.take_control(None)
        assert message ==view.END_GAME

class BalanceTest(unittest.TestCase):
    
    def test_main_loop_runs_and_breaks(self):
        with patch('view.SceneView.take_control') as myVC:
            with patch('balanceui.UserInterface.present') as myUI:
                myVC.return_value = view.END_GAME
                myUI.return_value = view.GET_SCENE_VIEW
                game = Balance()
                run = game.run()
                myVC.assert_called_once()
                assert run == view.END_GAME

if __name__ == '__main__':
    unittest.main()
