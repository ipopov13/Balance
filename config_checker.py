# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 15:36:28 2019

Config checker for the Balance rogue-like RPG framework.

Define key value types at the start and then check all sections enmasse
Section names must be unique and all small caps!

Requirements checked:
    
    Settings:
        All keys in all sections are mandatory and with a fixed type
    Modifiers:
        DEFAULT has the basic 'available_to','description','applied' keys
        Each basic modifier has the 'available_to' and 'applied' keys and they
            have a value that is allowed
        Each specific mod value has a unique legal name starting with
            'basic_name:'
        Each specific mod value has the 'description' key but no other
            basic keys
        Each specific mod value must have at least one key other than that
            which exists in the character_template.ini as a stat (that is,
            the mod actually modifies something in the character)
        That other key(s) must have a value that is applicable to the stat it
            references (number for a numeric stat, text for labels, etc.)
    Character template:
        DEFAULT has all the basic keys (current,min,max,trigger_on_min,
                trigger_on_max,paired_with,governs) with the
                triggers/pair/govern empty
        Each stat must have a unique legal name (a..z_)
        Each stat must have a current, min and max value defined either
            specifically or through DEFAULT, all numeric, min<=current<=max
        All governs and triggers must reference actual governs/trigger values
            from constants (need lists of those for easy checking)
        Every 'paired_with' property must reference an existing different stat
        A stat pool that is referenced in other stats' "paired_with" property
            cannot be paired itself
        There can be only one stat that GOVERN_TIME
    Scene:
        DEFAULT should have all the keys
        divisor should be >=0
        fills,markers,m_styles,statuses must be two for modulo_gauge and 
            breakpoints+1 for gauge
        only one of markers/statuses can be defined, and only for gauges
        statuses cannot be longer than the total_length-2
        breakpoints in the range 1-99, ordered ascending
        number type stats must have a label, label style and value style
        label length + len(max stat) must be < total_len (no touching of
            labels)
        gauges must have fills
        gauges with marker/statuses must have overlay styles
    Terrains:
        DEFAULT has all the keys
        each terrain has a style, ID, char & type
        all IDs are unique!
        each terrain with an asset key has the value equal to the terrain name
    Themes:
        DEFAULT has all the keys
        any peak distances are less than world size!
    Terrain distributions:
        Each name starts with an existing theme name +':'
        Each section has terrains and (distribution XOR fraction) defined
        All terrains are csv lists of existing terrain names
        All distributions are three digits, digits only, and not 000
        Any other keys reference existing themes
        All values are correct ranges within the themes' min-max values
        
        
@author: IvanPopov
"""