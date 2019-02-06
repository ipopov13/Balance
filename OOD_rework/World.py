# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:42:32 2019

World class for the Balance rogue-like RPG

@author: IvanPopov
"""

from gameobject import Being

class World:
    def __init__(self,player_choices):
        # The center of the world, usually the player :P
        self._activeBeing=Being(player_choices)
        #TODO: Randomize world params (create world data)
        #TODO: Choose good spot for player as a param dict
        spot={}
        self._activeBeing.init_scene_view(spot)
        self.is_live=True
        self._current_view=None

    def setup(self):
        """
        Pass a list of starting commands. 
        viewSceneCommand corresponds to the ctrl+1 shortcut
        """
        return ['viewSceneCommand']

    def run(self,command):
        (additional_commands,self._current_view) = self._activeBeing.execute_command(command)
        return additional_commands