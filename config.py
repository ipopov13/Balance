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
                                 config['settings']))
    return new_parser[key]

def get_config(section=''):
    new_parser = configparser.ConfigParser()
    new_parser.read(os.path.join(config['game_path'],
                                 config[section]))
    return [new_parser[t] for t in new_parser.sections()]

def simplify(parsed_dict):
    simple = {}
    for key in parsed_dict:
        try:
            simple[key] = parsed_dict.getint(key)
        except ValueError:
            try:
                simple[key] = parsed_dict.getboolean(key)
            except ValueError:
                simple[key] = parsed_dict.get(key)
    return simple