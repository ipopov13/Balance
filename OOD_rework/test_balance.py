"""
Created on Wed Feb  6 09:41:53 2019

Tests for the Balance rogue-like RPG

@author: IvanPopov
"""
import unittest

#from module import function/object
from balance import Balance

class BalanceTest(unittest.TestCase):
    
    def test_world_creation_message_sent(self):
        ui=unittest.mock.Mock()
        Balance(ui)
        ui.getWorld.assert_called_once()


if __name__ == '__main__':
    unittest.main()
