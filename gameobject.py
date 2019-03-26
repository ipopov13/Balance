# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:00:45 2019

GameObject factories for the Balance rogue-like RPG

Called by the handlers to create all game objects.

Each subfamily has a metaclass that handles automatic registration of
 subclasses and loading from the ini files.

@author: IvanPopov
"""
import config


class GameObject:
    
    @classmethod
    def register_subclass(cls,subcls):
        if subcls.id_ in cls._subs:
            raise ValueError('Subclass id repeats twice: {subcls.id_}!')
        cls._subs[subcls.id_] = subcls
    
    @classmethod
    def get_instance(cls,id_=None):
        try:
            return cls._subs[id_]()
        except KeyError:
            raise ValueError(f'Subclass not specified correctly, got "{id_}", '
                             'but {cls} does not have that subclass.')


class DataLoaderMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if bases == (GameObject,):
            cls.load_data()
        return cls
    

class Being(GameObject,metaclass=DataLoaderMeta):
    """
    Covers all active actors in the game
    """
    _modifiers = {}
    
    @classmethod
    def load_data(cls):
        modifiers = config.get_config(section='modifiers')
        for modifier in modifiers:
            cls._modifiers[modifier.name] = config.simplify(modifier)
    
    def __init__(self):
        """
        Create a Being of the specified type. Specified in subclasses.
        """
        pass


class PlayableCharacter(Being):
        
    def __init__(self,npc=False):
        if not npc:
            self.char = '@'
            self.style = 7
        self._stats = {}
        self._current_modifiers = []
        stats = config.get_config(section='character_template')
        for stat in stats:
            self._stats[stat.name] = config.simplify(stat)
        
    def get_stat(self,stat=None):
        """Return the current level of a stat"""
        try:
            return self._stats[stat]['current']
        except KeyError:
            raise ValueError(f'Bad stat identifier: "{stat}".')
            
    def _stat_can_change(self,stat,amount):
        return self._stats[stat]['min'] \
           <= (self._stats[stat]['current'] + amount) \
           <= self._stats[stat]['max']
            
    def change_stat(self,stat=None,amount=None):
        """
        Change the current level of a stat taking into account paired
        stats and min/max levels
        """
        if stat is None or amount is None:
            raise TypeError(f'Stat or amount not set: stat"{stat}",'
                            f'amount"{amount}".')
        if self._stat_can_change(stat,amount):
            paired_stat = self._stats[stat]['paired_with']
            if paired_stat:
                if self._stat_can_change(paired_stat,-1*amount):
                    self._stats[paired_stat]['current'] += -1*amount
                else:
                    return
            self._stats[stat]['current'] += amount
        else:
            raise ValueError(f'Stat would go out of bounds: stat:"{stat}",'
                             f'amount:"{amount}".')
            
    def check_triggers(self, stat):
        """
        Returns any activated triggers for the querried stat.
        
        Should probably be internal and called automatically on stat change!
        """
        if self.get_stat(stat=stat) == self._stats[stat]['min']:
            return self._stats[stat]['trigger_on_min']
        elif self.get_stat(stat=stat) == self._stats[stat]['max']:
            return self._stats[stat]['trigger_on_max']
        else:
            return ''
        
    @property
    def available_stat_selections(self):
        """
        Return the number of character stat selections the player
        needs to do
        """
        selections = []
        for stat in self._stats:
            if self._stats[stat]['trigger_on_min'] == 'READY_TO_CONTINUE' and \
                self.get_stat(stat) > 0:
                selections.append(stat)
        return len(selections)
        
    def next_stat_selection(self):
        """
        Return a list of stat names ending with the stat pool name
        
        Every character stat pool in the template (having the
        READY_TO_CONTINUE trigger on it's min value) triggers a stat
        modification screen listing only the stats linked to it and
        itself, so that the player can make adjustments. This method
        returns a list of the stat names that depend on the pool,
        starting with the name of the pool itself.
        
        If no pool is found the method raises StopIteration, as it is
        not supposed to be called when all pools are already depleted.
        """
        # Look for a non-empty stat pool
        pool = ''
        for pool in self._stats:
            if self._stats[pool]['trigger_on_min'] == 'READY_TO_CONTINUE' and \
                self.get_stat(pool) > 0:
                break
        if pool:
            stat_list = [pool]
            for stat in self._stats:
                if self._stats[stat]['paired_with'] == pool:
                    stat_list.append(stat)
            return stat_list
        else:
            raise StopIteration("No more stat selections available!")
        
    def apply_stat_change(self,change):
        """
        Change a stat
        
        Input is 'stat:amount'
        """
        stat,amount = change.split(':')
        self.change_stat(stat=stat,amount=int(amount))
        
    @property
    def available_modifiers(self):
        """
        Return the number of character creation modifiers the player
        needs to select
        """
        available_mods = []
        for mod in self._modifiers:
            if self._modifiers[mod]['applied'] == 'AT_CHARACTER_CREATION' and \
                mod not in self._current_modifiers:
                available_mods.append(mod)
        return len(available_mods)
        
    def next_modifier(self):
        """
        Every character modification defined with AT_CHARACTER_CREATION
        triggers a selection screen. Only one value of the modification
        can be selected. This is used for races, classes, etc.
        
        Returns the modifer.name and a list of its values
        [modifier, [values]]
        """
        mod_and_values = []
        for mod in self._modifiers:
            if self._modifiers[mod]['applied'] == 'AT_CHARACTER_CREATION' and \
                mod not in self._current_modifiers:
                mod_and_values = [mod, []]
                break
        if not mod:
            raise StopIteration("No more modifiers available!")
        for value in self._modifiers:
            if value.startswith(mod+':'):
                mod_and_values[1].append(value)
        return mod_and_values
                
    def apply_modifier(self,modifier):
        """
        Modifier is 'modifierName:value' as found in
        character_modifiers.ini
        """
        if modifier not in self._modifiers:
            raise ValueError(f"Unknown modifer ID:{modifier}")
        for stat in self._modifiers[modifier]:
            if stat in self._stats:
                self.change_stat(stat=stat,
                                 amount=self._modifiers[modifier][stat])
        self._current_modifiers.append(modifier.split(':')[0])

class Item(GameObject):
    pass


class Environment(GameObject):
    pass


class RegistrableEnvMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if bases != (Environment,):
            bases[-1].register_subclass(cls)
        else:
            cls.load_subs()
        return cls
    

class Effect(Environment, metaclass=RegistrableEnvMeta):
    _subs = {}
    
    @classmethod
    def load_subs(cls):
        pass


class Terrain(Environment, metaclass=RegistrableEnvMeta):
    _subs = {}
    
    @classmethod
    def load_subs(cls):
        for terrain in config.get_config(section='terrains'):
            class NewTerrain(cls):
                id_ = terrain.name
                char  = terrain['char']
                type_  = terrain['type']
                style = terrain.getint('style')
                spawned_creature = terrain['spawned_creature']
                tire_move = terrain.getint('tire_move')
                tire_stay = terrain.getint('tire_stay')
                creates_context = terrain.getboolean('creates_context')
                passable_for_types = eval(terrain['passable_for_types'])
                single_char_id  = terrain['id']
                asset  = terrain['asset']


class Theme(Environment, metaclass=RegistrableEnvMeta):
    _subs = {}
    
    @classmethod
    def load_subs(cls):
        for theme in config.get_config(section='themes'):
            if theme['terrains']:
                class NewTheme(cls):
                    id_ = theme.name
                    theme_breakpoints = eval(theme['theme_level_breakpoints'])
                    terrain_distribution = eval(theme['terrain_distribution'])
                    modifiers = eval(theme['modifiers'])
                    mod_thresholds = eval(theme['mod_thresholds'])
                    terrains = eval(theme['terrains'])
    
    @classmethod
    def get_structures(cls, themes):
        pass
    
    @classmethod
    def get_terrains(cls, themes, num=0):
        return [Terrain.get_instance(id_='dirt')]*num