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
from screen import Screen
from terminal import Terminal
from terminal import Pixel
from assets import StaticScreens
import ai
import world
import gameobject
import config
import constants as const

class BalanceTest(unittest.TestCase):
    
    def test_main_loop_runs_and_breaks(self):
        with patch('screen.Screen.take_control') as myScreen:
            myScreen.return_value = None
            game = Balance()
            game.run()
            myScreen.assert_called_once()
                
class ScreenTest(unittest.TestCase):
    
    def test_screen_activity_loop(self):
        with patch('screen.Screen._terminal') as screen:
            screen.get_command.return_value = 'q'
            dm = Screen.get_starting_screen()
            result = dm.take_control()
            screen.load_data.assert_called_with({})
            screen.get_command.assert_called()
            screen.present.assert_called()
            assert result == None

class TerminalTest(unittest.TestCase):
    
    def test_load_data(self):
        with patch('terminal.Terminal._console') as console:
            screen = Terminal()
            screen.load_data(StaticScreens.tester)
            assert screen._text == StaticScreens.tester
        
    def test_present(self):
        with patch('terminal.Terminal._console') as console:
            screen = Terminal()
            screen.load_data(StaticScreens.tester)
            screen.present()
            console.text.assert_called_once_with(0, 0,'test',125)
        
    def test_get_command(self):
        with patch('msvcrt.getch') as char_input:
            char_input.return_value = b'test'
            screen = Terminal()
            command = screen.get_command()
            assert command == 'test'
        
    def test_calls_console_only_for_changes(self):
        with patch('terminal.Terminal._console') as console:
            screen = Terminal()
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
        with patch('terminal.Terminal._console') as console:
            screen = Terminal()
            screen.load_data(StaticScreens.tester)
            screen.present()
            console.reset_mock()
            screen.load_data(StaticScreens.tester)
            screen.present()
            console.text.assert_not_called()
    
    def test_attach_raises_on_bad_coords(self):
        with patch('terminal.Terminal._console') as console:
            screen = Terminal()
            scene = world.Scene({'Nature':35})
            with self.assertRaises(ValueError):
                screen.attach_scene(x=0,scene=scene)
            with self.assertRaises(ValueError):
                screen.attach_scene(y=0,scene=scene)
            with self.assertRaises(ValueError):
                screen.attach_scene(x=screen._width,y=0,scene=scene)
            with self.assertRaises(ValueError):
                screen.attach_scene(x=0,y=screen._height,scene=scene)
            with self.assertRaises(ValueError):
                screen.attach_scene(x=-1,y=0,scene=scene)
            with self.assertRaises(ValueError):
                screen.attach_scene(x=0,y=-1,scene=scene)
    
    def test_attach_scene(self):
        with patch('terminal.Terminal._console') as console:
            screen = Terminal()
            terrain = mock.Mock()
            terrain.char = 'a'
            terrain.style = 8
            tile = world.Tile(terrain)
            scene = mock.Mock()
            scene.tiles.return_value = {(i,i):tile for i in range(10)}.items()
            screen.attach_scene(x=0,y=0,scene=scene)
            assert len(screen._text)==10
        
    def test_raise_on_bad_input(self):
        screen = Terminal()
        screen.load_data({(x,x+1):{'text':''} \
                              for x in range(screen._height)})
        assert isinstance(screen,Terminal)
        with self.assertRaises(ValueError):
            screen.load_data({(x,x+1):{'text':''} \
                                  for x in range(screen._height+1)})
        screen.load_data({(0,0):{'text':'a'*screen._width}})
        assert isinstance(screen,Terminal)
        with self.assertRaises(ValueError):
            screen.load_data({(0,0):{'text':'a'*(screen._width+1)}})
        with self.assertRaises(ValueError):
            screen.load_data({(0,0):{'text':'a','style':260}})
        

class PixelTest(unittest.TestCase):
    
    def test_attach_raises_on_nonpresentable(self):
        p = Pixel(0)
        with self.assertRaises(AttributeError):
            p.attach('a')
    
    def test_update(self):
        terminal = mock.Mock()
        test_data = {'text':'s','style':3}
        p = Pixel(terminal)
        p.update(test_data)
        terminal.update.assert_called_once_with(p)


class AITest(unittest.TestCase):
    
    def test_execute_raises_unknown_command(self):
        myAI = ai.AI()
        with self.assertRaises(ValueError):
            myAI.execute('asddafae')


class WorldTest(unittest.TestCase):
    
    def test_start_world(self):
        with patch('gameobject.PlayableCharacter') as getter:
            my_world = world.World()
            # test race call
            getter.assert_called_once()
            # test world creation
            my_world.start()
            assert my_world._theme_peaks != {}
            pairs = list(my_world._theme_peaks.keys())
            assert max([i[0] for i in pairs])<=my_world._columns
            assert max([i[1] for i in pairs])<=my_world._rows
            assert min([i[0] for i in pairs])>=0
            assert min([i[1] for i in pairs])>=0
            # test starting coordinates are set
            assert my_world._current_scene_key is not None
            # test starting scene is created
            assert isinstance(my_world.current_scene, world.Scene)
            # test world reset at start()
            first_world = deepcopy(my_world._theme_peaks)
            my_world.start()
            assert first_world != my_world._theme_peaks
            # test that a single theme generates the correct number of peaks
            themes = config.get_config(section='themes')
            for theme in themes:
                if theme['distribution'] == const.PEAKS:
                    break
            dist = min(my_world._rows, theme.getint('average_peak_distance'))
            settings = config.get_settings(key='world')
            areas = (1+settings.getboolean('is_globe')) \
                    * settings.getint('size')**2
            assert sum([list(v.keys()).count(theme.name) for v in 
                        my_world._theme_peaks.values()]) == areas/dist**2
            
    def test_calc_themes(self):
        with patch('gameobject.PlayableCharacter') as _:
            my_world = world.World()
            my_world.start()
            assert list(my_world.current_scene._themes.keys()) == \
                                            [t.name for t in my_world._themes]
                                            
    def test_move_player(self):
        with patch('gameobject.PlayableCharacter') as pc:
            with patch('world.Scene') as scene_class:
                d = const.GO_E
                pc.return_value = mock.Mock()
                scene = mock.Mock()
                scene.move_being.return_value = const.SUCCESSFUL
                scene.remove_being.return_value = (0,0)
                scene_class.return_value = scene
                my_world = world.World()
                my_world.start()
                my_world._scenes = {(0,0):my_world.current_scene}
                my_world._current_scene_key = (0,0)
                my_world.move_player(direction=d)
                scene.move_being.assert_called_once_with(being=pc.return_value,
                                                 direction=d)
                assert my_world._current_scene_key == (0,0)
                scene.move_being.return_value = const.GOING_EAST
                my_world.move_player(direction=d)
                scene.remove_being.assert_called_once_with(pc.return_value,
                                    direction=scene.move_being.return_value,
                                    keep_y=False)
                assert my_world._current_scene_key == (1,0)
                scene.move_being.return_value = const.GOING_WEST
                my_world.move_player(direction=d)
                assert my_world._current_scene_key == (0,0)
                scene.move_being.return_value = const.GOING_SOUTH
                my_world.move_player(direction=d)
                assert my_world._current_scene_key == (0,1)
                scene.move_being.return_value = const.GOING_NORTH
                my_world.move_player(direction=d)
                assert my_world._current_scene_key == (0,0)
                my_world._settings['is_globe'] = False
                my_world.move_player(direction=d)
                assert my_world._current_scene_key == (0,0)
                scene.move_being.return_value = const.GOING_WEST
                my_world.move_player(direction=d)
                assert my_world._current_scene_key == (0,0)
                my_world._settings['is_globe'] = True
                my_world.move_player(direction=d)
                assert my_world._current_scene_key == \
                    (my_world._columns-1,0)
                scene.move_being.return_value = const.GOING_EAST
                my_world.move_player(direction=d)
                assert my_world._current_scene_key == (0,0)
                scene.remove_being.reset_mock()
                scene.move_being.return_value = const.GOING_NORTH
                my_world.move_player(direction=d)
                assert my_world._current_scene_key == \
                    (my_world._columns//2,0)
                scene.remove_being.assert_called_once_with(pc.return_value,
                                    direction=scene.move_being.return_value,
                                    keep_y=True)
                my_world.move_player(direction=d)
                assert my_world._current_scene_key == (0,0)
                

class SceneTest(unittest.TestCase):
    
    def test_remove_being(self):
        scene = world.Scene({'Nature':35})
        being = gameobject.PlayableCharacter()
        x = scene._width-1
        y = scene._height-1
        scene.insert_being(coords=(x,y),being=being)
        being_spot = scene.remove_being(being)
        assert being_spot == (x,y)
        scene.insert_being(coords=(x,y),being=being)
        being_spot = scene.remove_being(being,direction=const.GOING_EAST)
        assert being_spot == (0,y)
        scene.insert_being(coords=(x,y),being=being)
        being_spot = scene.remove_being(being,direction=const.GOING_SOUTH)
        assert being_spot == (x,0)
        scene.insert_being(coords=(0,0),being=being)
        being_spot = scene.remove_being(being,direction=const.GOING_WEST)
        assert being_spot == (x,0)
        scene.insert_being(coords=(0,0),being=being)
        being_spot = scene.remove_being(being,direction=const.GOING_NORTH)
        assert being_spot == (0,y)
    
    def test_insert_being(self):
        """Also tests Tile.being"""
        scene = world.Scene({'Nature':35})
        being = gameobject.PlayableCharacter()
        with self.assertRaises(ValueError):
            scene.insert_being()
        with self.assertRaises(ValueError):
            scene.insert_being(being,coords=(scene._width,scene._height))
        with self.assertRaises(ValueError):
            scene.insert_being(being,coords=(0,-1))
        with self.assertRaises(ValueError):
            scene.insert_being(being,coords=(-1,0))
        x = scene._width//2
        y = scene._height//2
        scene.insert_being(coords=(x,y),being=being)
        assert being in scene._beings
        with self.assertRaises(ValueError):
            scene.insert_being(being,coords=(0,0))
        assert scene._tiles[(x,y)].being is being
        
    def test_move_being(self):
        scene = world.Scene({'Nature':35})
        being = gameobject.PlayableCharacter()
        scene.insert_being(coords=(0,0),being=being)
        result = scene.move_being(being=being,direction='5')
        assert scene._beings[being]==(0,0)
        assert result == const.SUCCESSFUL
        result = scene.move_being(being=being,direction='2')
        assert scene._beings[being]==(0,1)
        assert result == const.SUCCESSFUL
        assert scene._tiles[(0,0)].being is None
        assert scene._tiles[(0,1)].being is being
        scene.move_being(being=being,direction='3')
        assert scene._beings[being]==(1,2)
        scene.move_being(being=being,direction='4')
        assert scene._beings[being]==(0,2)
        scene.move_being(being=being,direction='6')
        assert scene._beings[being]==(1,2)
        scene.move_being(being=being,direction='7')
        assert scene._beings[being]==(0,1)
        scene.move_being(being=being,direction='8')
        assert scene._beings[being]==(0,0)
        scene.move_being(being=being,direction='2')
        scene.move_being(being=being,direction='9')
        assert scene._beings[being]==(1,0)
        result = scene.move_being(being=being,direction='8')
        assert scene._beings[being]==(1,0)
        assert result == const.GOING_NORTH
        scene.move_being(being=being,direction='4')
        result = scene.move_being(being=being,direction='4')
        assert scene._beings[being]==(0,0)
        assert result == const.GOING_WEST
        scene._beings = {}
        scene.insert_being(coords=(scene._width-1,scene._height-1),
                           being=being)
        result = scene.move_being(being=being,direction='2')
        assert scene._beings[being]==(scene._width-1,scene._height-1)
        assert result == const.GOING_SOUTH
        result = scene.move_being(being=being,direction='6')
        assert scene._beings[being]==(scene._width-1,scene._height-1)
        assert result == const.GOING_EAST
        

class TileTest(unittest.TestCase):
    
    def test_pixel(self):
        terrain = mock.Mock()
        terrain.char = 'a'
        terrain.style = 8
        tile = world.Tile(terrain)
        pixel = mock.Mock()
        with self.assertRaises(AttributeError):
            tile.pixel = 1
        tile.pixel = pixel
        pixel.update.assert_called_once_with({'text':terrain.char,
                                              'style':terrain.style})
    
    def test_char_and_style(self):
        terrain = mock.Mock()
        terrain.char = 'a'
        terrain.style = 8
        with self.assertRaises(AttributeError):
            tile = world.Tile(1)
        tile = world.Tile(terrain)
        assert tile.char == terrain.char
        assert tile.style == terrain.style
        being = mock.Mock()
        being.char = 'b'
        being.style = 9
        tile.being = being
        assert tile.char == being.char
        assert tile.style == being.style
        
class PlayableCharacterTest(unittest.TestCase):
        
    def test_get_max_stat(self):
        being = gameobject.PlayableCharacter()
        being._stats = {'stat': {'min':0,'max':10,'current':5,
                                 'paired_with':'',
                                 'trigger_on_min':''}}
        assert being.get_max_stat('stat') == 10
        
    def test_get_change_stat(self):
        being = gameobject.PlayableCharacter()
        being._stats = {'stat': {'min':0,'max':10,'current':5,
                                 'paired_with':'',
                                 'trigger_on_min':''}}
        assert being.get_stat(stat='stat') == 5
        being.change_stat(stat='stat',amount=4)
        assert being.get_stat(stat='stat') == 9
        with self.assertRaises(ValueError):
            being.change_stat(stat='stat',amount=4)
        being.change_stat(stat='stat',amount=-3)
        assert being.get_stat(stat='stat') == 6
        with self.assertRaises(ValueError):
            being.change_stat(stat='stat',amount=-8)
            
    def test_check_triggers(self):
        being = gameobject.PlayableCharacter()
        being._stats['tester_stat'] = {'min':0,'max':10,'current':0,
                                       'trigger_on_min':'boom',
                                       'trigger_on_max':'baam',
                                       'paired_with':''}
        assert being.check_triggers('tester_stat')=='boom'
        being.change_stat('tester_stat',10)
        assert being.check_triggers('tester_stat')=='baam'
            
    def test_available_next_stat_selection(self):
        being = gameobject.PlayableCharacter()
        being._stats = {'stat': {'min':0,'max':10,'current':0,
                                 'paired_with':'pool',
                                 'trigger_on_min':''},
                        'pool': {'min':0,'max':99,'current':5,
                                 'trigger_on_min':'READY_TO_CONTINUE',
                                 'paired_with':''}}
        assert being.available_stat_selections == 1
        assert being.next_stat_selection() == ['pool','stat']
        being._stats = {}
        assert being.available_stat_selections == 0
        with self.assertRaises(StopIteration):
            being.next_stat_selection()
            
    def test_available_next_apply_modifier(self):
        being = gameobject.PlayableCharacter()
        being._stats = {
                'stat': {'min':0,'max':10,'current':0,
                         'paired_with':'',
                         'trigger_on_min':''}}
        gameobject.PlayableCharacter._modifiers = {
                'mod': {'applied':'AT_CHARACTER_CREATION'},
                'mod:val': {'applied':'','stat':5}}
        assert being.available_modifiers == 1
        assert being.next_modifier() == ['mod',['mod:val']]
        being.apply_modifier('mod:val')
        assert being.get_stat('stat') == 5
        assert being.available_modifiers == 0
        with self.assertRaises(StopIteration):
            being.next_modifier()

class TerrainsTest(unittest.TestCase):

    def test_all_terrains_loaded(self):
        assert len(gameobject.Terrain._terrains) == \
               len(config.get_config(section='terrains'))

    def test_get_terrains(self):
        num = 10
        assert len(gameobject.Terrain.generate_terrains({'Nature':10},num)) \
            == num

    def test_get_structures(self):
        assert gameobject.Terrain.get_structures({}) == 'structures'

if __name__ == '__main__':
    unittest.main()
