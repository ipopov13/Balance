# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 09:11:30 2019

Screen class for the Balance rogue-like RPG.

@author: IvanPopov
"""

class Screen:
    
    def __init__(self,*,chars='',fores=None,backs=None):
        self._x_limit = 79
        self._y_limit = 25
        chars = chars.split('\n')
        if fores is None:
            fores = []
        else:
            fores = fores.split('\n')
        if backs is None:
            backs = []
        else:
            backs = backs.split('\n')
        ## Do validation of input
        for array in [chars,fores,backs]:
            if array:
                if len(array) > self._y_limit:
                    raise ValueError("A Screen object cannot have "
                                     "more than 25 rows!")
                if max([len(x) for x in array]) > self._x_limit:
                    raise ValueError("A Screen object cannot have "
                                     "more than 79 columns!")
        ## Build data dictionary
        self._data = {}
        for x in range(self._x_limit):
            for y in range(self._y_limit):
                try:
                    fore = self._normalize_style(fores[y][x])
                except IndexError:
                    fore = 0
                try:
                    back = self._normalize_style(backs[y][x])
                except IndexError:
                    back = 0
                try:
                    char = chars[y][x]
                except IndexError:
                    char = ' '
                self._change_pixel(x,y,char,fore,back)
                    
    def _normalize_style(self,style_char):
        style = ord(style_char)-ord('a')
        if not 0 <= style <= 15:
            raise ValueError("Invalid character for foreground or "
                             "background style! Only characters in "
                             "the range [a,p] are allowed.")
        return style
    
    def _change_pixel(self,x,y,char,fore,back):
        ## Only store visible data
        if (char,fore,back) != (' ',0,0):
            self._data[(x,y)] = (char,fore+16*back)
                
    def get_pixels(self):
        """Yield the state of all pixels in range"""
        for y in range(self._y_limit):
            for x in range(self._x_limit):
                try:
                    yield (x,y,*self._data[(x,y)])
                except KeyError:
                    yield (x,y,' ',0)
                    
    def set_pixel(self,*,x=None,y=None,char=' ',fore='a',back='a'):
        if x is not None and y is not None:
            fore = self._normalize_style(fore)
            back = self._normalize_style(back)
            self._change_pixel(x,y,char,fore,back)