# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:00:45 2019

GameObject factories for the Balance rogue-like RPG

Called by the handlers to create all game objects.

Each subfamily has a metaclass that handles automatic registration of
 subclasses and loading from the ini files.

Game objects implement .present(). Their data is changed by the game
logic in the handlers.

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
    
    def present(self):
        """
        Return a default presentation dictionary
        
        This returns a blank space and should be overridden by
        visible subclasses.
        """
        return {'char':' ', 'style':0}


class Being(GameObject):
    """
    Covers all active actors in the game
    """
    def __init__(self):
        """
        Create a Being of the specified type. Defined in subclasses.
        """
        pass
        
    def get_stat(self,stat=None):
        """Return the current level of a stat"""
        try:
            return self.stats[stat][0]
        except KeyError:
            raise ValueError(f'Bad stat identifier: "{stat}".')
            
    def change_stat(self,stat=None,amount=None):
        """Safely change the current level of a stat"""
        if stat is None or amount is None:
            raise TypeError(f'Stat or amount not set: stat"{stat}",'
                            f'amount"{amount}".')
        new_stat_level = self.stats[stat][0] +amount
        if self.stats[stat][1] <= new_stat_level <= self.stats[stat][2]:
            self.stats[stat][0] += amount
        else:
            raise ValueError(f'Stat would go out of bounds: stat:"{stat}",'
                             f'amount:"{amount}".')


class RegistrableBeingMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if bases != (Being,):
            bases[-1].register_subclass(cls)
        return cls


class PlayableRace(Being, metaclass=RegistrableBeingMeta):
    _subs = {}
        
    def __init__(self):
        ## Stats format: name->[current,min,max]
        self.stats = {'Str':[5,1,10],'Dex':[5,1,10],'Int':[5,1,10],
                      'Cre':[5,1,10],'Cun':[5,1,10],'Spi':[5,1,10],
                      'Tra':[5,1,10],
                      'stat_pool':[7,0,999]
                      }
        self._post_init()
        
    def _post_init(self):
        """Do race specific modifications here"""
        raise NotImplementedError


class Human(PlayableRace):
    id_ = 'human'
    
    def _post_init(self):
        pass
        

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
        for terrain in config.get_terrains():
            class NewTerrain(cls):
                id_ = terrain.name
                char  = terrain['char']
                style = terrain.getint('style')
                spawned_creature = terrain['spawned_creature']
                tire_move = terrain.getint('tire_move')
                tire_stay = terrain.getint('tire_stay')
                creates_context = terrain.getboolean('creates_context')
                passable_for_types = eval(terrain['passable_for_types'])