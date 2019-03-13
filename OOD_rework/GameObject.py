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


class PlayableRace(Being):
    
    def __init__(self):
        self.stats = {'Str':5,
                      'Dex':5,
                      'Int':5,
                      'Cre':5,
                      'Spi':5,
                      'Tra':5,
                      }
        self.extra_points = 5


class Human(PlayableRace):
    name = 'human'


class Item(GameObject):
    pass


class Environment(GameObject):
    pass


class Effect(Environment):
    pass


class Terrain(Environment):
    pass