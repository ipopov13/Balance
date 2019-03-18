# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:15:37 2019

Config file for the Balance rogue-like framework.

@author: IvanPopov
"""
import os
import configparser

game_path = ".\Balance\design"
game_settings_file = 'game_settings.ini'
themes_file = 'themes.ini'
parser = configparser.ConfigParser()

def get_game_settings():
    parser.read(os.path.join(game_path,game_settings_file))
    return parser['game']

def get_world_settings():
    new_parser = configparser.ConfigParser()
    new_parser.read(os.path.join(game_path,game_settings_file))
    return new_parser['world']

def get_themes():
    new_parser = configparser.ConfigParser()
    new_parser.read(os.path.join(game_path,themes_file))
    return new_parser