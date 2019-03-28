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
from terminal import Terminal
from assets import StaticScreens
import constants as const


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
            if const.UNKNOWN_COMMAND not in cls._commands:
                raise ValueError(f'{name} must implement the UNKNOWN_COMMAND!')
            if cls._is_starter_instance == True:
                bases[0]._starters += 1
                if bases[0]._starters > 1:
                    raise ValueError('Cannot have two starter subclasses of '
                                     f'{bases[0].__name__}!')
            bases[0].register_subclass(cls)
        return cls


class DataManager(metaclass=DMMeta):
    _terminal = Terminal()
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
        self._terminal.reset()
        DataManager._terminal.load_data(self._screen_template)
        DataManager._terminal.load_data(self._screen_details)
        ## Handle commands
        refresh = False
        while next_dm == self.id_ and not refresh:
            DataManager._terminal.load_data(self._dynamic_screen_content)
            DataManager._terminal.present()
            command =  DataManager._terminal.get_command()
            message = self._commands.get(command,
                                         self._commands[const.UNKNOWN_COMMAND])
            next_dm,refresh = self._ai.execute(message)
            if next_dm == const.SILENT_UNKNOWN:
                next_dm = self.id_
        return DataManager._subclass_instances[next_dm]
    
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
        screen initialization procedure by returning static session
        specific data to lay on top of the template, as well as
        attaching objects like the current scene to screen pixels!
        """
        return {}
    
    
class SceneDM(DataManager):
    id_ = const.GET_SCENE
    _screen_template = StaticScreens.scene
    _is_starter_instance = False
    _commands = {const.GO_E:const.MOVE+':'+const.GO_E,
                 const.GO_S:const.MOVE+':'+const.GO_S,
                 const.GO_W:const.MOVE+':'+const.GO_W,
                 const.GO_N:const.MOVE+':'+const.GO_N,
                 const.GO_NE:const.MOVE+':'+const.GO_NE,
                 const.GO_SE:const.MOVE+':'+const.GO_SE,
                 const.GO_SW:const.MOVE+':'+const.GO_SW,
                 const.GO_NW:const.MOVE+':'+const.GO_NW,
                 const.STAY:const.MOVE+':'+const.STAY,
                 const.UNKNOWN_COMMAND:const.SILENT_UNKNOWN}
    
    @property
    def _screen_details(self):
        self._screen.attach_scene(x=1,y=1,
                                  scene=self._ai.game_data.current_scene)
        return {}
    
    @property
    def _dynamic_screen_content(self):
        return {}
    
    
class StarterDM(DataManager):
    id_ = const.GET_MENU
    _screen_template = StaticScreens.starter
    _is_starter_instance = True
    _commands = {const.N_KEY:const.NEW_GAME,
                 const.L_KEY:const.LOAD_GAME,
                 const.Q_KEY:const.QUIT_GAME,
                 const.UNKNOWN_COMMAND:const.SILENT_UNKNOWN}
    
    
class ModifierSelectionDM(DataManager):
    id_ = const.GET_MODIFIER_SELECTION
    _screen_template = {}
    _is_starter_instance = False
    _commands = {const.Q_KEY:const.QUIT_GAME,
                 const.UNKNOWN_COMMAND:const.SILENT_UNKNOWN}
    
    @property
    def _screen_details(self):
        modifier,mod_values = self._ai.player.next_modifier()
        mod_string = ''
        for i,value in enumerate(mod_values,1):
            mod_string += f'        {i}) {value}\n'
            self._commands[str(i)] = const.SELECT_MODIFIER+':'+value
        return {(0,i):{'text':t} for (i,t) in enumerate(f'''
    Choose a {modifier} for your character:
{mod_string}'''.split('\n'))}
    
    
class StatSelectionDM(DataManager):
    id_ = const.GET_STAT_SELECTION
    _screen_template = {}
    _is_starter_instance = False
    _commands = {const.Q_KEY:const.QUIT_GAME,
                 const.RETURN_KEY:const.SILENT_UNKNOWN,
                 const.UNKNOWN_COMMAND:const.SILENT_UNKNOWN}
    
    @property
    def _screen_details(self):
        self._stats = self._ai.player.next_stat_selection()
        stat_string = ''
        basic_line = '        {:<%d}({})-      +({})\n'
        self._max_len = max([len(stat) for stat in self._stats])+3
        for i,stat in enumerate(self._stats[1:],ord('A')):
            line = basic_line %(self._max_len)
            stat_string += line.format(stat.capitalize(),chr(i+32),chr(i))
            self._commands[chr(i)] = const.ALTER_STAT+f':{stat}:1'
            self._commands[chr(i+32)] = const.ALTER_STAT+f':{stat}:-1'
        return {(0,i):{'text':t} for (i,t) in enumerate(f'''
    Modify your stats:    (-/+)
{stat_string}
        
        Points left:'''.split('\n'))}
    
    @property
    def _dynamic_screen_content(self):
        content = {}
        stat_column = 8+self._max_len+6
        for i,stat in enumerate(self._stats[1:],2):
            content[(stat_column,i)] = \
                {'text':f'{self._ai.player.get_stat(stat):>3}',
                 'style':10}
        content[(stat_column,i+3)] = \
            {'text':f'{self._ai.player.get_stat(self._stats[0]):>3}',
             'style':10}
        final_row = len(self._stats)+4
        if self._ai.player.check_triggers(self._stats[0]) \
            == const.READY_TO_CONTINUE:
            content[(4,final_row)] = {
                    'text':'Press ENTER to continue!','style':13}
            self._commands[const.RETURN_KEY] = const.NEW_GAME
        else:
            content[(4,final_row)] = {
                    'text':'                        '}
            self._commands[const.RETURN_KEY] = const.SILENT_UNKNOWN
        return content