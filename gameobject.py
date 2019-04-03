# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:00:45 2019

GameObject factories for the Balance rogue-like RPG

Called by the handlers to create all game objects.

Each subfamily has a metaclass that handles automatic registration of
 subclasses and loading from the ini files.

@author: IvanPopov
"""
import random
import config
import constants as const


class GameObject:
    """The abstract parent of all game objects."""

    @classmethod
    def register_subclass(cls, subcls):
        """Register a subclass in the mapping"""
        if subcls.id_ in cls._subs:
            raise ValueError('Subclass id repeats twice: {subcls.id_}!')
        cls._subs[subcls.id_] = subcls

    @classmethod
    def get_instance(cls, id_=None):
        """Return an instance of the called subclass"""
        try:
            return cls._subs[id_]()
        except KeyError:
            raise ValueError(f'Subclass not specified correctly, got "{id_}", '
                             'but {cls} does not have that subclass.')


class DataLoaderMeta(type):
    """Metaclass for loading data from ini at class definition"""
    def __new__(mcs, name, bases, class_dict):
        cls = type.__new__(mcs, name, bases, class_dict)
        cls.load_data()
        return cls


class PlayableCharacter(GameObject, metaclass=DataLoaderMeta):
    """
    Covers all active actors in the game
    """
    _modifiers = {}

    @classmethod
    def load_data(cls):
        """Load the modifier data for constructing beings"""
        modifiers = config.get_config(section='modifiers')
        for modifier in modifiers:
            cls._modifiers[modifier.name] = config.simplify(modifier)

    def __init__(self, npc=False):
        if not npc:
            self.char = const.PLAYER
            self.style = const.DEFAULT_PLAYER_STYLE
        self._stats = {}
        self._current_modifiers = []
        stats = config.get_config(section='character_template')
        for stat in stats:
            self._stats[stat.name] = config.simplify(stat)

    def move_time(self):
        """Increase the time stat of the being, if any"""
        for stat in self._stats:
            if self._stats[stat]['governs'] == const.GOVERN_TIME:
                self.change_stat(stat=stat, amount=1)

    def get_stat(self, stat=None):
        """Return the current level of a stat"""
        try:
            return self._stats[stat]['current']
        except KeyError:
            raise ValueError(f'Bad stat identifier: "{stat}".')

    def get_max_stat(self, stat=None):
        """Return the maximum level of a stat"""
        try:
            return self._stats[stat]['max']
        except KeyError:
            raise ValueError(f'Bad stat identifier: "{stat}".')

    def _stat_can_change(self, stat, amount):
        return self._stats[stat]['min'] \
           <= (self._stats[stat]['current'] + amount) \
           <= self._stats[stat]['max']

    def change_stat(self, stat=None, amount=None):
        """
        Change the current level of a stat taking into account paired
        stats and min/max levels
        """
        if stat is None or amount is None:
            raise TypeError(f'Stat or amount not set: stat"{stat}",'
                            f'amount"{amount}".')
        if self._stat_can_change(stat, amount):
            paired_stat = self._stats[stat]['paired_with']
            if paired_stat:
                if self._stat_can_change(paired_stat, -1*amount):
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
        trigger = ''
        if self.get_stat(stat=stat) == self._stats[stat]['min']:
            trigger = self._stats[stat]['trigger_on_min']
        elif self.get_stat(stat=stat) == self._stats[stat]['max']:
            trigger = self._stats[stat]['trigger_on_max']
        return trigger

    @property
    def available_stat_selections(self):
        """
        Return the number of character stat selections the player
        needs to do
        """
        selections = []
        for stat in self._stats:
            if self._stats[stat]['trigger_on_min'] == const.READY_TO_CONTINUE \
                and self.get_stat(stat) > 0:
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
            if self._stats[pool]['trigger_on_min'] == const.READY_TO_CONTINUE \
                and self.get_stat(pool) > 0:
                break
        if pool:
            stat_list = [pool]
            for stat in self._stats:
                if self._stats[stat]['paired_with'] == pool:
                    stat_list.append(stat)
            return stat_list
        else:
            raise StopIteration("No more stat selections available!")

    @property
    def available_modifiers(self):
        """
        Return the number of character creation modifiers the player
        needs to select
        """
        available_mods = []
        for mod in PlayableCharacter._modifiers:
            if PlayableCharacter._modifiers[mod]['applied'] == \
                const.AT_CHARACTER_CREATION \
                and mod not in self._current_modifiers:
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
        for mod in PlayableCharacter._modifiers:
            if PlayableCharacter._modifiers[mod]['applied'] \
                == const.AT_CHARACTER_CREATION \
                and mod not in self._current_modifiers:
                mod_and_values = [mod, []]
                for value in PlayableCharacter._modifiers:
                    if value.startswith(mod+':'):
                        mod_and_values[1].append(value)
                break
        if not mod_and_values:
            raise StopIteration("No more modifiers available!")
        return mod_and_values

    def apply_modifier(self, modifier):
        """
        Modifier is 'modifierName:value' as found in
        character_modifiers.ini
        """
        if modifier not in PlayableCharacter._modifiers:
            raise ValueError(f"Unknown modifer ID:{modifier}")
        for stat in PlayableCharacter._modifiers[modifier]:
            if stat in self._stats:
                self.change_stat(
                    stat=stat,
                    amount=PlayableCharacter._modifiers[modifier][stat])
        self._current_modifiers.append(modifier.split(':')[0])

class Item(GameObject):
    """Movable passive objects in the game"""
    pass


class Environment(GameObject):
    """Unmovable passive objects in the game"""
    pass


class RegistrableEnvMeta(type):
    """Registation metaclass for environments"""
    def __new__(mcs, name, bases, class_dict):
        cls = type.__new__(mcs, name, bases, class_dict)
        if bases != (Environment,):
            bases[-1].register_subclass(cls)
        else:
            cls.load_subs()
        return cls


class Effect(Environment, metaclass=RegistrableEnvMeta):
    """Non-physical environment"""
    _subs = {}

    @classmethod
    def load_subs(cls):
        pass
    
    
class Terrain(Environment, metaclass=DataLoaderMeta):
    """Physical environment factory"""
    _subs = {}
    _distributions = {}
    _types = ['structure', 'additional', 'basic']

    @classmethod
    def load_data(cls):
        for terrain in config.get_config(section='terrains'):
            class NewTerrain:
                id_ = terrain.name
                char = terrain['char']
                type_ = terrain['type']
                style = terrain.getint('style')
                single_char_id = terrain['id']
                asset = terrain['asset']
            cls._subs[terrain.name] = NewTerrain
        for distribution in config.get_config(section='terrain_distribution'):
            major_theme = distribution.name.split(':')[0]
            cls._distributions.setdefault(major_theme, []).append(distribution)
    
    @classmethod
    def get_structures(cls, themes):
        return 'structures'

    @classmethod
    def generate_terrains(cls, themes, num=0):
        allowed_terrain = {}
        modifiers = []
        for theme in themes:
            terrains, distribution, modifications = \
                cls._define_area(pov=theme, context=themes)
            if distribution:
                allowed_terrain[theme] = \
                    cls._pick_terrains(terrains=terrains,
                                       distribution=distribution)
            modifiers += modifications
        # Calculate allotments using themes from the allowed list
        theme_allocation = cls._allocate(values=themes,
                                         keys=allowed_terrain.keys(),
                                         num=num)
        # Generate a list of allowed instances
        result = cls._fill_allotments(allotments=theme_allocation,
                                      allowed=allowed_terrain)
        # Replace the needed fraction of terrains at random for each modifier
        result = cls._modify(terrains=result, mods=modifiers)
        # Create instances
        result = cls._instantiate(result)
        return result

    @classmethod
    def _define_area(cls, *, pov=None, context=None):
        terrains = []
        distribution = ''
        mods = []
        if pov in cls._distributions:
            for distr in cls._distributions[pov]:
                if cls._matches(distr=distr, context=context):
                    distr_terrains = distr['terrains'].split(',')
                    if distr['distribution']:
                        terrains += distr_terrains
                        distribution = max([distribution,
                                            distr['distribution']])
                    elif distr['fraction']:
                        mods.append({'fraction':float(distr['fraction']),
                                     'terrains':distr_terrains})
        return (terrains, distribution, mods)
    
    @classmethod
    def _pick_terrains(cls, *, terrains=None, distribution=None):
        picks = []
        terrains = cls._stratify(terrains)
        for type_, num in zip(cls._types, distribution):
            for j in range(int(num)):
                try:
                    picks.append(random.choice(terrains[type_]))
                except IndexError:
                    pass
        return picks
    
    @classmethod
    def _allocate(cls, *, values=None, keys=None, num=None):
        keys = list(keys)
        total = sum([values[key] for key in keys])
        allocation = {key:round(num * values[key]/total) for key in keys}
        allocated = sum(allocation.values())
        while allocated != num:
            if allocated < num:
                change = 1
            else:
                change = -1
            allocation [random.choice(keys)] += change
            allocated += change
        return allocation
    
    @classmethod
    def _fill_allotments(cls, *, allotments=None, allowed=None):
        result = []
        for theme, i in allotments.items():
            for j in range(i):
                result.append(random.choice(allowed[theme]))
        return result
    
    @classmethod
    def _modify(cls, *, terrains=None, mods=None):
        for mod in mods:
            num = round(len(terrains) * mod['fraction'])
            for i in random.choices(range(len(terrains)), k=num):
                terrains[i] = random.choice(mod['terrains'])
        return terrains
                
        
    @classmethod
    def _matches(cls, *, distr=None, context=None):
        matches = True
        for theme in distr.keys():
            if theme in context:
                bounds = [int(x) for x in distr[theme].split('..')]
                bounds[1] += 1
                if context[theme] not in range(*bounds):
                    matches = False
                    break
        return matches

    @classmethod
    def _stratify(cls, terrains):
        type_dict = {}
        for terrain in terrains:
            type_dict.setdefault(cls._subs[terrain].type_, []).append(terrain)
        return type_dict
        
    @classmethod
    def _instantiate(cls, result):
        for i, id_ in enumerate(result):
            result[i] = cls._subs[id_]()
        return result
