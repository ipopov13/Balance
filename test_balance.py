"""
Created on Wed Feb  6 09:41:53 2019

Tests for the Balance rogue-like RPG

@author: IvanPopov
"""
import unittest
from unittest import mock
from unittest.mock import patch
from copy import deepcopy

#from module import function/object
from balance import Balance
from datamanager import DataManager
from screen import Screen
from screen import Pixel
from assets import StaticScreens
import ai
from world import World
from world import Scene
from world import Tile
import gameobject
import config

class BalanceTest(unittest.TestCase):
    
    def test_main_loop_runs_and_breaks(self):
        with patch('datamanager.DataManager.take_control') as myDM:
            myDM.return_value = None
            game = Balance()
            game.run()
            myDM.assert_called_once()
                
class DMTest(unittest.TestCase):
    
    def test_dm_activity_loop(self):
        with patch('datamanager.DataManager._screen') as screen:
            screen.get_command.return_value = 'q'
            dm = DataManager.get_starting_dm()
            result = dm.take_control()
            screen.load_data.assert_called_with({})
            screen.get_command.assert_called()
            screen.present.assert_called()
            screen.update_pixels.assert_called()
            assert result == None

class ScreenTest(unittest.TestCase):
    
    def test_load_data(self):
        with patch('screen.Screen._console') as console:
            screen = Screen()
            screen.load_data(StaticScreens.tester)
            assert screen._text == StaticScreens.tester
        
    def test_present(self):
        with patch('screen.Screen._console') as console:
            screen = Screen()
            screen.load_data(StaticScreens.tester)
            screen.present()
            console.text.assert_called_once_with(0, 0,'test',125)
        
    def test_get_command(self):
        with patch('msvcrt.getch') as char_input:
            char_input.return_value = b'test'
            screen = Screen()
            command = screen.get_command()
            assert command == 'test'
        
    def test_calls_console_only_for_changes(self):
        with patch('screen.Screen._console') as console:
            screen = Screen()
            obj = mock.Mock()
            obj.present.return_value = {'char':'a','style':8}
            screen.attach(x=0,y=0,presentable=obj)
            screen.update_pixels()
            screen.present()
            console.text.assert_called_once_with(0,0,'a',8)
            console.text.reset_mock()
            screen.update_pixels()
            screen.present()
            console.text.assert_not_called()
            screen.load_data(StaticScreens.tester)
            screen.present()
            console.text.assert_called_once_with(0, 0,'test',125)
            console.text.reset_mock()
            screen.present()
            console.text.assert_not_called()
            screen.load_data(StaticScreens.tester2)
            screen.present()
            console.text.assert_called_once_with(0, 0,'test2',126)
        
    def test_does_not_call_console_when_no_changes(self):
        with patch('screen.Screen._console') as console:
            screen = Screen()
            screen.load_data(StaticScreens.tester)
            screen.present()
            console.reset_mock()
            screen.load_data(StaticScreens.tester)
            screen.present()
            console.text.assert_not_called()
    
    def test_attach_update_clear(self):
        with patch('screen.Screen._console') as console:
            screen = Screen()
            obj = mock.Mock()
            screen.attach(x=0,y=0,presentable=obj)
            assert screen._pixels[(0,0)].is_active
            screen.update_pixels()
            obj.present.assert_called_once()
            screen.reset()
            assert not screen._pixels[(0,0)].is_active
    
    def test_attach_raises_on_bad_coords(self):
        with patch('screen.Screen._console') as console:
            screen = Screen()
            obj = mock.Mock()
            with self.assertRaises(ValueError):
                screen.attach(x=0,presentable=obj)
    
    def test_attach_scene(self):
        with patch('screen.Screen._console') as console:
            screen = Screen()
            tile = mock.Mock()
            tile.present.return_value = 0
            scene = {(i,i):tile for i in range(10)}
            screen.attach_scene(x=0,y=0,scene=scene)
            screen.update_pixels()
            assert len(list(screen._get_changed_pixels()))==10
        
    def test_raise_on_bad_input(self):
        screen = Screen()
        screen.load_data({(x,x+1):{'text':''} \
                              for x in range(screen._y_limit)})
        assert isinstance(screen,Screen)
        with self.assertRaises(ValueError):
            screen.load_data({(x,x+1):{'text':''} \
                                  for x in range(screen._y_limit+1)})
        screen.load_data({(0,0):{'text':'a'*screen._x_limit}})
        assert isinstance(screen,Screen)
        with self.assertRaises(ValueError):
            screen.load_data({(0,0):{'text':'a'*(screen._x_limit+1)}})
        with self.assertRaises(ValueError):
            screen.load_data({(0,0):{'text':'a','style':260}})
        

class PixelTest(unittest.TestCase):
    
    def test_update_raises_on_no_presentable(self):
        p = Pixel()
        with self.assertRaises(IOError):
            p.update()
    
    def test_attach_raises_on_nonpresentable(self):
        p = Pixel()
        with self.assertRaises(TypeError):
            p.attach('a')
    
    def test_attach_and_update_from_object(self):
        test_data = {'char':'s','style':3}
        p = Pixel()
        obj = mock.Mock()
        p.attach(obj)
        obj.present.return_value = test_data
        p.update()
        obj.present.assert_called_once()
        assert p.data == ['s',3]


class AITest(unittest.TestCase):
    
    def test_execute_raises_unknown_command(self):
        myAI = ai.AI()
        with self.assertRaises(ValueError):
            myAI.execute('asddafae')
            
    def test_starting_race(self):
        with patch('world.World.start') as starter:
            myAI = ai.AI()
            myAI.execute(ai.CHOOSE_HUMAN_RACE)
            starter.assert_called_once_with(race='human')


class WorldTest(unittest.TestCase):
    
    def test_start_world(self):
        with patch('gameobject.PlayableRace.get_instance') as getter:
            race = 'human'
            world = World()
            world.start(race=race)
            # test race call
            getter.assert_called_once_with(id_=race)
            # test world creation
            assert world._theme_peaks != {}
            # test starting coordinates are set
            assert world._current_scene_key is not None
            # test starting scene is created
            assert isinstance(world.current_scene, Scene)
            # test world reset at start()
            first_world = deepcopy(world._theme_peaks)
            world.start(race=race)
            assert first_world != world._theme_peaks
            # test that a single theme generates the correct number of peaks
            themes = config.get_themes()
            for theme in themes:
                if theme['distribution'] == 'peaks':
                    break
            dist = theme.getint('average_peak_distance')
            settings = config.get_settings(key='world')
            areas = (1+settings.getboolean('is_globe')) \
                    * settings.getint('size')**2
            assert sum([list(v.keys()).count(theme.name) for v in 
                        world._theme_peaks.values()]) == areas/dist**2
    
    def test_get_stat(self):
        with patch('gameobject.PlayableRace.get_stat') as getter:
            race = 'human'
            stat = 'Str'
            gd = World()
            gd.start(race=race)
            gd.get_stat(stat)
            getter.assert_called_once_with(stat=stat)
    
    def test_change_stat(self):
        with patch('gameobject.PlayableRace.change_stat') as changer:
            race = 'human'
            stat = 'Str'
            amount = 10
            gd = World()
            gd.start(race=race)
            gd.change_stat(stat=stat,amount=amount,from_pool=False)
            changer.assert_called_with(stat=stat,amount=amount)
            
    def test_calc_themes(self):
        with patch('gameobject.PlayableRace.get_instance') as _:
            race = 'human'
            world = World()
            world.start(race=race)
            assert list(world.current_scene._themes.keys()) == \
                                            [t.name for t in world._themes]

class SceneTest(unittest.TestCase):
    
    def test_refresh(self):
        assert 1==0
    
    def test_insert_being(self):
        """Also tests Tile.being"""
        scene = Scene({'Nature':35})
        being = gameobject.PlayableRace.get_instance(id_='human')
        with self.assertRaises(ValueError):
            scene.insert_being()
        x = scene._width//2
        y = scene._height//2
        scene.insert_being(being)
        assert scene._tiles[(x,y)].being is being
        with self.assertRaises(ValueError):
            scene.insert_being(being,coords=(0,0))

class TileTest(unittest.TestCase):
    pass
        

class PlayableRaceTest(unittest.TestCase):
    
    def test_get_being(self):
        being = gameobject.PlayableRace.get_instance(id_='human')
        assert isinstance(being,gameobject.Human)
        
class BeingTest(unittest.TestCase):
        
    def test_get_stat(self):
        being = gameobject.PlayableRace.get_instance(id_='human')
        assert being.get_stat(stat='Str') == 5
        
    def test_change_stat(self):
        being = gameobject.PlayableRace.get_instance(id_='human')
        being.change_stat(stat='Str',amount=4)
        assert being.get_stat(stat='Str') == 9
        with self.assertRaises(ValueError):
            being.change_stat(stat='Str',amount=4)
        being.change_stat(stat='Str',amount=-3)
        assert being.get_stat(stat='Str') == 6
        with self.assertRaises(ValueError):
            being.change_stat(stat='Str',amount=-8)

class TerrainsTest(unittest.TestCase):

    def test_all_terrains_loaded(self):
        assert len(gameobject.Terrain._subs)==len(list(config.get_terrains()))

class ThemeTest(unittest.TestCase):

    def test_get_structures(self):
        assert 1==0

    def test_get_terrains(self):
        assert 1==0

if __name__ == '__main__':
    unittest.main()