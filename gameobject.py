# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:00:45 2019

GameObject factories for the Balance rogue-like RPG

Called by the handlers to create all game objects.

Each subfamily has a metaclass that handles automatic registration of
 subclasses and loading from the ini files.

@author: IvanPopov
"""
import config


class GameObject:
    
    @classmethod
    def register_subclass(cls,subcls):
        if subcls.id_ in cls._subs:
            raise ValueError('Subclass id repeats twice: {subcls.id_}!')
        cls._subs[subcls.id_] = subcls
    
    @classmethod
    def get_instance(cls,id_=None):
        try:
            return cls._subs[id_]()
        except KeyError:
            raise ValueError(f'Subclass not specified correctly, got "{id_}", '
                             'but {cls} does not have that subclass.')


class Being(GameObject):
    """
    Covers all active actors in the game
    """
    def __init__(self):
        """
        Create a Being of the specified type. Specified in subclasses.
        """
        pass
        
    def get_stat(self,stat=None):
        """Return the current level of a stat"""
        try:
            return self._stats[stat]['current']
        except KeyError:
            raise ValueError(f'Bad stat identifier: "{stat}".')
            
    def change_stat(self,stat=None,amount=None):
        """Safely change the current level of a stat"""
        if stat is None or amount is None:
            raise TypeError(f'Stat or amount not set: stat"{stat}",'
                            f'amount"{amount}".')
        new_stat_level = self._stats[stat]['current'] + amount
        if self._stats[stat]['min'] \
           <= new_stat_level \
           <= self._stats[stat]['max']:
            self._stats[stat]['current'] += amount
        else:
            raise ValueError(f'Stat would go out of bounds: stat:"{stat}",'
                             f'amount:"{amount}".')


class PlayableCharacter(Being):
        
    def __init__(self):
        self._stats = {}
        stats = config.get_config(section='character_template')
        for stat in stats:
            self._stats[stat.name] = config.simplify(stat)
        load available modifiers AT_START_OF_GAME!
        

class Item(GameObject):
    pass


class Environment(GameObject):
    pass


class RegistrableEnvMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if bases != (Environment,):
            bases[-1].register_subclass(cls)
        else:
            cls.load_subs()
        return cls
    

class Effect(Environment, metaclass=RegistrableEnvMeta):
    _subs = {}
    
    @classmethod
    def load_subs(cls):
        pass


class Terrain(Environment, metaclass=RegistrableEnvMeta):
    _subs = {}
    
    @classmethod
    def load_subs(cls):
        for terrain in config.get_config(section='terrains'):
            class NewTerrain(cls):
                id_ = terrain.name
                char  = terrain['char']
                type_  = terrain['type']
                style = terrain.getint('style')
                spawned_creature = terrain['spawned_creature']
                tire_move = terrain.getint('tire_move')
                tire_stay = terrain.getint('tire_stay')
                creates_context = terrain.getboolean('creates_context')
                passable_for_types = eval(terrain['passable_for_types'])
                single_char_id  = terrain['id']
                asset  = terrain['asset']


class Theme(Environment, metaclass=RegistrableEnvMeta):
    _subs = {}
    
    @classmethod
    def load_subs(cls):
        for theme in config.get_config(section='themes'):
            if theme['terrains']:
                class NewTheme(cls):
                    id_ = theme.name
                    theme_breakpoints = eval(theme['theme_level_breakpoints'])
                    terrain_distribution = eval(theme['terrain_distribution'])
                    modifiers = eval(theme['modifiers'])
                    mod_thresholds = eval(theme['mod_thresholds'])
                    terrains = eval(theme['terrains'])
    
    @classmethod
    def get_structures(cls, themes):
        pass
    
    @classmethod
    def get_terrains(cls, themes, num=0):
        return [Terrain.get_instance(id_='dirt')]*num