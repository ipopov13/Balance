# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:15:37 2019

Config file for the Balance rogue-like framework.

@author: IvanPopov
"""
import json
import os

game_path = ".\Balance_tester\design"
settings_file = 'game_settings.txt'

def get_settings():
    with open(os.path.join(game_path,settings_file)) as infile:
        return json.load(infile)