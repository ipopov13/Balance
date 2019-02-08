"""
Created on Wed Feb  6 09:41:53 2019

Balance rogue-like RPG

Main instance

@author: IvanPopov
"""
import controllers as con


class Balance:
    
    def __init__(self):
        self._pc = con.PlayerController()
        self._state = con.GAME_IS_RUNNING
        
    def main_loop(self):
        """Run the game until finished"""
        while self._state != con.GAME_IS_OVER:
            self._state = self._pc.run()

    
if __name__ == '__main__':
    game=Balance()
    game.main_loop()