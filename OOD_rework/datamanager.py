# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:51:49 2019

DataManager/Handler classes for the Balance rogue-like RPG

This family of classes contains the logic of the game. Every
 functionality is expected to exist as a handler that responds to
 specific messages by modifying the game state passed in the game_data
 variable and then returning the data back to the calling DM.

Handlers register with a specific DM in order to handle messages sent by
 the player (keyboard commands) or the AI (message_string's).
 
Requirements:
    DMs refresh the screen using the console
        receive a command from the console
        call AI.evaluate_command()
        call the AI.turn() in a loop
        call a handler for each object they get from the AI
        return a DM instance if a handler sent it in response
    Handlers change game data
        return 0 or a DM instance

@author: IvanPopov
"""
import Console
import ai

class DataManager:
    _console = None
    _ai = ai.AI()
    
    @classmethod
    def get_starting_dm(cls):
        """Return the DM registered as the starter one"""
        return cls()
        
    def __init__(self,personal_message=''):
        if DataManager._console is None:
            DataManager._console = Console.getconsole()
            DataManager._console.title("Balance")
        self._screen = {'char':['a'], 'style':[7]}
        self._unknown_command_dme = None
                
    def take_control(self):
        """The DM activity loop"""
        next_dm = 0
        while not next_dm:
            command = self._present()
            next_dm = self._ai.execute(command)
        return next_dm
    
    def _present(self):
        self._update_screen()
        row_length = 79
        x = 0
        y = 0
        for ch,st in zip(self._screen['char'],self._screen['style']):
            DataManager._console.text(x,y,ch,st)
            x+=1
            if x>row_length:
                x = 0
                y += 1
        return DataManager._console.getchar()
    
    def _update_screen(self):
        pass
    

class CommandHandler:
    pass


class TestHandler(CommandHandler):
    
    def execute(self, _):
        return 'command'