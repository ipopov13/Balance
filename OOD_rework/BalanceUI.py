# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:11:54 2019

User interface class for the Balance rogue-like RPG

UI receives a View for display and responds with the next command
of the player. It also manages saving/loading games.

@author: IvanPopov
"""
import Console


class UserInterface:

    def __init__(self):
        self._con = Console.getconsole()
        self._con.title("Balance")
        
    def get_pc_request(self):
        pass