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
    race_selection = {(0,i):{'text':t} for (i,t) in enumerate('''
    Choose race:
        1) Human'''.split('\n'))}
    stat_selection = {(0,i):{'text':t} for (i,t) in enumerate('''
    Modify stats:
        Strength          (s/S)
        Dexterity         (d/D)
        Inteligence       (i/I)
        Creativity        (c/C)
        Spirit            (p/P)
        Tradition         (t/T)
        
        Points left:
            
    
    You can go (b)ack to race selection or (q)uit.'''.split('\n'))}
    tester = {(0,0):{'text':'test','style':125}}
    tester2 = {(0,0):{'text':'test2','style':126}}