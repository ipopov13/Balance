# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:41:01 2019

Scene manages initial (randomized, except for the player character)
placement of objects and makes access to them easy (ordered by coords
and layer(being, item, terrain, effect, in that order!).

Views are constructed from interface elements. Views control the
placement of interface elements.

Interface elements are constructed from presentables. They set
constraints and order (size of the element, placement of the
presentables inside).

Presentables are just windows into the data of the game. They control
their own visualization (text and color).

@author: IvanPopov
"""     

class Scene:
    def __init__(self,objects):
        pass
        

class View:
    
    def __init__(self,being):
        pass
        
        
class CharacterView(View):
    pass