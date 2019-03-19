# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:15:37 2019

Config functions for the Balance rogue-like framework.

@author: IvanPopov
"""
import os
import configparser
from glob import glob

parser = configparser.ConfigParser()
parser.read('config.ini')
config = parser['general']

def get_game_settings():
    new_parser = configparser.ConfigParser()
    new_parser.read(os.path.join(config['game_path'],
                                 config['game_settings_file']))
    return new_parser['game']

def get_world_settings():
    new_parser = configparser.ConfigParser()
    new_parser.read(os.path.join(config['game_path'],
                                 config['game_settings_file']))
    return new_parser['world']

def get_themes():
    new_parser = configparser.ConfigParser()
    new_parser.read(os.path.join(config['game_path'],
                                 config['themes_file']))
    return new_parser

def get_terrains():
    terrains = glob(config['terrains_folder']+'/*.ini')
    new_parser = configparser.ConfigParser()
    for terrain in terrains:
        new_parser.read(terrain)
        yield new_parser
    