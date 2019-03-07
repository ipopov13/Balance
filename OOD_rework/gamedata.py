# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:42:32 2019

GameData class for the Balance rogue-like RPG

Only instances of GameData can create new GameObjects and contain them.
 The class includes methods for these operations and a rigid structure
 for containing the objects that the users (DataManagers) can rely
 upon.
 
Only DataManagers can call the GameData methods.

Include it as a View class property to isolate from the loop and for
 sharing between Views without passing it every time?
 
Do the Views need access to it? - Probably, they need to be able to
 make screens (their main task), which is not trivial.
 
Game data may need to copy itself in new instances (for loading)?

@author: IvanPopov
"""


def get_empty_data():
    return {'beings':[],
            'items':[],
            'terrains':[],
            'effects':[],
            'message_buffer':[]}