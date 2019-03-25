# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:42:32 2019

World/Scene/Tile classes for the Balance rogue-like RPG framework

These are the classes that handle gameobjects directly.

World manages Scene coordinates and transitions and keeps&calculates
 theme values worldwide. It also does save/load of the whole game data.
Scene manages area data and terrain placement in a collection of Tiles,
 as well as active tasks that are related to the whole area (like NPCs
 building houses).
Tile manages a list of game objects residing in the same physical
 location in the game.

@author: IvanPopov
"""
from collections import defaultdict
import pickle
from glob import glob
import random

import gameobject
import config

class World:
    """
    Holds all scenes in a (coords):scene dict,
     knows internally which scene is active (current scene key), keeps
     internally the world generation data (points of high forces and
     modifiers) to use when unvisited scenes are required, and the message
     buffer.
    Exposes:
    .start() method for char creation.
    .get_stat() defaulting to controlled char
    .change_stat() defaulting to controlled char
    .current_scene property returning the current active scene
    Game load/save
    """
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
        self._controlled_being = gameobject.PlayableCharacter()
        self._theme_peaks = {}
        self._themes = config.get_config(section='themes')
        self._settings = config.get_settings(key='world')
        self._rows = self._settings.getint('size')
        self._columns = self._rows * (2 if \
                                self._settings.getboolean('is_globe') else 1)
        self._current_scene_key = None
        self._scenes = {}
        
    @property
    def player(self):
        return self._controlled_being
    
    def start(self,*,race=None):
        """Initialize the world instance"""
        self._generate_theme_peaks()
        self._set_starting_coords()
        self._scenes = {}
        self._ready_scene()
        self.current_scene.insert_being(being=self._controlled_being)
        
    def _ready_scene(self,coords=None):
        if coords is None:
            coords = self._current_scene_key
        if coords in self._scenes:
            self._current_scene_key = coords
        else:
            themes = self._calculate_themes(coords)
            self._scenes[coords] = Scene(themes)
        self._scenes[coords].refresh()
        
    def _set_starting_coords(self):
        for theme in self._themes:
            if theme.getboolean('sets_starting_point'):
                break
        self._current_scene_key = \
            random.choice([coords for coords in self._theme_peaks \
                           if theme.name in self._theme_peaks[coords]])
        
    def _generate_theme_peaks(self):
        self._theme_peaks = defaultdict(lambda:{})
        for theme in self._themes:
            if theme['distribution'] != 'peaks':
                continue
            peak_distance = min(self._rows,
                                theme.getint('average_peak_distance'))
            peak_min = theme.getint('peak_minimum')
            peak_max = theme.getint('peak_maximum')
            for x in range(0,self._rows,peak_distance):
                for y in range(0,self._columns,peak_distance):
                    spot = random.randint(0,peak_distance**2-1)
                    actual_x = x + (spot % peak_distance)
                    actual_y = y + (spot // peak_distance)
                    level = random.randint(peak_min,peak_max)
                    self._theme_peaks[(actual_x,actual_y)].update(
                                                            {theme.name:level})
                    
    def _calculate_themes(self,coords):
        x0, y0 = coords
        max_distance = 0
        themes = {}
        theme_gradients = {}
        for theme in self._themes:
            themes[theme.name] = 0
            if theme['distribution'] != 'peaks':
                themes[theme.name] = theme.getint('peak_maximum') - \
                                                theme.getint('peak_maximum') \
                                                / int(self._rows/2) \
                                                * abs(self._rows/2-.5-y0)
                continue
            effective_distance = theme.getint('peak_maximum') \
                                 // theme.getint('gradient')
            max_distance = max(max_distance, effective_distance)
            theme_gradients[theme.name] = theme.getint('gradient')
        for x in range(x0-max_distance, x0+max_distance+1):
            y_delta = max_distance - abs(x0-x)
            for y in range(y0-y_delta, y0+y_delta+1):
                if (x,y) in self._theme_peaks:
                    dist = sum([abs(x0-x),abs(y0-y)])
                    for theme,value in self._theme_peaks[(x,y)].items():
                        effective_value = value - dist*theme_gradients[theme]
                        if effective_value > themes[theme]:
                            themes[theme] = effective_value
        return themes
    
    @property
    def current_scene(self):
        return self._scenes[self._current_scene_key]
        
        
class Scene:
    """
    Scene object:
    The scene keeps theme values and timing information, lists of resident
     beings to be given random positions next time, etc., so that the dict
     of (coords):tile is kept as clean as possible. It will also provide
     access to the tile methods and attributes for passage/visibility/
     opacity. Scene will also get the Terrain objects and add them into
     tiles, then request any thematic structures and place them, along with
     their NPCs, and finally request additional NPC spawns if needed.
    TODO:
    .current_scene_tiles() generator over the tiles for pixel coupling
    """
    
    def __init__(self,themes):
        self._themes = themes
        self._tiles = {}
        self._beings = {}
        settings = config.get_settings(key='scene')
        self._width = settings.getint('width')
        self._height = settings.getint('height')
        structures = gameobject.Theme.get_structures(themes)
        self._set_structures(structures)
        empty_spots = self._width*self._height - len(self._tiles)
        terrains = gameobject.Theme.get_terrains(themes,num=empty_spots)
        self._lay_terrains(terrains)
        
    def _set_structures(self,structures):
        pass
    
    def _lay_terrains(self,terrains):
        for x in range(self._width):
            for y in range(self._height):
                if (x,y) not in self._tiles:
                    terrain = random.randint(0,len(terrains)-1)
                    self._tiles[(x,y)] = Tile(terrains.pop(terrain))
    
    def refresh(self):
        """resetting timed out objects, randomizing positions of
        resident beings, resolving being intentions by changing
        terrain, etc."""
        pass
    
    def insert_being(self,being=None,coords=None):
        """
        Place being as close to coords as possible based on
        terrain passability.
        """
        if being is None:
            raise ValueError("No being passed to scene!")
        if being in self._beings.values():
            raise ValueError(f"Duplicate being in scene! {being}")
        if coords is None:
            x = self._width//2
            y = self._height//2
            self._tiles[(x,y)].being = being
            self._beings[(x,y)] = being
        else:
            self._tiles[coords].being = being
            self._beings[coords] = being
    

class Tile:
    """
    Tiles summarize the group of objects that they contain (intent,
    effect, terrain, item, being).
    
    Tiles should update their pixels proactively when they change, not
    let pixels query them! This way only the pixels that are changed
    will be updated and a huge amount of calls will be saved in the
    screen update as the screen would only need to update its labels!
    """
    
    def __init__(self,terrain):
        self._terrain = terrain
        self._being = None
        
    @property
    def being(self):
        return self._being
    
    @being.setter
    def being(self,value):
        if value is not None and self._being is not None:
            raise ValueError("Tile is already occupied!")
        self._being = value