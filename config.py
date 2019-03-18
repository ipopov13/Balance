# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:15:37 2019

Config file for the Balance rogue-like framework.

@author: IvanPopov
"""
import os
import configparser

game_path = ".\Balance\design"
settings_file = 'game_settings.ini'
parser = configparser.ConfigParser()

def get_settings():
    parser.read(os.path.join(game_path,settings_file))
    return parser['game_settings']