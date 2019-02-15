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
import view
import datamanager
import gamedata

class BalanceTest(unittest.TestCase):
    
    def test_main_loop_runs_and_breaks(self):
        with patch('view.StarterView.take_control') as myVC:
            myVC.return_value = datamanager.END_GAME
            game = Balance()
            run = game.run()
            myVC.assert_called_once()
            assert run == datamanager.END_GAME
                
    
class ViewTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        class TestView(view.View):
            
            def _post_init(self):
                self._getter_message = 'testing view'
                self._dm = datamanager.DataManager()
        
            def _update_screen(self,game_data):
                pass
        
        cls.test_view = TestView()
        
    @classmethod
    def tearDownClass(cls):
        del(cls.test_view)
    
    def test_returns_message(self):
        message = self.test_view.take_control(None)
        assert message == datamanager.END_GAME
        
    def test_calls_console(self):
        with patch('view.View._console') as myConsole:
            self.test_view.take_control(None)
            assert myConsole.method_calls != []
            
    def test_calls_dm_update_data(self):
        with patch('datamanager.DataManager.update_data') as myDM:
            myDM.return_value = datamanager.END_GAME
            self.test_view.take_control(None)
            myDM.assert_called_once()
        
    ## TODO: Test subclasses conform to View interface
    
class DMTest(unittest.TestCase):
    
    def test_abstract_dm_returns_end(self):
        dm = datamanager.DataManager()
        assert dm.update_data(data={},command='???') == datamanager.END_GAME

    def test_starter_does_nothing_on_unknown_command(self):
        my_dm = datamanager.StarterManager()
        my_data = gamedata.get_empty_data()
        my_dm.update_data(data=my_data,command='???')
        assert my_data == gamedata.get_empty_data()
    
    def test_starter_sends_correct_message(self):
        my_dm = datamanager.StarterManager()
        my_data = gamedata.get_empty_data()
        message = my_dm.update_data(data=my_data,command='n')
        assert message != datamanager.GET_CHARACTER_CREATION_VIEW
    
    def test_starter_gets_new_game_data(self):
        my_dm = datamanager.StarterManager()
        my_data = gamedata.get_empty_data()
        my_dm.update_data(data=my_data,command='n')
        assert my_data != gamedata.get_empty_data()

    def test_starter_gets_loaded_game_data(self):
        my_dm = datamanager.StarterManager()
        my_data = gamedata.get_empty_data()
        my_dm.update_data(data=my_data,command='l')
        assert my_data != gamedata.get_empty_data()
        
## TODO: test starting dms (load and new game) fully init game data?
    #It's probably gameData's responsibility
    ## TODO: Test every functionality added with a specific test case!

class GameDataTest(unittest.TestCase):
    pass

class GameObjectTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
