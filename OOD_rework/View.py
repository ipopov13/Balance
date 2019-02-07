# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:41:01 2019

Views are generated using a specific Being instance and are passed by it into
the World.currentView property for visualization.
Views can be displayed with a standard AvailableViews View. Shortcuts
for the views:
Ctrl+0 : AvailableViews
Ctrl+1 : Scene
Ctrl+2 : CharacterSheet
Ctrl+3 : Inventory
TODO: Ctrl+4, etc. : All other views

All views can be accessed by all beings, but may not have content for them -
they have a default empty version.
Using the shortcuts (that is, changing views) does not move the game time
forward (looking at the information is free). Using a view's specific commands
may cost the player turns.
A View has a list of available commands and sending an unknown one sends back
a message and may expend time (depending on the view properties).

@author: IvanPopov
"""

from gameobject import Being

class PlayerController:
    # The full list of admin commands used for the game
    # (save,load,quit,change view)
    _admin_command_list={}
    
    def __init__(self,player_choices,scene_params):
        self._controlled_being=Being(player_choices)
        self._scene=Scene(self._controlled_being,scene_params)
    
    def process_command(self,command):
        """Check if the command is admin and provide the required View
        subclass instance, or update the current view and return it
        """
        pass
        

class Scene:
    def __init__(self,player,scene_params):
        self._player=player
        

class View:
    
    def __init__(self,being):
        self._owner=being
        
    def update(self,command):
        """Updates the view and returns any emergent extra commands"""
        pass
        
        
class CharacterView(View):
    pass