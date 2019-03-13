# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:42:32 2019

GameData class for the Balance rogue-like RPG

Controlled being object: default for character description views and
 control, and the one that is used when the focus being is reset to
 None; Usually the player character
Current scene key: the coords of the current scene object (also a key
 to the object in the seen scenes dict)
Seen scenes: dict (coords: scene object) for maintaining a persistent
 world.
World data: the randomized array of values (or formula for calculating
 them) used to build yet unseen scenes.
Message buffer: List of messages added by the handlers, that have to be
 shown to the player. Fixed length of 100 elements?

@author: IvanPopov
"""
import pickle
from glob import glob
import random
import gameobject

class GameData:
    _game_list = {}
    
    @classmethod
    def save(cls, game):
        """Store the data to file using the controlled being name"""
        filename = game._controlled_being.name+str(random.randint(100,999))
        with open(f'{filename}.bal','wb') as outfile:
            pickle.dump(outfile, game)
    
    @classmethod
    def get_saved_games(cls):
        """Return a list of found saved games and keep it"""
        for f in glob('*.bal'):
            with open(f,'rb') as infile:
                game = pickle.load(infile)
                cls._game_list[game._controlled_being.name] = game
        return cls._game_list
    
    @classmethod
    def load(cls, index):
        """Return the GameData object at that index"""
        return cls._game_list[index]
    
    def __init__(self):
        self._controlled_being = None
        self._current_scene_key = None
        self._scenes = {}
        self._world = {}
        self._message_buffer = []
    
    def start_human(self):
        self._controlled_being = gameobject.Human()
        
    def get_stat(self,stat):
        return self._controlled_being.stats[stat]
        
    def change_stat(self,stat,amount):
        if 0 < self._controlled_being.stats[stat]+amount < 11:
            self._controlled_being.stats[stat] += amount