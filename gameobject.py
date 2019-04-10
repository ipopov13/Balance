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
from collections import namedtuple
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
        modifiers = config.get_config(section='character_modifiers')
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


class TerrainLoader(type):
    """Metaclass for loading the terrain data and distribution"""
    def __new__(mcs, name, bases, class_dict):
        cls = type.__new__(mcs, name, bases, class_dict)
        for terrain in config.get_config(section='terrains'):
            cls._terrains[terrain.name] = config.simplify(terrain)
        for theme in config.get_config(section='terrain_distribution'):
            cls._terrain_odds[theme.name] = config.simplify(theme)
        for theme in config.get_config(section='terrain_modifiers'):
            cls._terrain_modifiers[theme.name] = theme
        return cls

    
class Terrain(Environment, metaclass=TerrainLoader):
    """Physical environment factory"""
    _terrains = {}
    _terrain_odds = {}
    _terrain_modifiers = {}
    
    @classmethod
    def get_structures(cls, themes):
        return 'structures'

    @classmethod
    def terrain_generator(cls, area_themes):
        # Get terrain probabilities from the distribution
        terrain_probabilities = {}
        for theme, distrib in cls._terrain_odds.items():
            for id_ in distrib:
                terrain_probabilities[id_] = \
                    terrain_probabilities.get(id_, 0) \
                    + distrib[id_]/area_themes[theme]
        ids = list(terrain_probabilities.keys())
        probs = [terrain_probabilities[k] for k in ids]
        cummulative_probs = [sum(probs[0:i]) for i in range(1, len(probs)+1)]
        # Get available modifications
        modifications = {}
        Mod = namedtuple('Mod',['probability','new_terrain'])
        for group in cls._terrain_modifiers:
            theme, threshold = group.split(':')
            threshold = int(threshold)
            prob = 0
            if threshold > 0 and area_themes[theme] > threshold:
                prob = (area_themes[theme] - threshold)/(100 - threshold)
            elif threshold < 0 and area_themes[theme] <= abs(threshold):
                threshold = abs(threshold)
                prob = (threshold - area_themes[theme])/threshold
            if prob:
                for old_terrain, new_terrain in \
                    cls._terrain_modifiers[group].items():
                    modifications.setdefault(old_terrain, []) \
                        .append(Mod(probability=prob,
                                    new_terrain=new_terrain))
        for changes in modifications.values():
            changes.sort()
        # Define terrain id generator
        def generator ():
            # Select terrain id
            choice = random.uniform(0, cummulative_probs[-1])
            id_ = ids[len([x for x in cummulative_probs if x < choice])]
            # Modify id
            for mod in modifications.get(id_, []):
                if random.random() <= mod.probability:
                    id_ = mod.new_terrain
                    break
            return id_
        return generator
    
    @classmethod
    def visualize(cls, terrain_id):
        return cls._terrains[terrain_id]