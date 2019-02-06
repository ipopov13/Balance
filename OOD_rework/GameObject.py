# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:00:45 2019

GameObject abstract class for the Balance rogue-like RPG

@author: IvanPopov
"""

import view

class GameObject:
    pass

class Item(GameObject):
    pass

class Being(GameObject):
    """
    Only called by the world object for player init, and by itself for scene
    contents (other beings in the scene). What is the difference between Player
    and Being? (Or npc and being?)
    """
    # The full list of admin commands used for the game
    # (save,load,quit,change view)
    _admin_command_list={}
    
    def __init__(self,player_choices,location_info=None,scene=None):
        """
        Create a Being with the set parameters
        Either location_info or scene have to be passed, the former
        creating an active character, while the latter 
        Optional scene can be passed for creating NPCs inside a scene owned by
        the player character.
        """
        self._views=self._init_non_scenes()
        self._views['scene']=scene
        self._current_view_key='scene'
        self._action='' #the action that the Being will take this turn
    
    def init_scene_view(self,spot):
        self._views['scene']=view.SceneView(self,spot)
    
    def _init_non_scenes(self):
        """
        Return a dict of all non-scene views initialized with the Being
        """
        return {}
    
    def execute_command(self, command):
        """
        Set the action, update self.currentViewKey, then update the
        corresponding View and return it along with any extra commands.
        """
        self._translate_command(command)
        self._update_view_key()
        additional_commands = self._views[self._current_view_key].update()
        return (additional_commands,self._views[self._currentviewkey])
    
    def _update_view_key(self):
        if self._action in self._views:
            self._currentViewKey=self._action
    
    def _translate_command(self,command):
        """
        Set action based on the commands allowed by the current view
        """
        # Check if command is game admin (not view specific)
        self._action=self._admin_command_list.get(command,'?')
        # Look through view specific commands if not admin
        if self._action=='?':
            self._action=self._views[self._currentviewkey].available_commands.get(command,'?')