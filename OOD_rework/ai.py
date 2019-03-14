# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:41:01 2019

AI module for the Balance rogue-like RPG.

The AI inits a dictionary of messages:handlers (messages are unique so
 that handlers for different DMs don't clash).
The AI loads/creates the game data when handling commands from the
 starting DM.
The AI gets the message sent by the DM and updates the controlled being
 object.
Then it calls the handler associated with the respective action.
The handler changes the game data accordingly. It also increments the
 controlled object's timer property if the action takes time, and
 returns 0 if no DM change is necessary, or a DM ID string if it is.
The AI checks if all active objects are at the same point in time. If
 not, it picks the next one to act, decides on its action and sends it
 to a handler.
This repeats until all active objects have their timer properties equal
 (everyone has acted).
In the end of a turn if any handler returned a DM ID the AI sends it
 back, or returns 0.
 
Every functionality is expected to exist as a handler that responds to
 specific messages by modifying the game state passed in the game_data
 variable and then returning the data back to the calling DM.
 
Handlers respond to specific messages sent by the AI.
 
Requirements:
    Handlers change game data
        return 0 or a DM instance
        
@author: IvanPopov
"""
from gamedata import GameData

## DM calls (only sent, not expected to be handled)
## Handled
STARTER_NEW_GAME = 'starter_new_game'
QUIT_GAME = 'quit_game'
SILENT_UNKNOWN = 'silently do nothing'
CHOOSE_HUMAN_RACE = 'choose human race'
GET_RACE_SELECTION = 'get character selection'
GET_STAT_SELECTION = 'get stat selection'
STAT_SEL_DECR_STR = 'stat selection decrease strength'
STAT_SEL_INCR_STR = 'stat selection increase strength'
STAT_SEL_DECR_DEX = 'stat selection decrease dex'
STAT_SEL_INCR_DEX = 'stat selection increase dex'
STAT_SEL_DECR_INT = 'stat selection decrease int'
STAT_SEL_INCR_INT = 'stat selection increase int'
STAT_SEL_DECR_CRE = 'stat selection decrease cre'
STAT_SEL_INCR_CRE = 'stat selection increase cre'
STAT_SEL_DECR_SPI = 'stat selection decrease spi'
STAT_SEL_INCR_SPI = 'stat selection increase spi'
STAT_SEL_DECR_TRA = 'stat selection decrease tra'
STAT_SEL_INCR_TRA = 'stat selection increase tra'
## Unhandled
STARTER_LOAD_GAME = 'starter_load_game'
GET_SCENE = 'get scene view'

class AI:
    game_data = GameData()
    _handler_mapping = {}
    
    @classmethod
    def register_handler(cls,handler):
        if handler.message in cls._handler_mapping:
            raise ValueError(f"Repeated handler message: '{handler.message}'!")
        cls._handler_mapping[handler.message] = handler()
    
    def execute(self, command):
        """
        Pass the command to a handler, update the game data and
        return the next DM ID string or None
        """
        if command not in AI._handler_mapping:
            raise ValueError(f"Unknown message to AI: '{command}'!")
        result = AI._handler_mapping[command].execute()
        return result


class CHMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if bases != ():
            AI.register_handler(cls)
        return cls

class CommandHandler(metaclass=CHMeta):
    message = ''
    
    def execute(self):
        """
        Execute an action on the game data
        
        Concrete handler subclasses override this method
        """
        raise NotImplementedError
        

class QuitHandler(CommandHandler):
    message = QUIT_GAME
    
    def execute(self):
        return None
        

class SilentUnknownHandler(CommandHandler):
    message = SILENT_UNKNOWN
    
    def execute(self):
        return SILENT_UNKNOWN
        

class StarterNewGameHandler(CommandHandler):
    message = STARTER_NEW_GAME
    
    def execute(self):
        return GET_RACE_SELECTION
        

class GetRaceSelHandler(CommandHandler):
    message = GET_RACE_SELECTION
    
    def execute(self):
        return GET_RACE_SELECTION
        

class ChooseHumanRaceHandler(CommandHandler):
    message = CHOOSE_HUMAN_RACE
    
    def execute(self):
        AI.game_data.start(race='human')
        return GET_STAT_SELECTION
    
class StatSelDecrSTRHandler(CommandHandler):
    message = STAT_SEL_DECR_STR
    
    def execute(self):
        AI.game_data.change_stat('Str',-1)
        return GET_STAT_SELECTION
    
class StatSelIncrSTRHandler(CommandHandler):
    message = STAT_SEL_INCR_STR
    
    def execute(self):
        AI.game_data.change_stat('Str',1)
        return GET_STAT_SELECTION
    
class StatSelDecrDEXHandler(CommandHandler):
    message = STAT_SEL_DECR_DEX
    
    def execute(self):
        AI.game_data.change_stat('Dex',-1)
        return GET_STAT_SELECTION
    
class StatSelIncrDEXHandler(CommandHandler):
    message = STAT_SEL_INCR_DEX
    
    def execute(self):
        AI.game_data.change_stat('Dex',1)
        return GET_STAT_SELECTION
    
class StatSelDecrINTHandler(CommandHandler):
    message = STAT_SEL_DECR_INT
    
    def execute(self):
        AI.game_data.change_stat('Int',-1)
        return GET_STAT_SELECTION
    
class StatSelIncrINTHandler(CommandHandler):
    message = STAT_SEL_INCR_INT
    
    def execute(self):
        AI.game_data.change_stat('Int',1)
        return GET_STAT_SELECTION
    
class StatSelDecrCREHandler(CommandHandler):
    message = STAT_SEL_DECR_CRE
    
    def execute(self):
        AI.game_data.change_stat('Cre',-1)
        return GET_STAT_SELECTION
    
class StatSelIncrCREHandler(CommandHandler):
    message = STAT_SEL_INCR_CRE
    
    def execute(self):
        AI.game_data.change_stat('Cre',1)
        return GET_STAT_SELECTION
    
class StatSelDecrSPIHandler(CommandHandler):
    message = STAT_SEL_DECR_SPI
    
    def execute(self):
        AI.game_data.change_stat('Spi',-1)
        return GET_STAT_SELECTION
    
class StatSelIncrSPIHandler(CommandHandler):
    message = STAT_SEL_INCR_SPI
    
    def execute(self):
        AI.game_data.change_stat('Spi',1)
        return GET_STAT_SELECTION
    
class StatSelDecrTRAHandler(CommandHandler):
    message = STAT_SEL_DECR_TRA
    
    def execute(self):
        AI.game_data.change_stat('Tra',-1)
        return GET_STAT_SELECTION
    
class StatSelIncrTRAHandler(CommandHandler):
    message = STAT_SEL_INCR_TRA
    
    def execute(self):
        AI.game_data.change_stat('Tra',1)
        return GET_STAT_SELECTION