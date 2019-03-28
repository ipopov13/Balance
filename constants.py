# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 09:13:29 2019

Constants file for the Balance rogue-like RPG platform.

Contains all string constants for the game: triggers, dm call, action
 calls, world/scene directions, key values: can be used to do key
 mappings. Only mappable sceneDM keys are in the config, all other
 constants are hardcoded in the constats.py. The file can have a config
 reading func that gets the mapped keys and assigns them to the
 constant names. This ensures there are no strings in the code
 apart from fixed ini fields.

@author: IvanPopov
"""

## Stat triggers
READY_TO_CONTINUE = 'READY_TO_CONTINUE'
## Modifier "applied" values
AT_CHARACTER_CREATION = 'AT_CHARACTER_CREATION'
## Screen constants
DEFAULT_PIXEL_STYLE = 7
DEFAULT_PIXEL_CHAR = ' '
## Theme distributions
PEAKS = 'peaks'
POLES = 'poles'
## World/Scene/Tile constants
SUCCESSFUL = 'SUCCESSFUL'
GOING_NORTH = 'GOING_NORTH'
GOING_SOUTH = 'GOING_SOUTH'
GOING_EAST = 'GOING_EAST'
GOING_WEST = 'GOING_WEST'
## Gameobject properties
PLAYER = '@'
DEFAULT_PLAYER_STYLE = 7
## SceneDM commands. Mappable keys from ini overwrite these.
GO_N = '8'
GO_S = '2'
GO_W = '4'
GO_E = '6'
GO_SW = '1'
GO_SE = '3'
GO_NW = '7'
GO_NE = '9'
STAY = '5'
## Fixed commands for DMs other than Scene
N_KEY = 'n'
L_KEY= 'l'
Q_KEY = 'q'
RETURN_KEY = '\r'
UNKNOWN_COMMAND = 'unknown command'
## Action calls
NEW_GAME = 'begin new game'
QUIT_GAME = 'quit_game'
SILENT_UNKNOWN = 'silently do nothing'
SELECT_MODIFIER = 'selected modifier'
ALTER_STAT = 'alter stat'
MOVE = 'the player moves'
## DM calls
GET_MENU = 'menu screen'
GET_MODIFIER_SELECTION = 'get modifier selection screen'
GET_SCENE = 'get scene view'
GET_STAT_SELECTION = 'get stat selection'
## Unhandled action calls
LOAD_GAME = 'starter_load_game'
