"""
Created on Wed Feb  6 09:41:53 2019

Tests for the Balance rogue-like RPG

@author: IvanPopov
"""
import unittest
from unittest import mock
from unittest.mock import patch

#from module import function/object
from balance import Balance
from world import World
from balanceui import UserInterface

class UITest(unittest.TestCase):
    
    def test_get_world(self):
        ui=UserInterface()
        assert isinstance(ui.get_world(),World)

class BalanceTest(unittest.TestCase):
    
    def test_world_creation_message_sent(self):
        ui=mock.Mock()
        Balance(ui)
        ui.get_world.assert_called_once()
        
    def test_run_world_with_command(self):
        ui=mock.Mock()
        ui.get_world().setup.return_value = ['test','test2']
        ui.get_world().run.return_value = []
        game=Balance(ui)
        game._run_world()
        ui.get_world().run.assert_called_with('test')
        
    def test_display(self):
        ui=mock.Mock()
        game=Balance(ui)
        game._display()
        ui.display.assert_called_with(ui.get_world())
        
    def test_get_command(self):
        ui=mock.Mock()
        game=Balance(ui)
        game._get_new_command()
        ui.get_command.assert_called_once()

class WorldTest(unittest.TestCase):
    
    def test_world_setup(self):
        world=World({})
        assert world.setup()[-1]=='viewSceneCommand'
        
    def test_run(self):
        with patch('view.PlayerController.process_command') as mockPC:
            mockPC.return_value=(1,2)
            test_command='test'
            world=World({})
            additional_commands=world.run(test_command)
            mockPC.assert_called_once_with(test_command)
            assert additional_commands==1

if __name__ == '__main__':
    unittest.main()
