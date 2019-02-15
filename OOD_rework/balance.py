# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 10:06:51 2019

Main instance for the Balance rogue-like RPG

Balance is a View manager. It calls the View initializer function
 prepare_views() and serves the game data to the next View in the
 queue, starting with the StarterView if no message is available.
 If a View returns END_GAME the loop breaks.
 
Requirements:
    After receiving a correct command it gives control to the called View
    After receiving a wrong command it raises ValueError
    After receiving END_GAME it breaks out

@author: IvanPopov
"""
import view


class Balance:
    
    def __init__(self):
        self._views = view.prepare_views()
        self._message = view.GET_STARTING_VIEW
        self._game_data = {}
        
    
    def run(self):
        """
        Call the next required View to action, then resolve the
        returned message by calling another View or ending the game.
        """
        while self._message in self._views:
            self._message = self._views[self._message].take_control(
                self._game_data
                )
        return self._message


if __name__ == '__main__':
    game=Balance()
    _ = game.run()