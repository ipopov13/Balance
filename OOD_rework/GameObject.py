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

Public initSceneView(spot): /start up the scene using the params passed by world

Public executeCommand(command): /set the intent and then update the corresponding View and set its key in self.currentViewKey
If command in self.views[self.currentviewkey].commands:
Check if view changes (a ctrl+ command)
Set new view key
Self.updateIntent(command)
Additional_commands = Self.views[self.currentviewkey].update()
Return (additional_commands, Self.views[self.currentviewkey])

private initNonScenes(): /add all non-scene view that are applicable to the Being
    """
    def __init__(self,player_choices):
        # Dict of views that are available for the Being. Always contains the
        # standard ones (AvailableViews, Scene, CharSheet, Inventory), while
        # others are added/removed according to the Being's properties and
        # development.
        self.views=self.initNonScenes()
        self.currentViewKey='scene'
        self.intent='' #the action that the Being will take this turn
    
    def initSceneView(self,spot):
        pass
    
    def initNonScenes(self):
        return {}
    
    def executeCommand(self, command):
        additional_commands=[]
        return (additional_commands,self.views[self.currentviewkey])