# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:41:01 2019

Views are generated using a specific Being instance and are passed by it into
the World.currentView property for visualization.
Views can be displayed with a standard AvailableViews View. Shortcuts
for the views:
Ctrl+0 : AvailableViews
Ctrl+1 : Scene
Ctrl+2 : CharacterSheet
Ctrl+3 : Inventory
TODO: Ctrl+4, etc. : All other views

All views can be accessed by all beings, but may not have content for them -
they have a default empty version.
Using the shortcuts (that is, changing views) does not move the game time
forward (looking at the information is free). Using a view's specific commands
may cost the player turns.
A View has a list of available commands and sending an unknown one sends back
a message and may expend time (depending on the view properties).

@author: IvanPopov
"""

class View:
    def __init__(self,being):
        self._caller=being
        

class SceneView(View):
    def __init__(self,being,spot):
        super().__init__(being) 