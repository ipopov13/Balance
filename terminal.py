# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 09:11:30 2019

Terminal class for the Balance rogue-like RPG framework.

@author: IvanPopov
"""
import Console
import msvcrt
from copy import deepcopy
import config
import constants as const


class Terminal:
    _console = Console.getconsole()
    
    def __init__(self):
        settings = config.get_settings(key='terminal')
        self._width = settings.getint('width')
        self._height = settings.getint('height')
        self._pixels = {}
        self._text = {}
        self._presented_text = {}
        settings = config.get_settings()
        Terminal._console.title(settings['name'])
        
    def load_data(self,template):
        """Load a styled text dictionary from assets"""
        ## Do validation of input
        for coords,text in template.items():
            if not (0 <= text.get('style',0) <= 255):
                raise ValueError("Styles can only be in the range 0-255!"
                                 f" Got '{text['style']}'")
            if len(text['text']) > self._width:
                raise ValueError("A Terminal object cannot have "
                                 f"more than {self._width} columns!")
            if len(text['text'])+coords[0] > self._width:
                raise ValueError("Template string will run off screen!")
            if coords[1] > self._height:
                raise ValueError("A Terminal object cannot have "
                                 f"more than {self._height} rows!")
            self._text[coords] = text
    
    def attach_scene(self,*,x=None,y=None,scene=None):
        for (x1,y1),presentable in scene.tiles():
            if x is None or y is None or \
                x < 0 or y < 0 or \
                x+x1>= self._width or y+y1>=self._height:
                raise ValueError("Invalid coordinates for attach_scene"
                                 f"{(x,y)}, scene is out of bounds.")
            self._pixels.setdefault((x+x1,y+y1), Pixel(self)) \
                        .attach(presentable)
            
    def reset(self):
        """Clear the contents of the terminal"""
        for pixel in self._pixels.values():
            pixel.reset()
        self._text = {}
        self._presented_text = {}
        self._console.page()
            
    def present(self):
        """
        Update the console with the current screen information
        
        Additionally store that information in order to implement minimum
        change needed.
        """
        for coords,text in self._text.items():
            if self._presented_text.get(coords,None) != self._text[coords]:
                self._console.text(*coords,
                                   text['text'],
                                   text.get('style',const.DEFAULT_PIXEL_STYLE))
        self._presented_text = deepcopy(self._text)
            
    def get_command(self):
        """Return a command from the console"""
        while True:
            a=msvcrt.getch()
            try:
                return a.decode()
            except UnicodeDecodeError:
                pass
                
    def update(self,pixel):
        """Receive data from pixel"""
        pixel_found = False
        for coords in self._pixels:
            if self._pixels[coords] == pixel:
                pixel_found = True
                break
        if pixel_found:
            self.load_data({coords:pixel.data})
        else:
            raise ValueError("Unknown pixel updating the terminal!")
    
    
class Pixel:
    
    def __init__(self, terminal):
        self._terminal = terminal
        self.data = {'text':const.DEFAULT_PIXEL_CHAR,
                      'style':const.DEFAULT_PIXEL_STYLE}
        self._presentable = None
        
    def attach(self,presentable):
        """
        Attach a presentable object to update from
        
        NOTE: The presentable should call the pixel.update method
        on attaching!
        """
        presentable.pixel = self
        self._presentable = presentable
    
    def reset(self):
        """Clear presentable"""
        try:
            self._presentable.pixel = None
        except AttributeError:
            pass
        self._presentable = None
        self.is_presented = True
        
    def update(self,visual):
        """Translate latest visual data to the terminal"""
        self.data = visual
        self._terminal.update(self)