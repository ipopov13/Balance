# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 10:06:51 2019

Main instance for the Balance rogue-like RPG
 
Requirements:
    Calls take_control() of the current DM.

@author: IvanPopov
"""

from datamanager import DataManager


class Balance:
    
    def __init__(self):
        self._dm = DataManager.get_starting_dm()
            
    def run(self):
        """
        Call DMs to action in sequence until no DM is available.
        """
        while self._dm is not None:
            self._dm = self._dm.take_control()


if __name__ == '__main__':
    game=Balance()
    game.run()