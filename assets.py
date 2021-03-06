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
    starter = {(0,i):{'text':t} for (i,t) in enumerate('''
               ___      _   _         _   _    _   ___   ____
              |   \    / |  |        / |  |\   |  /   \ |
              |___/   /  |  |       /  |  | \  |  |     |___
              |   \  /---|  |      /---|  |  \ |  |     |
              |___/ /    |  |___| /    |  |   \|  \___/ |____

                                    ver 0.7

                                   (n)ew game
                             (l)oad a previous game
                                   (q)uit game'''.split('\n'))}
    tester = {(0,0):{'text':'test','style':125}}
    tester2 = {(0,0):{'text':'test2','style':126}}
    scene = {(0,0):{'text':'scene view'}}