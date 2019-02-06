# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:42:32 2019

World class for the Balance rogue-like RPG

@author: IvanPopov
"""

from GameObject import Being

class World:
    def __init__(self,player_choices):
        self.activeBeing=Being(player_choices) #the center of the world, usually the player :P. This inits non-Scene views that are available. A player is initialized, but only the Being interface is used (then why is a Player initialized??)
        #TODO: Randomize world params (create world data)
        #TODO: Choose good spot for player as a param dict
        spot={}
        # TEST: Scene init was run with spot
        self.activeBeing.initSceneView(spot)
        self.living = True
        
    def isLive(self):
        """Accessed by the loop as a game-over signal"""
        return self.living

    def setup(self):
        return ['viewSceneCommand'] #pass a list of starting commands. viewSceneCommand corresponds to the ctrl+1 shortcut

    def run(self,command):
        (additional_commands,self.currentView) = self.activeBeing.executeCommand(command)
        return additional_commands