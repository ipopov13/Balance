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

class BalanceTest(unittest.TestCase):
    
    def test_main_loop_runs_and_breaks(self):
        with patch('datamanager.DataManager.take_control') as myDM:
            myDM.return_value = None
            game = Balance()
            game.run()
            myDM.assert_called_once()
                
class DMTest(unittest.TestCase):
    
    def test_dm_calls_console_and_gets_command(self):
        with patch('datamanager.DataManager._console') as console:
            command = 'command'
            console.getchar.return_value = command
            dm = DataManager.get_starting_dm()
            result = dm.take_control()
            console.text.assert_called_with(0,0,'a',7)
            assert result == command

class GameDataTest(unittest.TestCase):
    pass

class GameObjectTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
