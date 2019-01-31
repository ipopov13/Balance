import msvcrt
import random
from terrain import T
from inventory import stone
from inventory import wood_arrow
from inventory import wood_bolt

class Living_thing(object):
    def __init__(self):
        self.race_attrs={
            'elf':              {'Str':15,'End':16,'Dex':20,'Int':17,'Cre':5, 'Mnd':15},
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

class Player(Living_thing):
    def __init__(self, xy, race,force,start_force):
        super(Player,self).__init__()
        self.xy = xy
        self.base_attr = self.race_attrs[race]
        self.attr = {}
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
        if (key == '0'):
            return 1
        if 'troll2' in self.tool_tags and self.turn%2 and self.turn%2400<1200:
            self.game.message.message('day_troll')
            return 1
        if (key == '5'):
            self.game.message.message('')
            self.game.message.message('wait')
            if (self.energy < self.max_energy) and not (self.hunger>79 or self.thirst>79):
                self.energy += 1
        elif self.possessed and 'spirit of nature3' in self.tool_tags:
            self.game.possession_score(33,self)
        for a in range(2):
            self.xy[a] = self.xy[a] + md[key][a]
        self.check_passage(self.xy, x, y)
        self.game.draw_move(self, x, y)

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
            if not int(self.game.directions[direction]):
                if self.game.current_area != 'world':
                    self.game.message.message('leave_world')
                    xy[0] = x
                    xy[1] = y
                else:
                    xy[0] = x
                    xy[1] = y
                    self.game.message.message('nowhere_togo')
            else:
                xy[0] = x
                xy[1] = y
                self.game.change_place('area%s' %(self.game.directions[direction]),direction)
            return 1
        elif (T[self.game.land[xy[1]-1][xy[0]-21]].pass_through or \
             ('spirit of order1' in self.tool_tags and T[self.game.land[xy[1]-1][xy[0]-21]].id in '#o+`sS') or \
             ('spirit of chaos1' in self.tool_tags and T[self.game.land[xy[1]-1][xy[0]-21]].id in '#o+`sS') or \
             ('gnome1' in self.tool_tags and T[self.game.land[xy[1]-1][xy[0]-21]].id in 'nmA%') or \
             'waterform' in self.effects) and \
             not (self.possessed and T[self.game.land[xy[1]-1][xy[0]-21]].id in self.possessed[0].terr_restr):
            if 'waterform' in self.effects:
                return 0
            for a in self.game.all_creatures:
                if (a.xy == xy) and (a not in self.game.hidden):
                    if a.mode in ['hostile','standing_hostile']:
                        if not self.ride:
                            self.game.combat(self, a)
                        else:
                            self.game.message.message('no_riding_fighting')
                        xy[0] = x
                        xy[1] = y
                        return 1
                    else:
                        if a.t=='sentient' and not self.possessed:
                            self.game.message.creature('talk',a)
                            answer=msvcrt.getch()
                            if answer.lower()=='y':
                                xy[0] = x
                                xy[1] = y
                                self.game.talk(a)
                                return 1
                            else:
                                self.game.message.message('')
                                if 'goblin1' in self.tool_tags:
                                    self.game.message.creature('steal',a)
                                    answer=msvcrt.getch()
                                    if answer.lower()=='y':
                                        self.game.effect('force',{'Chaos':{'force':0.02,'goblin':0.02},'Nature':{'all':-.01},'Order':{'all':-.01}})
                                        xy[0] = x
                                        xy[1] = y
                                        self.game.pickpocket(a)
                                        return 1
                                    else:
                                        self.game.message.message('')
                        elif 'tame' in a.attr and 'tame' not in a.name and 'human2' in self.tool_tags\
                              and not self.possessed:
                            self.game.message.creature('tame',a)
                            answer=msvcrt.getch()
                            if answer.lower()=='y':
                                self.game.effect('force',{'Order':{'force':0.02,'human':0.02}})
                                self.game.tame(a)
                                xy[0] = x
                                xy[1] = y
                                return 1
                            else:
                                self.game.message.message('')
                        elif a in self.followers and 'human2' in self.tool_tags\
                              and not self.possessed:
                            self.game.message.creature('tamed_use',a)
                            answer=msvcrt.getch()
                            if answer.lower()=='y':
                                self.game.effect('force',{'Order':{'force':0.01,'human':0.01}})
                                self.game.command_tamed(a)
                                xy[0] = x
                                xy[1] = y
                                return 1
                            else:
                                self.game.message.message('')
                        elif 'spirit of nature2' in self.tool_tags and not self.possessed and not self.ride:
                            self.game.message.creature('possess',a)
                            answer=msvcrt.getch()
                            if answer.lower()=='y':
                                self.game.effect('force',{'Nature':{'force':0.03,'spirit of nature':0.03}})
                                self.game.possess(a)
                                xy[0] = x
                                xy[1] = y
                                return 1
                            else:
                                self.game.message.message('')
                        if not self.ride:
                            self.game.message.creature('attack',a)
                            answer=msvcrt.getch()
                            if answer.lower()=='y':
                                a.mode='hostile'
                                for each_other in self.game.all_creatures:
                                    if each_other.force==a.force and (a.t=='sentient' and each_other.t=='sentient') and not \
                                       (a.force=='Chaos' and (self.mode=='Chaos' or ('spirit of order3' in self.tool_tags and random.randint(1,30)>each_other.attr['Mnd']))):
                                        each_other.mode='hostile'
                                self.game.combat(self, a)
                            else:
                                self.game.message.message('')
                        xy[0] = x
                        xy[1] = y
                        return 1
            if (T[self.game.land[xy[1]-1][xy[0]-21]].tire_move > self.energy) and not \
               ('kraken1' in self.tool_tags and T[self.game.land[xy[1]-1][xy[0]-21]].id in 'wWt~') and not \
               ('winterwalk' in self.effects and T[self.game.land[xy[1]-1][xy[0]-21]].id in "'i") and not \
               ('summerwalk' in self.effects and T[self.game.land[xy[1]-1][xy[0]-21]].id in ",") and not \
               (self.possessed and self.possessed[0].race=='fish' and T[self.game.land[xy[1]-1][xy[0]-21]].id in 'wWt'):
                self.game.message.emotion('tired')
                if T[self.game.land[self.xy[1]-1][self.xy[0]-21]].drowning:
                    self.life -= 1
                    self.game.message.message('drown')
                xy[0] = x
                xy[1] = y
            elif not (self.possessed and self.possessed[0].race=='fish' and T[self.game.land[xy[1]-1][xy[0]-21]].id in 'wWt'):
                if ('kraken1' in self.tool_tags and T[self.game.land[xy[1]-1][xy[0]-21]].id in 'wWt~'):
                    self.game.message.message('kraken_move')
                elif ('winterwalk' in self.effects and T[self.game.land[xy[1]-1][xy[0]-21]].id in "'i"):
                    self.game.message.message('fairy_%smove' %(T[self.game.land[xy[1]-1][xy[0]-21]].name))
                elif ('summerwalk' in self.effects and T[self.game.land[xy[1]-1][xy[0]-21]].id in ","):
                    self.game.message.message('fairy_%smove' %(T[self.game.land[xy[1]-1][xy[0]-21]].name))
                elif ('gnome1' in self.tool_tags and T[self.game.land[xy[1]-1][xy[0]-21]].id in 'nmA%'):
                    self.energy -= T[self.game.land[xy[1]-1][xy[0]-21]].tire_move
                    if T[self.game.land[xy[1]-1][xy[0]-21]].id != 'n':
                        self.game.land[xy[1]-1]=self.game.land[xy[1]-1][:xy[0]-21]+'n'+self.game.land[xy[1]-1][xy[0]-20:]
                        self.game.effect('force',{'Nature':{'force':0.01,'gnome':0.01,'terrain':0.4},'Chaos':{'all':-.01},'Order':{'all':-.01}})
                    self.game.message.message('gnome_move')
                elif ('spirit of nature1' in self.tool_tags and T[self.game.land[xy[1]-1][xy[0]-21]].id in 'd'):
                    self.energy -= T[self.game.land[xy[1]-1][xy[0]-21]].tire_move
                    self.game.land[xy[1]-1]=self.game.land[xy[1]-1][:xy[0]-21]+'g'+self.game.land[xy[1]-1][xy[0]-20:]
                    self.game.effect('force',{'Nature':{'force':0.01,'spirit of nature':0.01,'terrain':0.4},'Chaos':{'all':-.01},'Order':{'all':-.01}})
                    self.game.message.message('nature_spirit_move')
                elif ('fairy1' in self.tool_tags and T[self.game.land[xy[1]-1][xy[0]-21]].id in '.a'):
                    self.energy -= T[self.game.land[xy[1]-1][xy[0]-21]].tire_move
                    self.game.land[xy[1]-1]=self.game.land[xy[1]-1][:xy[0]-21]+'g'+self.game.land[xy[1]-1][xy[0]-20:]
                    self.game.effect('force',{'Nature':{'force':0.01,'fairy':0.01,'terrain':0.4},'Chaos':{'all':-.01},'Order':{'all':-.01}})
                    self.game.message.message('fairy_move')
                elif ('dryad1' in self.tool_tags and T[self.game.land[xy[1]-1][xy[0]-21]].id in 'D'):
                    self.energy -= T[self.game.land[xy[1]-1][xy[0]-21]].tire_move
                    self.game.land[xy[1]-1]=self.game.land[xy[1]-1][:xy[0]-21]+'T'+self.game.land[xy[1]-1][xy[0]-20:]
                    self.game.effect('force',{'Nature':{'force':0.01,'dryad':0.01,'terrain':0.4},'Chaos':{'all':-.01},'Order':{'all':-.01}})
                    self.game.message.message('dryad_move')
                elif ('goblin2' in self.tool_tags and T[self.game.land[xy[1]-1][xy[0]-21]].id in 'wW'):
                    self.energy -= T[self.game.land[xy[1]-1][xy[0]-21]].tire_move
                    self.game.land[xy[1]-1]=self.game.land[xy[1]-1][:xy[0]-21]+'t'+self.game.land[xy[1]-1][xy[0]-20:]
                    self.game.effect('force',{'Chaos':{'force':0.01,'goblin':0.01,'terrain':0.4},'Nature':{'all':-.01},'Order':{'all':-.01}})
                    self.game.message.message('goblin_move')
                elif ('spirit of chaos2' in self.tool_tags and T[self.game.land[xy[1]-1][xy[0]-21]].id in 'gT'):
                    self.energy -= T[self.game.land[xy[1]-1][xy[0]-21]].tire_move
                    if T[self.game.land[xy[1]-1][xy[0]-21]].id=='g':
                        self.game.land[xy[1]-1]=self.game.land[xy[1]-1][:xy[0]-21]+'d'+self.game.land[xy[1]-1][xy[0]-20:]
                    elif T[self.game.land[xy[1]-1][xy[0]-21]].id=='T':
                        self.game.land[xy[1]-1]=self.game.land[xy[1]-1][:xy[0]-21]+'D'+self.game.land[xy[1]-1][xy[0]-20:]
                    self.game.effect('force',{'Chaos':{'force':0.01,'spirit of chaos':0.01,'terrain':0.4},'Nature':{'all':-.01},'Order':{'all':-.01}})
                    self.game.message.message('chaos_spirit_move')
                else:
                    self.energy -= T[self.game.land[xy[1]-1][xy[0]-21]].tire_move
                    self.game.message.message(T[self.game.land[xy[1]-1][xy[0]-21]].mess)
                for item in self.game.ground_items:
                    if item[:2] == xy:
                        self.game.message.use('gr_item',item[2],item[2].qty,xy)
                        break
        elif 'door_' in T[self.game.land[xy[1]-1][xy[0]-21]].world_name:
            self.game.open_door(xy,self)
            xy[0] = x
            xy[1] = y
        else:
            if not T[self.game.land[xy[1]-1][xy[0]-21]].pass_through:
                self.game.message.message(T[self.game.land[xy[1]-1][xy[0]-21]].mess)
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
            self.game.c.page()
            self.game.c.write(' You search through the items on the ground.\n What do you want to pick up?\n\n')
            for i in range(len(pile)):
                print(' '+chr(i+97)+')  ', pile[i][2].name+', %d x %s stones' %(pile[i][2].qty,str(pile[i][2].weight)))
                self.game.c.text(4,i+3,pile[i][2].tag,pile[i][2].color)
            print('\n You can carry %s more stones.\n Your backpack can take %s more stones.' %(str(self.max_weight - self.weight),
                                                                                                str(self.backpack)))
            i1 = ' '
            while 1:
                if msvcrt.kbhit():
                    i1 = msvcrt.getch()
                    break
            self.game.c.rectangle((0,0,60,2))
        elif len(pile) == 1:
            i1 = 'a'
            it = 1
        if len(pile) > 0:
            try:
                if pile[ord(i1)-97][2].qty > 1 and self.equipment['Backpack'] != []:
                    self.game.message.message('pickup')
                    a = ''
                    i = ' '
                    while ord(i) != 13:
                        i = msvcrt.getch()
                        if ord(i) in range(48,58):
                            self.game.c.write(i)
                            a += i
                    self.game.message.message('')
                    if a =='' or int(a)==0:
                        self.game.redraw_screen()
                        return 1
                    a=int(a)
                else:
                    a = 1
            except IndexError:
                self.game.redraw_screen()
                return 0
            if a > pile[ord(i1)-97][2].qty:
                a = pile[ord(i1)-97][2].qty
            if self.weight + pile[ord(i1)-97][2].weight * a <= self.max_weight and pile[ord(i1)-97][2].weight * a <= self.backpack:
                pile[ord(i1)-97][2].get_item(a)
                if len(pile) > 1:
                    self.game.redraw_screen()
                if a < pile[ord(i1)-97][2].qty:
                    pile[ord(i1)-97][2].qty -= a
                else:
                    ground.remove(pile[ord(i1)-97])
            elif self.weight + pile[ord(i1)-97][2].weight * a > self.max_weight:
                if len(pile) > 1:
                    self.game.redraw_screen()
                self.game.message.use('cant_carry', pile[ord(i1)-97][2])
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
                            self.game.redraw_screen()
                        self.backpack = 0
                    else:
                        if len(pile) > 1:
                            self.game.redraw_screen()
                        self.game.message.message('drop_first')
                else:
                    if len(pile) > 1:
                        self.game.redraw_screen()
                    self.game.message.use('cant_fit_in_backpack', pile[ord(i1)-97][2])

        if it == 0:
            self.game.message.message('no_pickup')

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
            print(' There\'s no place in your backpack so you drop\n the %s to the ground!' %drop.name)
            msvcrt.getch()
            for i in self.game.ground_items:
                if i[:2] == self.xy and i[2].id == drop.id and i[2].name == drop.name and i[2].stackable:
                    i[2].qty += drop.qty
                    dropped = 1
            if not dropped:
                self.game.ground_items.append([self.xy[0], self.xy[1],drop])
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
                    self.game.effect('temp_attr_reverse',v)
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
            for cr in self.game.game_creatures:
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
            self.game.ground_items.append([self.xy[0], self.xy[1], self.inventory[-1]])
            self.inventory[-1].lose_item()
            self.backpack = 0
        elif not dropped and self.equipment['Backpack'] != []:
            self.backpack -= self.equipment[self.equip_tags[item]].weight*self.equipment[self.equip_tags[item]].qty
        if self.equip_tags[item] in ['Right hand','Left hand'] or 'armour' in self.equipment[self.equip_tags[item]].type:
            self.weapon_dmg -= self.equipment[self.equip_tags[item]].dmg
        if self.equip_tags[item] in ['Right hand','Left hand']:
            self.weapon_weight -= self.equipment[self.equip_tags[item]].weight
            self.game.take_effect()
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
                print(' You are not strong enough to wield this weapon with your current one!')
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
            self.game.take_effect()
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
                self.game.effect('temp_attr',v)
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
                self.effects['midnight fears']=1200-self.turn%1200
            if item.effect['midnight fears']==0:
                item.name+=' (withered)'
                item.effect.pop('midnight fears')
        if 'sun armour' in item.effect and self.equip_tags[slot] in item.type:
            if self.turn%2400>=1200:
                item.effect['sun armour']=0
            else:
                self.effects['sun armour']=1200-self.turn%2400
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
                drop = self.inventory[0].drop_item(forced=True)
                dropped = 0
                print(' There\'s no place in your backpack for the %s so you drop it to the ground!\n' %drop.name)
                msvcrt.getch()
                for i in self.game.ground_items:
                    if i[:2] == self.xy and i[2].id == drop.id and i[2].name == drop.name and i[2].stackable:
                        i[2].qty += drop.qty
                        dropped = 1
                if not dropped:
                    self.game.ground_items.append([self.xy[0], self.xy[1],drop])
        elif self.equipment['Backpack'] != []:
            self.backpack += item.weight
        if self.equip_tags[slot] in ['Right hand','Left hand'] or 'armour' in item.type:
            self.weapon_dmg += item.dmg

    def find_equipment(self,slot):
        self.game.c.page()
        self.game.c.pos(0,3)
        found = 0
        items = ''
        for i in self.inventory:
            if self.equip_tags[slot] in ['Right hand','Left hand']:
                print(' '+chr(self.inventory.index(i)+97)+')', i.name.capitalize()+', %d x %s stones' %(i.qty,str(i.weight)))
                found += 1
                items += chr(self.inventory.index(i)+97)
            elif self.equip_tags[slot] in i.type:
                print(' '+chr(self.inventory.index(i)+97)+')', i.name.capitalize()+', %d x %s stones' %(i.qty,str(i.weight)))
                found += 1
                items += chr(self.inventory.index(i)+97)
        if not found:
            print(' You have nothing usefull to equip.')
            i1 = msvcrt.getch()
            return 0
        else:
            self.game.c.pos(0,1)
            print(' What do you want to equip?')
            i1 = msvcrt.getch()
            if i1 in items:
                self.equip(self.inventory[ord(i1)-97],slot)
            return 0

    def force_attack(self,defender):
        ## Force effects based on mode and enemy
        if self.mode=='Nature':
            if defender.force=='Nature':
                if self.hunger>60 and defender.t=='animal':
                    self.game.effect('force',{'Nature':{'force':0.01,'elf':0.01},'Chaos':{'all':-0.01},'Order':{'all':-0.01}})
                else:
                    self.game.effect('force',{'Nature':{'all':-0.02},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
            elif defender.force=='Order':
                if self.game.current_place['Chaos']>=self.game.current_place['Nature']:
                    self.game.effect('force',{'Nature':{'force':0.01,'elf':0.01,'terrain':0.05},'Chaos':{'all':-0.01},'Order':{'all':-0.01}})
                else:
                    self.game.effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
            elif defender.force=='Chaos':
                self.game.effect('force',{'Nature':{'force':0.01,'elf':0.01,'terrain':0.05},'Chaos':{'all':-0.01},'Order':{'force':0.01}})
        elif self.mode=='Chaos':
            if defender.force=='Nature':
                self.game.effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
            elif defender.force=='Order':
                self.game.effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
            elif defender.force=='Chaos':
                self.game.effect('force',{'Chaos':{'ork':0.01}})
        elif self.mode=='Order':
            if defender.force=='Nature':
                if defender.t=='animal':
                    self.game.effect('force',{'Nature':{'all':-0.01},'Order':{'force':0.01,'human':0.01,'terrain':0.05},'Chaos':{'all':-0.01}})
                else:
                    if self.game.current_place['Chaos']>=self.game.current_place['Order']:
                        self.game.effect('force',{'Nature':{'all':-0.01},'Chaos':{'all':-0.01},'Order':{'force':0.01,'human':0.01,'terrain':0.05}})
                    else:
                        self.game.effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
            elif defender.force=='Order':
                if defender.t=='animal':
                    self.game.effect('force',{'Nature':{'all':-0.01},'Order':{'force':0.01,'human':0.01,'terrain':0.05},'Chaos':{'all':-0.01}})
                else:
                    self.game.effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.1},'Order':{'all':-0.02}})
            elif defender.force=='Chaos':
                if defender.t=='animal':
                    self.game.effect('force',{'Nature':{'all':-0.01},'Order':{'force':0.01,'human':0.01,'terrain':0.05},'Chaos':{'all':-0.01}})
                else:
                    self.game.effect('force',{'Nature':{'force':0.01},'Chaos':{'all':-0.01},'Order':{'force':0.01,'human':0.01,'terrain':0.05}})

class NPC(Living_thing):
    __refs__ = []

    def __init__(self):
        super(NPC,self).__init__()
        self.__refs__.append(self)

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
        key = '0'
        mode = self.mode
        creature_sight=self.game.direct_path(self.xy, self.game.player.xy)
        creature_los = self.game.clear_los(creature_sight)
        player_los = self.game.clear_los(self.game.direct_path(self.game.player.xy,self.xy))
        if self.t=='sentient':
            if float(self.fear)/(self.fear+(self.attr['Int']+self.attr['Mnd'])*10)>random.random():
                mode='fearfull'
        if self.race=='troll' and self.game.current_place['Chaos']>=60 and self.game.player.turn%2 and self.game.player.turn%2400<1200:
            self.path=[]
            mode='wander'
        if mode in ['follow','hostile','fearfull_hide','fearfull'] and ('invisible' in self.game.player.effects or not creature_los):
            mode = 'wander'
        if mode in ['hostile','standing_hostile','fearfull_hide','fearfull'] and 'stealthy' in self.game.player.tool_tags and creature_los:
            hide_chance=self.game.player.attr['Dex']*3+self.game.player.attr['Int']-self.attr['Int']+len(creature_sight)
            if random.randint(1,100)<hide_chance:
                if mode=='standing_hostile':
                    mode='standing'
                else:
                    mode='wander'
        if 'ork1' in self.game.player.tool_tags and self.mode=='hostile' and creature_los:
            if ('human3' in self.game.player.tool_tags and random.random()<self.game.player.research_races['Chaos']['ork']/(2*(max([self.game.current_place['Order'],self.game.current_place['Nature']])+self.game.player.research_races['Chaos']['ork'])))\
               or (random.random()<self.game.player.races['Chaos']['ork']/(2*(max([self.game.current_place['Order'],self.game.current_place['Nature']])+self.game.player.races['Chaos']['ork']))):
                    mode='fearfull'
        ## wander, follow, hostile, fearfull_hide, standing_hostile, standing, guarding, fearfull
        if mode == 'guarding':
            fighting=0
            if 'target' in self.attr and self.attr['target']!=[] and self.attr['target'] in self.game.all_creatures:
                if len(self.game.direct_path(self.attr['target'].xy,self.game.player.xy))<5:
                    fighting=1
                    self.path=self.game.direct_path(self.xy,self.attr['target'].xy)
                else:
                    self.attr['target']=[]
            if not fighting:
                for enemy in self.game.all_creatures:
                    if enemy.mode=='hostile' and len(self.game.direct_path(enemy.xy,self.game.player.xy))<3 and self.game.clear_los(self.game.direct_path(self.xy,enemy.xy)):
                        fighting=1
                        self.attr['target']=enemy
                        self.path=self.game.direct_path(self.xy,self.game.player.attr['target'].xy)
            if not fighting:
                mode='follow'
        if mode == 'wander':
            if self.path:
                try:
                    if self.game.good_place(self,self.path[1]):
                        self.xy = self.path[1]
                        self.path = self.path[1:]
                    else:
                        self.path=[]
                except IndexError:
                    self.path=[]
                key = '5'
            else:
                if self.race=='troll' and self.game.current_place['Chaos']>=60 and self.game.player.turn%2 and self.game.player.turn%2400<1200:
                    key='5'
                else:
                    key = str(random.randint(1,9))
        if mode in ['follow','hostile','standing_hostile','guarding']:
            if mode != 'guarding':
                self.path = self.game.direct_path(self.xy, self.game.player.xy)
            shot=0
            if mode=='hostile' and 'shoot' in self.attr:
                if random.randint(1,40)<self.attr['Dex'] and len(self.path)>2:
                    self.game.shoot(self)
                    key='5'
                    shot=1
            if not shot:
                try:
                    if self.game.good_place(self,self.path[1]):
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
                            if self.game.good_place(self,[self.xy[a]+md[key][a] for a in range(2)]):
                                found_good=1
                            else:
                                the_key=key
                except IndexError:
                    key = str(random.randint(1,9))
        if mode == 'fearfull':
            self.xy[0] -= cmp(self.game.player.xy[0],x)
            self.xy[1] -= cmp(self.game.player.xy[1],y)
            key='0'
        if mode == 'fearfull_hide':
            if (abs(self.game.player.xy[0]-x) + abs(self.game.player.xy[1]-y)) < 7:
                self.xy[0] += cmp(self.area[4],x)
                self.xy[1] += cmp(self.area[5],y)
                if ((cmp(self.area[4],x) == 0) and (cmp(self.area[5],y) == 0)) and (self not in self.game.hidden):
                    self.game.hidden.append(self)
                key = '0'
            else:
                key = str(random.randint(1,9))
            if (self in self.game.hidden) and ([x,y] != self.area[4:]):
                self.game.hidden.remove(self)
        if mode == 'standing':
            key='5'
        for a in range(2):
            self.xy[a] = self.xy[a] + md[key][a]
        self.creature_passage(x, y)
        if self in self.game.hidden:
            if self.game.player.xy != self.xy:
                self.game.hide(self)
        else:
            if player_los or (self.game.current_place['Nature']>=33 and self.game.current_place['Temperature']>=33 and 'elf2' in self.game.player.tool_tags):
                self.game.draw_move(self, x, y)
            if self.race=='water elemental' and T[self.game.land[self.xy[1]-1][self.xy[0]-21]].id in 'wWt':
                self.attr['invisible']=2
            if 'invisible' in self.attr:
                self.game.hide(self)
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
        elif T[self.game.land[self.xy[1]-1][self.xy[0]-21]].id in self.terr_restr and not self.mode=='standing_hostile':
            self.xy[0] = x
            self.xy[1] = y
            return 1
        elif T[self.game.land[self.xy[1]-1][self.xy[0]-21]].pass_through or \
             (self.race=='spirit of order' and self.game.current_place['Order']>30 and T[self.game.land[self.xy[1]-1][self.xy[0]-21]].id in '#o+`sS') or \
             (self.race=='spirit of chaos' and self.game.current_place['Chaos']>30 and T[self.game.land[self.xy[1]-1][self.xy[0]-21]].id in '#o+`sS') or \
             (self.race=='gnome' and self.game.current_place['Nature']>30 and T[self.game.land[self.xy[1]-1][self.xy[0]-21]].id in 'nmA%'):
            for a in self.game.all_beings:
                if a.xy == self.xy and a.game_id != self.game_id:
                    self.xy[0] = x
                    self.xy[1] = y
                    if (self.mode=='guarding' and a.mode=='hostile') or (a.mode=='guarding' and self.mode=='hostile') or\
                       (a.xy == self.game.player.xy and self.mode in ['hostile','standing_hostile'] and 'waterform' not in self.game.player.effects):
                        self.game.combat(self,a)
                    return 1
            if T[self.game.land[self.xy[1]-1][self.xy[0]-21]].tire_move>self.energy:
                if T[self.game.land[self.xy[1]-1][self.xy[0]-21]].drowning and self.race!='fish':
                    self.life -= 1
                self.xy[0] = x
                self.xy[1] = y
            elif not (self.race=='kraken' and self.game.current_place['Chaos']>30 and T[self.game.land[self.xy[1]-1][self.xy[0]-21]].id in 'wWt~')\
                 and not (self.race=='fairy' and self.game.current_place['Nature']>60 and T[self.game.land[self.xy[1]-1][self.xy[0]-21]].id in "'i,")\
                 and not (self.race=='fish' and T[self.game.land[self.xy[1]-1][self.xy[0]-21]].id in "Wwt~"):
                self.energy-=T[self.game.land[self.xy[1]-1][self.xy[0]-21]].tire_move
            if self.mode=='standing_hostile':
                self.xy[0] = x
                self.xy[1] = y
        elif 'door_' in T[self.game.land[self.xy[1]-1][self.xy[0]-21]].world_name:
            self.game.open_door(self.xy,self)
            self.xy[0] = x
            self.xy[1] = y
        else:
              self.xy[0] = x
              self.xy[1] = y


class Human(NPC):
    def __init__(self,xy,area,path,terr_restr,emotion,fear,tag,name,mode,id,attr,WD,armour,f,r,game_id=0):
        super(Human,self).__init__()
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
            attr_d[a]=int(self.race_attrs[r][a]*self.game.current_place[f]/100.)
        if f=='Nature':
            emo=2
            arm=self.game.current_place[f]*3.5
            WD=self.game.current_place[f]/60
            if self.game.player.forces['Chaos']:
                if self.game.player.forces['Nature']-self.game.player.forces['Chaos']<self.game.current_place['Nature']-self.game.current_place['Chaos']:
                    mode='hostile'
            ammo=wood_arrow
        elif f=='Order':
            emo=7
            arm=self.game.current_place[f]*2.75
            WD=self.game.current_place[f]/40
            if self.game.player.forces['Chaos']:
                if self.game.player.forces['Order']-self.game.player.forces['Chaos']<self.game.current_place['Order']-self.game.current_place['Chaos']:
                    mode='hostile'
            ammo=wood_bolt
        elif f=='Chaos':
            emo=12
            arm=self.game.current_place[f]*2
            WD=self.game.current_place[f]/30
            if self.game.player.forces['Order']:
                if self.game.player.forces['Chaos']-self.game.player.forces['Order']<self.game.current_place['Chaos']-self.game.current_place['Order']:
                    mode='hostile'
            if self.game.player.forces['Nature']:
                if self.game.player.forces['Chaos']-self.game.player.forces['Nature']<self.game.current_place['Chaos']-self.game.current_place['Nature']:
                    mode='hostile'
            if 'spirit of order3' in self.game.player.tool_tags and random.randint(1,30)>attr_d['Mnd']:
                mode='fearfull'
            ammo=stone
        if self.game.player.possessed:
            mode='wander'
        duplica = Human(xy,self.area,self.path,self.terr_restr,emo,self.fear,r[0].upper(),r,
                        mode,self.id,attr_d,WD,arm,f,r,game_id=g_id)
        duplica.learning=random.random()
        duplica.attr['loot']=[[1310,100,1,4],[r,self.game.current_place[f]+self.game.current_place['Treasure']*10]]
        duplica.attr['shoot']=ammo
        if rand:
            duplica.random = True
            duplica.appearance=self.game.player.turn
        else:
            duplica.random = False
            duplica.appearance=0
        return duplica

class Animal(NPC):
    def __init__(self,xy,area,path,terr_restr,emotion,tag,name,mode,id,life,attr,WS,armour,f,r,game_id=0):
        super(Animal,self).__init__()
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

    def duplicate(self,x,y,g_id,f,r,rand=True):
        xy = [x, y]
        duplica = Animal(xy,self.area,self.path,self.terr_restr,self.emotion,self.tag,self.name,
                         self.mode,self.id,self.life,self.attr,self.weapon_skill,self.armour,f,r,game_id=g_id)
        duplica.learning=0
        if self.mode in ['hostile','fearfull_hide','fearfull'] and 'elf1' in self.game.player.tool_tags and self.t=='animal':
            duplica.mode = 'wander'
        if rand:
            duplica.random = True
            duplica.appearance=self.game.player.turn
        else:
            duplica.random = False
            duplica.appearance=0
        return duplica
