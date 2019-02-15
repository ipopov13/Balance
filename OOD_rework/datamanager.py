# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:51:49 2019

DataManager classes for the Balance rogue-like RPG

This family of classes contains the logic of the game. Every
 functionality is expected to exist as a DataManager that responds to
 specific messages by modifying the game state passed in the game_data
 variable and then returning the data back to the calling View.
 
Message chains are evaluated by DataManagers that have registered the
 messages with their View. Managers are common for all beings that
 the View deals with. Beings only differ in the messages they are
 allowed to send.
 
Emergent behavior is possible when all activities are available to more
 beings and if a completely persistent world is implemented. 
 Example: with "building", "trading", random travelling creatures,
 village design, and "long term goals" (allowing areas to develop in
 the absence of the player) it is possible for a local human to barter
 food for building materials with passing dwarf traders, and then to
 build a house over a long period of time. If there are more humans a
 village may emerge, and further modules may increase the number and
 diversity of persisting local beings.

@author: IvanPopov
"""
END_GAME = 'end game'


class DataManager:
    
    def __init__(self):
        pass
    
    def update_data(self,*,data={},command=''):
        return END_GAME
    
class EmptyManager:
    
    def __init__(self):
        raise NotImplementedError