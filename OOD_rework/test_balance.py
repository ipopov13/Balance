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
import controllers as con

class BalanceTest(unittest.TestCase):
    
    def test_main_loop_runs(self):
        with patch('controllers.PlayerController.run') as myPC:
            myPC.return_value = con.GAME_IS_OVER
            game = Balance()
            game.main_loop()
            myPC.assert_called_once()

if __name__ == '__main__':
    unittest.main()
