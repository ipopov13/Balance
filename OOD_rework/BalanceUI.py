# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:11:54 2019

User interface class for the Balance rogue-like RPG

@author: IvanPopov
"""
import pickle
import glob
import world
import Console

class UserInterface:

    def __init__(self):
        self.con=Console.getconsole()
        self.con.title("Balance")
        self.choice=''
    
    def get_world(self):
        self.con.write('''
               ___      _   _         _   _    _   ___   ____
              |   \    / |  |        / |  |\   |  /   \ |
              |___/   /  |  |       /  |  | \  |  |     |___
              |   \  /---|  |      /---|  |  \ |  |     |
              |___/ /    |  |___| /    |  |   \|  \___/ |____

                                    ver 0.6

                                   (n)ew game
                             (l)oad a previous game
                            ''')
        self._get_choice(['n','l'])
        self.con.page()
        if self.choice=='n':
            print('boom')
            self.get_command()
            return world.World(self._get_player_character())
        elif self.choice=='l':
            print('boom2')
            self.get_command()
            return self.choice_list("Please choose a game to run:",
                                    self._get_worlds())

    def _get_player_character(self):
        self.con.write("""
 The form your character may take in Balance is completely controlled by his or
 her actions. If you like to go around and kill things, you are likely to end
 up with an ork, while a character that spends his time in the mine will slowly
 become a dwarf. There are various actions both on your environment and other
 beings that will form your character. They are all connected to the three
 forces in the world of Balance - Order, Chaos, and Nature. Every action will
 align you more with one of the forces, and with one or more of the forms
 governed by it. This is the only way to mold your character in the game - you
 gain and loose abilities depending on the predominant form you hold. Choosing
 a form now gives you 34% attunement to it, and 34% alignment to the
 respective force. Your total form attunement can't be higher than your
 alignment to the respective force.""")
        self.get_command()
    
    def _get_worlds(self):
        #If load glob the saved worlds directory, unpickle the worlds and present a choiceList using their .present() strings
        #return chosen world
        pass

    def choice_list(self, prompt, presentables):
        pass
        # TODO:
#        Print prompt and the .present() strings of the objects in the list
#        Get player choice
#        Return chosen object
        
    def get_command(self):
        return 0
    
    def _get_choice(self,options,no_escape=True):
        self.choice=self.con.getchar().decode()
        self.con.write(self.choice)
        while self.choice not in options and no_escape:
            # TODO: Add error message to prompt for a correct choice?
            self.choice=self.con.getchar().decode()
            self.con.write(self.choice)
            