# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:41:01 2019

AI module for the Balance rogue-like RPG.

 Every
 functionality is expected to exist as a handler that responds to
 specific messages by modifying the game state passed in the game_data
 variable and then returning the data back to the calling DM.
 
Handlers register with a specific DM in order to handle messages sent by
 the player (keyboard commands) or the AI (message_string's).
 
Requirements:
    Handlers change game data
        return 0 or a DM instance
        
@author: IvanPopov
"""
STARTER_NEW_GAME = 'starter_new_game'
STARTER_LOAD_GAME = 'starter_load_game'
STARTER_UNKNOWN = 'starter unknown'

class AI:
    
    def execute(self, command):
        return 'command'
    

class CommandHandler:
    pass


class TestHandler(CommandHandler):
    
    def execute(self, _):
        return 'command'