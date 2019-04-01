# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:51:49 2019

Screen classes for the Balance rogue-like RPG framework.

This family of classes creates the screens of the game and translates
 player commands into messages understandable for the AI. Screens are
 singletons. At subclass definition they are entered into a dictionary
 in the abstract parent class and are returned from there whenever
 they are needed.

Order of Screen actions:
0) The Screen refreshes its terminal and presents it, getting
a player command back.
1) The Screen translates the raw command into a message.
2) The Screen calls AI.execute(message) for a full update of the game data
3) if a Screen ID was returned or the AI requested a refresh the active
    Screen returns the respective subclass ID (its own, if a refresh is
    needed) to be called by the main loop.
4) if the same ID is returned the Screen gets another command from the
 terminal and the process repeats.

Requirements for subclassing (enforced through the metaclass):
1) Screens have a unique id_
2) have a dictionary mapping keyboard hits to messages defined in
    the AI module
3) always have the UNKNOWN_COMMAND in their _commands dictionary,
    also mapping to a unique message constant in the ai module,
    (different screens can have different reactions to an unknown
    command)
4) can set their _is_starter_instance to True, but only ONE
    subclass can do that!

Requirements for testing (already covered in the abstract base class):
1) Screens refresh the screen using the console
2) receive a command from the console
3) call AI.execute()
4) return a Screen ID if the AI sent it in response

@author: IvanPopov
"""
import ai
from terminal import Terminal
from assets import StaticScreens
import constants as const
import config


class ScreenMeta(type):
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


class Screen(metaclass=ScreenMeta):
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
    def get_starting_screen(cls):
        """Return the Screen registered as the starter one"""
        for instance in cls._subclass_instances.values():
            if instance is not None and instance._is_starter_instance:
                return instance
    
    @classmethod
    def register_subclass(cls, subcls):
        cls._subclass_instances[subcls.id_] = subcls()
        
    def __init__(self):
        pass
        
    def take_control(self):
        """The Screen activity loop"""
        next_screen = self.id_
        ## Templating the screen
        self._terminal.reset()
        Screen._terminal.load_data(self._screen_template)
        Screen._terminal.load_data(self._screen_details)
        ## Handle commands
        refresh = False
        while next_screen == self.id_ and not refresh:
            Screen._terminal.load_data(self._dynamic_screen_content)
            Screen._terminal.present()
            command =  Screen._terminal.get_command()
            message = self._commands.get(command,
                                         self._commands[const.UNKNOWN_COMMAND])
            next_screen,refresh = self._ai.execute(message)
            if next_screen == const.SILENT_UNKNOWN:
                next_screen = self.id_
        return Screen._subclass_instances[next_screen]
    
    def _format_number(self,vis):
        content = {}
        x,y = [int(x) for x in vis['scene_pos'].split(',')]
        content[(x,y)] = {'text':vis['label'], 
                          'style':vis.getint('label_style')}
        space_left = vis.getint('total_length') - len(vis['label'])
        value_text = str(self._ai.player.get_stat(vis.name))[:space_left]
        content[(x+len(vis['label']),y)] = \
            {'text':value_text.rjust(space_left,' '),
             'style':vis.getint('value_style')}
        return content
        
    def _format_gauge(self,vis):
        content = {}
        x,y = [int(coord) for coord in vis['scene_pos'].split(',')]
        total_length = vis.getint('total_length')
        # Set up the gauge brackets
        content[(x,y)] = {'text':'['}
        content[(x+total_length-1,y)] = {'text':']'}
        # Define values and breakpoint index
        value = self._ai.player.get_stat(vis.name)
        max_value = self._ai.player.get_max_stat(vis.name)
        breaks = [int(style) for style in vis['breakpoints'].split(',') if style]
        divisor = vis.getint('divisor')
        if breaks:
            bracket = len([bp for bp in breaks if bp<value])
        elif divisor:
            bracket = (value // divisor) % 2
            value = value % divisor
            max_value = divisor-1
        else:
            bracket = 0
        # Preload properties
        fill = [int(style) for style in \
                vis['gauge_fills'].split(',')][bracket]
        # Get the gauge measurement
        fill_length = round(value / max_value * (total_length-2))
        # Define the overlay text (marker, status or none)
        overlay = ''
        if vis['markers']:
            # Adjust marker position
            overlay = ' '*(fill_length-1) + vis['markers'][bracket]
        elif vis['statuses']:
            # Fix status length if too long. -2 for the brackets
            overlay = vis['statuses'].split(',')[bracket][:total_length-2]
            overlay = overlay.center(total_length-2, ' ')
        overlay_style = 0
        if overlay:
           overlay_style = [int(style) for style in \
                      vis['overlay_styles'].split(',')][bracket]
        # Define gauge contents
        # Split the whole gauge into single character labels
        # for minimal refreshing
        for x_ in range(x+1,x+1+total_length-2):
            if vis.getboolean('perma_fill'):
                fill_ = fill
            else:
                fill_ = fill if x_<=x+fill_length else 0
            content[(x_,y)] = {'text':overlay[x_-x-1:x_-x] or ' ',
                               'style':fill_+overlay_style}
        return content
    
    @property
    def _dynamic_screen_content(self):
        """
        Concrete Screens should override this to implement their
        dynamic screen data presentation by extracting text from
        Screen._ai.game_data. This method should return a
        dictionary of (x,y):{'text':..., 'style':...},
        where (x,y) are coords of the beginning of the text,
        text is a single line string, and style is an integer in the
        range from 0 to 255. See Console guide for info on styles.
        """
        return {}
    
    @property
    def _screen_details(self):
        """
        Concrete Screens should override this to implement their
        screen initialization procedure by returning static session
        specific data to lay on top of the template, as well as
        attaching objects like the current scene to terminal pixels!
        """
        return {}
    
    
class Scene(Screen):
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
        self._terminal.attach_scene(x=20,y=2,
                                    scene=self._ai.game_data.current_scene)
        content = {(0,0):{'text':f'{self._ai.game_data._current_scene_key}'}}
        visuals = config.get_config(section='scene')
        # Integrate the visuals
        for vis in visuals:
            if vis['type'] == const.NUMBER_VISUAL:
                content.update(self._format_number(vis))
            elif vis['type'] == const.GAUGE_VISUAL \
                or vis['type'] == const.MODULO_GAUGE_VISUAL:
                content.update(self._format_gauge(vis))
            else:
                raise ValueError (f"Unknown visual type:{vis['type']}")
        return content
    
    @property
    def _dynamic_screen_content(self):
        content = {}
        visuals = config.get_config(section='scene')
        # Integrate the visuals
        for vis in visuals:
            if vis['type'] == const.NUMBER_VISUAL:
                content.update(self._format_number(vis))
            elif vis['type'] == const.GAUGE_VISUAL \
                or vis['type'] == const.MODULO_GAUGE_VISUAL:
                content.update(self._format_gauge(vis))
            else:
                raise ValueError (f"Unknown visual type:{vis['type']}")
        return content
    
    
class Menu(Screen):
    id_ = const.GET_MENU
    _screen_template = StaticScreens.starter
    _is_starter_instance = True
    _commands = {const.N_KEY:const.NEW_GAME,
                 const.L_KEY:const.LOAD_GAME,
                 const.Q_KEY:const.QUIT_GAME,
                 const.UNKNOWN_COMMAND:const.SILENT_UNKNOWN}
    
    
class ModifierSelection(Screen):
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
    
    
class StatDistribution(Screen):
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