# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 09:11:30 2019

Screen class for the Balance rogue-like RPG.

@author: IvanPopov
"""
import Console

DEFAULT_STYLE = 7
DEFAULT_CHAR = ' '

class Screen:
    _console = Console.getconsole()
    
    def __init__(self):
        self._x_limit = 79
        self._y_limit = 25
        self._pixels = {(x,y):Pixel() for x in range(self._x_limit) \
                                    for y in range(self._y_limit)}
        self._text = {}
        self._presented_text = {}
        Screen._console.title('Balance')
        
    def load_data(self,template):
        """Load a styled text dictionary from assets"""
        ## Do validation of input
        for coords,text in template.items():
            if not (0 <= text.get('style',0) <= 255):
                raise ValueError("Styles can only be in the range 0-255!"
                                 f" Got '{text['style']}'")
            if len(text['text']) > self._x_limit:
                raise ValueError("A Screen object cannot have "
                                 f"more than {self._x_limit} columns!")
            if len(text['text'])+coords[0] > self._x_limit:
                raise ValueError("Template string will run off screen!")
            if coords[1] > self._y_limit:
                raise ValueError("A Screen object cannot have "
                                 f"more than {self._y_limit} rows!")
            self._text[coords] = text
                    
    def attach(self,*,x=None,y=None,presentable=None):
        """Set pixel presentable"""
        try:
            self._pixels[(x,y)].attach(presentable)
        except KeyError:
            raise ValueError("Invalid coordinates for attach()!")
    
    def attach_scene(self,*,x=None,y=None,scene=None):
        for (x1,y1),presentable in scene.items():
            try:
                self._pixels[(x+x1,y+y1)].attach(presentable)
            except KeyError:
                raise ValueError("Invalid coordinates for attach_scene()!")
            
    def update_pixels(self):
        """Update all pixels"""
        for pixel in self._pixels.values():
            if pixel.is_active:
                pixel.update()
            
    def reset(self):
        """Clear the contents of the screen"""
        for pixel in self._pixels.values():
            pixel.reset()
        self._text = {}
        self._presented_text = {}
            
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
                self._console.text(*coords,text['text'],text.get('style',
                                                             DEFAULT_STYLE))
                self._presented_text[coords] = self._text[coords].copy()
            
    def get_command(self):
        """Return a single character command from the console"""
        return self._console.getchar().decode()
                
    def _get_changed_pixels(self):
        for coords,pixel in self._pixels.items():
            if pixel.is_active and not pixel.is_presented:
                yield (coords,pixel)
    
    
class Pixel:
    
    def __init__(self):
        self.is_presented = True
        self._data = {'char':DEFAULT_CHAR,
                      'style':DEFAULT_STYLE}
        self._presentable = None
       
    @property
    def data(self):
        return [self._data['char'], self._data['style']]
       
    @property
    def is_active(self):
        return self._presentable is not None
        
    def attach(self,presentable):
        """Attach a presentable object to update from"""
        if not hasattr(presentable,'present'):
            raise TypeError('Pixel can only be attached to a '
                            f'presentable object! Got {presentable}')
        self._presentable = presentable
    
    def reset(self):
        """Clear presentable"""
        self._presentable = None
        self.is_presented = True
        
    def update(self):
        """Get latest presentable data"""
        if self._presentable is not None:
            old_data = self._data.copy()
            self._data = self._presentable.present()
            if self._data != old_data:
                self.is_presented = False
        else:
            raise IOError("Trying to update a pixel with no presentable!")