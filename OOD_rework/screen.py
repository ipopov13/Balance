# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 09:11:30 2019

Screen class for the Balance rogue-like RPG.

@author: IvanPopov
"""
import Console

class Screen:
    _console = Console.getconsole()
    
    def __init__(self):
        self._x_limit = 79
        self._y_limit = 25
        self._data = {(x,y):Pixel() for x in range(self._x_limit) \
                                    for y in range(self._y_limit)}
        Screen._console.title('Balance')
        
    def load_template(self,*,chars='',fores='',backs=''):
        ## Do validation of input
        for array in [chars,fores,backs]:
            if array.count('\n') > self._y_limit - 1:
                raise ValueError("A Screen object cannot have "
                                 f"more than {self._y_limit} rows!")
        chars = chars.split('\n')
        fores = fores.split('\n')
        backs = backs.split('\n')
        for line in chars+fores+backs:
            if len(line) > self._x_limit:
                raise ValueError("A Screen object cannot have "
                                 f"more than {self._x_limit} columns!")
        ## Build data dictionary
        for x in range(self._x_limit):
            for y in range(self._y_limit):
                try:
                    fore = fores[y][x]
                except IndexError:
                    fore = None
                try:
                    back = backs[y][x]
                except IndexError:
                    back = None
                try:
                    char = chars[y][x]
                except IndexError:
                    char = None
                self._data[(x,y)].update(char=char,fore=fore,back=back)
                
    def _get_changed_pixels(self):
        for coords,pixel in self._data.items():
            if not pixel.is_presented:
                yield (coords,pixel)
                    
    def set_pixel(self,*,x=None,y=None,char=None,fore=None,back=None):
        """
        Set pixel information
        """
        if x is not None and y is not None:
            if 0<=x<=self._x_limit and 0<=y<=self._y_limit:
                ## Update pixel at (x,y)
                self._data[(x,y)].update(char=char,fore=fore,back=back)
            else:
                raise ValueError("Coordinates for set_pixel must be in range: "
                                 f"x=[0,{self._x_limit}], "
                                 f"y=[0,{self._y_limit}]!")
        else:
            raise ValueError("Both coordinates must be used for set_pixel()!")
            
    def present(self):
        """
        Update the console with the current screen information
        
        Additionally store that information in order to implement minimum
        change needed.
        """
        for coords,pixel in self._get_changed_pixels():
            pixel.is_presented = True
            self._console.text(*coords,*pixel.data)
            
    def get_command(self):
        """Return a single character command from the console"""
        return self._console.get_char().decode()
    
    
class Pixel:
    _default_char = ' '
    _default_fore = 7
    _default_back = 0
    
    def __init__(self):
        self.is_presented = False
        self._data = {'char':Pixel._default_char,
                     'fore':Pixel._default_fore,
                     'back':Pixel._default_back}
       
    @property
    def data(self):
        return [self._data['char'],
                self._data['fore'] + 16*self._data['back']]
        
    def update(self,*,char=None,fore=None,back=None):
        new_char = self._normalize_char(char)
        if char is not None and new_char != self._data['char']:
            self._data['char'] = new_char
            self.is_presented = False
        new_fore = self._normalize_style(fore, is_foreground = True)
        if fore is not None and new_fore != self._data['fore']:
            self._data['fore'] = new_fore
            self.is_presented = False
        new_back = self._normalize_style(back)
        if back is not None and new_back != self._data['back']:
            self._data['back'] = new_back
            self.is_presented = False
        if (char,fore,back) == (None,None,None):
            if self._data != {'char':Pixel._default_char,
                              'fore':Pixel._default_fore,
                              'back':Pixel._default_back}:
                self.is_presented = False
                self._data = {'char':Pixel._default_char,
                              'fore':Pixel._default_fore,
                              'back':Pixel._default_back}
                    
    def _normalize_style(self,style_char,is_foreground=False):
        defaults = [Pixel._default_back, Pixel._default_fore]
        if style_char is None:
            style = defaults[is_foreground]
        else:
            style = ord(style_char)-ord('a')
        if not 0 <= style <= 15:
            raise ValueError("Invalid character for foreground or "
                             "background style! Only characters in "
                             "the range [a,p] are allowed.")
        return style
    
    def _normalize_char(self, char):
        if char is None:
            return Pixel._default_char
        elif not isinstance(char,str):
            raise TypeError("Screen char must be a single character string!")
        elif len(char)!=1:
            raise ValueError("Screen char must be of length 1!")
        return char