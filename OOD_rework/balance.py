"""
Created on Wed Feb  6 09:41:53 2019

Balance rogue-like RPG

Main instance

@author: IvanPopov
"""

from balanceui import UserInterface


class Balance:
    def __init__(self,ui):
        self._ui=ui
        self._world=self._ui.get_world()
        self._command_queue = self._world.setup()
        
    def main_loop(self):
        while self.world.is_live:
            self._run_world()
            self._display()
            self._get_new_command()
        
    def _run_world(self):
        self._command_queue += self._world.run(self._command_queue.pop(0))
        
    def _display(self):
        self._ui.display(self._world)
        
    def _get_new_command(self):
        if not self._command_queue:
            self._command_queue.append(self._ui.getCommand())

    
if '__name__'=='__main__':
    ui=UserInterface()
    game=Balance(ui)
    game.main_loop()