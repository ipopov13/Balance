# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:41:01 2019

Views: implement the _update_current_view() method, can create screens
 for display. Do not implement any commands. Only Views are registered
 in the game instance, but they can include a large number of
 DataManagers by initializing instances of them with self as owner (so
 that the methods are called with the correct arguments).
 
Commands are translated to messages by the active View that receives
 them from the UI. The View executes the message chain using its
 DataManagers, then updates the screen and sends it for display to the
 UI, receiving the next user command in turn. Commands or messages
 eventually end the execution of a View and it sends back a call for
 another View, or the END_GAME message. Views cannot send messages to
 one another, they are completely independent.

Being introspection Views (all except StarterView and SceneView) only
 operate with the specific being that they have to display or modify,
 stored in the game_data['focus_being'].
 
Requirements:
    take_control must present a screen by calling the UI
    Must return a command that is in MESSAGES

@author: IvanPopov
"""
GET_STARTER_VIEW = 'get starter view'
GET_SCENE_VIEW = 'get scene view'
GET_INVENTORY_VIEW = 'get inventory view'
GET_EQUIPMENT_VIEW = 'get equipment view'
GET_CHARACTER_VIEW = 'get character view'
END_GAME = 'end game'
MESSAGES = [GET_STARTER_VIEW, GET_SCENE_VIEW, GET_INVENTORY_VIEW,
            GET_EQUIPMENT_VIEW, GET_CHARACTER_VIEW, END_GAME]

class View:
    
    def __init__(self, user_interface):
        self._user_interface = user_interface
        self._screen = []

    def take_control(self, game_data):
        """
        Take control of the screen and present self, then run a loop
        for commands from the player and finally return the call for
        the next View, or END_GAME if player quit/died.
        
        Subclasses need to override this.
        """
        command = ''
        while command not in MESSAGES:
            self._update_screen(command)
            command = self._present_screen()
        return command
    
    def _update_screen(self, command):
        pass
    
    def _present_screen(self):
        return self._user_interface.present(self._screen)

class StarterView(View):
    """
    Creates the player character and the initial game data,
    or loads an existing set of data from file,
    and put them in the received variable.
    """
    pass


class SceneView(View):
    """
    Contains and preserves information about the scene of the game.
    """
    pass


class CharacterView(View):
    pass


class EquipmentView(View):
    pass


class InventoryView(View):
    pass