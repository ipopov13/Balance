# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:41:01 2019

AI module for the Balance rogue-like RPG framework.

The AI inits a dictionary of messages:actions (messages are unique).
The AI loads/creates the game data when handling commands from the
Menu screen.
The AI gets the message sent by the current Screen and calls the action
associated with the respective command.
The action changes the game data accordingly. It also increments the
controlled object's timer property if the action takes time, and
returns a Screen ID or None if the game has ended, and a boolean refresh
argument to pass back to the Screen.
The AI checks if all active objects are at the same point in time. If
not, it picks the next one to act, decides on its action and sends it
to an action.
This repeats until all active objects have their timer properties equal
(everyone has acted).
In the end of a turn the AI returns the final Screen ID or None, plus
the refresh argument.
Every functionality is expected to exist as an action that responds to
specific messages by modifying the game state passed in the game_data
variable and then returning the next Screen ID and refresh.
        
@author: IvanPopov
"""
from world import World
import constants as const


class AI:
    game_data = World()
    _action_mapping = {}
    
    @classmethod
    def register_action(cls,action):
        if action.message in cls._action_mapping:
            raise ValueError(f"Repeated action message: '{action.message}'!")
        cls._action_mapping[action.message] = action()
        
    def __init__(self):
        self.game_data.start()
    
    def execute(self, command):
        """
        Pass the command to an action, update the game data and
        return the next DM ID string or None
        
        Refresh: Whether the DM called should be reinitialized. Used
        for repeating DMs like StatSelection and ModifierSelection
        """
        if ':' in command:
            command,subcommand = command.split(':',1)
        else:
            subcommand = ''
        # Make sure the command is real
        if command not in AI._action_mapping:
            raise ValueError(f"Unknown message to AI: '{command}'!")
        result = AI._action_mapping[command].execute(subcommand=subcommand,
                                                     world=self.game_data)
        return result
    
    @property
    def player(self):
        return self.game_data.player


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
    message = const.QUIT_GAME
    
    def execute(self,**kwarg):
        return (None, False)
        

class DoNothing(Action):
    message = const.SILENT_UNKNOWN
    
    def execute(self,**kwarg):
        return (const.SILENT_UNKNOWN, False)
        

class Move(Action):
    message = const.MOVE
    
    def execute(self,subcommand=None,**kwarg):
        refresh = AI.game_data.move_player(subcommand)
        return (const.GET_SCENE, refresh)
        

class BeginGame(Action):
    message = const.NEW_GAME
    
    def execute(self,world=None,**kwarg):
        if world.player.available_modifiers:
            return (const.GET_MODIFIER_SELECTION, True)
        elif world.player.available_stat_selections:
            return (const.GET_STAT_SELECTION, True)
        else:
            return (const.GET_SCENE, False)
        

class ChooseModifier(Action):
    message = const.SELECT_MODIFIER
    
    def execute(self,subcommand=None,world=None,**kwarg):
        world.player.apply_modifier(subcommand)
        if world.player.available_modifiers:
            return (const.GET_MODIFIER_SELECTION, True)
        elif world.player.available_stat_selections:
            return (const.GET_STAT_SELECTION, True)
        else:
            return (const.GET_SCENE, False)
    
    
class ChangeStat(Action):
    message = const.ALTER_STAT
    
    def execute(self,subcommand=None,world=None,**kwarg):
        stat,amount = subcommand.split(':')
        amount = int(amount)
        try:
            world.player.change_stat(stat,amount)
        except ValueError:
            pass
        return (const.GET_STAT_SELECTION, False)
    
    
class DisplayScene(Action):
    message = const.GET_SCENE
    
    def execute(self,**kwarg):
        return (const.GET_SCENE, True)