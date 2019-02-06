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

class WorldTest(unittest.TestCase):
    
    def test_world_creation(self):
        with patch('gameobject.Being.init_scene_view') as mockBeing:
            World({})
        mockBeing.assert_called_once_with({})
    
    def test_world_setup(self):
        world=World({})
        assert world.setup()[-1]=='viewSceneCommand'
    
    def test_world_run_sends_commands(self):
        with patch('gameobject.Being.execute_command') as mockBeing:
            mockBeing.return_value = ('new_command','')
            world=World({})
            assert world.run('test_command')=='new_command'

    def test_world_run_updates_current_view(self):
        with patch('gameobject.Being.execute_command') as mockBeing:
            mockBeing.return_value = ('','new_view')
            world=World({})
            world.run('test_command')
            assert world._current_view=='new_view'

if __name__ == '__main__':
    unittest.main()
