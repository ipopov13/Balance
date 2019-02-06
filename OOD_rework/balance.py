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
        self.world=ui.getWorld() # TEST: outgoing command
        self.command_queue = self.world.setup() #this adds setup commands to the queue # noTEST: outgoing query
        
    def main_loop(self):
        while self.world.IsLive:
            self.command_queue += self.world.run(self.command_queue.pop(0)) # TEST: outgoing command&query
            self.ui.display(self.world) # TEST: outgoing command
            if not self.command_queue:
                self.command_queue.append(self.ui.getCommand()) # noTEST: outgoing query
        self.world.finish() # TEST: outgoing command
    
if '__name__'=='__main__':
    ui=UI()
    game=Balance(ui)