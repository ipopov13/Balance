# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 09:11:30 2019

Screen class for the Balance rogue-like RPG.

@author: IvanPopov
"""

class Screen:
    _default_char = ' '
    _default_fore = 7
    _default_back = 0
    
    def __init__(self,*,chars='',fores='',backs=''):
        self._x_limit = 79
        self._y_limit = 25
        
    def load_template(self,*,chars='',fores='',backs=''):
        for array in [chars,fores,backs]:
            if array.count('\n') > self._y_limit - 1:
                raise ValueError("A Screen object cannot have "
                                 f"more than {self._y_limit} rows!")
        chars = chars.split('\n')
        fores = fores.split('\n')
        backs = backs.split('\n')
        ## Do validation of input
        for line in chars+fores+backs:
            if len(line) > self._x_limit:
                raise ValueError("A Screen object cannot have "
                                 f"more than {self._x_limit} columns!")
        ## Build data dictionary
        self._data = {}
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
                self.set_pixel(x=x,y=y,char=char,fore=fore,back=back)
                    
    def _normalize_style(self,style_char,is_foreground=False):
        defaults = [Screen._default_back, Screen._default_fore]
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
            return Screen._default_char
        elif not isinstance(char,str):
            raise TypeError("Screen char must be a single character string!")
        elif len(char)!=1:
            raise ValueError("Screen char must be of length 1!")
        return char
                
    def _get_pixels(self):
        """Yield the state of all pixels in range"""
        for y in range(self._y_limit):
            for x in range(self._x_limit):
                try:
                    d = self._data[(x,y)]
                    yield (x,y,d['char'],d['fore']+16*d['back'])
                except KeyError:
                    pass
#                    yield (x,y,Screen._default_char,
#                           Screen._default_fore+ 16*Screen._default_back)
                    
    def set_pixel(self,*,x=None,y=None,char=None,fore=None,back=None):
        """
        Set pixel information
        
        If only coords are given and pixel exists, deletes it
        If pixel does not exist, creates it
        """
        if x is not None and y is not None:
            if 0<=x<=self._x_limit and 0<=y<=self._y_limit:
                if (x,y) not in self._data:
                    self._data[(x,y)] = {'char':Screen._default_char,
                                         'fore':Screen._default_fore,
                                         'back':Screen._default_back}
                change = False
                if char is not None:
                    self._data[(x,y)]['char'] = self._normalize_char(char)
                    change = True
                if fore is not None:
                    self._data[(x,y)]['fore'] = self._normalize_style(fore)
                    change = True
                if back is not None:
                    self._data[(x,y)]['back'] = self._normalize_style(back)
                    change = True
                if not change:
                    self._data.pop((x,y))
            else:
                raise ValueError("Coordinates for set_pixel must be in range: "
                                 f"x=[0,{self._x_limit}], "
                                 f"y=[0,{self._y_limit}]!")
        else:
            raise ValueError("Both coordinates must be used for set_pixel()!")