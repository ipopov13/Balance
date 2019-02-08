# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:00:45 2019

GameObject factories for the Balance rogue-like RPG

Called by the World to create all game objects.

Game objects implement .present() and .act(), and can give requests for
new objects to their controller. Their data is changed by the game
logic in the controller.

How do they choose their actions?

@author: IvanPopov
"""


class GameObject:
    
    def present(self):
        """
        Return a default presentation dictionary
        
        This returns a blank space and should be overridden by
        visible subclasses.
        """
        return {'character':' ', 'style':0}
    
    def act(self):
        """
        Choose an action for the object
        
        This should be overridden by active subclasses.
        """
        return None


class Being(GameObject):
    """
    Covers all active actors in the game
    """
    def __init__(self,player_choices):
        """
        Create a Being with the set parameters
        """
        pass


class Item(GameObject):
    pass


class Environment(GameObject):
    pass


class Effect(Environment):
    pass


class Terrain(Environment):
    pass