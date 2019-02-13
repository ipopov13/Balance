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
END_GAME = 'end game'
GET_STARTING_VIEW = 'get starting view'
GET_DEFAULT_VIEW = 'get default view'


class View:
    
    messages = {}
    
    def __init__(self, user_interface):
        self._user_interface = user_interface
        self._screen = []
        self._getter_message = None
        self._set_as_default=False
        self._post_init()
        self._add_member(self,message=self._getter_message)
    
    def _add_member(self, member, *, message=None):
        if not message:
            raise ValueError('Please supply a real message!')
        if message in self.messages:
            raise ValueError('Message already exists, please revise!')
        if member.__class__ not in View.__subclasses__():
            raise ValueError('Please supply a View subclass as member!')
        self.messages[message] = member
        if self._set_as_default:
            if '' in self.messages:
                raise ValueError('Second View set as default, there can only be one default!')
            self.messages[GET_DEFAULT_VIEW] = member

    def take_control(self, game_data):
        """
        Take control of the screen and present self, then run a loop
        for commands from the player and finally return the call for
        the next View, or END_GAME if player quit/died.
        """
        command = None
        while command not in self.messages and command != END_GAME:
            self._update_data(data=game_data,command=command)
            self._update_screen(game_data)
            command = self._present()
        return command
    
    def _present(self):
        return self._user_interface.present(self._screen)
        
    def _post_init(self):
        """
        Subclasses need to override this!
        
        Used by subclasses to set their unique getter message and
        declare themselves as default View (only one can be default)!
        """
        raise NotImplementedError
    
    def _update_data(self,*,data={},command=''):
        """
        Subclasses need to override this!
        
        Update the game data using the known DataManagers.
        """
        raise NotImplementedError

    def _update_screen(self,game_data):
        """
        Subclasses need to override this!
        
        Build the updated screen.
        """
        raise NotImplementedError


class StarterView(View):
    """
    Creates the player character and the initial game data,
    or loads an existing set of data from file,
    and put them in the received variable.
    """
        
    def _post_init(self):
        self._getter_message = GET_STARTING_VIEW
    
    def _update_data(self,*,data={},command=''):
        pass

    def _update_screen(self,game_data):
        pass

class SceneView(View):
        
    def _post_init(self):
        self._getter_message = 'get scene view'
        self._set_as_default = True
    
    def _update_data(self,*,data={},command=''):
        pass

    def _update_screen(self,game_data):
        pass


class CharacterView(View):
        
    def _post_init(self):
        self._getter_message = 'get character view'
    
    def _update_data(self,*,data={},command=''):
        pass

    def _update_screen(self,game_data):
        pass


class EquipmentView(View):
        
    def _post_init(self):
        self._getter_message = 'get equipment view'
    
    def _update_data(self,*,data={},command=''):
        pass

    def _update_screen(self,game_data):
        pass


class InventoryView(View):
        
    def _post_init(self):
        self._getter_message = 'get inventory view'
    
    def _update_data(self,*,data={},command=''):
        pass

    def _update_screen(self,game_data):
        pass
        

def prepare_views(ui):
    """
    Initialize all View subclasses.
    Returns the full message dictionary.
    """
    for subview in View.__subclasses__():
        instance = subview(ui)
    return instance.messages

__all__ = [prepare_views,GET_STARTING_VIEW,END_GAME]