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
import config

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
        self._theme_peaks = {}
        self._themes = config.get_themes()
        self._settings = config.get_world_settings()
        self._rows = self._settings.getint('size')
        self._columns = self._rows * (2 if \
                                self._settings.getboolean('is_globe') else 1)
    
    def start(self,*,race=None):
        """Initialize the world instance"""
        # Start a player character
        self._controlled_being = gameobject.PlayableRace.get_being(race=race)
        # Generate theme peak points
        self._generate_theme_peaks()
        
    def _generate_theme_peaks(self):
        self._theme_peaks = {}
        peak_density = self._themes['DEFAULT'].getint('peak_rarity')
        peak_min = self._themes['DEFAULT'].getint('peak_minimum')
        for x in range(0,self._rows,peak_density):
            for y in range(0,self._columns,peak_density):
                spot = random.randint(0,peak_density**2-1)
                actual_x = x + (spot % peak_density)
                actual_y = y + (spot // peak_density)
                theme = random.choice(self._themes.sections())
                level = random.randint(peak_min,100)
                self._theme_peaks[(actual_x,actual_y)] = {theme:level}
        
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