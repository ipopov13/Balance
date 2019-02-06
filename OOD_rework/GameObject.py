# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:00:45 2019

GameObject abstract class for the Balance rogue-like RPG

@author: IvanPopov
"""

import View

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
    # The full list of admin commands used for the game (save,load,quit,change view)
    _admin_command_list={}
    
    def __init__(self,player_choices,scene=None):
        """
        Create a Being with the set parameters
        Optional scene can be passed for creating NPCs inside a scene owned by
        the player character.
        """
        self.views=self.initNonScenes()
        self.views['scene']=scene
        self.currentViewKey='scene'
        self.action='' #the action that the Being will take this turn
    
    def initSceneView(self,spot):
        self.views['scene']=View.SceneView(self,spot)
    
    def initNonScenes(self):
        """
        Return a dict of all non-scene views initialized with the Being
        """
        return View.
    
    def executeCommand(self, command):
        """
        Set the action, update self.currentViewKey, then update the
        corresponding View and return it along with any extra commands.
        """
        self.translate_command(command)
        self.update_view_key()
        additional_commands = self.views[self.currentviewkey].update()
        return (additional_commands,self.views[self.currentviewkey])
    
    def update_view_key(self):
        if self.action in self.views:
            self.currentViewKey=self.action
    
    def translate_command(self,command):
        """
        Set action based on the commands allowed by the current view
        """
        # Check if command is game admin (not view specific)
        self.action=self._admin_command_list.get(command,'?')
        # Look through view specific commands if not admin
        if self.action=='?':
            self.action=self.views[self.currentviewkey].available_commands.get(command,'?')