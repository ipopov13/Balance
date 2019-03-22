# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:15:37 2019

Config functions for the Balance rogue-like framework.

@author: IvanPopov
"""
import os
import configparser

parser = configparser.ConfigParser()
parser.read('config.ini')
config = parser['general']

def get_settings(key='game'):
    new_parser = configparser.ConfigParser()
    new_parser.read(os.path.join(config['game_path'],
                                 config['game_settings_file']))
    return new_parser[key]

def get_themes():
    new_parser = configparser.ConfigParser()
    new_parser.read(os.path.join(config['game_path'],
                                 config['themes_file']))
    return [new_parser[t] for t in new_parser.sections()]

def get_terrains():
    new_parser = configparser.ConfigParser()
    new_parser.read(os.path.join(config['game_path'],
                                 config['terrains_file']))
    for terrain in new_parser.sections():
        yield new_parser[terrain]
    
def get_char_template():
    new_parser = configparser.ConfigParser()
    new_parser.read(os.path.join(config['game_path'],
                                 config['character_template_file']))
    return [new_parser[t] for t in new_parser.sections()]