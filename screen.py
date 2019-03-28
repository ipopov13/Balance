# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 09:11:30 2019

Screen class for the Balance rogue-like RPG.

@author: IvanPopov
"""
import Console
import msvcrt
from copy import deepcopy
import config
import constants as const


class Screen:
    _console = Console.getconsole()
    
    def __init__(self):
        settings = config.get_settings(key='screen')
        self._width = settings.getint('width')
        self._height = settings.getint('height')
        self._pixels = {(x,y):Pixel() for x in range(self._width) \
                                    for y in range(self._height)}
        self._text = {}
        self._presented_text = {}
        settings = config.get_settings()
        Screen._console.title(settings['name'])
        
    def load_data(self,template):
        """Load a styled text dictionary from assets"""
        ## Do validation of input
        for coords,text in template.items():
            if not (0 <= text.get('style',0) <= 255):
                raise ValueError("Styles can only be in the range 0-255!"
                                 f" Got '{text['style']}'")
            if len(text['text']) > self._width:
                raise ValueError("A Screen object cannot have "
                                 f"more than {self._width} columns!")
            if len(text['text'])+coords[0] > self._width:
                raise ValueError("Template string will run off screen!")
            if coords[1] > self._height:
                raise ValueError("A Screen object cannot have "
                                 f"more than {self._height} rows!")
            self._text[coords] = text
                    
    def attach(self,*,x=None,y=None,presentable=None):
        """Set pixel presentable"""
        try:
            self._pixels[(x,y)].attach(presentable)
        except KeyError:
            raise ValueError("Invalid coordinates for attach()!")
    
    def attach_scene(self,*,x=None,y=None,scene=None):
        for (x1,y1),presentable in scene.tiles():
            try:
                self._pixels[(x+x1,y+y1)].attach(presentable)
            except KeyError:
                raise ValueError("Invalid coordinates for attach_scene()!")
            
    def reset(self):
        """Clear the contents of the screen"""
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
        for coords,pixel in self._get_changed_pixels():
            pixel.is_presented = True
            self._console.text(*coords,*pixel.data)
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
            #self._console.text(30,10,f'#{a.decode()}#')
            try:
                return a.decode()
            except UnicodeDecodeError:
                pass
                
    def _get_changed_pixels(self):
        for coords,pixel in self._pixels.items():
            if pixel.is_active and not pixel.is_presented:
                yield (coords,pixel)
    
    
class Pixel:
    
    def __init__(self):
        self.is_presented = True
        self._data = {'char':const.DEFAULT_PIXEL_CHAR,
                      'style':const.DEFAULT_PIXEL_STYLE}
        self._presentable = None
       
    @property
    def data(self):
        return [self._data['char'], self._data['style']]
       
    @property
    def is_active(self):
        return self._presentable is not None
        
    def attach(self,presentable):
        """Attach a presentable object to update from"""
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
        """Receive latest presentable data"""
        self._data = visual
        self.is_presented = False