"""
Created on Wed Feb  6 09:41:53 2019

Balance rogue-like RPG

Main loop

@author: IvanPopov
"""

from BalanceUI import UI

class Balance:
    def __init__(self,ui):
        self.ui=ui
        self.world=ui.getWorld()
        self.command_queue = self.world.setup() #this adds setup commands to the queue # noTEST: outgoing query
        
    def main_loop(self):
        while self.world.isLive(): # noTEST: outgoing query
            self.run_world()
            self.display()
            self.get_new_command()
        
    def run_world(self):
        self.command_queue += self.world.run(self.command_queue.pop(0))
        
    def display(self):
        self.ui.display(self.world)
        
    def get_new_command(self):
        if not self.command_queue:
            self.command_queue.append(self.ui.getCommand()) # noTEST: outgoing query
    
if '__name__'=='__main__':
    ui=UI()
    game=Balance(ui)
    game.main_loop()