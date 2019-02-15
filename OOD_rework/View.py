# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:41:01 2019

The View executes the message chain using its
 DataManager, then updates the screen and displays it,
 receiving the next user command in turn. Commands or messages
 eventually end the execution of a View and it sends back a call for
 another View, or the END_GAME message. Views cannot send messages to
 one another, they are completely independent.

Being introspection Views (all except StarterView and SceneView) only
 operate with the specific being that they have to display or modify,
 stored in the game_data['focus_being'].
 
Requirements:
    take_control must present a screen by calling the console
    take_control must call the dm's update_data()

@author: IvanPopov
"""
import Console
import datamanager

GET_STARTING_VIEW = 'get starting view'
GET_DEFAULT_VIEW = 'get default view'


class View:
    
    messages = {}
    _console = None
    
    def __init__(self):
        if View._console is None:
            View._console = Console.getconsole()
            View._console.title("Balance")
        self._screen = {'char':'test',
                        'color':[1,None,23,45,56]}
        self._getter_message = None
        self._set_as_default=False
        self._post_init()
        self._add_member(self,message=self._getter_message)
    
    def _add_member(self, member, *, message=None):
        if not message:
            raise ValueError('Please supply a real message!')
        if message in View.messages:
            raise ValueError('Message already exists, please revise!')
        if member.__class__ not in View.__subclasses__():
            raise ValueError('Please supply a View subclass as member!')
        View.messages[message] = member
        if self._set_as_default:
            if '' in View.messages:
                raise ValueError(
                  'Second View set as default, there can only be one default!'
                  )
            View.messages[GET_DEFAULT_VIEW] = member

    def take_control(self, game_data):
        """
        Take control of the screen and present self, then run a loop
        for commands from the player and finally return the call for
        the next View, or END_GAME if player quit/died.
        """
        command = None
        while command != datamanager.END_GAME and command not in View.messages:
            self._update_screen(game_data)
            player_input = self._present()
            command = self._dm.update_data(data=game_data,command=player_input)
        return command
    
    def _present(self):
        """
        Display the screen dict in the console.
        screen = {'char':[],
                  'color':[]}
        """
        x=0
        y=0
        for ch,col in zip(self._screen['char'],self._screen['color']):
            try:
                if col is None:
                    col = 7
                View._console.text(x,y,ch,col)
            except:
                raise TypeError('%s\t%s\t%s\t%s' %(x,y,ch,col))
            x+=1
        return View._console.getchar()
        
    def _post_init(self):
        """
        Subclasses need to override this!
        
        Used by subclasses to:
        1) (required) set their unique getter message
        2) (required) initialize their personal DataManager
        3) (optional) declare themselves as default View
           NOTE: Only one View subclass can be default!
        """
        self._getter_message = ''
        self._dm = datamanager.EmptyManager()
        #self._set_as_default = False
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
        self._dm = datamanager.DataManager()
    
    def _update_screen(self,game_data):
        pass

class SceneView(View):
        
    def _post_init(self):
        self._getter_message = 'get scene view'
        self._dm = datamanager.DataManager()
        self._set_as_default = True

    def _update_screen(self,game_data):
        pass


class CharacterView(View):
        
    def _post_init(self):
        self._getter_message = 'get character view'
        self._dm = datamanager.DataManager()

    def _update_screen(self,game_data):
        pass


class EquipmentView(View):
        
    def _post_init(self):
        self._getter_message = 'get equipment view'
        self._dm = datamanager.DataManager()

    def _update_screen(self,game_data):
        pass


class InventoryView(View):
        
    def _post_init(self):
        self._getter_message = 'get inventory view'
        self._dm = datamanager.DataManager()

    def _update_screen(self,game_data):
        pass
        

def prepare_views():
    """
    Initialize all View subclasses.
    Returns the full message dictionary.
    """
    for subview in View.__subclasses__():
        subview()
    return View.messages

__all__ = [prepare_views,GET_STARTING_VIEW]