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
import constants as const

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
        self._settings = config.simplify(config.get_settings(key='world'))
        self._rows = self._settings['size']
        self._columns = self._rows * (2 if \
                                self._settings['is_globe'] else 1)
        self._current_scene_key = None
        self._scenes = {}
        
    @property
    def player(self):
        return self._controlled_being
    
    def start(self):
        """Initialize the world instance"""
        self._generate_theme_peaks()
        self._set_starting_coords()
        self._scenes = {}
        self._ready_scene()
        self.current_scene.insert_being(being=self._controlled_being)
        
    def _ready_scene(self,coords=None):
        if coords is None:
            coords = self._current_scene_key
        if coords not in self._scenes:
            themes = self._calculate_themes(coords)
            self._scenes[coords] = Scene(themes)
        
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
            if theme['distribution'] != const.PEAKS:
                continue
            peak_distance = min(self._rows,
                                theme.getint('average_peak_distance'))
            peak_min = theme.getint('peak_minimum')
            peak_max = theme.getint('peak_maximum')
            for x in range(0,self._columns,peak_distance):
                for y in range(0,self._rows,peak_distance):
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
            if theme['distribution'] != const.PEAKS:
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
    
    def _change_coords(self,direction=None):
        directions = {const.GOING_SOUTH:(0,1),const.GOING_WEST:(-1,0),
                      const.GOING_EAST:(1,0),const.GOING_NORTH:(0,-1),}
        x,y = self._current_scene_key
        x = x + directions[direction][0]
        y = y + directions[direction][1]
        keep_scene_y = False
        if not self._settings['is_globe']:
            x = max(0,x)
            x = min(x,self._columns)
            y = max(0,y)
            y = min(y,self._rows)
        else:
            if y == -1:
                y = 0
                x += self._columns//2
                keep_scene_y = True
            elif y == self._rows:
                y = self._rows-1
                x += self._columns//2
                keep_scene_y = True
            if x == -1:
                x = self._columns-1
            elif x >= self._columns:
                x -= self._columns
        return ((x,y), keep_scene_y)
    
    def move_player(self,direction):
        """
        Change the position of the player in the scene & world
        
        Returns True if the scene changed and needs refreshing
        """
        move = self.current_scene.move_being(direction=direction,
                                             being=self.player)
        if move is not const.SUCCESSFUL:
            new_coords,keep_scene_y = self._change_coords(direction=move)
            if new_coords == self._current_scene_key:
                return False
            self._ready_scene(new_coords)
            player_position = \
                self.current_scene.remove_being(self.player,
                                                direction=move,
                                                keep_y=keep_scene_y)
            self._current_scene_key = new_coords
            self.current_scene.insert_being(being=self.player,
                                            coords=player_position)
            return True
        else:
            return False
        
        
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
        structures = gameobject.Terrain.get_structures(themes)
        self._set_structures(structures)
        empty_spots = self._width*self._height - len(self._tiles)
        terrains = gameobject.Terrain.generate_terrains(themes,num=empty_spots)
        self._lay_terrains(terrains)
        
    def _set_structures(self,structures):
        pass
    
    def _lay_terrains(self,terrains):
        for x in range(self._width):
            for y in range(self._height):
                if (x,y) not in self._tiles:
                    terrain = random.randint(0,len(terrains)-1)
                    self._tiles[(x,y)] = Tile(terrains.pop(terrain))
    
    def insert_being(self,being=None,coords=None):
        """
        Place being as close to coords as possible based on
        terrain passability.
        """
        if being is None:
            raise ValueError("No being passed to scene!")
        if being in self._beings:
            raise ValueError(f"Duplicate being in scene! {being}")
        if coords is None:
            x = self._width//2
            y = self._height//2
            self._tiles[(x,y)].being = being
            self._beings[being] = (x,y)
        else:
            if self._are_valid(coords):
                self._tiles[coords].being = being
                self._beings[being] = coords
            else:
                raise ValueError("Invalid coords for being insertion:"
                                 f" {coords}")
    
    def move_being(self,*,being=None,direction=None):
        """
        Reassign being coordinates and tile
        
        Returns success or a direction for the World to handle
        """
        old_coords = self._beings[being]
        new_coords = self._change_coords(coords=old_coords,direction=direction)
        if self._are_valid(new_coords):
            self._beings[being] = new_coords
            self._tiles[old_coords].being = None
            self._tiles[new_coords].being = being
            return const.SUCCESSFUL
        else:
            return self._compass(new_coords)
                
    def remove_being(self,being=None,direction=None,keep_y=False):
        """
        Remove a being and returns its last position
        
        If a travel direction is given modify the position for correct
        insertion into the next scene.
        """
        if being is None:
            raise ValueError("Cannot call remove_being with no being!")
        try:
            coords = self._beings.pop(being)
        except KeyError:
            raise ValueError(f"Unknown being to remove:{being}")
        self._tiles[coords].being = None
        x,y = coords
        if direction is not None:
            if x == 0 and direction == const.GOING_WEST:
                x = self._width-1
            elif x == self._width-1 and direction == const.GOING_EAST:
                x = 0
            if y == 0 and direction == const.GOING_NORTH and not keep_y:
                y = self._height-1
            elif y == self._height-1 and direction == const.GOING_SOUTH \
                and not keep_y:
                y = 0
        return (x,y)
                
    def _are_valid(self,coords):
        x,y = coords
        return 0<=x<self._width and 0<=y<self._height
            
    def tiles(self):
        return self._tiles.items()
    
    def _change_coords(self,*,coords=None,direction=None):
        directions = {const.GO_SW:(-1,1), const.GO_S:(0,1), const.GO_SE:(1,1),
                      const.GO_W: (-1,0), const.STAY:(0,0), const.GO_E: (1,0),
                      const.GO_NW:(-1,-1),const.GO_N:(0,-1),const.GO_NE:(1,-1)}
        x,y = coords
        x = x + directions[direction][0]
        y = y + directions[direction][1]
        return (x,y)
    
    def _compass(self,coords):
        x,y = coords
        if x<0 and y>=0:
            return const.GOING_WEST
        elif x>=0 and y<0:
            return const.GOING_NORTH
        elif x<0 and y<0:
            return const.GOING_NORTH
        elif x>=self._width:
            return const.GOING_EAST
        elif y>=self._height:
            return const.GOING_SOUTH
    

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
        if not (hasattr(terrain,'char') and hasattr(terrain,'style')):
            raise AttributeError("Bad terrain object supplied to tile:"
                                 f" {terrain}.")
        self._terrain = terrain
        self._being = None
        self._pixel = None
        
    @property
    def being(self):
        return self._being
    
    @being.setter
    def being(self,value):
        if value is not None and self._being is not None:
            raise ValueError("Tile is already occupied!")
        self._being = value
        try:
            self._pixel.update(self.data)
        except AttributeError:
            pass
        
    @property
    def pixel(self):
        return self._pixel
    
    @pixel.setter
    def pixel(self,pixel):
        if not hasattr(pixel,'update'):
            raise AttributeError("Attached object cannot be updated!")
        self._pixel = pixel
        self._pixel.update(self.data)
        
    @property
    def data(self):
        return {'text':self.char,'style':self.style}
        
    @property
    def char(self):
        if self.being is not None:
            return self.being.char
        elif self._terrain is not None:
            return self._terrain.char
        else:
            raise ValueError("Tile has no terrain to present!")
        
    @property
    def style(self):
        if self.being is not None:
            return self.being.style
        elif self._terrain is not None:
            return self._terrain.style
        else:
            raise ValueError("Tile has no terrain to present!")