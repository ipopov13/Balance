# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:00:45 2019

GameObject factories for the Balance rogue-like RPG

Called by the handlers to create all game objects.

Game objects implement .present(). Their data is changed by the game
logic in the handlers.

@author: IvanPopov
"""


class GameObject:
    
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
    def __init__(self,player_choices):
        """
        Create a Being with the set parameters
        """
        pass


class RegistrableBeingMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if bases != (Being,):
            bases[-1].register_subclass(cls)
        return cls


class PlayableRace(Being, metaclass=RegistrableBeingMeta):
    _subs = {}
    
    @classmethod
    def register_subclass(cls,race):
        if race.name in cls._subs:
            raise ValueError('Race name repeats twice: {race.name}!')
        cls._subs[race.name] = race
    
    
    @classmethod
    def get_being(cls,race=None):
        try:
            return cls._subs[race]()
        except KeyError:
            raise ValueError(f'Race not specified correctly, got "{race}". {list(cls._subs.keys())}')
        
    def __init__(self):
        self.stats = {'Str':5,'Dex':5,'Int':5,'Cre':5,'Cun':5,'Spi':5,'Tra':5,
                      'stat_p':5
                      }
        self._post_init()
        
    def _post_init(self):
        """Do race specific modifications here"""
        raise NotImplementedError
        


class Human(PlayableRace):
    name = 'human'
    
    def _post_init(self):
        pass


class Item(GameObject):
    pass


class Environment(GameObject):
    pass


class Effect(Environment):
    pass


class Terrain(Environment):
    pass