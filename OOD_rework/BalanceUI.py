# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:11:54 2019

User interface class for the Balance rogue-like RPG

@author: IvanPopov
"""
import pickle
import World

class UI:

    def __init__(self):
        pass
    
    def getWorld(self):
        pass
        # TODO:
        #Display starting screen
        #If new return World(self.getPlayerCharacter())
        #If load glob the saved worlds directory, unpickle the worlds and present a choiceList using their .present() strings
        #return chosen world

    def getPlayerCharacter(self):
        pass

    def choiceList(self, prompt, presentables):
        pass
        # TODO:
#        Print prompt and the .present() strings of the objects in the list
#        Get player choice
#        Return chosen object