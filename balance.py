# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 10:06:51 2019

Main instance for the Balance rogue-like RPG
 
Requirements:
    Calls take_control() of the current DM.

@author: IvanPopov
"""
import os
from glob import glob
import json

class Balance:
    
    @classmethod
    def get_games(cls):
        """List available games and change the config accordingly"""
        games = glob('./*/design/game_settings.txt')
        names = []
        for g in games:
            with open(g) as infile:
                settings = json.load(infile)
                names.append((settings['name'],os.path.dirname(g)))
        choice = input('Select game to run:\n%s\n' %('\n'.join(['%d) %s' %(i,game[0]) for i,game in enumerate(names)])))
        game_path = names[int(choice)][1]
        with open('config.py') as infile:
            data = infile.readlines()
        for line in range(len(data)):
            if data[line].startswith('game_path ='):
                data[line] = f'game_path = "{game_path}"\n'
        with open('config.py','w') as outfile:
            outfile.write(''.join(data))
    
    def __init__(self):
        ## Delay import until game has been selected
        from datamanager import DataManager
        
        self._dm = DataManager.get_starting_dm()
            
    def run(self):
        """
        Call DMs to action in sequence until no DM is available.
        """
        while self._dm is not None:
            self._dm = self._dm.take_control()


if __name__ == '__main__':
    Balance.get_games()
    game=Balance()
    game.run()
    os._exit(0)