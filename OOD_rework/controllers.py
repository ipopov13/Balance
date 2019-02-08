# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 10:06:51 2019

Player controller class for the Balance rogue-like RPG

PC inits a world (set of params and gameobject data) and a UI and inits
a scene (asking world to create a player character, then the other
objects of the area they reside in, then passing the objects to the
Scene initializer). Then it creates a new View using the scene and
sends it to the UI to display, getting back a command from the player.

On run() the PC instance translates the command, then resolves the
Scene by calling the objects to action in order of initiative and
resolving conflicts, changing objects and fulfilling the intents of
all and potentially requesting more objects (if some object created
a request; the objects are added to the scene with the proper location
that is embedded in the request.) from the world. Then it creates a
new View using the scene and sends it for presentation again.

Alternatively, the PC may respond to the command by generating a new
View based on some object's statistics (usually the player character),
and send it for presenting instead.

@author: IvanPopov
"""
from world import World
from balanceui import UserInterface
from view import Scene

GAME_IS_OVER = True
GAME_IS_RUNNING = False

class PlayerController:
    
    def __init__(self):
        self._ui = UserInterface()
        self._world = World()
        objects = self._world.create_scene_objects(self._ui.get_pc_request())
        self._scene = Scene(objects)
    
    def run(self):
        """
        Display the scene and get a command back
        
        Returns False if the game is still running, True if it ended.
        """
        return GAME_IS_RUNNING