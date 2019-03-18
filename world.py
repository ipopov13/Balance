# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:42:32 2019

World class for the Balance rogue-like RPG

Holds all the gameobjects created, all scenes in a (coords):scene dict,
 knows internally which scene is active (current scene key), keeps
 internally the world generation data (points of high forces and
 modifiers) to use when unvisited scenes are required, and the message
 buffer.
Exposes:
.current_scene_tiles() generator over the tiles for pixel coupling
.start() method for char creation.
.get_attribute() defaulting to controlled char
.change_attribute() defaulting to controlled char
Game load/save

@author: IvanPopov
"""
import pickle
from glob import glob
import random
import gameobject

class World:
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
    
    def start(self,*,race=None):
        """Initialize a player character"""
        self._controlled_being = gameobject.PlayableRace.get_being(race=race)
        
    def get_stat(self,stat):
        """Return the stat of a being"""
        return self._controlled_being.get_stat(stat=stat)
        
    def change_stat(self,stat,amount,from_pool=True):
        """Change the stats of the player character"""
        ## If using pool check availability first
        if from_pool:
            try:
                self._controlled_being.change_stat(stat='stat_pool',
                                                   amount=-1*amount)
            except ValueError:
                return
        try:
            ## Try to change stat
            self._controlled_being.change_stat(stat=stat,amount=amount)
        except ValueError:
            ## Reverse any changes made to pool
            if from_pool:
                self._controlled_being.change_stat(stat='stat_pool',
                                                   amount=amount)
            return