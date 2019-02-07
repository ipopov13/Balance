# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:42:32 2019

World class for the Balance rogue-like RPG

@author: IvanPopov
"""

from view import PlayerController

class World:
    def __init__(self,player_choices):
        #TODO: Randomize world params (create world data)
        starting_location=self._get_starting_location(player_choices)
        # The center of the world, usually the player :P
        self._player_controller=PlayerController(player_choices,starting_location)
        self.is_live=True
        self._current_view=None

    def setup(self):
        """
        Pass a list of starting commands. 
        viewSceneCommand corresponds to the ctrl+1 shortcut
        """
        return ['viewSceneCommand']

    def run(self,command):
        (additional_commands,self._current_view) = self._player_controller.process_command(command)
        return additional_commands
    
    def _get_starting_location(self,player_choices):
        """Return the parameters for creating the starting location"""
        #TODO: Choose good spot for player as a param dict
        pass