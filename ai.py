# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:41:01 2019

AI module for the Balance rogue-like RPG.

The AI inits a dictionary of messages:actions (messages are unique).
The AI loads/creates the game data when handling commands from the
 starting DM.
The AI gets the message sent by the DM and updates the controlled being
 object.
Then it calls the action associated with the respective command.
The action changes the game data accordingly. It also increments the
 controlled object's timer property if the action takes time, and
 returns a DM ID or None if the game has ended.
The AI checks if all active objects are at the same point in time. If
 not, it picks the next one to act, decides on its action and sends it
 to an action.
This repeats until all active objects have their timer properties equal
 (everyone has acted).
In the end of a turn the AI returns the final DM ID or None.
 
Every functionality is expected to exist as an action that responds to
 specific messages by modifying the game state passed in the game_data
 variable and then returning the next DM ID.
        
@author: IvanPopov
"""
from world import World

## Handled
NEW_GAME = 'starter_new_game'
QUIT_GAME = 'quit_game'
SILENT_UNKNOWN = 'silently do nothing'
GET_MODIFIER_SELECTION = 'get modifier selection'
## Unhandled
STARTER_LOAD_GAME = 'starter_load_game'
GET_SCENE = 'get scene view'
SELECT_MODIFIER = 'selected modifier:'
ALTER_STAT = 'alter stat:'
GET_STAT_SELECTION = 'get stat selection'

class AI:
    game_data = World()
    _action_mapping = {}
    
    @classmethod
    def register_action(cls,action):
        if action.message in cls._action_mapping:
            raise ValueError(f"Repeated handler message: '{handler.message}'!")
        cls._action_mapping[action.message] = action()
    
    def execute(self, command):
        """
        Pass the command to an action, update the game data and
        return the next DM ID string or None
        
        Refresh: Whether the DM called should be reinitialized. Used
        for repeating DMs like StatSelection and ModifierSelection
        """
        command,subcommand = command.split(':',1)
        # Delay displaying scene if the player has stats to select
        if command == GET_SCENE and self.game_data.available_stat_selections:
            result = GET_STAT_SELECTION
            refresh = True
            return (result, refresh)
        if command not in AI._action_mapping:
            raise ValueError(f"Unknown message to AI: '{command}'!")
        # Specify actions available at game start
        if AI._action_mapping[command] == NEW_GAME:
            subcommand = {'mods':self.game_data.available_modifiers,
                          'stats':self.game_data.available_stat_selections}
        result = AI._action_mapping[command].execute(subcommand=subcommand)
        refresh = False
        # Enforce all modifiers has been selected
        if self.game_data.available_modifiers:
            result = GET_MODIFIER_SELECTION
            refresh = True
        return (result, refresh)
    
    def next_stat_selection(self):
        return self.game_data.next_stat_selection()
    
    def next_modifier(self):
        return self.game_data.next_modifier()
        
    def get_stat(self,*,stat=None):
        """Query the game data for the player stat"""
        return self.game_data.get_stat(stat=stat)


class ActionMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if bases != ():
            AI.register_action(cls)
        return cls

class Action(metaclass=ActionMeta):
    message = ''
    
    def execute(self,**kwarg):
        """
        Execute an action on the game data
        
        Concrete handler subclasses override this method
        """
        raise NotImplementedError
        

class Quit(Action):
    message = QUIT_GAME
    
    def execute(self,**kwarg):
        return None
        

class DoNothing(Action):
    message = SILENT_UNKNOWN
    
    def execute(self,**kwarg):
        return SILENT_UNKNOWN
        

class StartNewGame(Action):
    message = NEW_GAME
    
    def execute(self,subcommand={},**kwarg):
        if subcommand['mods']:
            return GET_MODIFIER_SELECTION
        elif subcommand['stats']:
            return GET_STAT_SELECTION
        else:
            return GET_SCENE
        

class ChooseModifier(Action):
    message = SELECT_MODIFIER
    
    def execute(self,subcommand=None,**kwarg):
        AI.game_data.apply_modifier(subcommand)
        return GET_STAT_SELECTION
    
    
class ChangeStat(Action):
    message = ALTER_STAT
    
    def execute(self,subcommand=None,**kwarg):
        AI.game_data.apply_stat_change(subcommand)
        return GET_STAT_SELECTION
    
    
class DisplayScene(Action):
    message = GET_SCENE
    
    def execute(self,**kwarg):
        return GET_SCENE