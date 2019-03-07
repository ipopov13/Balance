# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:51:49 2019

DataManager classes for the Balance rogue-like RPG

This family of classes creates the screens of the game and passes
 player commands to the AI.
 
Requirements for subclassing (enforced through the metaclass):
    DMs have a unique id_
        have a dictionary mapping keyboard hits to messages defined in
          the ai module
        always have the UNKNOWN_COMMAND in their _commands dictionary,
          also mapping to a unique message constant in the ai module,
          thatis handled by a dedicated handler (different screens can
          have different reactions to an unknown command)
        can set their _is_starter_instance to True, but only ONE
          subclass can do that!
    
Requirements for testing (already covered in the abstract base class):
    DMs refresh the screen using the console
        receive a command from the console
        call AI.execute()
        return a DM instance if the AI sent it in response

@author: IvanPopov
"""
import Console
import ai

UNKNOWN_COMMAND = 'unknown command'

class DMMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if bases != ():
            if cls.id_ == bases[0].id_:
                raise ValueError('You must define a unique id_ string for the'
                                 f' {name} class!')
            if cls.id_ in bases[0]._subclass_instances:
                raise ValueError('You must define a unique id_ string for the'
                                 f' {name} class!')
            if cls._commands == {}:
                raise ValueError('You must define player commands for the '
                                 f'{name} class!')
            if UNKNOWN_COMMAND not in cls._commands:
                raise ValueError(f'{name} must implement the UNKNOWN_COMMAND!')
            if cls._is_starter_instance == True:
                bases[0]._starters += 1
                if bases[0]._starters > 1:
                    raise ValueError('Cannot have two starter subclasses of '
                                     f'{bases[0].__name__}!')
            bases[0].register_subclass(cls)
        return cls


class DataManager(metaclass=DMMeta):
    _console = None
    _ai = None
    _subclass_instances = {}
    _starters = 0
    
    ## These should be redefined in every subclass!
    id_ = 'Make this unique for every subclass!'
    _commands = {}
    _is_starter_instance = False
    
    @classmethod
    def get_starting_dm(cls):
        """Return the DM registered as the starter one"""
        for instance in cls._subclass_instances.values():
            if instance._is_starter_instance:
                return instance
    
    @classmethod
    def register_subclass(cls, subcls):
        cls._subclass_instances[subcls.id_] = subcls()
        
    def __init__(self,personal_message=''):
        if DataManager._console is None:
            DataManager._console = Console.getconsole()
            DataManager._console.title("Balance")
        if DataManager._ai is None:
            DataManager._ai = ai.AI()
        self._screen = {'char':['a'], 'style':[7]}
                
    def take_control(self):
        """The DM activity loop"""
        next_dm = 0
        while not next_dm:
            command = self._present()
            message = self._commands.get(command,
                                         self._commands[UNKNOWN_COMMAND])
            next_dm = self._ai.execute(message)
        return next_dm
    
    def _present(self):
        self._update_screen()
        row_length = 79
        x = 0
        y = 0
        for ch,st in zip(self._screen['char'],self._screen['style']):
            DataManager._console.text(x,y,ch,st)
            x+=1
            if x>row_length:
                x = 0
                y += 1
        return DataManager._console.getchar()
    
    def _update_screen(self):
        """
        Concrete DMs should override this to implement their
        screen updating procedure!
        """
        pass
    
    
class StarterDM(DataManager):
    id_ = 'starter'
    _is_starter_instance = True
    _commands = {'n':ai.STARTER_NEW_GAME,
                 'l':ai.STARTER_LOAD_GAME,
                 UNKNOWN_COMMAND:ai.STARTER_UNKNOWN}
    
    def _update_screen(self):
        pass