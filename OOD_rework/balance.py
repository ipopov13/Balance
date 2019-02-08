"""
Created on Wed Feb  6 09:41:53 2019

Balance rogue-like RPG

Main instance

@author: IvanPopov
"""
from controllers import PlayerController


class Balance:
    
    def __init__(self):
        self._pc = PlayerController()
        self.finished = False
        
    def main_loop(self):
        """Run the game until finished"""
        while not self.finished:
            self.finished = self._pc.run()

    
if __name__ == '__main__':
    game=Balance()
    game.main_loop()