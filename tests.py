"""
Created on Thu Jan 31 2018

Unit tests for the Balance game

@author: IvanPopov
"""

import unittest
from game import Game

class GameTest(unittest.TestCase):
    def test_game_loads(self):
        g=Game()
        self.assertEqual(g.c.title(), "Balance")