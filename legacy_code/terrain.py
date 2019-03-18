from collections import defaultdict

class KeepRefs(object):
    __refs__ = defaultdict(dict)
    def __init__(self,name):
        self.__refs__[self.__class__][name]=self

class Terrain(KeepRefs):
    def __init__(self, name = 'dirt', world_name = 'no_world_name', the_id = '.', colour = 6, char = '.', mess = '',
                 pass_through = True, degradable = True, workable = True,
                 degrade_to = {'Nature':'.','Order':'.','Chaos':'.'}, degr_mess = {'Nature':'','Order':'','Chaos':''},
                 degrade_tool = {'Nature':[],'Order':[],'Chaos':[]}, tire = {'Nature':0,'Order':0,'Chaos':0},
                 tire_move = 0, drink = {}, loot = {'Nature':[],'Order':[],'Chaos':[]}, random_creatures = [],
                 force_effects={'Nature':{},'Order':{},'Chaos':{}},sittable = True,drowning=False,clear_los=True):
        super(Terrain,self).__init__(the_id)
        self.colour = colour
        self.name = name
        self.world_name = world_name
        self.id = the_id
        self.char = char
        self.mess = mess
        self.pass_through = pass_through
        self.degradable = degradable
        self.workable = workable
        self.degrade_to = degrade_to
        self.degrade_tool = degrade_tool
        self.degr_mess = degr_mess
        self.tire = tire
        self.tire_move = tire_move
        self.drink = drink
        self.loot = loot
        self.random_creatures = random_creatures
        self.force_effects=force_effects
        self.sittable=sittable
        self.drowning=drowning
        self.clear_los=clear_los

## name = 'dirt', world_name, id = '.', colour = 6, char = '.', mess = '', pass_through = True, degradable = True, workable = True
## degrade_to = {modes}, degr_mess = {modes}, degrade_tool = {modes}, tire = {modes}, tire_move = 0, drink = {},
## loot = {modes}[[id,chance[1-100],min,max],['treasure',chance,grade,trove]],
## random_creatures = [[cr_id,chance(1-1000)],...], force_effects={modes:{'all':,'force':,race:,'terrain':}}
##
## Vuzmojno e suzdavane na creature profil vuv vid na teren, chieto ID nikoga nqma da se izpolzva na karta, a
## kato identifikator predi imeto na mestnostta, opredelqsht sluchainata i naselenost sus sushtestva i mnojitelq
## kum shansa za izkopavane na sukrovishte. Primer e 'mechka'-ta po-dolu.
## !!! VAJNO !!! Vseki teren trqbva da se dobavq v all!
        
## Vratite se pishat s world_name = 'door_o' ili 'door_c' za otvorena i zatvorena suotvetno
        
## Spisuk na izpolzvanite tagove: " NE MOJE DA E TAG!
##  .,+><aAbBdDfFgiIJlLmnoOpsStTwW%#`'~:

treasure1 = Terrain(the_id='treasure1',loot=100)
mechka = Terrain(the_id='mechka',random_creatures=[[4,500]])

dirt = Terrain(world_name='road',degrade_to = {'Nature':'.','Order':'a','Chaos':'.'},
                degr_mess = {'Nature':'propose_plant','Order':'dig_earth','Chaos':'dig_earth'},
                degrade_tool = {'Nature':['inherent'],'Order':['shovel'],'Chaos':['shovel']},
                tire={'Nature':0,'Order':150,'Chaos':150},
                loot = {'Nature':[[1303,30,1,3],[1304,30,1,3]],'Order':[[1306,70,1,3],['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                      ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]],
                        'Chaos':[['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                      ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]]},
                force_effects={'Nature':{},
                               'Order':{'Chaos':{'all':-.05},'Order':{'force':0.05,'human':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.05},'Chaos':{'force':0.05,'goblin':0.05,'terrain':0.2}}})
grass = Terrain('grass', 'plains', 'g', 10, '.',degrade_to = {'Nature':'g','Order':'a','Chaos':'.'},
                degr_mess = {'Nature':'clean_grass','Order':'dig_earth','Chaos':'dig_earth'},
                degrade_tool = {'Nature':['inherent'],'Order':['shovel'],'Chaos':['shovel']},
                tire={'Nature':0,'Order':150,'Chaos':150},
                loot = {'Nature':[[1305,50,1,2],[9,25,1,2]],
                        'Order':[[1306,70,1,3],['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                      ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]],
                        'Chaos':[['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                      ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]]},
                force_effects={'Nature':{'Nature':{'force':0.01,'spirit of nature':0.01,'terrain':.05},'Chaos':{'all':-.01}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'human':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.05},'Chaos':{'force':0.05,'goblin':0.05,'terrain':0.2}}})
bones = Terrain('bones', 'plains', 'B', 11, '.','walk_bones',degrade_to = {'Nature':'.','Order':'B','Chaos':'B'},
                degr_mess = {'Nature':'cover_bones','Order':'dig_bones','Chaos':'dig_bones'},
                degrade_tool = {'Nature':['earth'],'Order':['shovel'],'Chaos':['inherent']},
                tire={'Nature':50,'Order':50,'Chaos':30},tire_move=10,
                loot = {'Nature':[],'Order':[['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                      ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]],
                        'Chaos':[['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                      ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]]},
                force_effects={'Nature':{'Nature':{'force':0.03,'spirit of nature':0.03,'terrain':.2,'expend':'earth'},'Chaos':{'all':-.03}},
                               'Order':{'Nature':{'all':-.03},'Order':{'force':0.03,'human':0.03}},
                               'Chaos':{'Nature':{'all':-.03},'Chaos':{'force':0.03,'goblin':0.03}}})
farmland = Terrain('farmland', 'farmland', 'a', 96, '|',degrade_to = {'Nature':'a','Order':'a','Chaos':'.'},
                degr_mess = {'Nature':'propose_plant','Order':'propose_plant','Chaos':'dig_earth'},
                degrade_tool = {'Nature':['inherent'],'Order':['inherent'],'Chaos':['shovel']},
                tire={'Nature':0,'Order':0,'Chaos':150},
                loot = {'Nature':[[1303,100,4,5],[1304,30,1,2],[1306,60,1,3]],'Order':[[1306,60,1,3]],
                        'Chaos':[['treasure',0.4,'small',False],['treasure',0.2,'medium',False],['treasure',0.1,'large',False],
                      ['treasure',0.08,'small',True],['treasure',0.04,'medium',True],['treasure',0.02,'large',True]]},
                force_effects={'Nature':{},
                               'Order':{},
                               'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                        'Chaos':{'force':0.05,'spirit of chaos':0.05,'terrain':0.2}}})
tree = Terrain('tree', 'forest', 'T', 10, 'T','tree',degrade_to = {'Nature':'T','Order':':','Chaos':'.'},
                degr_mess = {'Nature':'clean_tree','Order':'cut_tree','Chaos':'fire_tree'},
                degrade_tool = {'Nature':['inherent'],'Order':['axe'],'Chaos':['fire']},
                tire={'Nature':0,'Order':150,'Chaos':10},
                loot = {'Nature':[],'Order':[[14,100,4,7]],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.01,'dryad':0.01,'terrain':.05},'Chaos':{'all':-.01}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'human':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.03},'Order':{'all':-.03},
                                        'Chaos':{'force':0.03,'imp':0.03,'terrain':0.2,'fire_up':25}}},clear_los=False)
d_grass = Terrain('diseased grass', 'plains', 'd', 8, '.',degrade_to = {'Nature':'g','Order':'.','Chaos':'.'},
                degr_mess = {'Nature':'heal_grass','Order':'fire_grass','Chaos':'stomp_grass'},
                degrade_tool = {'Nature':['nature healing set'],'Order':['fire'],'Chaos':['inherent']},
                tire={'Nature':20,'Order':10,'Chaos':30},
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.02,'elf':0.02,'terrain':.2},'Chaos':{'all':-.01}},
                               'Order':{'Nature':{'all':-.01},'Chaos':{'all':-.01},
                                        'Order':{'force':0.01,'human':0.01,'terrain':0.2,'fire_up':5}},
                               'Chaos':{'Nature':{'all':-.02},'Order':{'all':-.02},
                                        'Chaos':{'force':0.02,'goblin':0.02,'terrain':0.05}}})
d_tree = Terrain('diseased tree','forest','D',8,'T','d_tree',degrade_to = {'Nature':'T','Order':'.','Chaos':'.'},
                degr_mess = {'Nature':'heal_tree','Order':'fire_tree','Chaos':'fire_tree'},
                degrade_tool = {'Nature':['nature healing set'],'Order':['fire'],'Chaos':['fire']},
                tire={'Nature':20,'Order':10,'Chaos':10},
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.02,'dryad':0.02,'terrain':.2},
                                         'Chaos':{'all':-.01},'Order':{'all':-.01}},
                               'Order':{'Nature':{'all':-.02},
                                        'Order':{'force':0.01,'human':0.01,'terrain':0.2,'fire_up':25}},
                               'Chaos':{'Nature':{'all':-.02},
                                        'Chaos':{'force':0.01,'imp':0.01,'terrain':0.05,'fire_up':25}}},clear_los=False)
frozen_tree = Terrain('frozen tree', 'forest', 'F', 11, 'T','frozen_tree',degrade_to = {'Nature':'T','Order':'T','Chaos':'.'},
                degr_mess = {'Nature':'thaw_tree','Order':'thaw_tree','Chaos':'tear_tree'},
                degrade_tool = {'Nature':['fire'],'Order':['fire'],'Chaos':['big hammer']},
                tire={'Nature':100,'Order':100,'Chaos':150},
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.05,'dryad':0.05,'terrain':.2},
                                         'Chaos':{'all':-.05}},
                               'Order':{'Chaos':{'all':-.05},
                                        'Order':{'force':0.05,'spirit of order':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                        'Chaos':{'force':0.05,'troll':0.05,'terrain':0.05}}},clear_los=False)
jungle = Terrain('jungle trees', 'forest', 'J', 2, 'T','jungle', False,
                 degrade_to = {'Nature':'J','Order':'T','Chaos':'.'},
                degr_mess = {'Nature':'forage','Order':'cut_tree','Chaos':'fire_tree'},
                degrade_tool = {'Nature':['inherent'],'Order':['axe'],'Chaos':['fire']},
                tire={'Nature':20,'Order':150,'Chaos':10},
                loot = {'Nature':[['forage',100,1,3]],'Order':[[14,100,4,9]],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.02,'elf':0.02},
                                         'Chaos':{'all':-.01}},
                               'Order':{'Nature':{'all':-.05},
                                        'Order':{'force':0.05,'human':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.02},'Order':{'all':-.02},
                                        'Chaos':{'force':0.02,'imp':0.02,'terrain':0.2,'fire_up':50}}},clear_los=False)
bush = Terrain('bush', '', 'b', 10, '#','bush',degrade_to = {'Nature':'b','Order':'.','Chaos':'.'},
                degr_mess = {'Nature':'forage','Order':'root_bushes','Chaos':'fire_bush'},
                degrade_tool = {'Nature':['inherent'],'Order':['inherent'],'Chaos':['fire']},
                tire={'Nature':20,'Order':30,'Chaos':10},tire_move = 15,
                loot = {'Nature':[['forage',40,1,2]],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.02,'elf':0.02},'Chaos':{'all':-.02}},
                               'Order':{'Nature':{'all':-.02},'Order':{'force':0.02,'human':0.02,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.02},'Order':{'all':-.02},
                                        'Chaos':{'force':0.02,'imp':0.02,'terrain':0.2,'fire_up':15}}},clear_los=False)
lichen = Terrain('lichen mound', '', 'l', 10, 'o','lichen',degrade_to = {'Nature':'l','Order':'.','Chaos':'.'},
                degr_mess = {'Nature':'call_the_seed','Order':'dig_earth','Chaos':'ravage_lichen'},
                degrade_tool = {'Nature':['inherent'],'Order':['shovel'],'Chaos':['inherent']},
                tire={'Nature':100,'Order':150,'Chaos':30},tire_move = 10,
                loot = {'Nature':[['ntreasure',0.8]],'Order':[[1306,40,2,3]],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.05,'gnome':0.05},'Chaos':{'all':-.05},'Order':{'all':-.05}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.05},
                                        'Chaos':{'force':0.02,'spirit of chaos':0.02,'terrain':0.2}}})
rock = Terrain('rock', 'mountains', '%', 8, '%', 'rock', False, True, True,
               degrade_to = {'Nature':'%','Order':'.','Chaos':'.'},
                degr_mess = {'Nature':'touch_rock','Order':'break_rock','Chaos':'break_rock'},
                degrade_tool = {'Nature':['inherent'],'Order':['pickaxe','pick','big hammer'],'Chaos':['pickaxe','pick','big hammer']},
                tire={'Nature':0,'Order':150,'Chaos':150},tire_move=20,
                loot = {'Nature':[[1304,30,1,2]],'Order':[[1306,100,1,3],[4,100,3,8],[5,30,1,1]],'Chaos':[[4,100,1,5]]},
                force_effects={'Nature':{'Nature':{'force':0.01,'gnome':0.01},'Chaos':{'all':-.01},'Order':{'all':-.01}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.05},'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2}}},clear_los=False)
well = Terrain('well', 'mountains', 'O', 1, 'O', 'well_pass', True, True, True,
               degrade_to = {'Nature':'O','Order':'O','Chaos':'.'},
                degr_mess = {'Nature':'clean_well','Order':'clean_well','Chaos':'crush_well'},
                degrade_tool = {'Nature':['inherent'],'Order':['inherent'],'Chaos':['pickaxe','pick','big hammer']},
                tire={'Nature':10,'Order':10,'Chaos':150},drink = {'energy':20, 'thirst':20},
                loot = {'Nature':[[1303,40,2,4],[1304,30,1,2]],'Order':[[1306,40,1,2]],'Chaos':[[4,100,1,4]]},
                force_effects={'Nature':{'Nature':{'force':0.01,'fairy':0.01},'Chaos':{'all':-.01}},
                               'Order':{'Chaos':{'all':-.01},'Order':{'force':0.01,'spirit of order':0.01}},
                               'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                        'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2,'population':-2}}},sittable=False)
mossy_rock = Terrain('mossy rock', 'mountains', 'n', 10, '%', 'rock', False, True, True,
               degrade_to = {'Nature':'n','Order':'.','Chaos':'.'},
                degr_mess = {'Nature':'touch_rock','Order':'break_rock','Chaos':'break_rock'},
                degrade_tool = {'Nature':['inherent'],'Order':['pickaxe','pick','big hammer'],'Chaos':['pickaxe','pick','big hammer']},
                tire={'Nature':0,'Order':150,'Chaos':150},tire_move=10,
                loot = {'Nature':[[1304,30,1,2]],'Order':[[4,100,3,8],[5,5,1,2]],'Chaos':[[4,100,1,5]]},
                force_effects={'Nature':{'Nature':{'force':0.01,'gnome':0.01},'Chaos':{'all':-.01},'Order':{'all':-.01}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.05},'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2}}},clear_los=False)
mine_rock = Terrain('rock', 'mountains', 'm', 8, '%', 'rock', False, False, True,
               degrade_to = {'Nature':'m','Order':'.','Chaos':'.'},
                degr_mess = {'Nature':'touch_rock','Order':'break_rock','Chaos':'break_rock'},
                degrade_tool = {'Nature':['inherent'],'Order':['pickaxe','pick','big hammer'],'Chaos':['pickaxe','pick','big hammer']},
                tire={'Nature':0,'Order':150,'Chaos':150},tire_move=20,
                loot = {'Nature':[[1304,30,1,2]],'Order':[[4,100,3,8],[5,60,1,3]],'Chaos':[[4,100,1,5]]},
                force_effects={'Nature':{'Nature':{'force':0.01,'gnome':0.01},'Chaos':{'all':-.01},'Order':{'all':-.01}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05}},
                               'Chaos':{'Nature':{'all':-.05},'Chaos':{'force':0.05,'troll':0.05}}},clear_los=False)
wall = Terrain('wall', 'wall???', '#', 7, '#', 'wall', False, True, True,
               degrade_to = {'Nature':'#','Order':'#','Chaos':'.'},
                degr_mess = {'Nature':'paint_wall','Order':'strenghten_wall','Chaos':'break_wall'},
                degrade_tool = {'Nature':['color clay'],'Order':['clay'],'Chaos':['pickaxe','pick','big hammer']},
                tire={'Nature':20,'Order':20,'Chaos':150},tire_move=20,
                loot = {'Nature':[],'Order':[],'Chaos':[[4,100,1,4]]},
                force_effects={'Nature':{'Nature':{'force':0.02,'fairy':0.02,'expend':'color clay'},'Chaos':{'all':-.02}},
                               'Order':{'Chaos':{'all':-.02},'Order':{'force':0.02,'dwarf':0.02,'expend':'clay'}},
                               'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                        'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2,'population':-1}}},clear_los=False)
wooden_fence = Terrain('wooden fence', 'wall???', 'o', 6, '#', 'fence', False, True, True,
               degrade_to = {'Nature':'o','Order':'o','Chaos':'.'},
                degr_mess = {'Nature':'paint_fence','Order':'strenghten_fence','Chaos':'break_fence'},
                degrade_tool = {'Nature':['flowers'],'Order':['hammer'],'Chaos':['big hammer']},
                tire={'Nature':0,'Order':20,'Chaos':100},tire_move=20,
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.01,'fairy':0.01,'terrain':0.05,'expend':'flowers'},'Chaos':{'all':-.01}},
                               'Order':{'Chaos':{'all':-.02},'Order':{'force':0.02,'spirit of order':0.02}},
                               'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                        'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2,'population':-1}}})
pavement = Terrain('pavement', 'town','p',7,
               degrade_to = {'Nature':'.','Order':'p','Chaos':'.'},
                degr_mess = {'Nature':'remove_pavement','Order':'repair_pavement','Chaos':'destroy_pavement'},
                degrade_tool = {'Nature':['pick','pickaxe'],'Order':['hammer','crude hammer'],'Chaos':['pick','pickaxe','big hammer']},
                tire={'Nature':150,'Order':50,'Chaos':150},
                loot = {'Nature':[[4,100,3,8],[1303,100,1,2]],'Order':[],'Chaos':[[4,100,1,3]]},
                force_effects={'Nature':{'Nature':{'force':0.05,'gnome':0.05,'terrain':0.2},'Chaos':{'all':-.05},'Order':{'all':-.05}},
                               'Order':{'Chaos':{'all':-.03},'Nature':{'all':-.03},'Order':{'force':0.03,'dwarf':0.03}},
                               'Chaos':{'Order':{'all':-.05},
                                        'Chaos':{'force':0.05,'spirit of chaos':0.05,'terrain':0.2,'population':-1}}})
sand = Terrain('sand', 'beach',',',14,
               degrade_to = {'Nature':'.','Order':',','Chaos':','},
                degr_mess = {'Nature':'lay_earth','Order':'dig_sand','Chaos':'dig_sand'},
                degrade_tool = {'Nature':['earth'],'Order':['shovel'],'Chaos':['shovel']},
                tire={'Nature':40,'Order':150,'Chaos':150},tire_move=10,
                loot = {'Nature':[],'Order':[['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                      ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]],
                        'Chaos':[['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                      ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]]},
                force_effects={'Nature':{'Chaos':{'all':-.03},
                                         'Nature':{'force':0.03,'dryad':0.03,'terrain':0.3,'expend':'earth'}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05,'terrain':0.05}},
                               'Chaos':{'Nature':{'all':-.05},'Chaos':{'force':0.05,'spirit of chaos':0.05,'terrain':0.05}}})
swamp = Terrain('swamp', 'swamp',"~",10,'~','swamp',
               degrade_to = {'Nature':'.','Order':'.','Chaos':'~'},
                degr_mess = {'Nature':'remove_swamp','Order':'remove_swamp','Chaos':'dig_earth'},
                degrade_tool = {'Nature':['shovel'],'Order':['shovel'],'Chaos':['shovel']},
                tire={'Nature':150,'Order':150,'Chaos':200},tire_move=20,
                loot = {'Nature':[[1304,30,1,2],[1303,30,1,2]],'Order':[[1306,30,1,2]],
                        'Chaos':[['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                      ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]]},
                force_effects={'Nature':{'Chaos':{'all':-.05},
                                         'Nature':{'force':0.05,'water elemental':0.05,'terrain':0.2}},
                               'Order':{'Chaos':{'all':-.05},'Order':{'force':0.05,'human':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},'Chaos':{'force':0.07,'kraken':0.07,'terrain':0.05}}},
                sittable=False)
snow = Terrain('snow', 'snowy peak',"'",15,
               degrade_to = {'Nature':'.','Order':'.','Chaos':'.'},
                degr_mess = {'Nature':'remove_snow','Order':'remove_snow','Chaos':'remove_snow'},
                degrade_tool = {'Nature':['shovel'],'Order':['shovel'],'Chaos':['shovel']},
                tire={'Nature':100,'Order':100,'Chaos':100},tire_move=10,
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Chaos':{'all':-.05},
                                         'Nature':{'force':0.05,'spirit of nature':0.05,'terrain':0.2}},
                               'Order':{'Chaos':{'all':-.05},'Order':{'force':0.05,'spirit of order':0.05,'terrain':0.2}},
                               'Chaos':{'Chaos':{'force':0.05,'goblin':0.05,'terrain':0.05}}})
ice = Terrain('ice', 'snowy peak',"i",9,mess='ice',
               degrade_to = {'Nature':'w','Order':'w','Chaos':'w'},
                degr_mess = {'Nature':'thaw_ice','Order':'break_ice','Chaos':'break_ice'},
                degrade_tool = {'Nature':['fire'],'Order':['crude hammer','pick','hammer','big hammer'],'Chaos':['crude hammer','pick','hammer','big hammer']},
                tire={'Nature':50,'Order':150,'Chaos':150},tire_move=20,
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Chaos':{'all':-.03},
                                         'Nature':{'force':0.03,'water elemental':0.03,'terrain':0.2}},
                               'Order':{'Order':{'force':0.05,'dwarf':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'water elemental':-0.05},'Chaos':{'force':0.05,'kraken':0.05,'terrain':0.05}}})
ice_block = Terrain('ice block', 'mountains', 'I', 11, '%', 'ice_block', False, True, True,
               degrade_to = {'Nature':'i','Order':'i','Chaos':'i'},
                degr_mess = {'Nature':'thaw_ice','Order':'break_ice','Chaos':'break_ice'},
                degrade_tool = {'Nature':['fire'],'Order':['crude hammer','pick','hammer','big hammer'],'Chaos':['crude hammer','pick','hammer','big hammer']},
                tire={'Nature':50,'Order':150,'Chaos':150},
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Chaos':{'all':-.03},
                                         'Nature':{'force':0.03,'water elemental':0.03,'terrain':0.2}},
                               'Order':{'Order':{'force':0.05,'dwarf':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'water elemental':-0.05},'Chaos':{'force':0.05,'kraken':0.05,'terrain':0.05}}},clear_los=False)
log = Terrain('log', 'log???', ':',6,':', 'log',degrade_to = {'Nature':':','Order':'.','Chaos':'.'},
                degr_mess = {'Nature':'care_log','Order':'cut_log','Chaos':'fire_tree'},
                degrade_tool = {'Nature':['inherent'],'Order':['axe'],'Chaos':['fire']},
                tire={'Nature':10,'Order':150,'Chaos':10},
                loot = {'Nature':[],'Order':[[14,100,3,6]],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.01,'dryad':0.01,'terrain':.05},'Chaos':{'all':-.01}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'human':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.02},'Order':{'all':-.02},
                                        'Chaos':{'force':0.01,'imp':0.01,'terrain':0.2,'fire_up':25}}})
water = Terrain('water', 'sea','w',1,'~','water',degrade_to = {'Nature':'w','Order':'t','Chaos':'t'},
                degr_mess = {'Nature':'clean_water','Order':'search_water','Chaos':'contaminate_water'},
                degrade_tool = {'Nature':['inherent'],'Order':['inherent'],'Chaos':['inherent']},
                tire={'Nature':50,'Order':250,'Chaos':10},tire_move=30,drink = {'energy':20, 'thirst':20},
                loot = {'Nature':[],'Order':[['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                      ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.03,'water elemental':0.03,'terrain':.05},'Chaos':{'all':-.03}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.03},'Order':{'all':-.03},
                                        'Chaos':{'force':0.03,'kraken':0.03,'terrain':0.2}}},sittable=False,drowning=True)
dirty_water = Terrain('dirty water', 'sea','t',8,'~','water',degrade_to = {'Nature':'w','Order':'t','Chaos':'t'},
                degr_mess = {'Nature':'clean_water','Order':'search_water','Chaos':'contaminate_water'},
                degrade_tool = {'Nature':['inherent'],'Order':['inherent'],'Chaos':['inherent']},
                tire={'Nature':50,'Order':250,'Chaos':10},tire_move=35,drink = {'energy':5, 'thirst':-5},
                loot = {'Nature':[],'Order':[['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                      ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.03,'water elemental':0.03,'terrain':.3},'Chaos':{'all':-.03}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05,'terrain':0.05}},
                               'Chaos':{'Nature':{'all':-.03},'Order':{'all':-.03},
                                        'Chaos':{'force':0.03,'kraken':0.03,'terrain':0.05}}},sittable=False,drowning=True)
magic_water = Terrain('magical spring', 'magic water???','W',9,'~','magic_water',
                      degrade_to = {'Nature':'W','Order':'w','Chaos':'t'},
                degr_mess = {'Nature':'honor_water','Order':'search_water','Chaos':'contaminate_water'},
                degrade_tool = {'Nature':['inherent'],'Order':['inherent'],'Chaos':['inherent']},
                tire={'Nature':0,'Order':250,'Chaos':10},tire_move=10,drink = {'energy':100, 'thirst':40},
                loot = {'Nature':[['wtreasure',0.8]],'Order':[['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                      ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.03,'water elemental':0.03,'terrain':.05},'Chaos':{'all':-.05}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.03},'Order':{'all':-.03},
                                        'Chaos':{'force':0.03,'kraken':0.03,'terrain':0.2}}},sittable=False)
waterfall = Terrain('waterfall', 'river','f',11,'~',pass_through=False,
                      degrade_to = {'Nature':'f','Order':'%','Chaos':'w'},
                degr_mess = {'Nature':'clean_water','Order':'stop_waterfall','Chaos':'destroy_waterfall'},
                degrade_tool = {'Nature':['inherent'],'Order':['shovel'],'Chaos':['pickaxe','pick','big hammer']},
                tire={'Nature':50,'Order':250,'Chaos':250},
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.03,'water elemental':0.03,'terrain':.05},'Chaos':{'all':-.03}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05,'terrain':0.2}},
                               'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                        'Chaos':{'force':0.05,'kraken':0.05,'terrain':0.2}}},clear_los=False)
lava = Terrain('lava', 'lava','L',12,'~','lava',pass_through=False,degradable=False,
                      degrade_to = {'Nature':'L','Order':'L','Chaos':'L'},
                degr_mess = {'Nature':'ritual_calm_fire','Order':'ritual_suppress_fire','Chaos':'ritual_awaken_fire'},
                degrade_tool = {'Nature':['inherent'],'Order':['inherent'],'Chaos':['inherent']},
                tire={'Nature':50,'Order':50,'Chaos':50},
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.05,'terrain':.05,'calm_lava':175},
                                         'Chaos':{'all':-.05},'Order':{'all':-.05}},
                               'Order':{'Nature':{'all':-.05},'Chaos':{'all':-.05},
                                        'Order':{'force':0.05,'dwarf':0.05,'terrain':0.05,'suppress_lava':150}},
                               'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                        'Chaos':{'force':0.05,'spirit of chaos':0.05,'terrain':0.05,'awaken_lava':-125}}})
lava_rock = Terrain('lava rock', 'mountains', 'A', 8, '~', '',
               degrade_to = {'Nature':'A','Order':'.','Chaos':'.'},
                degr_mess = {'Nature':'touch_rock','Order':'break_rock','Chaos':'break_rock'},
                degrade_tool = {'Nature':['inherent'],'Order':['pickaxe','pick','big hammer'],'Chaos':['pickaxe','pick','big hammer']},
                tire={'Nature':0,'Order':150,'Chaos':150},tire_move=20,
                loot = {'Nature':[],'Order':[[1308,100,2,5]],'Chaos':[[4,100,1,5]]},
                force_effects={'Nature':{'Nature':{'force':0.01,'gnome':0.01},'Chaos':{'all':-.01},'Order':{'all':-.01}},
                               'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05}},
                               'Chaos':{'Nature':{'all':-.05},'Chaos':{'force':0.05,'troll':0.05}}})
wood_door_c = Terrain('wooden door','door_c','+',6,'+','',False,True,True,
               degrade_to = {'door':'`','Nature':'+','Order':'+','Chaos':'.'},
                degr_mess = {'Nature':'paint_door','Order':'strenghten_door','Chaos':'break_door'},
                degrade_tool = {'Nature':['flowers'],'Order':['hammer'],'Chaos':['big hammer']},
                tire={'Nature':0,'Order':40,'Chaos':100},tire_move=20,
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.01,'fairy':0.01,'terrain':0.05,'expend':'flowers'},'Chaos':{'all':-.01}},
                               'Order':{'Chaos':{'all':-.02},'Order':{'expend':'wood','force':0.02,'spirit of order':0.02}},
                               'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                        'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2,'population':-1}}},clear_los=False)
wood_door_o = Terrain('wooden door','door_o','`',6,'`','',True,True,True,
               degrade_to = {'door':'+','Nature':'`','Order':'`','Chaos':'.'},
                degr_mess = {'Nature':'paint_door','Order':'strenghten_door','Chaos':'break_door'},
                degrade_tool = {'Nature':['flowers'],'Order':['hammer'],'Chaos':['big hammer']},
                tire={'Nature':0,'Order':40,'Chaos':100},
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.01,'fairy':0.01,'terrain':0.05,'expend':'flowers'},'Chaos':{'all':-.01}},
                               'Order':{'Chaos':{'all':-.02},'Order':{'expend':'wood','force':0.02,'spirit of order':0.02}},
                               'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                        'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2,'population':-1}}})
stone_door_c = Terrain('stone door','door_c','s',7,'+','',False,True,True,
               degrade_to = {'door':'S','Nature':'s','Order':'s','Chaos':'.'},
                degr_mess = {'Nature':'paint_door','Order':'strenghten_door','Chaos':'break_door'},
                degrade_tool = {'Nature':['flowers'],'Order':['hammer'],'Chaos':['big hammer']},
                tire={'Nature':0,'Order':40,'Chaos':100},tire_move=20,
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.01,'fairy':0.01,'terrain':0.05,'expend':'flowers'},'Chaos':{'all':-.01}},
                               'Order':{'Chaos':{'all':-.02},'Order':{'expend':'clay','force':0.02,'spirit of order':0.02}},
                               'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                        'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2,'population':-1}}},clear_los=False)
stone_door_o = Terrain('stone door','door_o','S',7,'`','',True,True,True,
               degrade_to = {'door':'s','Nature':'S','Order':'S','Chaos':'.'},
                degr_mess = {'Nature':'paint_door','Order':'strenghten_door','Chaos':'break_door'},
                degrade_tool = {'Nature':['flowers'],'Order':['hammer'],'Chaos':['big hammer']},
                tire={'Nature':0,'Order':40,'Chaos':100},
                loot = {'Nature':[],'Order':[],'Chaos':[]},
                force_effects={'Nature':{'Nature':{'force':0.01,'fairy':0.01,'terrain':0.05,'expend':'flowers'},'Chaos':{'all':-.01}},
                               'Order':{'Chaos':{'all':-.02},'Order':{'expend':'clay','force':0.02,'spirit of order':0.02}},
                               'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                        'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2,'population':-1}}})
up_stair = Terrain('staircase going up','','>',7,'>','up_stair',True,False,False,clear_los=False)
down_stair = Terrain('staircase going down','','<',7,'<','down_stair',True,False,False,clear_los=False)

T = Terrain.__refs__[Terrain]
