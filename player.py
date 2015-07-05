import message
import msvcrt
from terrain import T
import random
from inventory import put_item
from inventory import stone
from inventory import wood_arrow
from inventory import wood_bolt

race_attrs={'elf':              {'Str':15,'End':16,'Dex':20,'Int':17,'Cre':5, 'Mnd':15},
            'gnome':            {'Str':12,'End':14,'Dex':14,'Int':20,'Cre':14,'Mnd':15},
            'spirit of nature': {'Str':12,'End':10,'Dex':18,'Int':18,'Cre':8, 'Mnd':20},
            'dryad':            {'Str':10,'End':10,'Dex':20,'Int':17,'Cre':13,'Mnd':15},
            'water elemental':  {'Str':16,'End':18,'Dex':17,'Int':14,'Cre':5, 'Mnd':13},
            'fairy':            {'Str':8, 'End':9, 'Dex':19,'Int':17,'Cre':8, 'Mnd':18},
            
            'human':            {'Str':14,'End':14,'Dex':16,'Int':16,'Cre':20,'Mnd':16},
            'dwarf':            {'Str':18,'End':16,'Dex':12,'Int':14,'Cre':20,'Mnd':12},
            'spirit of order':  {'Str':12,'End':10,'Dex':14,'Int':18,'Cre':18,'Mnd':20},
            
            'ork':              {'Str':18,'End':18,'Dex':13,'Int':10,'Cre':2, 'Mnd':12},
            'troll':            {'Str':20,'End':20,'Dex':4, 'Int':8, 'Cre':1, 'Mnd':8},
            'spirit of chaos':  {'Str':15,'End':13,'Dex':12,'Int':18,'Cre':3, 'Mnd':20},
            'goblin':           {'Str':11,'End':15,'Dex':17,'Int':11,'Cre':10,'Mnd':13},
            'kraken':           {'Str':19,'End':17,'Dex':14,'Int':15,'Cre':4, 'Mnd':13},
            'imp':              {'Str':10,'End':15,'Dex':16,'Int':15,'Cre':8, 'Mnd':15}}


class Player:
    def __init__(self, xy, race,force,game):
        self.game=game
        self.xy = xy
        self.base_attr = race_attrs[race]
        self.attr = {}
        start_force = 34.
        for x in self.base_attr:
            self.attr[x] = int(self.base_attr[x] * start_force/100.)
        self.max_attr = self.attr.copy()
        self.races = {'Nature':{'elf':.0,'gnome':.0,'spirit of nature':.0,'dryad':.0,'water elemental':.0,'fairy':.0,},
                      'Order':{'human':.0,'dwarf':.0,'spirit of order':.0},
                      'Chaos':{'ork':.0,'troll':.0,'spirit of chaos':.0,'goblin':.0,'kraken':.0,'imp':.0}}
        self.forces={'Nature':0.0,'Order':0.0,'Chaos':0.0}
        self.forces[force] += start_force
        self.start_force=force
        self.races[force][race] += start_force
        self.locked_race=race
        self.research_race='human'
        self.research_force='Order'
        self.research_races = {'Nature':{'elf':.0,'gnome':.0,'spirit of nature':.0,'dryad':.0,'water elemental':.0,'fairy':.0,},
                      'Order':{'human':.0,'dwarf':.0,'spirit of order':.0},
                      'Chaos':{'ork':0.0,'troll':.0,'spirit of chaos':.0,'goblin':.0,'kraken':.0,'imp':.0}}
        self.research_forces={'Nature':0.0,'Order':0.0,'Chaos':0.0}
        self.mode=force
        self.worked_places={'Nature':[],'Chaos':[],'Order':[]}
        self.max_weight = self.attr['Str']*10
        self.max_weaps = self.attr['Str']
        self.energy = self.attr['End']*100
        self.max_energy = self.attr['End']*100
        self.dmg = max([self.attr['Str'] / 5, 1])
        self.life = self.attr['End'] + self.attr['End']/4
        self.max_life = self.attr['End'] + self.attr['End']/4
        self.target=[]
        self.turn = 0
        self.place_time = 1
        self.tag = '@'
        self.id = 0
        self.game_id = 0
        self.inventory = []
        self.equipment = {'Head':[],'Neck':[],'Chest':[],'Back':[],'Arms':[],'Right hand':[],'Left hand':[],'On hands':[],
                     'Belt':[],'Legs':[],'Feet':[],'Backpack':[],'Sheath':[],'Belt tool 1':[],'Belt tool 2':[],
                     'Ammunition':[],'Left ring':[],'Right ring':[],'Jewel':[]}
        self.equip_tags = ['Backpack','Head','Neck','Chest','Jewel','Back','Arms','Right hand','Left hand','On hands',
                           'Left ring','Right ring','Belt','Legs','Feet','Sheath','Belt tool 1','Belt tool 2','Ammunition']
        self.backpack = 0
        self.free_hands = 2
        self.equiped_weaps = 0
        self.weapon_weight = 0
        self.battle_att=0
        self.att_att=''
        self.def_att=''
        self.skills = {}
        self.tool_tags = ['inherent']
        self.attr_colors = {'Str':7,'End':7,'Dex':7,'Int':7,'Cre':7,'Mnd':7}
        self.weapon_dmg = 0
        self.weapon_skills = {'Unarmed':float(self.attr['Dex'])}
        self.weapon_skill = float(self.attr['Dex'])
        self.armour = 0
        self.armour_weight = 0
        self.armour_mod=1
        self.emotion = 7
        self.weight = 0
        self.thirst = 0
        self.hunger = 0
        self.work = 0
        self.known_areas = []
        self.sit = False
        self.rest = 1
        self.name = ''
        self.effects = {}
        self.land_effects = {}
        self.followers = []
        self.ride = []
        self.possessed=[]
        self.marked_stone=[]

    def move(self,key):
        md = {'1':[-1,1], '2':[0,1], '3':[1,1], '4':[-1,0], '5':[0,0],
              '6':[1,0], '7':[-1,-1], '8':[0,-1], '9':[1,-1], '0':[0,0]}
        x = self.xy[0]
        y = self.xy[1]
        a = 0
    ##    try:
        if (key == '0'):
            return 1
        if 'troll2' in self.tool_tags and self.turn%2 and self.turn%2400<1200:
            message.message('day_troll')
            return 1
        if (key == '5'):
            message.message('')
            message.message('wait')
            if (self.energy < self.max_energy) and not (self.hunger>79 or self.thirst>79):
                self.energy += 1
        elif self.possessed and 'spirit of nature3' in self.tool_tags:
            init_screen.possession_score(33,self)
        for a in range(2):
            self.xy[a] = self.xy[a] + md[key][a]
        self.check_passage(self.xy, x, y)
        init_screen.draw_move(self, x, y)
    ##    except KeyError:
    ##        message.message('movement_error')

    def check_passage(self,xy, x, y):
        if (xy[0] == 20) or (xy[0] == 79) or (xy[1] == 0) or (xy[1] == 24):
            if (xy[0] == 20):
                direction = 2
            elif (xy[0] == 79):
                direction = 3
            elif (xy[1] == 0):
                direction = 0
            elif (xy[1] == 24):
                direction = 1
            if not int(init_screen.directions[direction]) and init_screen.current_area != 'world':
                message.message('leave_world')
                xy[0] = x
                xy[1] = y
                return 1
            elif not int(init_screen.directions[direction]) and init_screen.current_area == 'world':
                xy[0] = x
                xy[1] = y
                message.message('nowhere_togo')
            else:
                xy[0] = x
                xy[1] = y
                travel = init_screen.change_place('area%s' %(init_screen.directions[direction]),direction)
            return 1
        elif (T[init_screen.land[xy[1]-1][xy[0]-21]].pass_through or \
             ('spirit of order1' in self.tool_tags and T[init_screen.land[xy[1]-1][xy[0]-21]].id in '#o+`sS') or \
             ('spirit of chaos1' in self.tool_tags and T[init_screen.land[xy[1]-1][xy[0]-21]].id in '#o+`sS') or \
             ('gnome1' in self.tool_tags and T[init_screen.land[xy[1]-1][xy[0]-21]].id in 'nmA%') or \
             'waterform' in self.effects) and \
             not (self.possessed and T[init_screen.land[xy[1]-1][xy[0]-21]].id in self.possessed[0].terr_restr):
            if 'waterform' in self.effects:
                return 0
            for a in all_creatures:
                if (a.xy == xy) and (a not in hidden):
                    if a.mode in ['hostile','standing_hostile']:
                        if not self.ride:
                            init_screen.combat(self, a)
                        else:
                            message.message('no_riding_fighting')
                        xy[0] = x
                        xy[1] = y
                        return 1
                    else:
                        if a.t=='sentient' and not self.possessed:
                            message.creature('talk',a)
                            answer=msvcrt.getch()
                            if answer.lower()=='y':
                                xy[0] = x
                                xy[1] = y
                                init_screen.talk(a)
                                return 1
                            else:
                                message.message('')
                                if 'goblin1' in self.tool_tags:
                                    message.creature('steal',a)
                                    answer=msvcrt.getch()
                                    if answer.lower()=='y':
                                        effect('force',{'Chaos':{'force':0.02,'goblin':0.02},'Nature':{'all':-.01},'Order':{'all':-.01}})
                                        xy[0] = x
                                        xy[1] = y
                                        init_screen.pickpocket(a)
                                        return 1
                                    else:
                                        message.message('')
                        elif 'tame' in a.attr and 'tame' not in a.name and 'human2' in self.tool_tags\
                              and not self.possessed:
                            message.creature('tame',a)
                            answer=msvcrt.getch()
                            if answer.lower()=='y':
                                effect('force',{'Order':{'force':0.02,'human':0.02}})
                                init_screen.tame(a)
                                xy[0] = x
                                xy[1] = y
                                return 1
                            else:
                                message.message('')
                        elif a in self.followers and 'human2' in self.tool_tags\
                              and not self.possessed:
                            message.creature('tamed_use',a)
                            answer=msvcrt.getch()
                            if answer.lower()=='y':
                                effect('force',{'Order':{'force':0.01,'human':0.01}})
                                init_screen.command_tamed(a)
                                xy[0] = x
                                xy[1] = y
                                return 1
                            else:
                                message.message('')
                        elif 'spirit of nature2' in self.tool_tags and not self.possessed and not self.ride:
                            message.creature('possess',a)
                            answer=msvcrt.getch()
                            if answer.lower()=='y':
                                effect('force',{'Nature':{'force':0.03,'spirit of nature':0.03}})
                                init_screen.possess(a)
                                xy[0] = x
                                xy[1] = y
                                return 1
                            else:
                                message.message('')
                        if not self.ride:
                            message.creature('attack',a)
                            answer=msvcrt.getch()
                            if answer.lower()=='y':
                                a.mode='hostile'
                                for each_other in all_creatures:
                                    if each_other.force==a.force and (a.t=='sentient' and each_other.t=='sentient') and not (a.force=='Chaos' and (self.mode=='Chaos' or ('spirit of order3' in self.tool_tags and random.randint(1,30)>each_other.attr['Mnd']))):
                                        each_other.mode='hostile'
                                init_screen.combat(self, a)
                            else:
                                message.message('')
                        xy[0] = x
                        xy[1] = y
                        return 1
            if (T[init_screen.land[xy[1]-1][xy[0]-21]].tire_move > self.energy) and not \
               ('kraken1' in self.tool_tags and T[init_screen.land[xy[1]-1][xy[0]-21]].id in 'wWt~') and not \
               ('winterwalk' in self.effects and T[init_screen.land[xy[1]-1][xy[0]-21]].id in "'i") and not \
               ('summerwalk' in self.effects and T[init_screen.land[xy[1]-1][xy[0]-21]].id in ",") and not \
               (self.possessed and self.possessed[0].race=='fish' and T[init_screen.land[xy[1]-1][xy[0]-21]].id in 'wWt'):
                message.emotion('tired')
                if T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].drowning:
                    self.life -= 1
                    message.message('drown')
                xy[0] = x
                xy[1] = y
            elif not (self.possessed and self.possessed[0].race=='fish' and T[init_screen.land[xy[1]-1][xy[0]-21]].id in 'wWt'):
                if ('kraken1' in self.tool_tags and T[init_screen.land[xy[1]-1][xy[0]-21]].id in 'wWt~'):
                    message.message('kraken_move')
                elif ('winterwalk' in self.effects and T[init_screen.land[xy[1]-1][xy[0]-21]].id in "'i"):
                    message.message('fairy_%smove' %(T[init_screen.land[xy[1]-1][xy[0]-21]].name))
                elif ('summerwalk' in self.effects and T[init_screen.land[xy[1]-1][xy[0]-21]].id in ","):
                    message.message('fairy_%smove' %(T[init_screen.land[xy[1]-1][xy[0]-21]].name))
                elif ('gnome1' in self.tool_tags and T[init_screen.land[xy[1]-1][xy[0]-21]].id in 'nmA%'):
                    self.energy -= T[init_screen.land[xy[1]-1][xy[0]-21]].tire_move
                    if T[init_screen.land[xy[1]-1][xy[0]-21]].id != 'n':
                        init_screen.land[xy[1]-1]=init_screen.land[xy[1]-1][:xy[0]-21]+'n'+init_screen.land[xy[1]-1][xy[0]-20:]
                        effect('force',{'Nature':{'force':0.01,'gnome':0.01,'terrain':0.4},'Chaos':{'all':-.01},'Order':{'all':-.01}})
                    message.message('gnome_move')
                elif ('spirit of nature1' in self.tool_tags and T[init_screen.land[xy[1]-1][xy[0]-21]].id in 'd'):
                    self.energy -= T[init_screen.land[xy[1]-1][xy[0]-21]].tire_move
                    init_screen.land[xy[1]-1]=init_screen.land[xy[1]-1][:xy[0]-21]+'g'+init_screen.land[xy[1]-1][xy[0]-20:]
                    effect('force',{'Nature':{'force':0.01,'spirit of nature':0.01,'terrain':0.4},'Chaos':{'all':-.01},'Order':{'all':-.01}})
                    message.message('nature_spirit_move')
                elif ('fairy1' in self.tool_tags and T[init_screen.land[xy[1]-1][xy[0]-21]].id in '.a'):
                    self.energy -= T[init_screen.land[xy[1]-1][xy[0]-21]].tire_move
                    init_screen.land[xy[1]-1]=init_screen.land[xy[1]-1][:xy[0]-21]+'g'+init_screen.land[xy[1]-1][xy[0]-20:]
                    effect('force',{'Nature':{'force':0.01,'fairy':0.01,'terrain':0.4},'Chaos':{'all':-.01},'Order':{'all':-.01}})
                    message.message('fairy_move')
                elif ('dryad1' in self.tool_tags and T[init_screen.land[xy[1]-1][xy[0]-21]].id in 'D'):
                    self.energy -= T[init_screen.land[xy[1]-1][xy[0]-21]].tire_move
                    init_screen.land[xy[1]-1]=init_screen.land[xy[1]-1][:xy[0]-21]+'T'+init_screen.land[xy[1]-1][xy[0]-20:]
                    effect('force',{'Nature':{'force':0.01,'dryad':0.01,'terrain':0.4},'Chaos':{'all':-.01},'Order':{'all':-.01}})
                    message.message('dryad_move')
                elif ('goblin2' in self.tool_tags and T[init_screen.land[xy[1]-1][xy[0]-21]].id in 'wW'):
                    self.energy -= T[init_screen.land[xy[1]-1][xy[0]-21]].tire_move
                    init_screen.land[xy[1]-1]=init_screen.land[xy[1]-1][:xy[0]-21]+'t'+init_screen.land[xy[1]-1][xy[0]-20:]
                    effect('force',{'Chaos':{'force':0.01,'goblin':0.01,'terrain':0.4},'Nature':{'all':-.01},'Order':{'all':-.01}})
                    message.message('goblin_move')
                elif ('spirit of chaos2' in self.tool_tags and T[init_screen.land[xy[1]-1][xy[0]-21]].id in 'gT'):
                    self.energy -= T[init_screen.land[xy[1]-1][xy[0]-21]].tire_move
                    if T[init_screen.land[xy[1]-1][xy[0]-21]].id=='g':
                        init_screen.land[xy[1]-1]=init_screen.land[xy[1]-1][:xy[0]-21]+'d'+init_screen.land[xy[1]-1][xy[0]-20:]
                    elif T[init_screen.land[xy[1]-1][xy[0]-21]].id=='T':
                        init_screen.land[xy[1]-1]=init_screen.land[xy[1]-1][:xy[0]-21]+'D'+init_screen.land[xy[1]-1][xy[0]-20:]
                    effect('force',{'Chaos':{'force':0.01,'spirit of chaos':0.01,'terrain':0.4},'Nature':{'all':-.01},'Order':{'all':-.01}})
                    message.message('chaos_spirit_move')
                else:
                    self.energy -= T[init_screen.land[xy[1]-1][xy[0]-21]].tire_move
                    message.message(T[init_screen.land[xy[1]-1][xy[0]-21]].mess)
                for item in init_screen.ground_items:
                    if item[:2] == xy:
                        message.use('gr_item',item[2],item[2].qty,xy)
                        break
        elif 'door_' in T[init_screen.land[xy[1]-1][xy[0]-21]].world_name:
            init_screen.open_door(xy,self)
            xy[0] = x
            xy[1] = y
        else:
            if not T[init_screen.land[xy[1]-1][xy[0]-21]].pass_through:
                message.message(T[init_screen.land[xy[1]-1][xy[0]-21]].mess)
            xy[0] = x
            xy[1] = y

    def pick_up(self,ground):
        it = 0
        pile = []
        for item in ground:
            if item[:2] == self.xy:
                pile.append(item)
        if len(pile) > 1:
            it = 1
            init_screen.c.page()
            init_screen.c.write(' You search through the items on the ground.\n What do you want to pick up?\n\n')
            for i in range(len(pile)):
                print ' '+chr(i+97)+')  ', pile[i][2].name+', %d x %s stones' %(pile[i][2].qty,str(pile[i][2].weight))
                init_screen.c.text(4,i+3,pile[i][2].tag,pile[i][2].color)
            print '\n You can carry %s more stones.\n Your backpack can take %s more stones.' %(str(self.max_weight - self.weight),
                                                                                                str(self.backpack))
            i1 = ' '
            while 1:
                if msvcrt.kbhit():
                    i1 = msvcrt.getch()
                    break
            init_screen.c.rectangle((0,0,60,2))
        elif len(pile) == 1:
            i1 = 'a'
            it = 1
        if len(pile) > 0:
            try:
                if pile[ord(i1)-97][2].qty > 1 and self.equipment['Backpack'] != []:
                    message.message('pickup')                    
                    a = ''
                    i = ' '
                    while ord(i) != 13:
                        i = msvcrt.getch()
                        if ord(i) in range(48,58):
                            init_screen.c.write(i)
                            a += i
                    message.message('')
                    if a =='' or int(a)==0:
                        init_screen.redraw_screen()
                        return 1
                    a=int(a)
                else:
                    a = 1
            except IndexError:
                init_screen.redraw_screen()
                return 0
            if a > pile[ord(i1)-97][2].qty:
                a = pile[ord(i1)-97][2].qty
            if self.weight + pile[ord(i1)-97][2].weight * a <= self.max_weight and pile[ord(i1)-97][2].weight * a <= self.backpack:
                pile[ord(i1)-97][2].get_item(a)
                if len(pile) > 1:
                    init_screen.redraw_screen()
                if a < pile[ord(i1)-97][2].qty:
                    pile[ord(i1)-97][2].qty -= a
                else:
                    ground.remove(pile[ord(i1)-97])
            elif self.weight + pile[ord(i1)-97][2].weight * a > self.max_weight:
                if len(pile) > 1:
                    init_screen.redraw_screen()
                message.use('cant_carry', pile[ord(i1)-97][2])
            elif pile[ord(i1)-97][2].weight * a > self.backpack:
                if self.equipment['Backpack'] == []:
                    if 'two_handed' in pile[ord(i1)-97][2].type:
                        needed_hands = 2
                    else:
                        needed_hands = 1
                    if self.free_hands >= needed_hands:
                        pile[ord(i1)-97][2].get_item()
                        self.free_hands -= needed_hands
                        if 1 < pile[ord(i1)-97][2].qty:
                            pile[ord(i1)-97][2].qty -= 1
                        else:
                            ground.remove(pile[ord(i1)-97])
                        if len(pile) > 1:
                            init_screen.redraw_screen()
                        self.backpack = 0
                    else:
                        if len(pile) > 1:
                            init_screen.redraw_screen()
                        message.message('drop_first')
                else:
                    if len(pile) > 1:
                        init_screen.redraw_screen()
                    message.use('cant_fit_in_backpack', pile[ord(i1)-97][2])
            
        if it == 0:
            message.message('no_pickup')

    def take_off(self,item):
        has_it = 0
        dropped = 0
        for x in self.inventory:
            if self.equipment[self.equip_tags[item]].id == x.id and self.equipment[self.equip_tags[item]].name == x.name:
                has_it = 1
                break
        if self.backpack >= self.equipment[self.equip_tags[item]].weight*self.equipment[self.equip_tags[item]].qty or self.equip_tags[item] == 'Backpack' or (self.equipment['Backpack'] == [] and ((self.free_hands > 0 and self.equip_tags[item] not in ['Right hand','Left hand']) or  self.equip_tags[item] in ['Right hand','Left hand'])):
            if self.equipment[self.equip_tags[item]].stackable and has_it == 1:
                x.qty += self.equipment[self.equip_tags[item]].qty
            else:
                self.inventory.append(self.equipment[self.equip_tags[item]])
        else:
            drop = self.equipment[self.equip_tags[item]].duplicate(self.equipment[self.equip_tags[item]].qty)
            print ' There\'s no place in your backpack so you drop\n the %s to the ground!' %drop.name
            wait = msvcrt.getch()
            for i in init_screen.ground_items:
                if i[:2] == self.xy and i[2].id == drop.id and i[2].name == drop.name and i[2].stackable:
                    i[2].qty += drop.qty
                    dropped = 1
            if not dropped:
                init_screen.ground_items.append([self.xy[0], self.xy[1],drop])
                dropped = 1
        if 'weapon' in self.equipment[self.equip_tags[item]].type and self.equip_tags[item] in ['Right hand','Left hand']:
            if self.equiped_weaps == 1:
                self.weapon_skills[self.equipment[self.equip_tags[item]].weapon_type.capitalize()] = self.weapon_skill
                self.weapon_skill = self.weapon_skills['Unarmed']
            elif self.equiped_weaps == 2:
                if self.equip_tags[item] == 'Right hand':
                    self.weapon_skills[self.equipment[self.equip_tags[item]].weapon_type.capitalize()] = self.weapon_skill
                    self.weapon_skill = self.weapon_skills[self.equipment['Left hand'].weapon_type.capitalize()]
            self.equiped_weaps -= 1
            self.max_weaps += self.equipment[self.equip_tags[item]].weight
        if 'armour' in self.equipment[self.equip_tags[item]].type and self.equip_tags[item] in self.equipment[self.equip_tags[item]].type:
            self.armour -= self.equipment[self.equip_tags[item]].armour
            self.armour_weight -= self.equipment[self.equip_tags[item]].weight
            if self.armour_weight:
                self.armour_mod = min([float(self.max_weight)/self.armour_weight, 2]) - 1
            else:
                self.armour_mod=1
        if self.equip_tags[item] in self.equipment[self.equip_tags[item]].type:
            if 'temp_attr' in self.equipment[self.equip_tags[item]].effect:
                for v in self.equipment[self.equip_tags[item]].effect['temp_attr']:
                    used = effect('temp_attr_reverse',v)
            if 'invisibility' in self.equipment[self.equip_tags[item]].effect:
                self.equipment[self.equip_tags[item]].effect['invisibility']-=1
                if self.equipment[self.equip_tags[item]].effect['invisibility']<=0:
                    self.equipment[self.equip_tags[item]].name+=' (depleted)'
                    self.equipment[self.equip_tags[item]].effect.pop('invisibility')
                if 'invisible' in self.effects:
                    del(self.effects['invisible'])
            if 'winterwalk' in self.equipment[self.equip_tags[item]].effect:
                self.equipment[self.equip_tags[item]].effect['winterwalk']-=1
                if self.equipment[self.equip_tags[item]].effect['winterwalk']<=0:
                    self.equipment[self.equip_tags[item]].name+=' (depleted)'
                    self.equipment[self.equip_tags[item]].effect.pop('winterwalk')
                if 'winterwalk' in self.effects:
                    del(self.effects['winterwalk'])
            if 'summerwalk' in self.equipment[self.equip_tags[item]].effect:
                self.equipment[self.equip_tags[item]].effect['summerwalk']-=1
                if self.equipment[self.equip_tags[item]].effect['summerwalk']<=0:
                    self.equipment[self.equip_tags[item]].name+=' (depleted)'
                    self.equipment[self.equip_tags[item]].effect.pop('summerwalk')
                if 'summerwalk' in self.effects:
                    del(self.effects['summerwalk'])
            if 'fairyland' in self.equipment[self.equip_tags[item]].effect:
                self.equipment[self.equip_tags[item]].effect['fairyland']-=1
                if self.equipment[self.equip_tags[item]].effect['fairyland']<=0:
                    self.equipment[self.equip_tags[item]].name+=' (withered)'
                    self.equipment[self.equip_tags[item]].effect.pop('fairyland')
                if 'fairyland' in self.effects:
                    del(self.effects['fairyland'])
            if 'midnight fears' in self.equipment[self.equip_tags[item]].effect:
                self.equipment[self.equip_tags[item]].effect['midnight fears']-=1
                if self.equipment[self.equip_tags[item]].effect['midnight fears']<=0:
                    self.equipment[self.equip_tags[item]].name+=' (withered)'
                    self.equipment[self.equip_tags[item]].effect.pop('midnight fears')
                if 'midnight fears' in self.effects:
                    del(self.effects['midnight fears'])
            if 'sun armour' in self.equipment[self.equip_tags[item]].effect:
                self.equipment[self.equip_tags[item]].effect['sun armour']-=1
                if self.equipment[self.equip_tags[item]].effect['sun armour']<=0:
                    self.equipment[self.equip_tags[item]].name+=' (withered)'
                    self.equipment[self.equip_tags[item]].effect.pop('sun armour')
                if 'sun armour' in self.effects:
                    del(self.effects['sun armour'])
                    if self.sun_armour:
                        self.armour-=self.sun_armour
                        self.sun_armour=0
        if 'totem' in self.equipment[self.equip_tags[item]].type:
            for cr in game_creatures:
                if cr.name==self.equipment[self.equip_tags[item]].name[:-6]:
                    break
            temps=[]
            for ats in self.attr:
                the_at=int(cr.attr[ats]*self.equipment[self.equip_tags[item]].effect[cr.name]/100.)
                if the_at:
                    temps.append([ats,the_at])
            if temps:
                self.equipment[self.equip_tags[item]].effect['temp_attr']=temps[:]
        if self.equip_tags[item] == 'Backpack':
            for i in self.inventory[:-1]:
                i.lose_item(i.qty)
                self.inventory[-1].effect['contains'].append(i)
                self.inventory[-1].weight += i.weight * i.qty
                self.weight += i.weight * i.qty
            init_screen.ground_items.append([self.xy[0], self.xy[1], self.inventory[-1]])
            self.inventory[-1].lose_item()
            self.backpack = 0
        elif not dropped and self.equipment['Backpack'] != []:
            self.backpack -= self.equipment[self.equip_tags[item]].weight*self.equipment[self.equip_tags[item]].qty
        if self.equip_tags[item] in ['Right hand','Left hand'] or 'armour' in self.equipment[self.equip_tags[item]].type:
            self.weapon_dmg -= self.equipment[self.equip_tags[item]].dmg
        if self.equip_tags[item] in ['Right hand','Left hand']:
            self.weapon_weight -= self.equipment[self.equip_tags[item]].weight
            take_effect()
            if self.equipment['Backpack'] != []:
                self.free_hands += 1
                if 'two_handed' in self.equipment[self.equip_tags[item]].type:
                    self.free_hands += 1
        else:
            if self.equipment['Backpack'] == [] and not dropped:
                self.free_hands -= 1
                    
        self.equipment[self.equip_tags[item]] = []
            
    def equip(self,item,slot):
        if 'weapon' in item.type:
            if self.equiped_weaps==1 and item.weight>self.max_weaps:
                print ' You are not strong enough to wield this weapon with your current one!'
                msvcrt.getch()
                return 0
            else:
                self.max_weaps -= item.weight
        if item.stackable and item.qty > 1:
            self.equipment[self.equip_tags[slot]] = item.duplicate(1)
            item.qty -= 1
        else:
            self.equipment[self.equip_tags[slot]] = item
            self.inventory.remove(item)
        if self.equip_tags[slot] in ['Right hand','Left hand']:
            self.weapon_weight += item.weight
            take_effect()
            if 'two_handed' in item.type:
                if self.equip_tags[slot] == 'Right hand' and self.equipment['Left hand'] != []:
                    self.take_off(self.equip_tags.index('Left hand'))
                elif self.equip_tags[slot] == 'Left hand' and self.equipment['Right hand'] != []:
                    self.take_off(self.equip_tags.index('Right hand'))
                if self.equipment['Backpack'] != []:
                    self.free_hands -= 2
            else:
                if self.equipment['Backpack'] != []:
                    self.free_hands -= 1
        elif self.equipment['Backpack'] == [] or 'Backpack' in item.type:
            self.free_hands += 1
        if 'weapon' in item.type and self.equip_tags[slot] in ['Right hand','Left hand']:
            if item.weight < 6:
                learning_attr='Dex'
            else:
                learning_attr='Str'
            if item.weapon_type.capitalize() not in self.weapon_skills:
                self.weapon_skills[item.weapon_type.capitalize()] = float(self.attr[learning_attr])
            if self.equiped_weaps == 0:
                self.weapon_skills['Unarmed'] = self.weapon_skill
                self.weapon_skill = self.weapon_skills[item.weapon_type.capitalize()]
            elif self.equiped_weaps == 1 and self.equip_tags[slot] == 'Right hand':
                self.weapon_skills[self.equipment['Left hand'].weapon_type.capitalize()] = self.weapon_skill
                self.weapon_skill = self.weapon_skills[item.weapon_type.capitalize()]
            self.equiped_weaps += 1
        elif 'armour' in item.type and self.equip_tags[slot] in item.type:
            self.armour += item.armour
            self.armour_weight += item.weight
            self.armour_mod = min([float(self.max_weight)/self.armour_weight, 2]) - 1
        if 'temp_attr' in item.effect and self.equip_tags[slot] in item.type:
            for v in item.effect['temp_attr']:
                used = effect('temp_attr',v)
        if 'invisibility' in item.effect and self.equip_tags[slot] in item.type:
            self.effects['invisible']=10
        if 'winterwalk' in item.effect and self.equip_tags[slot] in item.type:
            self.effects['winterwalk']=1
        if 'summerwalk' in item.effect and self.equip_tags[slot] in item.type:
            self.effects['summerwalk']=1
        if 'fairyland' in item.effect and self.equip_tags[slot] in item.type:
            self.effects['fairyland']=1
        if 'midnight fears' in item.effect and self.equip_tags[slot] in item.type:
            if self.turn%2400<1200:
                item.effect['midnight fears']=0
            else:
                self.effects['midnight fears']=1200-ch.turn%1200
            if item.effect['midnight fears']==0:
                item.name+=' (withered)'
                item.effect.pop('midnight fears')
        if 'sun armour' in item.effect and self.equip_tags[slot] in item.type:
            if self.turn%2400>=1200:
                item.effect['sun armour']=0
            else:
                self.effects['sun armour']=1200-ch.turn%2400
                self.sun_armour=0
            if item.effect['sun armour']==0:
                item.name+=' (withered)'
                item.effect.pop('sun armour')
        if 'Backpack' in item.type and self.equip_tags[slot] not in ['Right hand','Left hand']:
            if len(self.inventory):
                self.backpack -= self.inventory[0].weight*self.inventory[0].qty
                self.free_hands += 1
            for i in item.effect['contains']:
                self.inventory.append(i)
                self.backpack -= i.weight*i.qty
                item.weight -= i.weight*i.qty
                if i.tool_tag:
                    self.tool_tags.append(i.tool_tag[0])
            item.effect['contains'] = []
            ## Tegloto koeto se pobira v ranicata e ravno na neinoto teglo po 6.
            self.backpack += item.weight * 6
            while self.backpack < 0:
                drop = self.inventory[0].drop_item('forced')
                dropped = 0
                print ' There\'s no place in your backpack for the %s so you drop it to the ground!\n' %drop.name
                wait = msvcrt.getch()
                for i in init_screen.ground_items:
                    if i[:2] == self.xy and i[2].id == drop.id and i[2].name == drop.name and i[2].stackable:
                        i[2].qty += drop.qty
                        dropped = 1
                if not dropped:
                    init_screen.ground_items.append([self.xy[0], self.xy[1],drop])
        elif self.equipment['Backpack'] != []:
            self.backpack += item.weight
        if self.equip_tags[slot] in ['Right hand','Left hand'] or 'armour' in item.type:
            self.weapon_dmg += item.dmg

    def find_equipment(self,slot):
        init_screen.c.page()
        init_screen.c.pos(0,3)
        found = 0
        items = ''
        for i in self.inventory:
            if self.equip_tags[slot] in ['Right hand','Left hand']:
                print ' '+chr(self.inventory.index(i)+97)+')', i.name.capitalize()+', %d x %s stones' %(i.qty,str(i.weight))
                found += 1
                items += chr(self.inventory.index(i)+97)
            elif self.equip_tags[slot] in i.type:
                print ' '+chr(self.inventory.index(i)+97)+')', i.name.capitalize()+', %d x %s stones' %(i.qty,str(i.weight))
                found += 1
                items += chr(self.inventory.index(i)+97)
        if not found:
            print ' You have nothing usefull to equip.'
            i1 = msvcrt.getch()
            return 0
        else:
            init_screen.c.pos(0,1)
            print ' What do you want to equip?'
            i1 = msvcrt.getch()
            if i1 in items:
                self.equip(self.inventory[ord(i1)-97],slot)
            return 0

    def force_attack(self,defender):
        ## Force effects based on mode and enemy
        if self.mode=='Nature':
            if defender.force=='Nature':
                if self.hunger>60 and defender.t=='animal':
                    effect('force',{'Nature':{'force':0.01,'elf':0.01},'Chaos':{'all':-0.01},'Order':{'all':-0.01}})
                else:
                    effect('force',{'Nature':{'all':-0.02},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
            elif defender.force=='Order':
                if init_screen.current_place['Chaos']>=init_screen.current_place['Nature']:
                    effect('force',{'Nature':{'force':0.01,'elf':0.01,'terrain':0.05},'Chaos':{'all':-0.01},'Order':{'all':-0.01}})
                else:
                    effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
            elif defender.force=='Chaos':
                effect('force',{'Nature':{'force':0.01,'elf':0.01,'terrain':0.05},'Chaos':{'all':-0.01},'Order':{'force':0.01}})
        elif self.mode=='Chaos':
            if defender.force=='Nature':
                effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
            elif defender.force=='Order':
                effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
            elif defender.force=='Chaos':
                effect('force',{'Chaos':{'ork':0.01}})
        elif self.mode=='Order':
            if defender.force=='Nature':
                if defender.t=='animal':
                    effect('force',{'Nature':{'all':-0.01},'Order':{'force':0.01,'human':0.01,'terrain':0.05},'Chaos':{'all':-0.01}})
                else:
                    if init_screen.current_place['Chaos']>=init_screen.current_place['Order']:
                        effect('force',{'Nature':{'all':-0.01},'Chaos':{'all':-0.01},'Order':{'force':0.01,'human':0.01,'terrain':0.05}})
                    else:
                        effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
            elif defender.force=='Order':
                if defender.t=='animal':
                    effect('force',{'Nature':{'all':-0.01},'Order':{'force':0.01,'human':0.01,'terrain':0.05},'Chaos':{'all':-0.01}})
                else:
                    effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.1},'Order':{'all':-0.02}})
            elif defender.force=='Chaos':
                if defender.t=='animal':
                    effect('force',{'Nature':{'all':-0.01},'Order':{'force':0.01,'human':0.01,'terrain':0.05},'Chaos':{'all':-0.01}})
                else:
                    effect('force',{'Nature':{'force':0.01},'Chaos':{'all':-0.01},'Order':{'force':0.01,'human':0.01,'terrain':0.05}})

class NPC(object):
    def creature_move(self):
        md = {'1':[-1,1], '2':[0,1], '3':[1,1], '4':[-1,0], '5':[0,0],
              '6':[1,0], '7':[-1,-1], '8':[0,-1], '9':[1,-1], '0':[0,0]}
        place_keys={'1':['1','2','4','3','7','8','6','9'],
                    '2':['2','1','3','4','6','7','9','8'],
                    '3':['3','2','6','1','9','4','8','7'],
                    '6':['6','3','9','2','8','1','7','4'],
                    '9':['9','6','8','3','7','2','4','1'],
                    '8':['8','9','7','6','4','3','1','2'],
                    '7':['7','8','4','9','1','6','2','3'],
                    '4':['4','7','1','8','2','9','3','6'],
                    '5':['1','2','3','4','6','7','8','9'],
                    '0':['0']}
        x = self.xy[0]
        y = self.xy[1]
        a = 0
        key = '0'
        mode = self.mode
        creature_sight=init_screen.direct_path(self.xy, ch.xy)
        creature_los = init_screen.clear_los(creature_sight)
        player_los = init_screen.clear_los(init_screen.direct_path(ch.xy,self.xy))
        if self.t=='sentient':
            if float(self.fear)/(self.fear+(self.attr['Int']+self.attr['Mnd'])*10)>random.random():
                mode='fearfull'
        if self.race=='troll' and init_screen.current_place['Chaos']>=60 and ch.turn%2 and ch.turn%2400<1200:
            self.path=[]
            mode='wander'
        if mode in ['follow','hostile','fearfull_hide','fearfull'] and ('invisible' in ch.effects or not creature_los):
            mode = 'wander'
        if mode in ['hostile','standing_hostile','fearfull_hide','fearfull'] and 'stealthy' in ch.tool_tags and creature_los:
            hide_chance=ch.attr['Dex']*3+ch.attr['Int']-self.attr['Int']+len(creature_sight)
            if random.randint(1,100)<hide_chance:
                if mode=='standing_hostile':
                    mode='standing'
                else:
                    mode='wander'
        if 'ork1' in ch.tool_tags and self.mode=='hostile' and creature_los:
            if ('human3' in ch.tool_tags and random.random()<ch.research_races['Chaos']['ork']/(2*(max([init_screen.current_place['Order'],init_screen.current_place['Nature']])+ch.research_races['Chaos']['ork'])))\
               or (random.random()<ch.races['Chaos']['ork']/(2*(max([init_screen.current_place['Order'],init_screen.current_place['Nature']])+ch.races['Chaos']['ork']))):
                    mode='fearfull'
        ## wander, follow, hostile, fearfull_hide, standing_hostile, standing, guarding, fearfull
        if mode == 'guarding':
            fighting=0
            if 'target' in self.attr and self.attr['target']!=[] and self.attr['target'] in all_creatures:
                if len(init_screen.direct_path(self.attr['target'].xy,ch.xy))<5:
                    fighting=1
                    self.path=init_screen.direct_path(self.xy,self.attr['target'].xy)
                else:
                    self.attr['target']=[]
            if not fighting:
                for enemy in all_creatures:
                    if enemy.mode=='hostile' and len(init_screen.direct_path(enemy.xy,ch.xy))<3 and init_screen.clear_los(init_screen.direct_path(self.xy,enemy.xy)):
                        fighting=1
                        self.attr['target']=enemy
                        self.path=init_screen.direct_path(self.xy,ch.attr['target'].xy)
            if not fighting:
                mode='follow'
        if mode == 'wander':
            if self.path:
                try:
                    if init_screen.good_place(self,self.path[1]):
                        self.xy = self.path[1]
                        self.path = self.path[1:]
                    else:
                        self.path=[]
                except IndexError:
                    self.path=[]
                key = '5'
            else:
                if self.race=='troll' and init_screen.current_place['Chaos']>=60 and ch.turn%2 and ch.turn%2400<1200: 
                    key='5'
                else:
                    key = str(random.randint(1,9))
        if mode in ['follow','hostile','standing_hostile','guarding']:
            if mode != 'guarding':
                self.path = init_screen.direct_path(self.xy, ch.xy)
            shot=0
            if mode=='hostile' and 'shoot' in self.attr:
                if random.randint(1,40)<self.attr['Dex'] and len(self.path)>2:
                    init_screen.shoot(self)
                    key='5'
                    shot=1
            if not shot:
                try:
                    if init_screen.good_place(self,self.path[1]):
                        self.xy = self.path[1]
                        self.path = self.path[1:]
                        key = '5'
                    else:
                        direction=[self.path[1][0]-self.xy[0],self.path[1][1]-self.xy[1]]
                        the_key='5'
                        for mdx in md:
                            if md[mdx]==direction:
                                the_key=mdx
                                break
                        found_good=0
                        breaker=0
                        while not found_good:
                            breaker+=1
                            if breaker==10:
                                key='5'
                                break
                            key = place_keys[mdx][(place_keys[mdx].index(the_key)+1)%len(place_keys[mdx])]
                            if init_screen.good_place(self,[self.xy[a]+md[key][a] for a in range(2)]):
                                found_good=1
                            else:
                                the_key=key
                except IndexError:
                    key = str(random.randint(1,9))
        if mode == 'fearfull':
            self.xy[0] -= cmp(ch.xy[0],x)
            self.xy[1] -= cmp(ch.xy[1],y)
            key='0'
        if mode == 'fearfull_hide':
            if (abs(ch.xy[0]-x) + abs(ch.xy[1]-y)) < 7:
                self.xy[0] += cmp(self.area[4],x)
                self.xy[1] += cmp(self.area[5],y)
                if ((cmp(self.area[4],x) == 0) and (cmp(self.area[5],y) == 0)) and (self not in hidden):
                    hidden.append(self)
                key = '0'
            else:
                key = str(random.randint(1,9))
            if (self in hidden) and ([x,y] != self.area[4:]):
                hidden.remove(self)
        if mode == 'standing':
            key='5'
        for a in range(2):            
            self.xy[a] = self.xy[a] + md[key][a]
        self.creature_passage(x, y)
        if self in hidden:
            if ch.xy != self.xy:
                init_screen.hide(self)
        else:
            if player_los or (init_screen.current_place['Nature']>=33 and init_screen.current_place['Temperature']>=33 and 'elf2' in ch.tool_tags):
                init_screen.draw_move(self, x, y)
            if self.race=='water elemental' and T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].id in 'wWt':
                self.attr['invisible']=2
            if 'invisible' in self.attr:
                init_screen.hide(self)
                self.attr['invisible']-=1
                if self.attr['invisible']==0:
                    del(self.attr['invisible'])

    def creature_passage(self, x, y):
        ## Check if creature is in its allowed area
        if (self.area != []):
            if (self.xy[0] < self.area[0]) or (self.xy[0] > self.area[2]) or (self.xy[1] < self.area[1]) or (self.xy[1] > self.area[3]):
                self.xy[0] = x
                self.xy[1] = y
                return 1
        ## Check if creature has moved beyond the screen boundaries
        if (self.xy[0] == 20) or (self.xy[0] == 79) or (self.xy[1] == 0) or (self.xy[1] == 24):
            self.xy[0] = x
            self.xy[1] = y
            return 1
        elif T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].id in self.terr_restr and not self.mode=='standing_hostile':
            self.xy[0] = x
            self.xy[1] = y
            return 1
        elif T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].pass_through or (self.race=='spirit of order' and init_screen.current_place['Order']>30 and T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].id in '#o+`sS') or (self.race=='spirit of chaos' and init_screen.current_place['Chaos']>30 and T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].id in '#o+`sS') or (self.race=='gnome' and init_screen.current_place['Nature']>30 and T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].id in 'nmA%'):
            for a in all_beings:
                if a.xy == self.xy and a.game_id != self.game_id:
                    self.xy[0] = x
                    self.xy[1] = y
                    if (self.mode=='guarding' and a.mode=='hostile') or (a.mode=='guarding' and self.mode=='hostile') or (a.xy == ch.xy and self.mode in ['hostile','standing_hostile'] and 'waterform' not in ch.effects):
                        init_screen.combat(self,a)
                    return 1
            if T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].tire_move>self.energy:
                if T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].drowning and self.race!='fish':
                    self.life -= 1
                self.xy[0] = x
                self.xy[1] = y
            elif not (self.race=='kraken' and init_screen.current_place['Chaos']>30 and T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].id in 'wWt~')\
                 and not (self.race=='fairy' and init_screen.current_place['Nature']>60 and T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].id in "'i,")\
                 and not (self.race=='fish' and T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].id in "Wwt~"):
                self.energy-=T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].tire_move
            if self.mode=='standing_hostile':
                self.xy[0] = x
                self.xy[1] = y
        elif 'door_' in T[init_screen.land[self.xy[1]-1][self.xy[0]-21]].world_name:
            init_screen.open_door(self.xy,self)
            self.xy[0] = x
            self.xy[1] = y
        else:
              self.xy[0] = x
              self.xy[1] = y

    
class Human(NPC):
    def __init__(self,xy,area,path,terr_restr,emotion,fear,tag,name,mode,id,attr,WD,armour,f,r,game_id=0):
        self.xy = xy[:]
        self.area = area[:]
        self.path = path[:]
        self.terr_restr = terr_restr
        self.emotion = emotion
        self.fear = fear
        self.tag = tag
        self.name = name
        self.t = 'sentient'
        self.mode = mode
        self.id = id
        self.attr = attr.copy()
        self.weapon_dmg = WD
        self.armour = int(armour)
        self.armour_mod=1
        self.weapon_skill = ((self.armour/3+max([1,WD])*40)/2)/20.0*self.attr['Dex']
        self.game_id = game_id
        self.force = f
        self.race = r
        self.life = self.attr['End'] + self.attr['End']/4
        self.max_weight = self.attr['Str']*10
        self.energy = self.attr['End']*100
        self.max_energy = self.attr['End']*100
        self.dmg = max([self.attr['Str'] / 5, 1])

    def duplicate(self,x,y,g_id,f,r,rand=False):
        xy = [x,y]
        attr_d={}
        mode=self.mode
        arm=self.armour
        WD=0
        for a in self.attr:
            attr_d[a]=int(race_attrs[r][a]*init_screen.current_place[f]/100.)
        if f=='Nature':
            emo=2
            arm=init_screen.current_place[f]*3.5
            WD=init_screen.current_place[f]/60
            if ch.forces['Chaos']:
                if ch.forces['Nature']-ch.forces['Chaos']<init_screen.current_place['Nature']-init_screen.current_place['Chaos']:
                    mode='hostile'
            ammo=wood_arrow
        elif f=='Order':
            emo=7
            arm=init_screen.current_place[f]*2.75
            WD=init_screen.current_place[f]/40
            if ch.forces['Chaos']:
                if ch.forces['Order']-ch.forces['Chaos']<init_screen.current_place['Order']-init_screen.current_place['Chaos']:
                    mode='hostile'
            ammo=wood_bolt
        elif f=='Chaos':
            emo=12
            arm=init_screen.current_place[f]*2
            WD=init_screen.current_place[f]/30
            if ch.forces['Order']:
                if ch.forces['Chaos']-ch.forces['Order']<init_screen.current_place['Chaos']-init_screen.current_place['Order']:
                    mode='hostile'
            if ch.forces['Nature']:
                if ch.forces['Chaos']-ch.forces['Nature']<init_screen.current_place['Chaos']-init_screen.current_place['Nature']:
                    mode='hostile'
            if 'spirit of order3' in ch.tool_tags and random.randint(1,30)>attr_d['Mnd']:
                mode='fearfull'
            ammo=stone
        if ch.possessed:
            mode='wander'
        duplica = Human(xy,self.area,self.path,self.terr_restr,emo,self.fear,r[0].upper(),r,
                        mode,self.id,attr_d,WD,arm,f,r,game_id=g_id)
        duplica.learning=random.random()
        duplica.attr['loot']=[[1310,100,1,4],[r,init_screen.current_place[f]+init_screen.current_place['Treasure']*10]]
        duplica.attr['shoot']=ammo
        if rand:
            duplica.random = True
            duplica.appearance=ch.turn
        else:
            duplica.random = False
            duplica.appearance=0
        return duplica

class Animal(NPC):
    def __init__(self,xy,area,path,terr_restr,emotion,tag,name,mode,id,life,attr,WS,armour,f,r,game_id=0):
        self.xy = xy[:]
        self.area = area[:]
        self.path = path[:]
        self.terr_restr = terr_restr
        self.emotion = emotion
        self.tag = tag
        self.name = name
        self.t = 'animal'
        self.mode = mode
        self.id = id
        self.life = life
        self.attr = attr.copy()
        self.weapon_dmg = 0
        self.weapon_skill = WS
        self.armour = armour
        self.armour_mod=1
        self.game_id = game_id
        self.force = f
        self.race = r
        self.max_weight = self.attr['Str']*10
        self.energy = self.attr['End']*100
        self.max_energy = self.attr['End']*100
        self.dmg = max([self.attr['Str'] / 5, 1])
        
    def duplicate(self,x,y,g_id,f,r,rand=False):
        xy = [x, y]
        duplica = Animal(xy,self.area,self.path,self.terr_restr,self.emotion,self.tag,self.name,
                         self.mode,self.id,self.life,self.attr,self.weapon_skill,self.armour,f,r,game_id=g_id)
        duplica.learning=0
        if self.mode in ['hostile','fearfull_hide','fearfull'] and 'elf1' in ch.tool_tags and self.t=='animal':
            duplica.mode = 'wander'
        if rand:
            duplica.random = True
            duplica.appearance=ch.turn
        else:
            duplica.random = False
            duplica.appearance=0
        return duplica

## Taming tags - pet, guard, ride, farm. [tag,difficulty,item requirement for taming,farming product id]
wood = Human([53, 20],[],[],'',7,0,'W','woodsman','wander',1,{'Str':6,'End':6,'Dex':4,'Int':4,'Cre':2,'Mnd':3},0,0,'Nature','elf')
wood_perm = Human([53, 20],[],[],'',7,0,'W','woodsman','wander',2,{'Str':6,'End':6,'Dex':4,'Int':4,'Cre':2,'Mnd':3},0,0,'Nature','elf')
##squirrel = Animal([30, 20],[],[],'wW',7,'s','squirrel','fearfull_hide',2,1,{'Str':1,'End':1,'Dex':3,'Int':2,'Cre':1,'Mnd':1},1,5,'Nature','squirrel')
random_squirrel = Animal([30, 20],[],[],'wW',7,'s','squirrel','wander',3,1,{'tame':['pet',25,1315],'Str':1,'End':1,'Dex':3,'Int':2,'Cre':1,'Mnd':1,'loot':[[1310,70,1,1],['squirrel skin',100,1,1]]},1,5,'Nature','squirrel')
bear = Animal([30, 20],[],[],'',6,'b','bear','wander',4,12,{'tame':['guard',95,1302],'Str':15,'End':10,'Dex':5,'Int':2,'Cre':1,'Mnd':12,'loot':[[1326,100,4,6],[1310,100,3,9],['bear skin',100,6,10]]},5,150,'Nature','bear')
wolf = Animal([30, 20],[],[],'',7,'w','wolf','wander',5,8,{'tame':['guard',60,1310],'Str':8,'End':10,'Dex':10,'Int':5,'Cre':1,'Mnd':12,'loot':[[1326,100,1,3],[1310,100,1,4],['wolf skin',100,3,6]]},10,50,'Nature','wolf')
dog = Animal([30, 20],[],[],'',6,'d','dog','wander',6,8,{'tame':['guard',40,1310],'Str':8,'End':10,'Dex':10,'Int':5,'Cre':1,'Mnd':3,'loot':[[1326,100,1,2],[1310,100,1,4],['dog skin',100,2,5]]},10,50,'Order','dog')
hyena = Animal([30, 20],[],[],'',8,'h','hyena','hostile',7,8,{'Str':12,'End':10,'Dex':10,'Int':5,'Cre':1,'Mnd':9,'loot':[[1326,100,1,3],[1310,100,1,4],['hyena skin',100,2,5]]},10,50,'Chaos','hyena')
grizzly = Animal([30, 20],[],[],'',7,'b','grizzly bear','hostile',8,12,{'Str':15,'End':10,'Dex':5,'Int':2,'Cre':1,'Mnd':13,'loot':[[1326,100,4,6],[1310,100,3,9],['bear skin',100,6,10]]},5,150,'Nature','grizzly')
snake = Animal([30, 20],[],[],'',10,'s','snake','wander',9,2,{'tame':['pet',70,1310],'Str':1,'End':1,'Dex':6,'Int':2,'Cre':1,'Mnd':7,'loot':[[1310,70,1,1],['snake skin',100,1,1]]},6,5,'Nature','snake')
poison_snake = Animal([30, 20],[],[],'',10,'s','poisonous snake','hostile',10,5,{'Str':15,'End':1,'Dex':6,'Int':2,'Cre':1,'Mnd':7,'loot':[[1310,70,1,1],['snake skin',100,1,1]]},6,5,'Chaos','poison snake')
polar_bear = Animal([30, 20],[],[],'',15,'b','polar bear','wander',11,12,{'tame':['guard',95,1310],'Str':15,'End':10,'Dex':5,'Int':2,'Cre':1,'Mnd':13,'loot':[[1326,100,4,6],[1310,100,3,9],['polar bear skin',100,6,10]]},5,150,'Nature','polar bear')
polar_wolf = Animal([30, 20],[],[],'',15,'w','polar wolf','wander',12,8,{'tame':['guard',60,1310],'Str':8,'End':10,'Dex':10,'Int':5,'Cre':1,'Mnd':13,'loot':[[1326,100,1,4],[1310,100,1,4],['polar wolf skin',100,3,6]]},10,50,'Nature','polar wolf')
wild_horse = Animal([30, 20],[],[],'',6,'h','wild horse','wander',13,12,{'tame':['ride',60,902],'Str':15,'End':10,'Dex':10,'Int':5,'Cre':1,'Mnd':10,'loot':[[1326,100,4,6],[1310,100,2,6],['horse skin',100,4,7]]},8,80,'Nature','wild horse')
camel = Animal([30, 20],[],[],'wWt',6,'c','camel','wander',14,12,{'tame':['ride',60,902],'Str':15,'End':10,'Dex':10,'Int':5,'Cre':1,'Mnd':5,'loot':[[1326,100,4,6],[1310,100,1,5],['camel skin',100,4,7]]},8,120,'Nature','camel')
giant_lizard = Animal([30, 20],[],[],'',2,'l','giant lizard','wander',15,15,{'Str':15,'End':10,'Dex':10,'Int':5,'Cre':1,'Mnd':6,'loot':[[1326,100,2,5],[1310,100,1,4],['lizard skin',100,2,5]]},8,150,'Chaos','giant lizard')
penguin = Animal([30, 20],[],[],'',8,'p','penguin','wander',16,2,{'tame':['pet',80,1310],'Str':1,'End':1,'Dex':6,'Int':2,'Cre':1,'Mnd':4,'loot':[[1310,100,1,2]]},6,5,'Nature','penguin')
monkey = Animal([30, 20],[],[],'wWt',6,'m','monkey','wander',17,5,{'tame':['pet',50,1301],'Str':5,'End':10,'Dex':10,'Int':5,'Cre':1,'Mnd':10,'loot':[[1310,100,1,3],['monkey skin',100,2,4]]},6,10,'Nature','monkey')
carnivore_bush = Animal([30, 20],[],[],".,+><aABdDfFgiIJlLmnoOpsStTwW%#`'~:",10,'#','carnivore plant','standing_hostile',18,10,{'Str':17,'End':10,'Dex':5,'Int':5,'Cre':1,'Mnd':5,'loot':[]},6,100,'Nature','plant')
wild_chicken = Animal([30, 20],[],[],'wWt',7,'c','wild chicken','wander',19,1,{'tame':['farm',25,1315,1321],'Str':1,'End':1,'Dex':3,'Int':2,'Cre':1,'Mnd':2,'loot':[[1310,100,1,1],[1323,100,10,20]]},1,5,'Order','chicken')
wild_cattle = Animal([30, 20],[],[],'wWt',8,'c','wild cattle','wander',20,15,{'tame':['farm',35,902,1322],'Str':25,'End':10,'Dex':5,'Int':2,'Cre':1,'Mnd':4,'loot':[[1326,100,4,6],[1310,100,10,15],['buffalo skin',100,3,8]]},1,100,'Order','cattle')
fish = Animal([30, 20],[],[],".,+><aAbBdDfFgiIJlLmnoOpsST%#`'~:",1,'f','fish','wander',100,5,{'Str':1,'End':4,'Dex':5,'Int':2,'Cre':1,'Mnd':1,'loot':[[1310,100,1,1]]},5,20,'Nature','fish')

random_creatures = [1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,100] ## ID-ta na random gadinite za loadvaneto
random_by_force = {'Nature':{'cold':[5,4,11,12,16,20],'warm':[3,9,5,4,13,18,19,20],'hot':[9,14,17]},
                   'Order':{'cold':[12,16,20,6],'warm':[9,6,13,19,20],'hot':[14,9,10,6]},
                   'Chaos':{'cold':[12,7],'warm':[7,8,10,19,20],'hot':[15,10,9]}}
water_creatures = [100]
game_creatures = [wood,wood_perm,random_squirrel,bear,fish,wolf,dog,hyena,grizzly,snake,poison_snake,polar_bear,polar_wolf,
                  wild_horse,camel,giant_lizard,penguin,monkey,carnivore_bush,wild_chicken,wild_cattle]

##['Backpack','Head','Neck','Chest','Jewel','Back','Arms','Right hand','Left hand','On hands',
## 'Left ring','Right ring','Belt','Legs','Feet','Sheath','Belt tool 1','Belt tool 2','Quiver/stone pouch']

import inventory
def start_inv(i): ##Unstackable items da se davat edno po edno
    if i == 'a':
        inventory.shoulder_bag.start_item(1,"healer's satchel")
        ch.inventory[0].color=10
        ch.equip(ch.inventory[0],0)
        inventory.cloth_pants.start_item(1)
        ch.equip(ch.inventory[0],13)
        inventory.cloth_shirt.start_item(1,"healer's tunic")
        ch.inventory[0].color=10
        ch.equip(ch.inventory[0],3)
        inventory.cloth_shoes.start_item(1)
        ch.equip(ch.inventory[0],14)
        inventory.cloth_cloak.start_item(1,"healer's cloak")
        ch.inventory[0].color=10
        ch.equip(ch.inventory[0],5)
        inventory.tinderbox.start_item(1)
        inventory.nature_heal_set.start_item(1)
        inventory.bread.start_item(2)
        inventory.bottle_water.start_item(2)
    elif i == 'b':
        inventory.shoulder_bag.start_item(1)
        ch.equip(ch.inventory[0],0)
        inventory.cloth_shoes.start_item(1)
        ch.equip(ch.inventory[0],14)
        inventory.cloth_robe.start_item(1,"traveler's robe")
        ch.equip(ch.inventory[0],3)
        inventory.light_staff.start_item(1,"traveler's staff")
        ch.equip(ch.inventory[0],7)
        inventory.tinderbox.start_item(1)
        inventory.bread.start_item(2)
        inventory.bottle_water.start_item(2)
    elif i == 'c':
        inventory.small_backpack.start_item(1)
        ch.equip(ch.inventory[0],0)
        inventory.cloth_pants.start_item(1,'gray pants')
        ch.equip(ch.inventory[0],13)
        inventory.wood_vest.start_item(1)
        ch.equip(ch.inventory[0],3)
        inventory.wood_boots.start_item(1)
        ch.equip(ch.inventory[0],14)
        random.choice(inventory.light_weapons).start_item(1)
        ch.equip(ch.inventory[0],7)
        inventory.bow.start_item(1,'elven bow')
        ch.inventory[0].color=10
        inventory.wood_arrow.start_item(50)
        inventory.tinderbox.start_item(1)
        inventory.bread.start_item(2)
        inventory.bottle_water.start_item(2)
        inventory.gem_amethyst.start_item(5)
        inventory.gem_lapis_lazuli.start_item(1)
    elif i == 'd':
        inventory.small_backpack.start_item(1)
        ch.equip(ch.inventory[0],0)
        inventory.cloth_pants.start_item(1)
        ch.equip(ch.inventory[0],13)
        inventory.leather_gloves.start_item(1,"miner's gloves")
        ch.equip(ch.inventory[0],9)
        inventory.cloth_shirt.start_item(1,"miner's shirt")
        ch.equip(ch.inventory[0],3)
        inventory.pick.start_item(1)
        ch.equip(ch.inventory[0],7)
        inventory.hammer.start_item(1,"builder's hammer")
        inventory.saw.start_item(1)
        inventory.pliers.start_item(1)
        inventory.tinderbox.start_item(1)
        inventory.bread.start_item(2)
        inventory.dagger.start_item(1)
        inventory.bottle_water.start_item(2)
    elif i == 'e':
        inventory.small_backpack.start_item(1)
        ch.equip(ch.inventory[0],0)
        inventory.cloth_pants.start_item(1)
        ch.equip(ch.inventory[0],13)
        inventory.cloth_shirt.start_item(1)
        ch.equip(ch.inventory[0],3)
        inventory.leather_boots.start_item(1,"farmer's boots")
        ch.equip(ch.inventory[0],14)
        inventory.shovel.start_item(1)
        ch.equip(ch.inventory[0],16)
        inventory.vegetable_seed.start_item(10)
        inventory.tinderbox.start_item(1)
        inventory.bread.start_item(2)
        inventory.bottle_water.start_item(2)
    elif i == 'f':
        inventory.small_backpack.start_item(1)
        ch.equip(ch.inventory[0],0)
        inventory.cloth_pants.start_item(1,'embroidered pants')
        ch.equip(ch.inventory[0],13)
        inventory.cloth_shirt.start_item(1,"merchant's shirt")
        ch.equip(ch.inventory[0],3)
        inventory.cloth_belt.start_item(1,"embroidered belt")
        ch.equip(ch.inventory[0],12)
        inventory.cloth_shoes.start_item(1,'fine shoes')
        ch.equip(ch.inventory[0],14)
        inventory.cloth_cloak.start_item(1,"merchants's cloak")
        ch.equip(ch.inventory[0],5)
        inventory.jewel_ring.start_item(1,"silver ring")
        ch.equip(ch.inventory[0],10)
        inventory.coins_silver.start_item(10)
        inventory.common_spices.start_item(5,'sack of spices')
        inventory.tinderbox.start_item(1)
        inventory.bread.start_item(2)
        inventory.bottle_water.start_item(2)
    elif i == 'g':
        inventory.small_backpack.start_item(1)
        ch.equip(ch.inventory[0],0)
        inventory.long_sword.start_item(1)
        ch.equip(ch.inventory[0],7)
        inventory.leather_pants.start_item(1)
        ch.equip(ch.inventory[0],13)
        inventory.leather_vest.start_item(1,"soldier's tunic")
        ch.equip(ch.inventory[0],3)
        inventory.leather_boots.start_item(1)
        ch.equip(ch.inventory[0],14)
        inventory.tinderbox.start_item(1)
        inventory.bread.start_item(2)
        inventory.bottle_water.start_item(2)
    elif i == 'h':
        inventory.small_backpack.start_item(1)
        ch.equip(ch.inventory[0],0)
        inventory.giant_club.start_item(1)
        ch.equip(ch.inventory[0],7)
        inventory.cloth_pants.start_item(1,'dirty waist wrap')
        ch.inventory[0].color=7
        ch.equip(ch.inventory[0],13)
        inventory.cloth_shoes.start_item(1,'old sandals')
        ch.inventory[0].color=7
        ch.equip(ch.inventory[0],14)
        inventory.tinderbox.start_item(1)
        inventory.bread.start_item(2)
        inventory.bottle_water.start_item(2)
    elif i == 'i':
        inventory.small_backpack.start_item(1)
        ch.equip(ch.inventory[0],0)
        random.choice(inventory.medium_weapons).start_item(1)
        ch.equip(ch.inventory[0],7)
        inventory.chain_pants.start_item(1)
        ch.equip(ch.inventory[0],13)
        inventory.chain_vest.start_item(1)
        ch.equip(ch.inventory[0],3)
        inventory.leather_boots.start_item(1)
        ch.equip(ch.inventory[0],14)
        inventory.leather_cloak.start_item(1)
        ch.equip(ch.inventory[0],5)
        inventory.dagger.start_item(1)
        inventory.tinderbox.start_item(1)
        inventory.bread.start_item(2)
        inventory.bottle_water.start_item(2)
    elif i == 'j':
        inventory.small_backpack.start_item(1)
        ch.equip(ch.inventory[0],0)
        inventory.cloth_robe.start_item(1)
        ch.equip(ch.inventory[0],3)
        inventory.magic_book.start_item(1)
        inventory.herb_set.start_item(1)
        inventory.tinderbox.start_item(1)
        inventory.bread.start_item(2)
        inventory.bottle_water.start_item(2)
    message.message('')

def take_effect():
    ch.max_weight = ch.attr['Str']*10
    ch.max_weaps = ch.attr['Str']
    ch.max_energy = ch.attr['End']*100
    ch.max_life = ch.attr['End'] + ch.attr['End']/4
    ch.dmg = max([ch.attr['Str'] / 5, 1])
    if ch.weapon_weight < 6:
        ch.att_att = 'Dex'
        ch.def_att = 'Dex'
        ch.battle_att = ch.attr['Dex']
    elif ch.weapon_weight < 10:
    ## Ako orujieto e sredno maksimalnata stoinost na umenieto stava 100 pri balans na Dex i Str
        the_max=max([ch.attr['Dex'],ch.attr['Str']])
        the_min=min([ch.attr['Dex'],ch.attr['Str']])
        ch.battle_att = min([the_max+(the_min-the_max*2/3),20])
        ch.att_att = 'Str'
        ch.def_att = 'Dex'
    else:
        ch.battle_att = ch.attr['Str']
        ch.att_att = 'Str'
        ch.def_att = 'Str'

def take_force_effect():
    for f in ch.races:
        for r in ch.races[f]:
            if ch.races[f][r]<30:
                if ch.research_races[f][r]<30:
                    for n in ['1','2','3']:
                        try:
                            ch.tool_tags.remove(r+n)
                            if r+n=='troll1':
                                ch.tool_tags.remove('big hammer')
                            if r+n=='imp1':
                                ch.tool_tags.remove('fire')
                        except ValueError:
                            pass
            elif ch.races[f][r]<60:
                if ch.research_races[f][r]<60:
                    for n in ['2','3']:
                        try:
                            ch.tool_tags.remove(r+n)
                        except ValueError:
                            pass
                if r+'1' not in ch.tool_tags:
                    ch.tool_tags.append(r+'1')
                    if r+'1'=='troll1':
                        ch.tool_tags.append('big hammer')
                    if r+'1'=='imp1':
                        ch.tool_tags.append('fire')
            elif ch.races[f][r]<90:
                for n in ['1','2']:
                    if r+n not in ch.tool_tags:
                        ch.tool_tags.append(r+n)
                        if r+n=='troll1':
                            ch.tool_tags.append('big hammer')
                        if r+n=='imp1':
                            ch.tool_tags.append('fire')
                if ch.research_races[f][r]<90:
                    try:
                        ch.tool_tags.remove(r+'3')
                        if r=='human':
                            for f in ch.research_forces:
                                ch.research_forces[f]=0.
                                for r in ch.research_races[f]:
                                    ch.research_races[f][r]=0.
                            take_research_effect()
                            ch.research_force='Order'
                            ch.research_race='human'
                    except ValueError:
                        pass
            elif ch.races[f][r]>=90:
                for n in ['1','2','3']:
                    if r+n not in ch.tool_tags:
                        ch.tool_tags.append(r+n)
                        if r+n=='troll1':
                            ch.tool_tags.append('big hammer')
                        if r+n=='imp1':
                            ch.tool_tags.append('fire')

def take_research_effect():
    for f in ch.research_races:
        for r in ch.research_races[f]:
            if r!='human':
                if ch.research_races[f][r]<30:
                    if ch.races[f][r]<30:
                        for n in ['1','2','3']:
                            try:
                                ch.tool_tags.remove(r+n)
                                if r+n=='troll1':
                                    ch.tool_tags.remove('big hammer')
                                if r+n=='imp1':
                                    ch.tool_tags.remove('fire')
                            except ValueError:
                                pass
                elif ch.research_races[f][r]<60:
                    if ch.races[f][r]<60:
                        for n in ['2','3']:
                            try:
                                ch.tool_tags.remove(r+n)
                            except ValueError:
                                pass
                    if r+'1' not in ch.tool_tags:
                        ch.tool_tags.append(r+'1')
                        if r+'1'=='troll1':
                            ch.tool_tags.append('big hammer')
                        if r+'1'=='imp1':
                            ch.tool_tags.append('fire')
                elif ch.research_races[f][r]<90:
                    for n in ['1','2']:
                        if r+n not in ch.tool_tags:
                            ch.tool_tags.append(r+n)
                            if r+n=='troll1':
                                ch.tool_tags.append('big hammer')
                            if r+n=='imp1':
                                ch.tool_tags.append('fire')
                    if ch.races[f][r]<90:
                        try:
                            ch.tool_tags.remove(r+'3')
                        except ValueError:
                            pass
                elif ch.research_races[f][r]>=90:
                    for n in ['1','2','3']:
                        if r+n not in ch.tool_tags:
                            ch.tool_tags.append(r+n)
                            if r+n=='troll1':
                                ch.tool_tags.append('big hammer')
                            if r+n=='imp1':
                                ch.tool_tags.append('fire')
    
def effect(k,v,xy=[],ot=''):
    if k == 'attr':
        mod = ch.attr[v[0]]-ch.max_attr[v[0]]
        ch.max_attr[v[0]] += v[1]
        ch.attr[v[0]] = ch.max_attr[v[0]] + mod
        take_effect()
    elif k == 'temp_attr':
        ch.attr[v[0]] += v[1]
        take_effect()
    elif k == 'temp_attr_reverse':
        ch.attr[v[0]] -= v[1]
        take_effect()
    elif k == 'energy':
        ch.energy += v
        if ch.life < ch.max_life:
            while ch.energy >= ch.max_energy and ch.life < ch.max_life:
                ch.life += 1
                ch.energy -= 100
        if ch.energy > ch.max_energy:
            ch.energy = ch.max_energy
    elif k == 'research':
        for x in v:
            if 'force' in v[x].keys():
                ## Izpolzva se za uvelichavane!
                ch.research_forces[x]=min([max([ch.research_forces[x]+v[x]['force'],0]),100])
                all_x=sum([ch.research_forces[f] for f in ch.research_forces])
                if all_x>100:
                    rorder=ch.research_forces.keys()
                    rorder.remove(ch.research_force)
                    random.shuffle(rorder)
                    rest=all_x-100
                    i=0
                    rall_x=sum([ch.research_forces[f] for f in rorder])
                    while rest>0 and rall_x>0:
                        if ch.research_forces[rorder[i%len(rorder)]]>0:
                            ch.research_forces[rorder[i%len(rorder)]]=max([ch.research_forces[rorder[i%len(rorder)]]-0.01,0])
                            every=0
                            for every in ch.research_races[rorder[i%len(rorder)]].keys():
                                if ch.research_races[rorder[i%len(rorder)]][every]==0:
                                    break
                            if not every:
                                ch.research_races[rorder[i%len(rorder)]].keys()[0]
                            effect('research',{rorder[i%len(rorder)]:{every:0}})
                            rest-=0.01
                        i+=1
                        rall_x=sum([ch.research_forces[f] for f in rorder])
                    if rest:
                        ch.research_forces[x]=min([max([ch.research_forces[x]-rest,0]),100])
                take_research_effect()
            ## Za uvelichavane i namalqvane na rasi.
            else:
                for y in v[x]:
                    ch.research_races[x][y]=min([max([ch.research_races[x][y]+v[x][y],0]),100])
                    all_x=sum([ch.research_races[x][f] for f in ch.research_races[x]])
                    if all_x>ch.research_forces[x]:
                        rorder=ch.research_races[x].keys()
                        rorder.remove(y)
                        if ch.research_race in rorder:
                            rorder.remove(ch.research_race)
                        random.shuffle(rorder)
                        rest=all_x-ch.research_forces[x]
                        i=0
                        rall_x=sum([ch.research_races[x][f] for f in rorder])
                        while rest>0 and rall_x>0:
                            if ch.research_races[x][rorder[i%len(rorder)]]>0:
                                ch.research_races[x][rorder[i%len(rorder)]]=max([ch.research_races[x][rorder[i%len(rorder)]]-0.01,0])
                                rest-=0.01
                            i+=1
                            rall_x=sum([ch.research_races[x][f] for f in rorder])
                        if rest>0:
                            ch.research_races[x][y]=min([max([ch.research_races[x][y]-rest,0]),100])
                    take_research_effect()
    elif k == 'force':
        ##{'Nature':{'force':0.01,'spirit of nature':0.01},'Chaos':{'all':-.01}}
        for x in v:
            if 'all' in v[x].keys():
                ## Izpolzva se za namalqvane, ne za uvelichavane!
                ch.forces[x]=min([max([ch.forces[x]+v[x]['all'],0]),100])
                for r in ch.races[x]:
                    ch.races[x][r]=min([max([ch.races[x][r]+v[x]['all'],0]),100])
                take_force_effect()
            if 'force' in v[x].keys():
                ## Izpolzva se za uvelichavane!
                ch.forces[x]=min([max([ch.forces[x]+v[x]['force'],0]),100])
            for y in v[x]:
                if y in ['all','force']:
                    pass
                elif y=='expend':
                    for each in ch.inventory:
                        if v[x][y] in each.tool_tag:
                            each.use_item('expend')
                            break
                ## Prirodniq ritual e nai-truden (25% pri 100 i 100), no nqma shans za izbuhvane i vsichki rasi go mogat
                elif y=='calm_lava':
                    chance=max(ch.races['Nature'].values())+ch.forces['Nature']-v[x][y]
                    check=random.randint(0,100)
                    if check<chance:
                        msvcrt.getch()
                        init_screen.combat_buffer+=' The lava recedes down in the earth. With a last flicker a spark flies up and   lands near your feet. You have received a Seed of Life!'
                        init_screen.land[xy[1]-1] = init_screen.land[xy[1]-1][:xy[0]-21]+'.'+init_screen.land[xy[1]-1][xy[0]-20:]
                        inventory.put_item([[1307,100,1,1]], xy)
                ## Rituala na reda e po-lesen (50% pri 100 i 100), no ako se provali izbuhva
                elif y=='suppress_lava':
                    chance=max(ch.races['Order'].values())+ch.forces['Order']-v[x][y]
                    check=random.randint(0,100)
                    if check<chance:
                        msvcrt.getch()
                        init_screen.combat_buffer+=' The lava bubles and dances, and then slowly turns darker - you managed to tame the power of the fire! With a last "BLOP!" the nearly black surface breaks and  in the last flickers you see something shiny. Maybe you can pry it out?'
                        init_screen.land[xy[1]-1] = init_screen.land[xy[1]-1][:xy[0]-21]+'A'+init_screen.land[xy[1]-1][xy[0]-20:]
                    else:
                        msvcrt.getch()
                        init_screen.combat_buffer+=' The lava errupts violently!'
                        for x1 in range(max([1,xy[1]-6]),min([24,xy[1]+6])):
                            for y1 in range(max([21,xy[0]-6]),min([79,xy[0]+6])):
                                if random.choice([0,1,2]):
                                    effect('force',{'Chaos':{'lava_fire':15}},[y1,x1])
                ## Rituala na haosa e nai-lesen (75% pri 100 i 100), no vinagi ima izbuhvane
                elif y=='awaken_lava':
                    chance=max(ch.races['Chaos'].values())+ch.forces['Chaos']-v[x][y]
                    check=random.randint(0,100)
                    if check<chance:
                        msvcrt.getch()
                        init_screen.combat_buffer+=' The lava bursts out of the earth and sprays the space around you! On the bottom of the smoking hole lies a small piece of black rock, emanating dread and      coldness.'
                        init_screen.land[xy[1]-1] = init_screen.land[xy[1]-1][:xy[0]-21]+'.'+init_screen.land[xy[1]-1][xy[0]-20:]
                        inventory.put_item([[1309,100,1,1]], xy)
                        for x1 in range(max([1,xy[1]-14]),min([24,xy[1]+14])):
                            for y1 in range(max([21,xy[0]-14]),min([79,xy[0]+14])):
                                if random.choice([0,1,2,3]):
                                    effect('force',{'Chaos':{'lava_fire':15}},[y1,x1])
                    else:
                        msvcrt.getch()
                        init_screen.combat_buffer+=' The lava errupts violently!'
                        for x1 in range(max([1,xy[1]-14]),min([24,xy[1]+14])):
                            for y1 in range(max([21,xy[0]-14]),min([79,xy[0]+14])):
                                if random.choice([0,1,2,3]):
                                    effect('force',{'Chaos':{'lava_fire':15}},[y1,x1])
                elif y=='fire_up':
                    spot_id=ot
                    spot_color=T[init_screen.land[xy[1]-1][xy[0]-21]].colour
                    ch.land_effects[ch.turn]=[v[x][y],'on_fire',init_screen.current_area,xy[:],spot_id,spot_color,2]
                elif y=='lava_fire':
                    spot_id=T[init_screen.land[xy[1]-1][xy[0]-21]].char
                    spot_color=T[init_screen.land[xy[1]-1][xy[0]-21]].colour
                    if init_screen.land[xy[1]-1][xy[0]-21] in ['T','g',':','J']:
                        init_screen.land[xy[1]-1] = init_screen.land[xy[1]-1][:xy[0]-21]+'.'+init_screen.land[xy[1]-1][xy[0]-20:]
                    if ch.land_effects.keys():
                        if max(ch.land_effects.keys())<ch.turn:
                            ch.land_effects[ch.turn]=[v[x][y]+random.randint(0,6),'on_fire',init_screen.current_area,xy[:],spot_id,spot_color,6]
                        else:
                            ch.land_effects[max(ch.land_effects.keys())+1]=[v[x][y]+random.randint(0,6),'on_fire',init_screen.current_area,xy[:],spot_id,spot_color,6]
                    else:
                        ch.land_effects[ch.turn]=[v[x][y]+random.randint(0,6),'on_fire',init_screen.current_area,xy[:],spot_id,spot_color,6]
                ## Izpolzva se za uvelichavane!
                elif y=='terrain':
                    if random.random()<v[x][y]:
                        if init_screen.current_place[x]<100:
                            init_screen.current_place[x]+=1
                        restf=['Nature','Chaos','Order']
                        restf.remove(x)
                        random.shuffle(restf)
                        if init_screen.current_place[restf[0]]>0:
                            init_screen.current_place[restf[0]]-=1
                        elif init_screen.current_place[restf[1]]>0:
                            init_screen.current_place[restf[1]]-=1
                        predominant_f={init_screen.current_place['Nature']:'Nature',init_screen.current_place['Order']:'Order',
                                       init_screen.current_place['Chaos']:'Chaos'}
                        init_screen.place_descriptions[init_screen.current_area] = 'A place of %s.' %(predominant_f[max(predominant_f.keys())])
                ## Izpolzva se za uvelichavane!
                elif y=='population':
                    init_screen.current_place['Population']=max([0,min([100,init_screen.current_place['Population']+v[x][y]])])
                ## Za uvelichavane i namalqvane na rasi.
                else:
                    ch.races[x][y]=min([max([ch.races[x][y]+v[x][y],0]),100])
                    all_x=sum([ch.races[x][f] for f in ch.races[x]])
                    if all_x>ch.forces[x]:
                        rorder=ch.races[x].keys()
                        rorder.remove(y)
                        if ch.locked_race in rorder:
                            rorder.remove(ch.locked_race)
                        random.shuffle(rorder)
                        rest=all_x-ch.forces[x]
                        i=0
                        rall_x=sum([ch.races[x][f] for f in rorder])
                        while rest>0 and rall_x>0:
                            if ch.races[x][rorder[i%len(rorder)]]>0:
                                ch.races[x][rorder[i%len(rorder)]]=max([ch.races[x][rorder[i%len(rorder)]]-0.01,0])
                                rest-=0.01
                            i+=1
                            rall_x=sum([ch.races[x][f] for f in rorder])
                        if rest:
                            ch.races[x][y]=min([max([ch.races[x][y]-rest,0]),100])
                    take_force_effect()
    elif k=='mass destruction':
        ch.land_effects[ch.turn]=[1,'mass destruction',init_screen.current_area]
    elif k=='dryad song':
        ch.land_effects[ch.turn]=[1,'dryad song',init_screen.current_area,ch.energy/100+1]
    elif k == 'thirst':
        ch.thirst -= v
        if ch.thirst < 0:
            ch.thirst = 0
    elif k == 'hunger':
        ch.hunger -= v
        if ch.hunger < 0:
            ch.hunger = 0
    elif k == 'container':
        init_screen.I[v].create_item()
    elif k == 'fill':
        try:
            init_screen.I[v[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]]].create_item()
        except KeyError:
            message.message('no_fill')
            i = msvcrt.getch()
            return 0
    elif k == 'gather':
        try:
            ## Izbira sluchaina bilka ot spisuka za suotvetniq teren i opredelq dali e namerena.
            choice = random.choice(v[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]])
            found = random.randint(1,100)
            if found <= choice.effect['chance']*ch.attr['Int']:
                choice.create_item()
            else:
                message.message('failed_gather')
                i = msvcrt.getch()
        except KeyError:
            message.message('no_gather')
            i = msvcrt.getch()
            return 0
    elif k=='transform':
        init_screen.possess(v,'trans')
    elif k=='plant_seed':
        if init_screen.land[ch.xy[1]-1][ch.xy[0]-21] in ['.','a','g']:
            message.message('plant_seed')
            ch.land_effects[ch.turn]=[int(1200*(1-.5*(init_screen.current_place['Nature']/100.))),'plant',init_screen.current_area,random.choice(v),ch.xy[:]]
        else:
            message.message('need_dirt')
            return 0
    elif k=='plant_vegetable':
        if init_screen.land[ch.xy[1]-1][ch.xy[0]-21]== 'a':
            message.message('plant_seed')
            ch.land_effects[ch.turn]=[int(1200*(1-.5*(init_screen.current_place['Nature']/100.))),'plant',init_screen.current_area,random.choice(v),ch.xy[:]]
        else:
            message.message('need_farm')
            return 0
    ## Za veche opredeleni semena na zelenchuci
    elif k=='plant_specific':
        if init_screen.land[ch.xy[1]-1][ch.xy[0]-21]== 'a':
            message.message('plant_seed')
            ch.land_effects[ch.turn]=[int(1200*(1-.5*(init_screen.current_place['Nature']/100.))),'plant',init_screen.current_area,random.choice(v[0]),ch.xy[:],v[1]]
        else:
            message.message('need_farm')
            return 0
    elif k=='break_rock':
        if 'hammer' in ch.tool_tags:
            effect('force',{'Order':{'force':0.01,'dwarf':0.01},'Nature':{'all':-.01}})
            if random.random()<0.05 or ('dwarf3' in ch.tool_tags and random.random()<0.15):
                the_turn=ch.turn+1
                while the_turn in ch.land_effects:
                    the_turn+=1
                ch.land_effects[the_turn]=[1,'plant',init_screen.current_area,random.choice(v),ch.xy[:]]
                message.message('found_gem')
            else:
                message.message('break_rock')
            msvcrt.getch()
        else:
            message.tool_msg('no_tool',['hammer'])
            msvcrt.getch()
            return 0
    elif k=='smelt_ore':
        if 'hammer' in ch.tool_tags:
            smelted=0
            for i in init_screen.ground_items:
                if i[:2]==ch.xy and i[2].id==505:
                    effect('force',{'Order':{'force':0.01,'dwarf':0.01},'Nature':{'all':-.01},'Chaos':{'all':-.01}})
                    if random.random()<(0.05*ch.attr['Cre']):
                        the_turn=ch.turn+1
                        while the_turn in ch.land_effects:
                            the_turn+=1
                        if random.random()<0.08 or ('dwarf3' in ch.tool_tags and random.random()<0.25):
                            ch.land_effects[the_turn]=[50,'plant',init_screen.current_area,v[1],ch.xy[:],
                                                      random.choice(['copper ingot','gold ingot','silver ingot'])]
                        else:
                            ch.land_effects[the_turn]=[50,'plant',init_screen.current_area,v[0],ch.xy[:]]
                        message.message('found_metal')
                        msvcrt.getch()
                    else:
                        message.message('failed_smelt')
                        msvcrt.getch()
                        return 0
                    smelted=1
                    break
            if not smelted:
                message.tool_msg('no_tool',['forge'])
                msvcrt.getch()
                return 0
        else:
            message.tool_msg('no_tool',['hammer'])
            msvcrt.getch()
            return 0
    elif k=='gnome_gem':
        if T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id in v[0] and 'gnome2' in ch.tool_tags:
            if 'ruby' not in v[1] and 'sapphire' not in v[1] and 'amethyst' not in v[1]:
                message.message(v[1])
            if 'topaz' in v[1]:
                effect('energy',ch.max_energy-ch.energy)
            elif 'emerald' in v[1]:
                effect('energy',ch.max_energy-ch.energy+100*(ch.max_life-ch.life))
            elif 'diamond' in v[1]:
                init_screen.current_place['Treasure']+=1
                init_screen.treasure_modifier -=1
            elif 'garnet' in v[1]:
                for x in all_creatures:
                    if x.mode != 'not_appeared' and x.t=='animal':
                        x.mode='fearfull'
            elif 'opal' in v[1]:
                mossy_coords=[]
                for y in range(len(init_screen.land)):
                    for x in range(len(init_screen.land[y])):
                        if init_screen.land[y][x]=='n' and [x+21,y+1] != ch.xy:
                            mossy_coords.append([x+21,y+1])
                ch.xy=random.choice(mossy_coords)
            elif 'turquoise' in v[1]:
                init_screen.land[ch.xy[1]-1] = init_screen.land[ch.xy[1]-1][:ch.xy[0]-21]+'W'+init_screen.land[ch.xy[1]-1][ch.xy[0]-20:]
                effect('force',{'Nature':{'terrain':1}})
            elif 'tourmaline' in v[1]:
                init_screen.land[ch.xy[1]-1] = init_screen.land[ch.xy[1]-1][:ch.xy[0]-21]+'n'+init_screen.land[ch.xy[1]-1][ch.xy[0]-20:]
                effect('force',{'Nature':{'terrain':1}})
            elif 'aquamarine' in v[1]:
                init_screen.land[ch.xy[1]-1] = init_screen.land[ch.xy[1]-1][:ch.xy[0]-21]+'w'+init_screen.land[ch.xy[1]-1][ch.xy[0]-20:]
                effect('force',{'Nature':{'terrain':1}})
            elif 'sapphire' in v[1]:
                for x in all_creatures:
                    if x.mode=='hostile':
                        if init_screen.clear_los(init_screen.direct_path(ch.xy,x.xy)):
                            x.life-=max([(ch.races['Nature']['gnome']-60)/4,1])
                            message.creature('sapphired',x)
            elif 'ruby' in v[1]:
                found_fire=0
                for x in ch.land_effects.keys():
                    if ch.land_effects[x][2]==init_screen.current_area and ch.land_effects[x][1]=='on_fire' \
                       and ch.land_effects[x][3]==ch.xy:
                        message.message(v[1])
                        found_fire=1
                        for x in all_creatures:
                            if x.mode=='hostile':
                                if init_screen.clear_los(init_screen.direct_path(ch.xy,x.xy)):
                                    x.life-=max([(ch.races['Nature']['gnome']-60)/2,1])
                                    message.creature('rubied',x)
                        break
                if not found_fire:
                    message.message('cant_use_gem')
                    return 0
            elif 'amethyst' in v[1]:
                if ch.marked_stone and init_screen.current_area==ch.marked_stone[0] and ch.xy==ch.marked_stone[1]:
                    ch.marked_stone=[]
                    message.message('amethyst0')
                else:
                    ch.marked_stone=[init_screen.current_area,ch.xy[:]]
                    message.message('amethyst1')
            elif 'lapis' in v[1]:
                init_screen.change_place('areaB','gnome')
            effect('force',{'Nature':{'force':0.03,'gnome':0.03},'Chaos':{'all':-.03},'Order':{'all':-.03}})
        else:
            message.message('cant_use_gem')
            return 0
    else:
        return 0

def game_time(i = '0'):
    hostile_in_sight=1
    if i in ['0','1','2','3','4','5','6','7','8','9']:
        if ch.work > 0:
            ch.work -= 10
            ch.energy -= 11
            if ch.work < 0:
                ch.work = 0
        else:
            ch.move(i)
            if 'human3' in ch.tool_tags and ch.research_race!='human':
                if init_screen.current_place[ch.research_force]==max([init_screen.current_place['Chaos'],init_screen.current_place['Order'],init_screen.current_place['Nature'],]) and init_screen.current_place[ch.research_force]>=ch.research_forces[ch.research_force]:
                    effect('research',{ch.research_force:{'force':0.01}})
            if ch.possessed and ch.possessed[0].mode=='temp':
                effect('force',{'Nature':{'terrain':0.1}})
        for x in all_creatures:
            if x.mode != 'not_appeared':
                if x.life < 1:
                    init_screen.c.scroll((x.xy[0], x.xy[1], x.xy[0]+1, x.xy[1]+1), 1, 1,
                                         T[init_screen.land[x.xy[1]-1][x.xy[0]-21]].colour,
                                         T[init_screen.land[x.xy[1]-1][x.xy[0]-21]].char)
                    all_creatures.remove(x)
                    all_beings.remove(x)
        for x in all_creatures:
            if not (x in ch.followers and x.xy==ch.xy) or (x in ch.possessed and x.xy==[1,1]):
                init_screen.hide(x)
            if x.mode != 'not_appeared':
                if x in ch.ride or x in ch.possessed or (x in ch.followers and x.xy==ch.xy):
                    continue
                x.creature_move()
            if init_screen.clear_los(init_screen.direct_path(ch.xy,x.xy)):
                if x.mode=='hostile':
                    hostile_in_sight=2
                if 'human3' in ch.tool_tags and ch.research_race!='human':
                    if x.race==ch.research_race and i!=0 and i!=5 and x.learning>0:
                        effect('research',{ch.research_force:{ch.research_race:0.01}})
                        x.learning-=0.01
            elif x.t=='sentient' and 'midnight fears' in ch.effects and x.mode=='hostile':
                x.fear+=int(ch.races['Nature']['fairy']/10)-abs(600-max([0,ch.turn%2400-1200])%1200)/100
        init_screen.draw_items()
        ch.turn += 1 * ch.place_time
        for cr in all_creatures:
            if (cr.energy < cr.max_energy):
                cr.energy += 1
            if (cr.energy > cr.max_energy):
                cr.energy = cr.max_energy
        if ch.place_time > 1:
            ch.hunger += ch.place_time/20
            ch.thirst += ch.place_time/20
        elif (ch.turn % 20) == 0:
            ch.hunger += 1
            ch.thirst += 1
            for fol in ch.followers+ch.ride:
                if fol.attr['tame'][0]=='farm':
                    if not fol.food%5 and fol.food>random.randint(64,100):
                        fol.farm+=1
                fol.food=max([fol.food-1,0])
                if fol.food<random.randint(0,25):
                    fol.mode='wander'
        if (ch.hunger > 100):
            ch.life -= 1
            ch.hunger = 100
        if (ch.thirst > 100):
            ch.life -= 2
            ch.thirst = 100
        if (ch.energy < ch.max_energy) and not (ch.hunger>79 or ch.thirst>79):
            ch.energy += ch.rest * ch.place_time
        if (ch.energy > ch.max_energy):
            ch.energy = ch.max_energy
        if (ch.life < ch.max_life) and ch.life!=0:
            if ch.energy == ch.max_energy:
                ch.life += 1
                ch.energy -= 100
        if (ch.life > ch.max_life):
            ch.life = ch.max_life
        if (ch.energy > (ch.max_energy * 0.2)):
            ch.emotion = 7
        else:
            ch.emotion = 2
        if not ch.possessed:
            for attr in ch.attr:
                new_sum = 0
                for each_force in ch.races:
                    for each_race in ch.races[each_force]:
                        new_sum += ch.races[each_force][each_race]*race_attrs[each_race][attr]/100.
                if int(new_sum) != ch.max_attr[attr]:
                        effect('attr',[attr, int(min([20,new_sum])) - ch.max_attr[attr]])
                if ch.attr[attr] > ch.max_attr[attr]:
                    ch.attr_colors[attr] = 10
                elif ch.attr[attr] < ch.max_attr[attr]:
                    ch.attr_colors[attr] = 12
                else:
                    ch.attr_colors[attr] = 7
        init_screen.draw_hud()
        if 'water elemental1' in ch.tool_tags and T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id in 'wWt':
            if 'waterform' not in ch.effects:
                ch.effects['invisible']=2
                if 'water elemental2' in ch.tool_tags:
                    if T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id in 'wW':
                        ch.hunger=max([0,ch.hunger-1])
                        ch.thirst=max([0,ch.thirst-1])
                        message.message('good_water')
                    elif T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id=='t':
                        ch.hunger=min([100,ch.hunger+10])
                        ch.thirst=min([100,ch.thirst+10])
                        message.message('bad_water')
            elif T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id=='W' and 'waterform' in ch.effects:
                ch.life=1
                ch.hunger=90
                ch.thirst=90
                del(ch.effects['waterform'])
                del(ch.effects['invisible'])
                message.message('reform_waterform')
                msvcrt.getch()
        if (init_screen.current_place['Nature']>=33 and init_screen.current_place['Temperature']>=33 and 'elf2' in ch.tool_tags) \
           or ('goblin1' in ch.tool_tags and ch.turn%2400>1200):
            if 'stealthy' not in ch.tool_tags:
                ch.tool_tags.append('stealthy')
        else:
            if 'stealthy' in ch.tool_tags:
                ch.tool_tags.remove('stealthy')
        if 'stealthy' in ch.tool_tags:
            ch.emotion=8
        for x in ch.effects.keys():
            if not (ch.equipment['Right ring'] and ch.equipment['Right ring'].name=='ring of winter' and (init_screen.current_place['Temperature']<33 or 'summerwalk' in ch.effects) and x=='winterwalk')\
               and not (ch.equipment['Left ring'] and ch.equipment['Left ring'].name=='ring of summer' and (init_screen.current_place['Temperature']>=66 or 'winterwalk' in ch.effects) and x=='summerwalk')\
               and not (x in ['fairyland','summerwalk','winterwalk','midnight fears','sun armour','invisible'] and 'fairyland' in ch.effects):
                ch.effects[x] -= 1
            if ch.effects[x]==0:
                if x=='waterform':
                    msvcrt.getch()
                    over = init_screen.game_over()
                    return over
                del(ch.effects[x])
                if x=='sun armour' and ch.sun_armour:
                    ch.armour-=ch.sun_armour
                    ch.sun_armour=0
            if 'invisible' in ch.effects:
                ch.emotion = 1
            if 'midnight fears' in ch.effects:
                ch.emotion+= 208
            if 'sun armour' in ch.effects:
                ch.emotion+= 224
                ch.armour=ch.armour-ch.sun_armour
                if ch.turn%2400>=1200:
                    ch.sun_armour=0
                else:
                    clothes_penalty={'Chest':10,'Back':8,'Arms':5,'On hands':5,'Belt':2,'Legs':7,'Feet':3}
                    penalty=0
                    for cl in clothes_penalty:
                        if ch.equipment[cl] and ch.equipment[cl].name!='dress of the fae':
                            penalty+=clothes_penalty[cl]
                    steps=[200,400,550,650,800,1000,1200]
                    adds=[60,120,180,240,180,120,60]
                    daytime=ch.turn%2400
                    for s in range(len(steps)):
                        if daytime<steps[s]:
                            ch.sun_armour=max([0,adds[s]-penalty*adds[s]/60])
                            ch.armour+=ch.sun_armour
                            break
        for x in ch.land_effects.keys():
            if ch.land_effects[x][0] > 0:
                ch.land_effects[x][0] -= 1
            if ch.land_effects[x][2]==init_screen.current_area:
                if ch.land_effects[x][1]=='mass destruction':
                    init_screen.combat_buffer+=' You unleash the power of the chaos rock! The world crumbles around you!'
                    message.combat_buffer()
                    msvcrt.getch()
                    for i1 in range(8):
                        effect('force',{'Chaos':{'terrain':1}})
                        for i2 in range(100):
                            place=[random.randint(22,78),random.randint(2,23)]
                            dest=T[init_screen.land[place[1]-1][place[0]-21]].degrade_to['Chaos']
                            if dest in ['`','+','s','S']:
                                dest='.'
                            init_screen.land[place[1]-1] = init_screen.land[place[1]-1][:place[0]-21]+dest+init_screen.land[place[1]-1][place[0]-20:]
                            init_screen.c.scroll((place[0],place[1],place[0]+1,place[1]+1), 1, 1, T[init_screen.land[place[1]-1][place[0]-21]].colour, T[init_screen.land[place[1]-1][place[0]-21]].char)
                        msvcrt.getch()
                if ch.land_effects[x][1]=='dryad song':
                    effect('force',{'Nature':{'dryad':.01,'terrain':.4,'force':.01},'Chaos':{'all':-0.02},'Order':{'all':-0.01}})
                    init_screen.combat_buffer+=' Leaves rustle, wood creaks, in your steps the grass grows higher!'
                    for i1 in range(30):
                        place=[random.randint(22,78),random.randint(2,23)]
                        growing={'.':'g','B':'g','g':'b','a':'g','T':'J','F':'T','b':'T','%':'n','m':'n','#':'n','o':'b',
                                 'p':'g',',':'g','~':'b','+':'T','`':'T',}
                        dest=T[init_screen.land[place[1]-1][place[0]-21]].id
                        if dest in growing:
                            dest=growing[dest]
                        init_screen.land[place[1]-1] = init_screen.land[place[1]-1][:place[0]-21]+dest+init_screen.land[place[1]-1][place[0]-20:]
                        init_screen.c.scroll((place[0],place[1],place[0]+1,place[1]+1), 1, 1, T[init_screen.land[place[1]-1][place[0]-21]].colour, T[init_screen.land[place[1]-1][place[0]-21]].char)
                        if ch.land_effects[x][3]>1:
                            ch.land_effects[ch.turn]=[1,'dryad song',init_screen.current_area,ch.land_effects[x][3]-2]
                if ch.land_effects[x][1]=='plant':
                    if ch.land_effects[x][0]==0:
##                        inventory.put_item([[ch.land_effects[x][3].id,100,1,1]],ch.land_effects[x][4])
                        if len(ch.land_effects[x])==5:
                            inventory.put_item([[ch.land_effects[x][3].id,100,1,1]],ch.land_effects[x][4])
                        ## Za opredeleni zelenchuci
                        elif len(ch.land_effects[x])==6:
                            new_veg=ch.land_effects[x][3].duplicate(1,ch.land_effects[x][5])
                            init_screen.ground_items.append([ch.land_effects[x][4][0],ch.land_effects[x][4][1],new_veg])
                if ch.land_effects[x][1]=='on_fire':
                    fxy=ch.land_effects[x][3]
                    if ch.land_effects[x][0]==0:
                        init_screen.c.scroll((fxy[0],fxy[1],fxy[0]+1,fxy[1]+1), 1, 1, T[init_screen.land[fxy[1]-1][fxy[0]-21]].colour, T[init_screen.land[fxy[1]-1][fxy[0]-21]].char)
                    else:
                        for cr in all_creatures:
                            if cr.mode != 'not_appeared':
                                if cr.xy==fxy:
                                    cr.life-=ch.land_effects[x][6]
                                if cr.life < 1:
                                    init_screen.c.scroll((cr.xy[0], cr.xy[1], cr.xy[0]+1, cr.xy[1]+1), 1, 1,
                                                         T[init_screen.land[cr.xy[1]-1][cr.xy[0]-21]].colour,
                                                         T[init_screen.land[cr.xy[1]-1][cr.xy[0]-21]].char)
                                    all_creatures.remove(cr)
                                    all_beings.remove(cr)
                                    init_screen.combat_buffer+=' The %s dies in the flames!' %(cr.name)
                        fire_color=random.choice([4,12,14])
                        init_screen.c.scroll((fxy[0],fxy[1],fxy[0]+1,fxy[1]+1), 1, 1, fire_color*16+ch.land_effects[x][5],ch.land_effects[x][4])
                        if ch.xy==fxy:
                            ch.life-=ch.land_effects[x][6]
                            init_screen.combat_buffer+=' You get burnt by the fire!'
            if ch.land_effects[x][0]==0:
                del(ch.land_effects[x])

        message.combat_buffer()

        if ch.life <= 0:
            if 'water elemental3' in ch.tool_tags and 'waterform' not in ch.effects:
                ch.effects['waterform']=100+int(100*(ch.races['Nature']['water elemental']-90))
                ch.effects['invisible']=100+int(100*(ch.races['Nature']['water elemental']-90))
                message.emotion('gain_waterform',ch.effects['waterform'])
            elif 'waterform' in ch.effects:
                message.emotion('gain_waterform',ch.effects['waterform'])
            else:
                msvcrt.getch()
                over = init_screen.game_over()
                return over
    else:
        message.message('?')
    ##Can't be 0 - ends the game
    return hostile_in_sight
