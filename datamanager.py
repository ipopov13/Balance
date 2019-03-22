# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:51:49 2019

DataManager classes for the Balance rogue-like RPG

This family of classes creates the screens of the game and passes
 player commands to the AI. DMs are singletons. At subclass definition
 they are entered into a dictionary in the abstract parent class and
 are returned from there whenever they are needed.
 
Order of DM actions:
0) The DM refreshes its screen and presents it in the console, getting
    a player command back.
1) The DM translates the raw command into a message.
2) The DM calls AI.execute(message) for a full update of the game data
3) The AI sends back 0 or a DM ID if screens have changed.
4) if a DM ID was returned the active DM returns the respective subclass
    instance, otherwise it repeats the loop.
    
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
import ai
from screen import Screen
from assets import StaticScreens

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
            if cls._screen_template == bases[0]._screen_template:
                raise ValueError('You must define a screen template for the '
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
    _screen = Screen()
    _ai = ai.AI()
    _subclass_instances = {None:None}
    _starters = 0
    
    ## These should be redefined in every subclass!
    id_ = 'Make this unique for every subclass!'
    _screen_template = StaticScreens.tester
    _commands = {}
    _is_starter_instance = False
    
    @classmethod
    def get_starting_dm(cls):
        """Return the DM registered as the starter one"""
        for instance in cls._subclass_instances.values():
            if instance is not None and instance._is_starter_instance:
                return instance
    
    @classmethod
    def register_subclass(cls, subcls):
        cls._subclass_instances[subcls.id_] = subcls()
        
    def __init__(self):
        pass
        
    def take_control(self):
        """The DM activity loop"""
        next_dm = self.id_
        ## Templating the screen
        self._screen.reset()
        DataManager._screen.load_data(self._screen_template)
        DataManager._screen.load_data(self._screen_details)
        ## Handle commands
        refresh = False
        while next_dm == self.id_ and not refresh:
            self._update_screen()
            DataManager._screen.present()
            command =  DataManager._screen.get_command()
            message = self._commands.get(command,
                                         self._commands[UNKNOWN_COMMAND])
            next_dm,refresh = self._ai.execute(message)
            if next_dm == ai.SILENT_UNKNOWN:
                next_dm = self.id_
        return DataManager._subclass_instances[next_dm]
    
    def _update_screen(self):
        DataManager._screen.load_data(self._screen_content)
        DataManager._screen.update_pixels()
    
    @property
    def _dynamic_screen_content(self):
        """
        Concrete DMs should override this to implement their dynamic
        screen data presentation by extracting text from
        DataManager._ai.game_data. This method should return a
        dictionary of (x,y):{'text':..., 'style':...},
        where (x,y) are coords of the beginning of the text,
        text is a single line string, and style is an integer in the
        range from 0 to 255. See Console guide for info on styles.
        """
        return {}
    
    @property
    def _screen_details(self):
        """
        Concrete DMs should override this to implement their
        screen initialization procedure, adding static session specific
        data from DataManager._ai.game_data on top of the template, as
        well as attaching world.current_scene to screen pixels!
        """
        return {}
    
    
class SceneDM(DataManager):
    id_ = ai.GET_SCENE
    _screen_template = StaticScreens.scene
    _is_starter_instance = False
    _commands = {UNKNOWN_COMMAND:ai.SILENT_UNKNOWN}
    
    @property
    def _screen_details(self):
        return {}
    
    @property
    def _dynamic_screen_content(self):
        return {}
    
    
class StarterDM(DataManager):
    id_ = 'starter'
    _screen_template = StaticScreens.starter
    _is_starter_instance = True
    _commands = {'n':ai.NEW_GAME,
                     'l':ai.STARTER_LOAD_GAME,
                     'q':ai.QUIT_GAME,
                     UNKNOWN_COMMAND:ai.SILENT_UNKNOWN}
    
    
class ModifierSelectionDM(DataManager):
    id_ = ai.GET_MODIFIER_SELECTION
    _screen_template = {}
    _is_starter_instance = False
    _commands = {'q':ai.QUIT_GAME,
                 UNKNOWN_COMMAND:ai.SILENT_UNKNOWN}
    
    @property
    def _screen_details(self):
        modifier,mod_values = self._ai.next_modifier()
        mod_string = ''
        for i,value in enumerate(mod_values,1):
            mod_string += f'        {i}) {value}\n'
            self._commands[str(i)] = ai.SELECT_MODIFIER+modifier+value
        return {(0,i):{'text':t} for (i,t) in enumerate(f'''
    Choose a {modifier} for your character:
{mod_string}'''.split('\n'))}
    
    
class StatSelectionDM(DataManager):
    id_ = ai.GET_STAT_SELECTION
    _screen_template = {}
    _is_starter_instance = False
    _commands = {'q':ai.QUIT_GAME,
                 '\r':ai.SILENT_UNKNOWN,
                 UNKNOWN_COMMAND:ai.SILENT_UNKNOWN}
    
    @property
    def _screen_details(self):
        self._stats = self._ai.next_stat_selection()
        stat_string = ''
        self._max_len = max([len(stat) for stat in self._stats])+3
        for i,stat in enumerate(self._stats,ord('A')):
            stat_string += ('        {:<%d}({})-      +({})\n' \
                            %(self._max_len)).format(stat,chr(i+32),chr(i))
            self._commands[chr(i)] = ai.ALTER_STAT+f'{stat}:1'
            self._commands[chr(i+32)] = ai.ALTER_STAT+f'{stat}:-1'
        return {(0,i):{'text':t} for (i,t) in enumerate(f'''
    Modify your stats:    (-/+)
{stat_string}
        
        Points left:'''.split('\n'))}
    
    @property
    def _dynamic_screen_content(self):
        content = {}
        stat_column = 8+self._max_len+6
        for i,stat in enumerate(self._stats,2):
            if stat == self._stats[-1]:
                i += 1
            content[(stat_column,i)] = {'text':str(self._ai.get_stat(stat)),
                                        'style':10}
        final_row = len(self._stats)+4
        if self._ai.check_triggers(self._stats[-1]):
            content[(4,final_row)] = {
                    'text':'Press ENTER to continue!','style':13}
            self._commands['\r'] = ai.GET_SCENE
        else:
            content[(4,final_row)] = {
                    'text':'                        '}
            self._commands['\r'] = ai.SILENT_UNKNOWN
        return content