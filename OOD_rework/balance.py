# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 10:06:51 2019

Main instance for the Balance rogue-like RPG

Balance is a View manager. It initis all Views and serves the game data
 to the next View in the queue, starting with the StarterView if no
 message is available. If a View returns END_GAME the loop breaks.
 
Requirements:
    VC inits all View subclasses
    After receiving a GET_ command it gives control to the called View
    After receiving END_GAME it breaks out

@author: IvanPopov
"""
import view
import balanceui


class Balance:
    
    def __init__(self):
        ui = balanceui.UserInterface()
        self._views = {view.GET_STARTER_VIEW: view.StarterView(ui),
            view.GET_SCENE_VIEW: view.SceneView(ui),
            view.GET_INVENTORY_VIEW: view.InventoryView(ui),
            view.GET_EQUIPMENT_VIEW: view.EquipmentView(ui),
            view.GET_CHARACTER_VIEW: view.CharacterView(ui)}
        self._message_queue = []
        self._game_data = {}
        
    
    def run(self):
        """
        Call the next required View to action, then resolve the
        returned message by calling another View or ending the game.
        """
        while True:
            try:
                message = self._message_queue.pop(0)
            except IndexError:
                message = view.GET_STARTER_VIEW
            if message == view.END_GAME:
                break
            else:
                self._message_queue.append(
                    self._views[message].take_control(self._game_data)
                    )
        return message


if __name__ == '__main__':
    game=Balance()
    _ = game.run()