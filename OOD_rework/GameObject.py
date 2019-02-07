# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:00:45 2019

GameObject abstract class for the Balance rogue-like RPG

@author: IvanPopov
"""


class GameObject:
    pass


class Item(GameObject):
    pass


class Being(GameObject):
    """
    Covers all active actors in the game
    
    Called by the PlayerController at player init, and by SceneView to init 
    other beings in the scene.
    """
    
    def __init__(self,player_choices):
        """
        Create a Being with the set parameters
        """
        self._action=''