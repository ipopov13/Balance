# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:11:54 2019

User interface class for the Balance rogue-like RPG

UI receives a call for display from a View and renders the screen.

@author: IvanPopov
"""
import Console


class UserInterface:

    def __init__(self):
        self._con = Console.getconsole()
        self._con.title("Balance")
        
    def present(self, screen):
        """
        Display the received screen dict in the console.
        screen = {'char':[],
                  'color':[]}
        """
        pass