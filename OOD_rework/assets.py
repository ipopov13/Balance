# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:43:23 2019

Assets classes for the Balance rogue-like RPG.

@author: IvanPopov
"""

class StaticScreens:
    """
    Screens should be dictionaries in the format:
        {'chars':String, 'fores':String, 'backs':String}
    """
    starter = {'chars':'''
               ___      _   _         _   _    _   ___   ____
              |   \    / |  |        / |  |\   |  /   \ |
              |___/   /  |  |       /  |  | \  |  |     |___
              |   \  /---|  |      /---|  |  \ |  |     |
              |___/ /    |  |___| /    |  |   \|  \___/ |____

                                    ver 0.7

                                   (n)ew game
                             (l)oad a previous game'''}
    tester = {'chars':'a','fores':'a','backs':'l'}