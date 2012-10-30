import msvcrt
import pickle
import random
import os
import Console
from os import curdir
from os import mkdir
from time import sleep
from glob import glob

############ CLASSES
class Game:

    def __init__(self):
        local_files=glob('*')
        self.start_game(local_files)

    def save(self):
    ##    c.write('Save to which file?')
    ##    a = ''
    ##    i = ' '
    ##    while ord(i) != 13:
    ##        i = msvcrt.getch()
    ##        if ord(i) in range(65,91) or ord(i) in range(97,123) or ord(i) == 46:
    ##            c.write(i)
    ##            a += i
        try:
            f = open(self.ch.name, 'w')
        except:
            return 0
        for x in range(23):
            f.write(land[x]+'\n')
        pickle.dump(self.ch, f)
        pickle.dump(self.ch.inventory, f)
        pickle.dump(self.ch.equipment, f)
        pickle.dump(self.ch.skills, f)
        pickle.dump(self.ch.spells, f)
        pickle.dump(self.ch.forces, f)
        pickle.dump(self.ch.races, f)
        pickle.dump(self.ch.effects, f)
        pickle.dump(self.ch.land_effects, f)
        pickle.dump(self.ch.known_areas, f)
        pickle.dump(self.ch.weapon_skills, f)
        pickle.dump(self.ch.attr_colors, f)
        creatures_left=[]
        for creature in all_creatures:
            if creature not in self.ch.followers+self.ch.ride+self.ch.possessed:
                creatures_left.append(creature)
        pickle.dump(creatures_left, f)
        pickle.dump(hidden, f)
        pickle.dump(ground_items, f)
        pickle.dump(directions, f)
        pickle.dump(world_places, f)
        pickle.dump(top_world_places, f)
        pickle.dump(place_descriptions, f)
        pickle.dump(map_coords, f)
        pickle.dump(current_area, f)
        pickle.dump(current_place, f)
        pickle.dump(treasure_modifier, f)
        pickle.dump(T_matrix, f)
        f.close()
        ## area files update
        os.chdir(os.curdir+r'\%s_dir' %(self.ch.name))
        new_files=glob('new_area*.dat')
        for f in [every.split('_')[-1] for every in new_files]:
            os.system('del %s' %(f))
        for f in new_files:
            os.system('ren %s %s' %(f,f.split('_')[-1]))
        os.chdir('..')

        return 1

    def start_game(self,fl):
        t = 0
        i = ''
        f = ''
        while t == 0:
            T_matrix=[]
            c.page()
            c.write('''
               ___      _   _         _   _    _   ___   ____
              |   \    / |  |        / |  |\   |  /   \ |
              |___/   /  |  |       /  |  | \  |  |     |___
              |   \  /---|  |      /---|  |  \ |  |     |
              |___/ /    |  |___| /    |  |   \|  \___/ |____

                                    ver 0.6 
                                         
                                   (n)ew game
                             (l)oad a previous game
                        ''')
            i = msvcrt.getch()
            if i == 'n':
                self.create_character(fl)
                t = draw_terr(self.ch.start_force)
            if i == 'l':
                c.write('Load which character? ')
                a = ''
                i = ' '
                while ord(i) != 13:
                    i = msvcrt.getch()
                    if ord(i) in range(65,91) or ord(i) in range(97,123) or ord(i) == 46:
                        c.write(i)
                        a += i
                t,T_matrix = load_terr(a)
        redraw_screen()
        c.pos(*self.ch.xy)
        
    def create_character(self,fl):
        races = {'a':'elf','b':'gnome','c':'spirit of nature','d':'dryad','e':'water elemental','f':'fairy','g':'human',
                 'h':'dwarf','i':'spirit of order','j':'ork','k':'troll','l':'spirit of chaos','m':'goblin','n':'kraken',
                 'o':'imp'}
        i = ''
        while i not in races.keys():
            c.page()
            c.write("""
 Every form your character takes in Balance is controlled by its respective
 Force - Nature, Order or Chaos. Every action will align you more with the
 Force of your chosen form and will increase your attunement to it. This is
 the main way of developing your character in the game - you gain and loose
 abilities based on the forms you hold. Choosing a form now gives you 34%
 attunement to it, and 34% alignment to the respective force. Your total
 form attunement can't be higher than your alignment to the respective force,
 and your total force alignment cannot exceed 100%.

 Choose your character's form:

            NATURE                 ORDER                   CHAOS
            
            a) Elf               g) Human                 j) Ork
           b) Gnome              h) Dwarf                k) Troll
      c) Spirit of Nature    i) Spirit of Order      l) Spirit of Chaos
           d) Dryad                                      m) Goblin
     e) Water Elemental                                  n) Kraken
           f) Fairy                                       o) Imp""")
            i = msvcrt.getch()
        race = races[i]
        if i < 'g':
            force='Nature'
        elif i > 'i':
            force='Chaos'
        else:
            force='Order'
        self.ch = make_player(race,force)
        take_force_effect(self.ch)
        all_beings = [self.ch]

        professions={'a':{'Order':'warrior','Nature':'defender','Chaos':'pillager'},
                     'b':{'Order':'scout','Nature':'ranger','Chaos':'roamer'},
                     'c':{'Order':'magician','Nature':'druid','Chaos':'shaman'},
                     'd':{'Order':'builder','Nature':'keeper','Chaos':'scavenger'}}
        i=''
        while i not in professions.keys():
            c.page()
            c.write("""
 You can now select your character's initial equipment based on your preferred
 role. The first choice is best for combat, the second favours stealth and
 hit-and-run tactics, the third uses the power of spirits and forces, and the
 last is for the creatively inclined. Every choice is also best suited for the
 respective action mode in the game.

 Once in the game you can do whatever you wish, this only equips you properly
 for one of the playing modes.

%s""" %('\n'.join(['    %s) %s' %(x,professions[x][force].capitalize()) for x in ['a','b','c','d']])))
            i = msvcrt.getch()
        self.ch.start_inv(i)
        while True:
            c.page()
            c.write('''
  Finally, what is your character's name? ''')
            a = ''
            i = ' '
            while ord(i) != 13:
                i = msvcrt.getch()
                if ord(i) in range(65,91) or ord(i) in range(97,123) or ord(i) == 46:
                    c.write(i)
                    a += i
            c.write(i)
            self.ch.name = a
            if self.ch.name in fl:
                print '\n  Character savefile already exists!'
                i1=msvcrt.getch()
            else:
                break
        mkdir(curdir+'//%s_dir' %(a))

    def main_loop(self):
        i = ' '
        clock = 1
        riding=0
        while i:
            if msvcrt.kbhit():
                message_message('')
                i = msvcrt.getch()
                if self.ch.ride and self.ch.ride[0].food>24 and i in ['1','2','3','4','5','6','7','8','9']:
                    if riding:
                        move(i,self.ch,riding)
                        self.ch.ride[0].food-=1
                        riding=0
                        continue
                    else:
                        riding=1
                if i == '0':
                    i = '-1'
                if i == 'S':
                    message_message('q')
                    i = msvcrt.getch()
                    if i == 'y' or i == 'Y':
                        if self.save():
                            redraw_screen()
                            i = '0'
                        else:
                            message_message('')
                            message_message('save_failed')
                    else:
                        message_message('')
                    continue
                if i == 'Q':
                    break
                if i == 'c':
                    character()
                    redraw_screen()
                    continue
                if i == 'l':
                    message_message('look')
                    look()
                    redraw_screen()
        ##            message_message('')
                    continue
                    i = '0'
                ## Form-dependent actions
                if 'waterform' not in self.ch.effects:
                    if i == 's' and current_area != 'world':
                        if self.ch.ride:
                            message_message('dismount')
                            self.ch.ride[0].mode='follow'
                            self.ch.ride[0].xy=ch.xy[:]
                            self.ch.backpack-=self.ch.ride[0].attr['Str']*2
                            while self.ch.backpack<0:
                                drop = self.ch.inventory[-1].drop_item('yes',10000)
                                dropped = 0
                                for item in ground_items:
                                    if item[:2] == self.ch.xy and item[2].id == drop.id and item[2].stackable and item[2].name == drop.name:
                                        item[2].qty += drop.qty
                                        dropped = 1
                                if not dropped:
                                    ground_items.append([self.ch.xy[0], self.ch.xy[1],drop])
                                message_use('create_drop',drop)
                                msvcrt.getch()
                            self.ch.followers.append(self.ch.ride[0])
                            self.ch.ride=[]
                            i='0'
                        elif self.ch.possessed:
                            if self.ch.possessed[0].mode=='temp':
                                message_creature('transform_outof',self.ch.possessed[0])
                            else:
                                message_creature('unpossess',self.ch.possessed[0])
                                self.ch.possessed[0].xy=self.ch.xy[:]
                                self.ch.possessed[0].mode='wander'
                            self.ch.life-=self.ch.possessed[0].life
                            self.ch.max_life-=self.ch.possessed[0].life
                            if self.ch.life<=0:
                                self.ch.possessed[0].life+=self.ch.life
                                self.ch.life=1
                            for at in self.ch.attr:
                                self.ch.attr[at]=self.ch.max_attr[at]
                            self.ch.possessed=[]
                            for cr in all_creatures:
                                if cr not in self.ch.followers+self.ch.ride+self.ch.possessed:
                                    if cr.force=='Nature':
                                        if self.ch.forces['Chaos']:
                                            if self.ch.forces['Nature']-self.ch.forces['Chaos']<\
                                               current_place['Nature']-current_place['Chaos']:
                                                cr.mode='hostile'
                                    elif cr.force=='Order':
                                        if self.ch.forces['Chaos']:
                                            if self.ch.forces['Order']-self.ch.forces['Chaos']<\
                                               current_place['Order']-current_place['Chaos']:
                                                cr.mode='hostile'
                                    elif cr.force=='Chaos':
                                        if self.ch.forces['Order']:
                                            if self.ch.forces['Chaos']-self.ch.forces['Order']<\
                                               current_place['Chaos']-current_place['Order']:
                                                cr.mode='hostile'
                                        if self.ch.forces['Nature']:
                                            if self.ch.forces['Chaos']-self.ch.forces['Nature']<\
                                               current_place['Chaos']-current_place['Nature']:
                                                cr.mode='hostile'
                                        if 'spirit of order3' in self.ch.tool_tags and random.randint(1,30)>cr.attr['Mnd']:
                                            cr.mode='fearfull'
                            i='0'
                        else:
                            if T[land[self.ch.xy[1]-1][self.ch.xy[0]-21]].id in unsittable:
                                message_message('no_sit')
                                i = '0'
                            else:
                                self.ch.sit = True
                                self.ch.rest = 25
                                message_message('sit')
                                i = '0'
                    if i == 'm':
                        if self.ch.mode == 'Nature':
                            self.ch.mode = 'Order'
                        elif self.ch.mode == 'Order':
                            self.ch.mode = 'Chaos'
                        elif self.ch.mode == 'Chaos':
                            self.ch.mode = 'Nature'
                        draw_mode()
                        c.pos(*self.ch.xy)
                        continue
                        i = '0'
                    if i == 'q' and current_area != 'world':
                        drink(self.ch.xy)
                        i = '0'
                    if not self.ch.possessed:
                        if i=='h':
                            if self.ch.target:
                                if (self.ch.equipment['Right hand'] and 'ranged' in self.ch.equipment['Right hand'].type) or (self.ch.equipment['Left hand'] and 'ranged' in self.ch.equipment['Left hand'].type):
                                    if self.ch.equipment['Right hand']:
                                        handed='Right hand'
                                    else:
                                        handed='Left hand'
                                    if self.ch.equipment['Ammunition']:
                                        if self.ch.equipment['Ammunition'].effect['shoot']==self.ch.equipment[handed].effect['shoot']:
                                            shoot(self.ch)
                                        else:
                                            message_message('wrong_ammo')
                                    else:
                                        message_message('need_ammo')
                                else:
                                    message_message('need_ranged_weapon')
                            else:
                                message_message('target_first')
                            i='0'
                        if i == 'i':
                            draw_inv()
                            redraw_screen()
                            if current_area == 'world':
                                i = '-1'
                            else:
                                i = '0'
                        if i == 'e':
                            draw_equip()
                            redraw_screen()
                            if current_area == 'world':
                                i = '-1'
                            else:
                                i = '0'
                        if i == 'k' and current_area != 'world':
                            cook()
                            redraw_screen()
                            i = '0'
                        if i == 'b' and not self.ch.ride:
                            if 'human1' in self.ch.tool_tags or 'dwarf1' in self.ch.tool_tags:
                                ground_items=build(ground_items)
                            else:
                                message_message('need_human1&dwarf1')
                            continue
                            i = '0'
                        if i == 't':
                            if 'dryad3' in self.ch.tool_tags:
                                dryad_grow()
                            else:
                                message_message('need_dryad3')
                            continue
                            i = '0'
                        if i == 'C' and not self.ch.ride:
                            ground_items=create(ground_items)
                            i = '0'
                        if i == '+' and current_area != 'world':
                            opened = find_to_open(self.ch.xy)
                            if opened:
                                redraw_screen()
                            i = '0'
                        if i == 'p' and current_area != 'world':
                            self.ch.pick_up(ground_items)
                            i = '0'
                        if i == 'w' and current_area != 'world' and not self.ch.ride:
                            self.ch.sit = False
                            self.ch.rest = 1
                            message_message('work')
                            i = ''
                            while not i:        
                                if msvcrt.kbhit():
                                    i = msvcrt.getch()
                            work(i)
                            continue
                            i = '0'
                        if i == 'r':
                            if 'human3' in self.ch.tool_tags:
                                research()
                                redraw_screen()
                            else:
                                message_message('need_human3')
                            continue
                    elif i in 'rwp+bkeiCt':
                        message_message('not_when_possessed')
                        msvcrt.getch()
                        i='0'
                elif i in 'rwmp+bkqseiCt':
                    message_message('not_in_waterform')
                    msvcrt.getch()
                    i='0'
        ##        if i == '<':
        ##            ch.sit = False
        ##            if T[land[ch.xy[1]-1][ch.xy[0]-21]].id == '<':
        ##                change_place('area'+directions[5],5)
        ##                message_message('going_down')
        ##                i = '0'
        ##            elif T[land[ch.xy[1]-1][ch.xy[0]-21]].id == '>':
        ##                message_message('nowhere_togo')
        ##                i = '0'
        ##            else:
        ##                message_message('no_stairs')
        ##                i = '0'
        ##        if i == '>':
        ##            ch.sit = False
        ##            if T[land[ch.xy[1]-1][ch.xy[0]-21]].id == '>':
        ##                change_place('area'+directions[4],4)
        ##                message_message('going_up')
        ##                i = '0'
        ##            elif T[land[ch.xy[1]-1][ch.xy[0]-21]].id == '<':
        ##                message_message('nowhere_togo')
        ##                i = '0'
        ##            else:
        ##                message_message('no_stairs')
        ##                i = '0'
        ##        if i == 'W':
        ##            if world_places[current_area] == [1,1]:
        ##                message_message('no_exit')
        ##            else:
        ##                current_area, entered = world(current_area)
        ##                redraw_screen()
        ##                if entered == 0:
        ##                    message_message('nowhere_togo')
        ##            i = '-1'
                if (i != '0') and (i != '5') and (i != '-1'):
                    self.ch.sit = False
                    self.ch.rest = 1
                clock = game_time(i)
                if clock == 0:
                    break
                c.pos(*self.ch.xy)
        self.clean_up()

    def clean_up(self):
        ## area files clean-up
        new_files=glob(r'%s_dir\new_area*.dat' %(ch.name))
        all_files=glob(r'%s_dir\*' %(ch.name))
        local_files=glob('*')
        for f in new_files:
            os.system('del %s' %(f))
        if '%s' %(ch.name) not in local_files:
            for f in all_files:
                os.system('del %s' %(f))
            os.system('rd %s_dir' %(ch.name))
        os._exit(0)

class Terrain:
    def __init__(self, name = 'dirt', world_name = 'no_world_name', id = '.', colour = 6, char = '.', mess = '',
                 pass_through = True, degradable = True, workable = True,
                 degrade_to = {'Nature':'.','Order':'.','Chaos':'.'}, degr_mess = {'Nature':'','Order':'','Chaos':''},
                 degrade_tool = {'Nature':[],'Order':[],'Chaos':[]}, tire = {'Nature':0,'Order':0,'Chaos':0},
                 tire_move = 0, drink = {}, loot = {'Nature':[],'Order':[],'Chaos':[]}, random_creatures = [],
                 force_effects={'Nature':{},'Order':{},'Chaos':{}}):
        self.colour = colour
        self.name = name
        self.world_name = world_name
        self.id = id
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

class item:
    def __init__(self,weight,type,tool_tag,weap_type,armour,dmg,name,id,stackable=False,qty=1,effect={},color=7,tag='?'):
        self.weight = weight
        self.type = type[:]
        self.tool_tag = tool_tag[:]
        self.weapon_type = weap_type
        self.armour = armour
        self.dmg = dmg
        self.name = name
        self.id = id
        self.stackable = stackable
        self.qty = qty
        self.effect = effect
        self.color = color
        self.tag = tag

    def duplicate(self,i=1,name=''): ## Mogat da se nastroivat cvetovete i imenata na predmetite v rechnika
        if name == '':
            name = self.name
        if self.name == 'vegetable' and name=='vegetable':
            name=random.choice(['carrot','tomato','potato','pepper','onion','cabbage','corn','lettuce','cucumber','radish','cauliflower'])
        elif self.name == 'flower' and name=='flower':
            name=random.choice(['rose'])
##        if self.name == 'herb' and name=='herb':
##            name=random.choice(['dill'])
        col = self.color
        t = self.type[:]
        ef = {}
        for key in self.effect.keys():
            if str(type(self.effect[key])) == "<type 'list'>":
                ef[key]=self.effect[key][:]
            else:
                ef[key]=self.effect[key]
        if 'ingot' in name:
            if 'craft' not in ef:
                ef['craft']='%s' %(name.split()[0])
        cols = {'black':112,'gray':7,'embroidered':201,'copper':6,'silver':15,'gold':14,'iron':7,'mouldy':2,'dirty':6}
        for x in name.split():
            if x in cols.keys() and 'enameled' not in t:
                col = cols[x]
                break
        for x in ['diamond','emerald','sapphire','ruby','pearl','amethyst','topaz','tourmaline','garnet','aquamarine',
                     'opal','turquoise','lapis lazuli']:
            if x+' encrusted' in name and x not in t:
                t.append(x)
        if 'enameled' in name and 'enameled' not in t:
            t.append('enameled')
            col = random.randint(1,15)
        if 'engraved' in name and 'engraving' not in ef:
            engraving = self.random_engraving()
            ef['engraving'] = engraving
        ## Tipa na bijutata se dobavq za da mogat da se pretopqvat za metala
        if 'gold' in name and ('ingot' in name or 'jewel' in self.type or 'coin' in self.type) and 'gold' not in t:
            t.append('gold')
        if 'silver' in name and ('ingot' in name or 'jewel' in self.type or 'coin' in self.type) and 'silver' not in t:
            t.append('silver')
        if 'copper' in name and ('ingot' in name or 'jewel' in self.type or 'coin' in self.type) and 'copper' not in t:
            t.append('copper')
        if 'iron' in name and ('jewel' in self.type or 'coin' in self.type) and 'iron' not in t:
            t.append('iron')
        if 'steel' in name and ('jewel' in self.type or 'coin' in self.type) and 'steel' not in t:
            t.append('steel')
        return item(self.weight, t, self.tool_tag, self.weapon_type, self.armour, self.dmg, name,
                       self.id, self.stackable, qty=i, effect=ef, color=col, tag=self.tag)

    def random_engraving(self):
        engraving = ''
        vowel = 'aoeiuy'
        consonant = 'rtplkhgfdszxcvbnmw'
        words = random.randint(1,3)
        for x in range(words):
            cap = 1
            syllables = random.randint(1,3)
            for y in range(syllables):
                chars=[consonant,vowel]
                random.shuffle(chars,random=random.random)
                for z in chars:
                    if cap:
                        engraving+=random.choice(z).upper()
                        cap = 0
                    else:
                        engraving+=random.choice(z)
            if x < words-1:
                engraving += ' '
        return engraving
            
    def get_item(self,qty=1,name=''):
        if name == '':
            name = self.name
        found=0
        if name == 'ring of winter' and current_place['Temperature']>=33:
            if ch.equipment['Left ring']:
                if ch.equipment['Left ring'].name=='ring of summer':
                    found=1
                else:
                    for it in ch.inventory:
                        if it.name=='ring of summer':
                            found=1
                            break
            if not found:
                name+=' (melted)'
                del(self.effect['winterwalk'])
                message_use('pickup_melt', self)
            else:
                message_use('pickup', self)
        elif name == 'ring of summer' and current_place['Temperature']<66:
            if ch.equipment['Right ring']:
                if ch.equipment['Right ring'].name=='ring of winter':
                    found=1
                else:
                    for it in ch.inventory:
                        if it.name=='ring of winter':
                            found=1
                            break
            if not found:
                name+=' (withered)'
                del(self.effect['summerwalk'])
                message_use('pickup_dry', self)
            else:
                message_use('pickup', self)
        else:
            message_use('pickup', self)
        has_it = 0
        for x in ch.inventory:
            if self.id == x.id and self.name == x.name:
                has_it = 1
                break
        if self.stackable and has_it == 1:
            x.qty += qty
            ch.weight += x.weight * qty
            ch.backpack -= x.weight * qty
        else:
            ch.inventory.append(self.duplicate(qty,name))
            ch.tool_tags += self.tool_tag
            ch.weight += self.weight * qty
            ch.backpack -= self.weight * qty

    def create_item(self,qty=1,name=''):
        has_it = 0
        if not name:
            name = self.name
        for x in ch.inventory:
            if self.id==x.id and name == x.name:
                has_it = 1
                break
        if (ch.weight + self.weight*qty <= ch.max_weight and self.weight*qty <= ch.backpack) or ch.equipment['Backpack'] == []:
            if self.stackable and has_it == 1:
                x.qty += qty
            else:
                ch.inventory.append(self.duplicate(qty,name))
                for tt in self.tool_tag:
                    ch.tool_tags.append(tt)
            ch.weight += self.weight * qty
            if ch.equipment['Backpack'] != []:
                ch.backpack -= self.weight * qty
            else:
                ch.free_hands -= 1
        else:
            drop = self.duplicate(qty,name)
            dropped = 0
            message_use('create_drop',drop)
            wait = msvcrt.getch()
            for item in ground_items:
                if item[:2] == ch.xy and item[2].id == drop.id and item[2].name == drop.name and item[2].stackable:
                    item[2].qty += drop.qty
                    dropped = 1
            if not dropped:
                ground_items.append([ch.xy[0], ch.xy[1],drop])

    def lose_item(self,i=1):
        if (i < self.qty):
            self.qty -= i
        else:
            if (i > self.qty):
                i = self.qty
            ch.inventory.remove(self)
            if self.tool_tag:
                for tag in self.tool_tag:
                    ch.tool_tags.remove(tag)
        ch.weight -= self.weight * i
        if ch.equipment['Backpack'] != []:
            ch.backpack += self.weight * i
        else:
            ch.free_hands += i
            if 'two_handed' in self.type:
                ch.free_hands += 1
        return i

    def drop_item(self,forced='',s=None):
        if self.qty >1 and not forced:
            message_message('how_much')
            a = ''
            i = ' '
            while ord(i) != 13:        
                i = msvcrt.getch()
                if ord(i) in range(48,58):
                    c.write(i)
                    a += i
            if self.weight*min([self.qty,int(a)]) > s:
                return None
            i = self.lose_item(int(a))
            duplica = self.duplicate(i)
            return duplica
        else:
            if self.weight*self.qty > s:
                return None
            i = self.lose_item(self.qty)
            return self

    def eat(self):      
        if 'food' in self.type or ('raw meat' in self.type and 'ork2' in ch.tool_tags):
            if (ch.hunger > 0):
                self.lose_item()
                for k,v in self.effect.items():
                    effect(k,v)
            else:
                message_use('over_eat',self)
                i = msvcrt.getch()
        if ('drink' in self.type):
            if ch.thirst > 0:
                self.lose_item()
                for k,v in self.effect.items():
                    effect(k,v)
            else:
                message_use('over_drink',self)
                i = msvcrt.getch()

    def use_item(self,ex=''):
        if ('food' in self.type) or ('drink' in self.type) or ('raw meat' in self.type and 'ork2' in ch.tool_tags):
            self.eat()
        elif (ex=='expend' and 'expendable' in self.type):
            self.lose_item()
        elif (ex=='' and 'expendable' not in self.type):
            used=0
            for k,v in self.effect.items():
                if k!='temp_attr':
                    used1 = effect(k,v)
                    if k=='transform':
                        del(self.effect['transform'])
                    if used1==None:
                        used+=1
##                    elif used1==0:
##                        used=0
            if used == 0:
                return 0
            if ('herb_set' not in self.tool_tag) and ('magic_book' not in self.tool_tag)\
                and ('totem' not in self.type) and (self.name!='lapis lazuli'):
                self.lose_item()
            if 'herb_set' in self.tool_tag:
                if 'herbalism' not in ch.skills:
                    ch.skills['herbalism'] = float(ch.attr['Int'])
                else:
                    learn = random.uniform(0,100)
                    if learn <= (ch.attr['Int'] - ch.skills['herbalism']/5)/ch.attr['Int']*100:
                        ch.skills['herbalism'] += 0.05

class Player:
    def __init__(self, xy, race,force):
        self.xy = xy
        self.base_attr = race_attrs[race]
        self.attr = {}
        start_force = 100.
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
        self.skills = {}
        self.spells = {}
        self.spell_cast = 0
        self.tool_tags = ['inherent']
        self.attr_colors = {'Str':7,'End':7,'Dex':7,'Int':7,'Cre':7,'Mnd':7}
        self.weapon_dmg = 0
        self.weapon_skills = {'Unarmed':float(self.attr['Dex'])}
        self.weapon_skill = float(self.attr['Dex'])
        self.armour = 0
        self.armour_weight = 0
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

    def start_inv(self,i): ##Unstackable items da se davat edno po edno
        if i == 'a':
            shoulder_bag.start_item(1,"healer's satchel")
            ch.inventory[0].color=10
            ch.equip(ch.inventory[0],0)
            cloth_pants.start_item(1)
            ch.equip(ch.inventory[0],13)
            cloth_shirt.start_item(1,"healer's tunic")
            ch.inventory[0].color=10
            ch.equip(ch.inventory[0],3)
            cloth_shoes.start_item(1)
            ch.equip(ch.inventory[0],14)
            cloth_cloak.start_item(1,"healer's cloak")
            ch.inventory[0].color=10
            ch.equip(ch.inventory[0],5)
            tinderbox.start_item(1)
            nature_heal_set.start_item(1)
            bread.start_item(2)
            bottle_water.start_item(2)
        elif i == 'b':
            shoulder_bag.start_item(1)
            ch.equip(ch.inventory[0],0)
            cloth_shoes.start_item(1)
            ch.equip(ch.inventory[0],14)
            cloth_robe.start_item(1,"traveler's robe")
            ch.equip(ch.inventory[0],3)
            light_staff.start_item(1,"traveler's staff")
            ch.equip(ch.inventory[0],7)
            tinderbox.start_item(1)
            bread.start_item(2)
            bottle_water.start_item(2)
        elif i == 'c':
            small_backpack.start_item(1)
            ch.equip(ch.inventory[0],0)
            cloth_pants.start_item(1,'gray pants')
            ch.equip(ch.inventory[0],13)
            wood_vest.start_item(1)
            ch.equip(ch.inventory[0],3)
            wood_boots.start_item(1)
            ch.equip(ch.inventory[0],14)
            random.choice(light_weapons).start_item(1)
            ch.equip(ch.inventory[0],7)
            bow.start_item(1,'elven bow')
            ch.inventory[0].color=10
            wood_arrow.start_item(50)
            tinderbox.start_item(1)
            bread.start_item(2)
            bottle_water.start_item(2)
            gem_amethyst.start_item(5)
            gem_lapis_lazuli.start_item(1)

            small_backpack.start_item(1)
            ch.equip(ch.inventory[0],0)
            cloth_pants.start_item(1)
            ch.equip(ch.inventory[0],13)
            leather_gloves.start_item(1,"miner's gloves")
            ch.equip(ch.inventory[0],9)
            cloth_shirt.start_item(1,"miner's shirt")
            ch.equip(ch.inventory[0],3)
            pick.start_item(1)
            ch.equip(ch.inventory[0],7)
            hammer.start_item(1,"builder's hammer")
            saw.start_item(1)
            pliers.start_item(1)
            tinderbox.start_item(1)
            bread.start_item(2)
            dagger.start_item(1)
            bottle_water.start_item(2)
        elif i == 'd':
            self.start_item(small_backpack,1)
            self.equip(self.inventory[0],0)
            self.start_item(cloth_robe,1)
            self.equip(self.inventory[0],3)
            self.start_item(bottle_water,2)
            self.start_item(bread,2)
            self.start_item(tinderbox,1)
            self.start_item(herb_set,1)
            self.start_item(magic_book,1)
            
            
        elif i == 'e':
            small_backpack.start_item(1)
            ch.equip(ch.inventory[0],0)
            cloth_pants.start_item(1)
            ch.equip(ch.inventory[0],13)
            cloth_shirt.start_item(1)
            ch.equip(ch.inventory[0],3)
            leather_boots.start_item(1,"farmer's boots")
            ch.equip(ch.inventory[0],14)
            shovel.start_item(1)
            ch.equip(ch.inventory[0],16)
            vegetable_seed.start_item(10)
            tinderbox.start_item(1)
            bread.start_item(2)
            bottle_water.start_item(2)
        elif i == 'f':
            small_backpack.start_item(1)
            ch.equip(ch.inventory[0],0)
            cloth_pants.start_item(1,'embroidered pants')
            ch.equip(ch.inventory[0],13)
            cloth_shirt.start_item(1,"merchant's shirt")
            ch.equip(ch.inventory[0],3)
            cloth_belt.start_item(1,"embroidered belt")
            ch.equip(ch.inventory[0],12)
            cloth_shoes.start_item(1,'fine shoes')
            ch.equip(ch.inventory[0],14)
            cloth_cloak.start_item(1,"merchants's cloak")
            ch.equip(ch.inventory[0],5)
            jewel_ring.start_item(1,"silver ring")
            ch.equip(ch.inventory[0],10)
            coins_silver.start_item(10)
            common_spices.start_item(5,'sack of spices')
            tinderbox.start_item(1)
            bread.start_item(2)
            bottle_water.start_item(2)
        elif i == 'g':
            small_backpack.start_item(1)
            ch.equip(ch.inventory[0],0)
            long_sword.start_item(1)
            ch.equip(ch.inventory[0],7)
            leather_pants.start_item(1)
            ch.equip(ch.inventory[0],13)
            leather_vest.start_item(1,"soldier's tunic")
            ch.equip(ch.inventory[0],3)
            leather_boots.start_item(1)
            ch.equip(ch.inventory[0],14)
            tinderbox.start_item(1)
            bread.start_item(2)
            bottle_water.start_item(2)
        elif i == 'h':
            small_backpack.start_item(1)
            ch.equip(ch.inventory[0],0)
            giant_club.start_item(1)
            ch.equip(ch.inventory[0],7)
            cloth_pants.start_item(1,'dirty waist wrap')
            ch.inventory[0].color=7
            ch.equip(ch.inventory[0],13)
            cloth_shoes.start_item(1,'old sandals')
            ch.inventory[0].color=7
            ch.equip(ch.inventory[0],14)
            tinderbox.start_item(1)
            bread.start_item(2)
            bottle_water.start_item(2)
        elif i == 'i':
            small_backpack.start_item(1)
            ch.equip(ch.inventory[0],0)
            random.choice(medium_weapons).start_item(1)
            ch.equip(ch.inventory[0],7)
            chain_pants.start_item(1)
            ch.equip(ch.inventory[0],13)
            chain_vest.start_item(1)
            ch.equip(ch.inventory[0],3)
            leather_boots.start_item(1)
            ch.equip(ch.inventory[0],14)
            leather_cloak.start_item(1)
            ch.equip(ch.inventory[0],5)
            dagger.start_item(1)
            tinderbox.start_item(1)
            bread.start_item(2)
            bottle_water.start_item(2)
        message_message('')


    def start_item(self,item,qty=1,name=''):
        the_item = item.duplicate(qty,name)
        self.inventory.append(the_item)
        if self.equipment['Backpack'] == []:
            self.free_hands -= 1
        else:
            self.backpack -= the_item.weight * qty
        self.tool_tags += the_item.tool_tag
        self.weight += the_item.weight * qty

    def pick_up(self,ground):
        it = 0
        pile = []
        for item in ground:
            if item[:2] == self.xy:
                pile.append(item)
        if len(pile) > 1:
            it = 1
            c.page()
            c.write(' You search through the items on the ground.\n What do you want to pick up?\n\n')
            for i in range(len(pile)):
                print ' '+chr(i+97)+')  ', pile[i][2].name+', %d x %s stones' %(pile[i][2].qty,str(pile[i][2].weight))
                c.text(4,i+3,pile[i][2].tag,pile[i][2].color)
            print '\n You can carry %s more stones.\n Your backpack can take %s more stones.' %(str(self.max_weight - self.weight),
                                                                                                str(self.backpack))
            i1 = ' '
            while 1:
                if msvcrt.kbhit():
                    i1 = msvcrt.getch()
                    break
            c.rectangle((0,0,60,2))
        elif len(pile) == 1:
            i1 = 'a'
            it = 1
        if len(pile) > 0:
            try:
                if pile[ord(i1)-97][2].qty > 1 and self.equipment['Backpack'] != []:
                    message_message('pickup')                    
                    a = ''
                    i = ' '
                    while ord(i) != 13:
                        i = msvcrt.getch()
                        if ord(i) in range(48,58):
                            c.write(i)
                            a += i
                    message_message('')
                    if a =='' or int(a)==0:
                        redraw_screen()
                        return 1
                    a=int(a)
                else:
                    a = 1
            except IndexError:
                redraw_screen()
                return 0
            if a > pile[ord(i1)-97][2].qty:
                a = pile[ord(i1)-97][2].qty
            if self.weight + pile[ord(i1)-97][2].weight * a <= self.max_weight and pile[ord(i1)-97][2].weight * a <= self.backpack:
                pile[ord(i1)-97][2].get_item(a)
                if len(pile) > 1:
                    redraw_screen()
                if a < pile[ord(i1)-97][2].qty:
                    pile[ord(i1)-97][2].qty -= a
                else:
                    ground.remove(pile[ord(i1)-97])
            elif self.weight + pile[ord(i1)-97][2].weight * a > self.max_weight:
                if len(pile) > 1:
                    redraw_screen()
                message_use('cant_carry', pile[ord(i1)-97][2])
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
                            redraw_screen()
                        self.backpack = 0
                    else:
                        if len(pile) > 1:
                            redraw_screen()
                        message_message('drop_first')
                else:
                    if len(pile) > 1:
                        redraw_screen()
                    message_use('cant_fit_in_backpack', pile[ord(i1)-97][2])
            
        if it == 0:
            message_message('no_pickup')

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
            for i in ground_items:
                if i[:2] == self.xy and i[2].id == drop.id and i[2].name == drop.name and i[2].stackable:
                    i[2].qty += drop.qty
                    dropped = 1
            if not dropped:
                ground_items.append([self.xy[0], self.xy[1],drop])
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
        if self.equip_tags[item] in self.equipment[self.equip_tags[item]].type:
            if 'temp_attr' in self.equipment[self.equip_tags[item]].effect:
                for v in self.equipment[self.equip_tags[item]].effect['temp_attr']:
                    used = effect('temp_attr_reverse',v)
            if 'invisibility' in self.equipment[self.equip_tags[item]].effect:
                self.equipment[self.equip_tags[item]].effect['invisibility']-=1
                if self.equipment[self.equip_tags[item]].effect['invisibility']<=0:
                    self.equipment[self.equip_tags[item]].name+=' (depleted)'
                    self.equipment[self.equip_tags[item]].effect.pop('invisibility')
                if 'invisible' in ch.effects:
                    del(self.effects['invisible'])
            if 'winterwalk' in self.equipment[self.equip_tags[item]].effect:
                self.equipment[self.equip_tags[item]].effect['winterwalk']-=1
                if self.equipment[self.equip_tags[item]].effect['winterwalk']<=0:
                    self.equipment[self.equip_tags[item]].name+=' (depleted)'
                    self.equipment[self.equip_tags[item]].effect.pop('winterwalk')
                if 'winterwalk' in ch.effects:
                    del(self.effects['winterwalk'])
            if 'summerwalk' in self.equipment[self.equip_tags[item]].effect:
                self.equipment[self.equip_tags[item]].effect['summerwalk']-=1
                if self.equipment[self.equip_tags[item]].effect['summerwalk']<=0:
                    self.equipment[self.equip_tags[item]].name+=' (depleted)'
                    self.equipment[self.equip_tags[item]].effect.pop('summerwalk')
                if 'summerwalk' in ch.effects:
                    del(self.effects['summerwalk'])
            if 'fairyland' in self.equipment[self.equip_tags[item]].effect:
                self.equipment[self.equip_tags[item]].effect['fairyland']-=1
                if self.equipment[self.equip_tags[item]].effect['fairyland']<=0:
                    self.equipment[self.equip_tags[item]].name+=' (withered)'
                    self.equipment[self.equip_tags[item]].effect.pop('fairyland')
                if 'fairyland' in ch.effects:
                    del(self.effects['fairyland'])
            if 'midnight fears' in self.equipment[self.equip_tags[item]].effect:
                self.equipment[self.equip_tags[item]].effect['midnight fears']-=1
                if self.equipment[self.equip_tags[item]].effect['midnight fears']<=0:
                    self.equipment[self.equip_tags[item]].name+=' (withered)'
                    self.equipment[self.equip_tags[item]].effect.pop('midnight fears')
                if 'midnight fears' in ch.effects:
                    del(self.effects['midnight fears'])
            if 'sun armour' in self.equipment[self.equip_tags[item]].effect:
                self.equipment[self.equip_tags[item]].effect['sun armour']-=1
                if self.equipment[self.equip_tags[item]].effect['sun armour']<=0:
                    self.equipment[self.equip_tags[item]].name+=' (withered)'
                    self.equipment[self.equip_tags[item]].effect.pop('sun armour')
                if 'sun armour' in ch.effects:
                    del(self.effects['sun armour'])
                    if self.sun_armour:
                        self.armour-=ch.sun_armour
                        self.sun_armour=0
        if 'totem' in self.equipment[self.equip_tags[item]].type:
            for cr in game_creatures:
                if cr.name==self.equipment[self.equip_tags[item]].name[:-6]:
                    break
            temps=[]
            for ats in ch.attr:
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
            ground_items.append([self.xy[0], self.xy[1], self.inventory[-1]])
            self.inventory[-1].lose_item()
            self.backpack = 0
        elif not dropped and self.equipment['Backpack'] != []:
            self.backpack -= self.equipment[self.equip_tags[item]].weight*self.equipment[self.equip_tags[item]].qty
        if self.equip_tags[item] in ['Right hand','Left hand'] or 'armour' in self.equipment[self.equip_tags[item]].type:
            self.weapon_dmg -= self.equipment[self.equip_tags[item]].dmg
        if self.equip_tags[item] in ['Right hand','Left hand']:
            self.weapon_weight -= self.equipment[self.equip_tags[item]].weight
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
        if 'temp_attr' in item.effect and self.equip_tags[slot] in item.type:
            for v in item.effect['temp_attr']:
                used = effect('temp_attr',v)
        if 'invisibility' in item.effect and self.equip_tags[slot] in item.type:
            ch.effects['invisible']=10
        if 'winterwalk' in item.effect and self.equip_tags[slot] in item.type:
            ch.effects['winterwalk']=1
        if 'summerwalk' in item.effect and self.equip_tags[slot] in item.type:
            ch.effects['summerwalk']=1
        if 'fairyland' in item.effect and self.equip_tags[slot] in item.type:
            ch.effects['fairyland']=1
        if 'midnight fears' in item.effect and self.equip_tags[slot] in item.type:
            if ch.turn%2400<1200:
                item.effect['midnight fears']=0
            else:
                ch.effects['midnight fears']=1200-ch.turn%1200
            if item.effect['midnight fears']==0:
                item.name+=' (withered)'
                item.effect.pop('midnight fears')
        if 'sun armour' in item.effect and self.equip_tags[slot] in item.type:
            if ch.turn%2400>=1200:
                item.effect['sun armour']=0
            else:
                ch.effects['sun armour']=1200-ch.turn%2400
                ch.sun_armour=0
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
                for i in ground_items:
                    if i[:2] == self.xy and i[2].id == drop.id and i[2].name == drop.name and i[2].stackable:
                        i[2].qty += drop.qty
                        dropped = 1
                if not dropped:
                    ground_items.append([self.xy[0], self.xy[1],drop])
        elif self.equipment['Backpack'] != []:
            self.backpack += item.weight
        if self.equip_tags[slot] in ['Right hand','Left hand'] or 'armour' in item.type:
            self.weapon_dmg += item.dmg

    def find_equipment(self,slot):
        c.page()
        c.pos(0,3)
        found = 0
        items = ''
        for i in self.inventory:
            if self.equip_tags[slot] in ['Right hand','Left hand']:
                print ' '+chr(self.index(i)+97)+')', i.name.capitalize()+', %d x %s stones' %(i.qty,str(i.weight))
                found += 1
                items += chr(self.index(i)+97)
            elif self.equip_tags[slot] in i.type:
                print ' '+chr(self.index(i)+97)+')', i.name.capitalize()+', %d x %s stones' %(i.qty,str(i.weight))
                found += 1
                items += chr(self.index(i)+97)
        if not found:
            print ' You have nothing usefull to equip.'
            i1 = msvcrt.getch()
            return 0
        else:
            c.pos(0,1)
            print ' What do you want to equip?'
            i1 = msvcrt.getch()
            if i1 in items:
                self.equip(self.inventory[ord(i1)-97],slot)
            return 0
            
class Human:
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
            attr_d[a]=int(race_attrs[r][a]*current_place[f]/100.)
        if f=='Nature':
            emo=2
            arm=current_place[f]*3.5
            WD=current_place[f]/60
            if ch.forces['Chaos']:
                if ch.forces['Nature']-ch.forces['Chaos']<current_place['Nature']-current_place['Chaos']:
                    mode='hostile'
            ammo=wood_arrow
        elif f=='Order':
            emo=7
            arm=current_place[f]*2.75
            WD=current_place[f]/40
            if ch.forces['Chaos']:
                if ch.forces['Order']-ch.forces['Chaos']<current_place['Order']-current_place['Chaos']:
                    mode='hostile'
            ammo=wood_bolt
        elif f=='Chaos':
            emo=12
            arm=current_place[f]*2
            WD=current_place[f]/30
            if ch.forces['Order']:
                if ch.forces['Chaos']-ch.forces['Order']<current_place['Chaos']-current_place['Order']:
                    mode='hostile'
            if ch.forces['Nature']:
                if ch.forces['Chaos']-ch.forces['Nature']<current_place['Chaos']-current_place['Nature']:
                    mode='hostile'
            if 'spirit of order3' in ch.tool_tags and random.randint(1,30)>attr_d['Mnd']:
                mode='fearfull'
            ammo=stone
        if ch.possessed:
            mode='wander'
        duplica = Human(xy,self.area,self.path,self.terr_restr,emo,self.fear,r[0].upper(),r,
                        mode,self.id,attr_d,WD,arm,f,r,game_id=g_id)
        duplica.learning=random.random()
        duplica.attr['loot']=[[1310,100,1,4],[r,current_place[f]+current_place['Treasure']*10]]
        duplica.attr['shoot']=ammo
        if rand:
            duplica.random = True
            duplica.appearance=ch.turn
        else:
            duplica.random = False
            duplica.appearance=0
        return duplica

class Animal:
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
        if rand:
            duplica.random = True
            duplica.appearance=ch.turn
        else:
            duplica.random = False
            duplica.appearance=0
        return duplica



################################ INVENTORY       ######################


def put_item(loot,xy=None):
    found_some=0
    for l in loot:
        chance = random.randint(0,10000)
        chance = chance/100.
        if l[0] == 'treasure':
            if treasure_modifier:
                chance = chance/treasure_modifier
            else:
                chance=100.
        elif l[0]== 'ntreasure' or l[0] == 'wtreasure':
            if ch.forces['Chaos']==0 and int(ch.forces['Nature']/10)+treasure_modifier>0:
                chance=chance/((ch.forces['Nature']/10.)+treasure_modifier)
            else:
                chance=100.
        if chance <= l[1]:
            if l[0] == 'treasure':
                creation = random_treasure(l[2],l[3])
                if l[3]==True:
                    current_place['Treasure']-=1
                    treasure_modifier -=1
            elif l[0] == 'ntreasure':
                if ch.forces['Nature']<40:
                    treasure_type=False
                    treasure_size=random.choice(['small','medium'])
                elif ch.forces['Nature']<75:
                    treasure_type=False
                    treasure_size=random.choice(['small','medium','large'])
                elif ch.forces['Nature']>75:
                    treasure_type=random.choice([False,True])
                    treasure_size=random.choice(['small','medium','large'])
                if treasure_type==True:
                    current_place['Treasure']=max(-int(ch.forces['Nature']/10.),
                                                              current_place['Treasure']-1)
                    treasure_modifier = max(-int(ch.forces['Nature']/10.),
                                                        treasure_modifier-1)
                land[xy[1]-1] = land[xy[1]-1][:xy[0]-21]+'.'+land[xy[1]-1][xy[0]-20:]
                creation = random_treasure(treasure_size,treasure_type)
            elif l[0] == 'wtreasure':
                if ch.forces['Nature']<40:
                    treasure_type=False
                    treasure_size=random.choice(['small','medium'])
                elif ch.forces['Nature']<75:
                    treasure_type=False
                    treasure_size=random.choice(['small','medium','large'])
                elif ch.forces['Nature']>75:
                    treasure_type=random.choice([False,True])
                    treasure_size=random.choice(['small','medium','large'])
                if treasure_type==True:
                    current_place['Treasure']=max(-int(ch.forces['Nature']/10.),
                                                              current_place['Treasure']-1)
                    treasure_modifier = max(-int(ch.forces['Nature']/10.),
                                                        treasure_modifier-1)
                land[xy[1]-1] = land[xy[1]-1][:xy[0]-21]+'W'+land[xy[1]-1][xy[0]-20:]
                creation = random_treasure(treasure_size,treasure_type)
            elif l[0] in race_attrs.keys():
                ## Can have main loot and additional items, added separately in the ground_items here
                ## Roll for quality for the main loot
                if l[0]=='ork':
                    quality=random.randint(0,100)<current_place['Chaos']/5+current_place['Treasure']
                    creation = random.choice(medium_weapons+heavy_weapons).duplicate(1)
                    if quality:
                        creation.name='orkish '+creation.name
                        creation.dmg=creation.dmg+1
                    if chance<=l[1]/4:
                        bonus = random.choice(plate_armour).duplicate(1)
                        ground_items.append([xy[0], xy[1], bonus])
                    elif chance<=l[1]/2:
                        bonus = random.choice(chain_armour).duplicate(1)
                        ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='troll':
                    quality=random.randint(0,100)<current_place['Chaos']/5+current_place['Treasure']
                    creation = random.choice(heavy_weapons).duplicate(1)
                    if chance<=l[1]/2:
                        if quality:
                            bonus = random.choice(gems).duplicate(1)
                            ground_items.append([xy[0], xy[1], bonus])
                        else:
                            bonus = random.choice(treasure_money).duplicate(1)
                            ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='spirit of chaos':
                    quality=random.randint(0,100)<current_place['Chaos']/5+current_place['Treasure']
                    creation = random.choice(cloth_armour).duplicate(1)
                    if quality:
                        creation.name='chaos '+creation.name
                        creation.armour=creation.armour+10
                        creation.color=12
                    if chance<=l[1]/4:
                        bonus = random.choice(misc_equipment).duplicate(1)
                        ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='goblin':
                    quality=random.randint(0,100)<current_place['Chaos']/5+current_place['Treasure']
                    creation = random.choice(light_weapons).duplicate(1)
                    if quality:
                        creation.name='wicked '+creation.name
                        creation.dmg=creation.dmg+1
                    if chance<=l[1]/4:
                        bonus = random_treasure('medium')
                        ground_items.append([xy[0], xy[1], bonus])
                    elif chance<=l[1]/2:
                        bonus = random_treasure()
                        ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='kraken':
                    quality=random.randint(0,100)<current_place['Chaos']/5+current_place['Treasure']
                    creation = random.choice(leather_armour).duplicate(1)
                    if quality:
                        creation.name='sealskin '+creation.name.split()[-1]
                        creation.armour=creation.armour+10
                        creation.color=7
                elif l[0]=='imp':
                    quality=random.randint(0,100)<current_place['Chaos']/5+current_place['Treasure']
                    if chance<=l[1]/1:
                        creation = light_staff.duplicate(1)
                        if quality:
                            creation.name='staff of fire'
                            creation.tool_tag.append('fire')
                    else:
                        continue
                elif l[0]=='human':
                    quality=random.randint(0,100)<current_place['Order']/5+current_place['Treasure']
                    creation = random.choice(human_tools).duplicate(1)
                    if chance<=l[1]/2:
                        if quality:
                            bonus = random.choice([medium_backpack,large_backpack]).duplicate(1)
                            ground_items.append([xy[0], xy[1], bonus])
                        else:
                            bonus = random.choice(small_containers).duplicate(1)
                            ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='dwarf':
                    quality=random.randint(0,100)<current_place['Order']/5+current_place['Treasure']
                    creation = random.choice([pick,shovel,pickaxe]).duplicate(1)
                    if quality:
                        creation.name='dwarven '+creation.name
                        creation.tool_tag=['shovel','pick','pickaxe']
                        if 'weapon' not in creation.type:
                            creation.type.append('weapon')
                        creation.dmg=2
                        creation.color=6
                elif l[0]=='spirit of order':
                    quality=random.randint(0,100)<current_place['Order']/5+current_place['Treasure']
                    creation = random.choice(cloth_armour).duplicate(1)
                    if quality:
                        creation.name='order '+creation.name
                        creation.armour=creation.armour+10
                        creation.color=9
                    if chance<=l[1]/4:
                        bonus = random.choice(misc_equipment).duplicate(1)
                        ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='elf':
                    quality=random.randint(0,100)<current_place['Nature']/5+current_place['Treasure']
                    creation = random.choice(leather_armour).duplicate(1)
                    if quality:
                        creation.name='elven '+creation.name
                        creation.armour=creation.armour+15
                        creation.color=15
                    if chance<=l[1]/2:
                        bonus = random.choice(flowers+(flower_seed,)).duplicate(1)
                        ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='gnome':
                    quality=random.randint(0,100)<current_place['Nature']/5+current_place['Treasure']
                    creation = random.choice(gems).duplicate(1)
                    if quality:
                        bonus = color_clay.duplicate(5)
                        ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='spirit of nature':
                    quality=random.randint(0,100)<current_place['Nature']/5+current_place['Treasure']
                    creation = flower_seed.duplicate(1)
                    if quality:
                        bonus = random.choice(gems).duplicate(1)
                        ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='dryad':
                    quality=random.randint(0,100)<current_place['Nature']/5+current_place['Treasure']
                    creation = random.choice(wood_armour).duplicate(1)
                    if quality:
                        creation.name='masterwork '+creation.name
                        creation.armour=creation.armour+15
                        creation.color=2
                    if chance<=l[1]/3:
                        bonus = random.choice(light_weapons).duplicate(1)
                        ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='water elemental':
                    quality=random.randint(0,100)<current_place['Nature']/5+current_place['Treasure']
                    creation = bottle_water.duplicate(1)
                    if quality:
                        creation.name='bottle of pure water'
                        creation.effect={'cook':'water','thirst':60,'energy':60,'container':7}
                elif l[0]=='fairy':
                    quality=random.randint(0,100)<current_place['Nature']/5+current_place['Treasure']
                    creation = random.choice(flowers+herbs).duplicate(1)
                    if chance<=l[1]/3:
                        if quality:
                            bonus = random_treasure('medium')
                            ground_items.append([xy[0], xy[1], bonus])
                        else:
                            bonus = random_treasure()
                            ground_items.append([xy[0], xy[1], bonus])
            elif l[0] == 'forage':
                qty = random.randint(l[2],l[3])
                creation = random.choice(foraged).duplicate(qty)
            elif l[0] == 'gnome_touch':
                creation = random.choice(gems).duplicate(1)
            elif l[0] == 'fairy_flowers':
                creation = rare_flower.duplicate(1)
                if 'fairy2' in ch.tool_tags:
                    if 550<ch.turn%2400<650:
                        creation.name='noon flower'
                        creation.color=190#224
                    elif 1750<ch.turn%2400<1850:
                        creation.name='midnight flower'
                        creation.color=30#208
                    elif current_place['Temperature']<33 and random.random()>current_place['Temperature']/33.:
                        creation.name='frost flower'
                        creation.color=155#144
                    elif current_place['Temperature']>=66 and random.random()<current_place['Temperature']-65/35.:
                        creation.name='desert flower'
                        creation.color=206
            elif 'skin' in str(l[0]):
                qty = random.randint(l[2],l[3])
                creation = skin.duplicate(qty)
                creation.name=l[0]
            else:
                qty = random.randint(l[2],l[3])
                creation = I[l[0]].duplicate(qty)
            if xy:
                found_it=0
                for existing in ground_items:
                    if existing[:2]==xy and existing[2].id==creation.id and existing[2].name==creation.name:
                        existing[2].qty+=creation.qty
                        found_it=1
                        break
                if not found_it:
                    ground_items.append([xy[0], xy[1], creation])
            else:
                return creation
            found_some += 1
    if found_some:
        return 1
    else:
        return 0

def random_treasure_chest(grade):
    a_bag = random.choice(eval('%s_containers' %grade))
    description = ['old ','mouldy ','ancient ','dirty ','worn ']
    bag_name = random.choice(description)+a_bag.name.split()[-1]
    the_bag = a_bag.duplicate(1,bag_name)
    return the_bag

def random_treasure(grade='small',trove=False):
    trove_grades={'small':[1,15],'medium':[2,15,30],'large':[3,15,30,45]}
    if trove:
        if grade == 'small':
            treasure_pile = ['small']
        elif grade == 'medium':
            treasure_pile = ['small','medium']
        elif grade == 'large':
            treasure_pile = ['small','medium','large']
        the_bag = random_treasure_chest(grade)
        for a in range(trove_grades[grade][0]):
            a_treasure = random_treasure(random.choice(treasure_pile))
            the_bag.effect['contains'].append(a_treasure)
            the_bag.weight += a_treasure.weight*a_treasure.qty
        these_money = list(treasure_money)
        for a in trove_grades[grade][1:]:
            some_money = random.choice(these_money)
            these_money.remove(some_money)
            quantity = random.randint(1,a)
            the_money = some_money.duplicate(quantity)
            the_bag.effect['contains'].append(the_money)
            the_bag.weight += the_money.weight*the_money.qty
        return the_bag
    else:
        metal = random.choice(['iron ','copper ','silver ','gold ','steel '])
        ancient = random.random()
        if ancient < 0.05:
            ancient = 1
            metal = 'ancient '+metal
        else:
            ancient = 0
        if random.random()<0.2:
            adding = random.choice(['enameled ','engraved ','notched ',
                                    '%s encrusted ' %random.choice(['diamond','emerald','sapphire','ruby','pearl','amethyst',
                                                                    'topaz','tourmaline','garnet','aquamarine','opal',
                                                                    'turquoise','lapis lazuli'])])
            metal = adding+metal
        selected = random.choice(eval('%s_treasure' %grade))
        new_treasure = selected.duplicate(1,metal+selected.name)
        if ancient:
            new_treasure.type.append('ancient')
        return new_treasure


## Polezno e materialite da tejat pone kolkoto produkta, ako ne i poveche - predpazva ot greshki
## Izkliuchenie sa golemite instrumenti kato nakovalnq i masa za rabota, pesht, mebeli
## {name:[Cre,[tools],product,needs1,needs2,...]}
## podpravki se pravqt ot bilki i cvetq
cook_recipes = {'sweet bread':[1,[],1311,'fruit','bread'],
                'fruit juice':[1,[],1312,'fruit','water'],
                'roasted meat':[1,['fire'],1313,'raw meat'],
                'get seeds':[4,[],1315,'vegetable'],
                'vegetable soup':[6,['fire','cauldron'],1316,'water','vegetable'],
                'boiled egg':[4,['fire','cauldron','water'],1324,'raw egg']}
CR = {}
for i in range(1,21):
    CR[i] = []
for rec in cook_recipes:
    for cre in range(cook_recipes[rec][0],21):
        CR.get(cre).append(rec)


build_recipes = {'wall':[6,['hammer'],'#',{'rock':15,'clay':5},150,
                         {'Order':{'population':1,'force':4.0,'human':2,'dwarf':2,'terrain':0.4},'Nature':{'all':-0.05},'Chaos':{'all':-0.05}}],
                 'pavement':[6,['hammer','chisel'],'p',{'rock':10,'clay':10},150,
                         {'Order':{'population':1,'force':4,'human':2,'dwarf':2,'terrain':0.4},'Nature':{'all':-0.05},'Chaos':{'all':-0.05}}],
                 'wooden fence':[4,['hammer'],'o',{'wood':8,'iron':2},150,
                         {'Order':{'population':1,'force':4,'human':2,'dwarf':2,'terrain':0.4},'Nature':{'all':-0.05},'Chaos':{'all':-0.05}}],
                 'well':[12,['hammer','shovel'],'O',{'rock':25,'clay':25},450,
                         {'Order':{'population':2,'force':4,'human':2,'dwarf':2,'terrain':0.4},'Nature':{'all':-0.01},'Chaos':{'all':-0.1}}],
                 'wooden door':[10,['hammer','saw',],'`',{'wood':5,'iron':5,'rock':5,'clay':5},250,
                         {'Order':{'population':1,'force':4,'human':2,'dwarf':2,'terrain':0.4},'Nature':{'all':-0.05},'Chaos':{'all':-0.05}}],
                 'stone door':[16,['hammer','chisel'],'S',{'iron':10,'rock':10,'clay':10},250,
                         {'Order':{'population':1,'force':4,'human':2,'dwarf':2,'terrain':0.4},'Nature':{'all':-0.05},'Chaos':{'all':-0.05}}],
                 'anvil':[16,['hammer','chisel'],504,{'iron':15,'rock':5,'clay':5},250,
                         {'Order':{'population':1,'force':4,'human':1.5,'dwarf':2.5,'terrain':0.4},'Nature':{'all':-0.05},'Chaos':{'all':-0.05}}],
                 'working table':[13,['hammer','saw'],506,{'iron':5,'wood':20},250,
                         {'Order':{'population':1,'force':4,'human':2.5,'dwarf':1.5,'terrain':0.4},'Nature':{'all':-0.05},'Chaos':{'all':-0.05}}],
                 'forge':[14,['hammer','chisel'],505,{'rock':30,'clay':25,'wood':15},350,
                         {'Order':{'population':1,'force':4,'human':1,'dwarf':3,'terrain':0.4},'Nature':{'all':-0.05},'Chaos':{'all':-0.05}}],
                 'cauldron':[8,['hammer'],503,{'iron':15},250,
                         {'Order':{'population':1,'force':4,'human':2,'dwarf':2,'terrain':0.4},'Nature':{'all':-0.05},'Chaos':{'all':-0.05}}]}
BR = {}
for i in range(1,21):
    BR[i] = []
for rec in build_recipes:
    for cre in range(build_recipes[rec][0],21):
        BR.get(cre).append(rec)

## Up to 9 items in every dictionary
craft_recipes = {'tools':{'pick':[12,['saw','hammer','anvil'],1,{'iron':3,'wood':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.02},'Chaos':{'all':-0.04}}],
                          'shovel':[12,['saw','hammer','anvil'],500,{'iron':2,'wood':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.02},'Chaos':{'all':-0.04}}],
                          'pickaxe':[12,['saw','hammer','anvil'],501,{'iron':3,'wood':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.02},'Chaos':{'all':-0.04}}],
                          'tinderbox':[12,['pliers','hammer','anvil'],502,{'iron':1,'rock':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.02},'Chaos':{'all':-0.04}}],
                          'hammer':[12,['saw','hammer','anvil'],507,{'iron':1,'wood':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.02},'Chaos':{'all':-0.04}}],
                          'saw':[12,['pliers','hammer','anvil'],508,{'iron':1,'wood':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.02},'Chaos':{'all':-0.04}}],
                          'chisel':[12,['saw','hammer','anvil'],509,{'iron':1,'wood':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.02},'Chaos':{'all':-0.04}}],
                          'pliers':[12,['hammer','anvil'],510,{'iron':2},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.02},'Chaos':{'all':-0.04}}],
                          'needle':[12,['pliers','hammer','anvil'],511,{'iron':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.02},'Chaos':{'all':-0.04}}],
                          },
                 'containers':{
                          'talisman pouch':[8,['cutting','needle','work_table'],21,{'leather':1},150,{'Order':{'force':0.03,'human':0.03},'Nature':{'all':-0.01},'Chaos':{'all':-0.02}}],
                          'shoulder bag':[8,['cutting','needle','work_table'],18,{'leather':3},150,{'Order':{'force':0.03,'human':0.03},'Nature':{'all':-0.03},'Chaos':{'all':-0.04}}],
                          'small backpack':[12,['cutting','needle','work_table'],17,{'leather':5},150,{'Order':{'force':0.03,'human':0.03},'Nature':{'all':-0.03},'Chaos':{'all':-0.04}}],
                          'small chest':[14,['hammer','saw','work_table'],19,{'iron':1,'wood':3},150,{'Order':{'force':0.03,'human':0.03},'Nature':{'all':-0.02},'Chaos':{'all':-0.04}}],
                          'wooden box':[10,['hammer','saw','work_table'],20,{'iron':1,'wood':2},150,{'Order':{'force':0.03,'human':0.03},'Nature':{'all':-0.02},'Chaos':{'all':-0.04}}],
                          'ivory box':[16,['hammer','saw','work_table'],22,{'iron':1,'bone':5},150,{'Order':{'force':0.03,'human':0.03},'Nature':{'all':-0.07},'Chaos':{'all':-0.02}}],
                          'medium backpack':[13,['cutting','needle','work_table'],23,{'leather':7},150,{'Order':{'force':0.03,'human':0.03},'Nature':{'all':-0.03},'Chaos':{'all':-0.04}}],
                          'large backpack':[14,['cutting','needle','work_table'],24,{'leather':9},150,{'Order':{'force':0.03,'human':0.03},'Nature':{'all':-0.03},'Chaos':{'all':-0.04}}],
                          'wooden chest':[12,['hammer','saw','work_table'],11,{'iron':1,'wood':5},150,{'Order':{'force':0.03,'human':0.03},'Nature':{'all':-0.02},'Chaos':{'all':-0.04}}]
                          },
                 'weapons':{
                          'long sword':[15,['anvil','hammer','pliers'],12,{'iron':5,'leather':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.04},'Chaos':{'all':-0.01}}],
                          'axe':[15,['anvil','hammer','pliers'],13,{'iron':5,'wood':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.04},'Chaos':{'all':-0.01}}],
                          'club':[8,['cutting','saw','work_table'],15,{'wood':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.04},'Chaos':{'all':-0.01}}],
                          'light staff':[10,['cutting','saw','work_table'],50,{'wood':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.04},'Chaos':{'all':-0.01}}],
                          'dagger':[10,['anvil','hammer','pliers'],51,{'iron':2,'leather':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.04},'Chaos':{'all':-0.01}}],
                          'crossbow':[14,['hammer','saw','work_table'],57,{'wood':2,'iron':1,'leather':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.04},'Chaos':{'all':-0.01}}],
                          'sling':[10,['cutting','needle','work_table'],58,{'leather':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.04},'Chaos':{'all':-0.01}}],
                          'bow':[12,['pliers','work_table'],56,{'wood':3},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.04},'Chaos':{'all':-0.01}}],
                          'short sword':[15,['anvil','hammer','pliers'],55,{'iron':4,'leather':1},150,{'Order':{'force':0.04,'human':0.02,'dwarf':0.02},'Nature':{'all':-0.04},'Chaos':{'all':-0.01}}]
                          },
                 'heavy weapons':{
                          'sceptre':[16,['anvil','hammer','pliers','saw'],52,{'iron':7,'leather':1},150,{'Order':{'force':0.04,'dwarf':0.04},'Nature':{'all':-0.04},'Chaos':{'all':-0.01}}],
                          'heavy hammer':[16,['anvil','hammer','pliers','saw'],53,{'iron':5,'wood':1,'leather':1},150,{'Order':{'force':0.04,'dwarf':0.04},'Nature':{'all':-0.04},'Chaos':{'all':-0.01}}],
                          'giant club':[8,['cutting','saw'],54,{'wood':2,'leather':1},150,{'Order':{'force':0.04,'dwarf':0.04},'Nature':{'all':-0.04},'Chaos':{'all':-0.01}}]
                          },
                 'clothes':{
                          'pants':[12,['cutting','needle','work_table'],100,{'cloth':6},300,{'Order':{'force':0.04,'human':0.04},'Chaos':{'all':-0.03}}],
                          'belt':[12,['cutting','needle','work_table'],101,{'cloth':2},300,{'Order':{'force':0.04,'human':0.04},'Chaos':{'all':-0.03}}],
                          'cloth gloves':[12,['cutting','needle','work_table'],102,{'cloth':2},300,{'Order':{'force':0.04,'human':0.04},'Chaos':{'all':-0.03}}],
                          'cloth cloak':[10,['cutting','needle','work_table'],103,{'cloth':4},300,{'Order':{'force':0.04,'human':0.04},'Chaos':{'all':-0.03}}],
                          'shirt':[12,['cutting','needle','work_table'],104,{'cloth':6},300,{'Order':{'force':0.04,'human':0.04},'Chaos':{'all':-0.03}}],
                          'hat':[12,['cutting','needle','work_table'],105,{'cloth':3},300,{'Order':{'force':0.04,'human':0.04},'Chaos':{'all':-0.03}}],
                          'robe':[10,['cutting','needle','work_table'],106,{'cloth':7},300,{'Order':{'force':0.04,'human':0.04},'Chaos':{'all':-0.03}}],
                          'shoes':[12,['cutting','needle','work_table'],107,{'cloth':2,'wood':1},300,{'Order':{'force':0.04,'human':0.04},'Chaos':{'all':-0.03}}],
                          'flower crown':[2,[],108,{'flowers':15},10,{'Nature':{'force':0.01,'fairy':0.01},'Chaos':{'all':-0.03}}]
                          },
                 'leather armour':{
                          'leather vest':[15,['cutting','needle','work_table'],8,{'leather':7},350,{'Order':{'force':0.04,'human':0.04},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}],
                          'leather pants':[15,['cutting','needle','work_table'],200,{'leather':5},350,{'Order':{'force':0.04,'human':0.04},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}],
                          'leather belt':[14,['cutting','needle','work_table'],201,{'leather':3},350,{'Order':{'force':0.04,'human':0.04},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}],
                          'leather gloves':[14,['cutting','needle','work_table'],202,{'leather':2},350,{'Order':{'force':0.04,'human':0.04},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}],
                          'leather cloak':[13,['cutting','needle','work_table'],203,{'leather':4},350,{'Order':{'force':0.04,'human':0.04},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}],
                          'leather cap':[13,['cutting','needle','work_table'],204,{'leather':2},350,{'Order':{'force':0.04,'human':0.04},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}],
                          'leather boots':[14,['cutting','needle','work_table'],205,{'leather':3,'wood':1},350,{'Order':{'force':0.04,'human':0.04},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}]
                          },
                 'chain armour':{
                          'chain vest':[16,['hammer','pliers','cutting','needle','work_table'],300,{'iron':4,'leather':4},450,{'Order':{'force':0.04,'dwarf':0.04},'Nature':{'all':-0.02},'Chaos':{'all':-0.03}}],
                          'chain pants':[16,['hammer','pliers','cutting','needle','work_table'],301,{'iron':4,'leather':4},450,{'Order':{'force':0.04,'dwarf':0.04},'Nature':{'all':-0.02},'Chaos':{'all':-0.03}}],
                          'chain belt':[14,['hammer','pliers','cutting','needle','work_table'],302,{'leather':1,'iron':2},450,{'Order':{'force':0.04,'dwarf':0.04},'Nature':{'all':-0.02},'Chaos':{'all':-0.03}}],
                          'chain gloves':[14,['hammer','pliers','cutting','needle','work_table'],303,{'iron':2,'leather':2},450,{'Order':{'force':0.04,'dwarf':0.04},'Nature':{'all':-0.02},'Chaos':{'all':-0.03}}],
                          'chain cloak':[14,['hammer','pliers','cutting','needle','work_table'],304,{'iron':4,'leather':3},450,{'Order':{'force':0.04,'dwarf':0.04},'Nature':{'all':-0.02},'Chaos':{'all':-0.03}}],
                          'chain coif':[15,['hammer','pliers','work_table'],305,{'iron':3,'leather':2},450,{'Order':{'force':0.04,'dwarf':0.04},'Nature':{'all':-0.02},'Chaos':{'all':-0.03}}],
                          'chain boots':[15,['hammer','pliers','cutting','needle','work_table'],306,{'iron':3,'leather':3,'wood':1},450,{'Order':{'force':0.04,'dwarf':0.04},'Nature':{'all':-0.02},'Chaos':{'all':-0.03}}]
                          },
                 'plate armour':{
                          'chestplate':[18,['hammer','pliers','cutting','needle','anvil'],400,{'iron':8,'leather':4},550,{'Order':{'force':0.06,'dwarf':0.06},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}],
                          'greaves':[18,['hammer','pliers','cutting','needle','anvil'],401,{'iron':8,'leather':4},550,{'Order':{'force':0.06,'dwarf':0.06},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}],
                          'plate belt':[15,['hammer','pliers','cutting','needle','anvil'],402,{'leather':1,'iron':3},550,{'Order':{'force':0.06,'dwarf':0.06},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}],
                          'plate gloves':[17,['hammer','pliers','cutting','needle','anvil'],403,{'iron':4,'leather':2},550,{'Order':{'force':0.06,'dwarf':0.06},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}],
                          'plate helm':[17,['hammer','pliers','cutting','needle','anvil'],404,{'iron':5,'leather':2},550,{'Order':{'force':0.06,'dwarf':0.06},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}],
                          'plate boots':[16,['hammer','pliers','cutting','needle','anvil'],405,{'iron':6,'leather':3,'wood':1},550,{'Order':{'force':0.06,'dwarf':0.06},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}]
                          },
##                 'jewelery':[14,['anvil','hammer','pliers'],jewels,350,
##                                   {'Order':{'force':0.05,'dwarf':0.05},'Nature':{'all':-0.03},'Chaos':{'all':-0.03}}],
                 'materials & ammunition':{
##                          'cloth':[],
                          'arrow':[5,['cutting','saw','work_table','hammer'],1318,{'iron':1,'wood':1,'feather':2},70,{'Nature':{'force':0.01,'elf':0.01},'Chaos':{'all':-0.01}}],
                          'bolt':[8,['cutting','saw','work_table','hammer'],1319,{'iron':1,'wood':1,'feather':2},70,{'Order':{'force':0.01,'human':0.01},'Chaos':{'all':-0.01}}],
                          'sling stone':[2,['hammer'],1320,{'rock':1},30,{}]
                          }
                 }
CrR = {}
for i in craft_recipes.keys():
    CrR[i]={}
    for i1 in range(1,21):
        CrR[i][i1] = []
for rec in craft_recipes:
    for each in craft_recipes[rec]:
        for cre in range(craft_recipes[rec][each][0],21):
            CrR[rec].get(cre).append(each)

################################ INVENTORY ^^^ #########################
################################ INIT_SCREEN #########################

##def reinitialize():
##    ch = Player([0, 0],attr = {'Str':10, 'End':5,'Dex':10})
##    ch.inventory = []
##    for tag in ch.equip_tags:
##        ch.equipment[tag] = []
##    all_beings = [ch]
##    all_creatures = []
##    hidden = []
    
def draw_items(the_spot=[]):
    for x in ground_items:
        if the_spot and x[:2]!=the_spot:
            continue
        i = 0
        for thing in all_beings:
            if (thing.xy[0] == x[0]) and (thing.xy[1] == x[1]) and thing not in hidden and thing.life>0:
                i += 1
                break
        if i == 0:
            c.scroll((x[0], x[1], x[0]+1, x[1]+1), 1, 1, x[2].color, x[2].tag)

def draw_mode():
    c.rectangle((15,16,20,19))
    mode_mod=['Nature','Order','Chaos'].index(ch.mode)
    c.text(15,mode_mod+16,'***',[10,9,12][mode_mod])

def draw_hud():
    c.rectangle((0,1,20,25))
    c.text(0,1,'%s' %(ch.name),7)
    for tag in ch.equip_tags:
        if ch.equipment[tag] != []:
            c.text(1+ch.equip_tags.index(tag),2,ch.equipment[tag].tag,ch.equipment[tag].color)
        else:
            c.text(1+ch.equip_tags.index(tag),2,' ',7)
    i = 10
    if (ch.life < (ch.max_life*0.7)) and (ch.life > (ch.max_life*0.2)):
        i = 14
    elif (ch.life <= (ch.max_life*0.2)):
        i = 12
    c.text(0,3,'Life %d/%d' %(ch.life,ch.max_life),i)
    try:
        if ch.sun_armour:
            c.text(0,4,'Armour ' + str(ch.armour),9+224)
        else:
            c.text(0,4,'Armour ' + str(ch.armour),9)
    except AttributeError:
        c.text(0,4,'Armour ' + str(ch.armour),9)
    c.text(0,5,'Str  ' + str(ch.attr['Str']),ch.attr_colors['Str'])
    c.text(0,6,'Dex  ' + str(ch.attr['Dex']),ch.attr_colors['Dex'])
    c.text(0,7,'End  ' + str(ch.attr['End']),ch.attr_colors['End'])
    c.text(0,8,'Int  ' + str(ch.attr['Int']),ch.attr_colors['Int'])
    c.text(0,9,'Cre  ' + str(ch.attr['Cre']),ch.attr_colors['Cre'])
    c.text(0,10,'Mnd  ' + str(ch.attr['Mnd']),ch.attr_colors['Mnd'])
    if ch.equipment['Ammunition']:
        c.text(11,4,'Ammo:',4)
        ammo_col=10
        ammo=1
        for am in ch.inventory:
            if am.id==ch.equipment['Ammunition'].id and am.name==ch.equipment['Ammunition'].name:
                ammo+=am.qty
                break
        if ammo<5:
            ammo_col=12
        elif ammo<11:
            ammo_col=14
        c.text(17,4,str(ammo),ammo_col)
    if ch.ride:
        c.text(11,6,'Mount:',7)
        if ch.ride[0].food<25:
            c.text(11,7,'Hungry!',12)
        elif ch.ride[0].food<75:
            c.text(11,7,'Normal',7)
        else:
            c.text(11,7,'Fresh',10)
    c.text(0,11,'Wg %.2f/%d' %(ch.weight, ch.max_weight),7)
    if ch.equipment['Backpack']:
        c.text(0,12,'Bag %.2f/%.2f' %(ch.equipment['Backpack'].weight*6-ch.backpack,ch.equipment['Backpack'].weight*6),7)
    else:
        c.text(0,12,'Bag --/--',7)
    if 'dwarf1' in ch.tool_tags:
        c.text(0,13,'Treasure feeling ' + str(current_place['Treasure']),13)
    daytime=ch.turn%2400
    day_tag=''
    day_color=7
    steps=[200,400,550,650,800,1000,1200,1450,1750,1850,2150,2400]
    step_names=['Early morning','Morning','Midday','High noon','Afternoon','Early evening','Evening',
                'After dark','Deep night','Midnight','After midnight','Before dawn']
    step_colors=[13,11,14,12,14,11,13,9,8,5,8,9]
    for s in range(len(steps)):
        if daytime<steps[s]:
            day_tag=step_names[s]
            day_color=step_colors[s]
            if steps[s]==200:
                passed=daytime/20
            else:
                passed=(daytime-steps[s-1])/((steps[s]-steps[s-1])/10)
            break
    c.text((20-len(day_tag))/2+1,14,day_tag,day_color)
    c.text(4,15,'['+'*'*passed+'-'*(10-passed)+']',day_color)
    c.text(0,16,'Nature %6.2f' %(ch.forces['Nature'])+'%',10)
    c.text(0,17,'Order  %6.2f' %(ch.forces['Order'])+'%',9)
    c.text(0,18,'Chaos  %6.2f' %(ch.forces['Chaos'])+'%',12)
##    try:
##        c.text(0,23,'%d' %(ch.hunger),7)
##    except:
##        pass
    draw_mode()
    
    c.rectangle((20,24,79,25))
    if current_place['Temperature']<16:
        climate=" It's very cold here!"
    elif current_place['Temperature']<33:
        climate=" It's cold here."
    elif current_place['Temperature']<66:
        climate=" The weather is nice and warm."
    elif current_place['Temperature']<85:
        climate=" The air is hot and dry."
    elif current_place['Temperature']>=85:
        climate=" You can barely breathe from the heat!"
    c.text(23,24,place_descriptions[current_area]+climate,7)

    if 'invisible' in ch.effects:
        c.text(0,19,'Invisible',7)
    if 'stealthy' in ch.tool_tags:
        c.text(10,19,'Stealth',7)
    if ch.emotion == 2:
        c.text(0,20,'Tired',7)
    if ch.sit == True:
        c.text(0,23,'Sitting',7)
    colour = 7
    if ch.hunger > 60:
        sign = 'Hungry'
        if 80 < ch.hunger < 100:
            colour = 12
            sign = 'HUNGRY'
        if ch.hunger == 100:
            if ch.turn%2 == 1:
                colour = 14
            else:
                colour = 12
            sign = 'STARVING!'
        c.text(0,21,sign,colour)
    colour = 7
    if ch.thirst > 60:
        sign = 'Thirsty'
        if 80 < ch.thirst < 100:
            colour = 12
            sign = 'THIRSTY'
        if ch.thirst == 100:
            if ch.turn%2 == 0:
                colour = 14
            else:
                colour = 12
            sign = 'DYING OF THIRST!'
        c.text(0,22,sign,colour)
    
def redraw_screen():
    c.page()
    for x in range(1,24):
        c.pos(21, x)
        for y in range(21,79):
            c.scroll((y,x,y+1,x+1), 1, 1, T[land[x-1][y-21]].colour, T[land[x-1][y-21]].char)
    for x in ch.land_effects.keys():
        if ch.land_effects[x][1]=='on_fire':
            fxy=ch.land_effects[x][3]
            if ch.land_effects[x][0]==0:
                c.scroll((fxy[0],fxy[1],fxy[0]+1,fxy[1]+1), 1, 1, T[land[fxy[1]-1][fxy[0]-21]].colour, T[land[fxy[1]-1][fxy[0]-21]].char)
                continue
            fire_color=random.choice([4,12,14])
            c.scroll((fxy[0],fxy[1],fxy[0]+1,fxy[1]+1), 1, 1, fire_color*16+ch.land_effects[x][5],ch.land_effects[x][4])
    draw_hud()
    draw_items()
    for creature in all_creatures:
        if creature not in hidden and (clear_los(direct_path(ch.xy,creature.xy)) or (current_place['Nature']>=33 and current_place['Temperature']>=33 and 'elf2' in ch.tool_tags)):
            draw_move(creature, creature.xy[0], creature.xy[1])
    
    if current_area == 'world':
        for place in world_places:
            if place != 'world' and place in ch.known_areas and str(world_places[place]) in top_world_places:
                x = world_places[place][0]
                y = world_places[place][1]
                c.scroll((x, y, x+1, y+1), 1, 1, 11, '?')
    draw_move(ch, ch.xy[0], ch.xy[1])
    c.pos(*ch.xy)

def draw_move(ch, x, y):
##    try:
    c.scroll((x, y, x+1, y+1), 1, 1, T[land[y-1][x-21]].colour, T[land[y-1][x-21]].char)
##    except:
##        print x, y, land[y-1][x-21]
    if current_area == 'world':
        if str([x, y]) in top_world_places and [x,y] in [world_places[a] for a in ch.known_areas]:
            c.scroll((x, y, x+1, y+1), 1, 1, 11, '?')
    c.pos(*ch.xy)
    if ch.tag=='@' and ch.possessed:
        c.scroll((ch.xy[0], ch.xy[1], ch.xy[0]+1, ch.xy[1]+1), 1, 1, ch.possessed[0].emotion, ch.possessed[0].tag)
    else:
        c.scroll((ch.xy[0], ch.xy[1], ch.xy[0]+1, ch.xy[1]+1), 1, 1, ch.emotion, ch.tag)

def hide(ch):
    x = ch.xy[0]
    y = ch.xy[1]
    c.scroll((x, y, x+1, y+1), 1, 1, T[land[y-1][x-21]].colour, T[land[y-1][x-21]].char)

def build_terr(new_ter):
    ok = 0
    if ch.hunger>79 or ch.thirst>79:
        return -4
    while 1:
        if (ch.energy < build_recipes[new_ter][4]) and (ch.work == 0):
            if ch.max_energy < build_recipes[new_ter][4]:
                return -2
            else:
                return -1
        elif ok!=1:
            ch.work = build_recipes[new_ter][4]
            ok=1
        hostiles=game_time('0')
        if hostiles==2:
            ch.work=0
            return -3
        if ch.work == 0:
            effect('force',build_recipes[new_ter][5])
            if 'str' in str(type(build_recipes[new_ter][2])):
                land[ch.xy[1]-1] = land[ch.xy[1]-1][:ch.xy[0]-21] + build_recipes[new_ter][2] + land[ch.xy[1]-1][ch.xy[0]-20:]
            elif 'int' in str(type(build_recipes[new_ter][2])):
                creation=I[build_recipes[new_ter][2]].duplicate()
                ground_items.append([ch.xy[0],ch.xy[1],creation])
            return 1
        elif ch.hunger>79 or ch.thirst>79:
            ch.work = 0
            return -4

def build(ground_items):
    mats={}
    for i in ground_items:
        if i[:2]==ch.xy:
            if 'buildmat' in i[2].type:
                if i[2].effect['build'] in mats:
                    mats[i[2].effect['build']]+=i[2].qty
                else:
                    mats[i[2].effect['build']]=i[2].qty
            else:
                message_message('clear_build_site')
                return ground_items
    mat_keys=mats.keys()
    selected_recipes={}
    the_build=''
    for r in BR[ch.attr['Cre']]:
        all_in=1
        needed_mats=build_recipes[r][3]
        needed_tools=[]
        for t in build_recipes[r][1]:
            if t not in ch.tool_tags[:]:
                needed_tools.append(t)
        if mats:
            for t in needed_mats:
                if not (t in mats and mats[t]==needed_mats[t]):
                    all_in=0
                    break
        else:
            all_in=0
        if all_in:
            selected_recipes[r]=needed_tools[:]
            if not needed_tools:
                the_build=r
        else:
            selected_recipes[r]=needed_tools[:]+''.join(['%s ' %(x) *needed_mats[x] for x in needed_mats]).strip().split()
    i=''
    while i!=' ' and i!='B':
        c.page()
        c.pos(1,0)
        c.write('''These are the structures you can build. YOU MUST PUT ALL THE NEEDED MATERIALS
 ON THE GROUND AT THE SPOT YOU WANT TO BUILD ON, AND HAVE THE TOOLS IN YOUR
 INVENTORY! ('B' to build, SPACE to exit)

 You have:                  You can build:\n''')
        for i1 in range(len(mat_keys)):
            print '   %s x %d' %(mat_keys[i1].capitalize(),mats[mat_keys[i1]])
        if selected_recipes:
            line=0
            for r in selected_recipes:
                c.text(28,line+5,'%s' %(r.capitalize()))
                if selected_recipes[r]:
                    c.text(29,line+6,'Needs: %s' %(','.join(['%d %s' %(selected_recipes[r].count(x),x.capitalize()) for x in set(selected_recipes[r])])))
                else:
                    c.text(29,line+6,"Press 'B' to build!",10)
                line+=2
        i=msvcrt.getch()
    if the_build and i=='B':
        redraw_screen()
        building=build_terr(the_build)
        if building == 1:
            c.pos(1,0)
            c.write('You build a %s.' %(the_build))
            new_ground_items=[]
            for m in ground_items:
                if m[:2]!=ch.xy or (build_recipes[the_build][2] in I and\
                   m[2].id==I[build_recipes[the_build][2]].id):
                    new_ground_items.append(m)
            return new_ground_items
        elif building == -2:
            message_emotion('not_tough')
        elif building == -1:
            message_emotion('tired')
        elif building == -4:
            message_emotion('exhausted')
        elif building == -3:
            message_emotion('hostiles')
        return ground_items
    else:
        redraw_screen()
        return ground_items

def craft_item(item_type,new_item):
    the_name=new_item
    if new_item.split()[0] in ['copper','silver','gold']:
        new_item=' '.join(new_item.split()[1:])
    ok = 0
    if ch.hunger>79 or ch.thirst>79:
        return -4,0
    while 1:
        if (ch.energy < craft_recipes[item_type][new_item][4]) and (ch.work == 0):
            if ch.max_energy < craft_recipes[item_type][new_item][4]:
                return -2,0
            else:
                return -1,0
        elif ok!=1:
            ch.work = craft_recipes[item_type][new_item][4]
            ok=1
        hostiles=game_time('0')
        if hostiles==2:
            ch.work=0
            return -3,0
        if ch.work == 0:
            effect('force',craft_recipes[item_type][new_item][5])
            creation=I[craft_recipes[item_type][new_item][2]].duplicate(name=the_name)
            if 'dwarf2' in ch.tool_tags:
                creation=add_gems(creation)
            elif 'fairy1' in ch.tool_tags and creation.name=='flower crown':
                creation=add_flowers(creation)
            ground_items.append([ch.xy[0],ch.xy[1],creation])
            return 1,creation.name
        elif ch.hunger>79 or ch.thirst>79:
            ch.work = 0
            return -4,0

def add_gems(creation):
    gems=[]
    for x in ch.inventory:
        if 'gem' in x.type:
            gems.append(x)
    if gems:
        c.page()
        c.write('''
  You can imbue the item with the power of gems you posses:
  (choose the gem you'd like to use or SPACE to continue)\n\n''')
        for x in range(len(gems)):
            print 
            c.write('  %s) %-12s (gives %d %s)' %(chr(97+x),gems[x].name.capitalize(),gems[x].effect['talisman']['temp_attr'][0][1],
                                                gems[x].effect['talisman']['temp_attr'][0][0]))
        i=msvcrt.getch()
        if ord(i)-97 in range(len(gems)):
            x=ord(i)-97
            creation.name=gems[x].name+' '+creation.name
            creation.effect=gems[x].effect['talisman'].copy()
            creation.color=gems[x].color
            gems[x].lose_item(1)
        return creation
    else:
        return creation
    
def add_flowers(creation):
    found=0
    flowers={}
    fltypes={'rare flower':'1','noon flower':'2','midnight flower':'3','frost flower':'4','desert flower':'5'}
    for fls in ch.inventory:
        if 'rare flower' in fls.type:
            flowers[fltypes[fls.name]]=fls
            found=1
    if found:
        possible={}
        c.page()
        c.write('''
  You can use the rare flowers you found to make the crown special!
  (choose the effect you'd like to use)

  ''')
        offset=4
        if '1' in flowers:
            possible['1']=[{'invisibility':3},'invisibility']
            c.write('''1) Short invisibility x 3 (starts when you put the crown on)\n  ''')
            c.text(5,offset,'Short invisibility',flowers['1'].color)
            offset+=1
        if 'fairy2' in ch.tool_tags:
            if '2' in flowers:
                possible['2']=[{'sun armour':1},'sunlit']
                c.write("""2) Sunlit crown (use ONLY AT DAY! Lasts till sunset or until you
  take it off. Envelops you in shining light that may absorb the power of
  enemy strikes. Clothes interfere with the power, and it is strongest at
  noon.)\n  """)
                c.text(5,offset,'Sunlit crown',flowers['2'].color)
                offset+=4
            if '3' in flowers:
                possible['3']=[{'midnight fears':1},'midnight']
                c.write("""3) Midnight crown (use ONLY AT NIGHT! Lasts till sunrise or
  until you take it off. Makes enemies that don't see you fearfull as time
  passes. Effect is strongest around midnight.)\n  """)
                c.text(5,offset,'Midnight crown',flowers['3'].color)
                offset+=3
            if '4' in flowers:
                possible['4']=[{'winterwalk':1},'ring of winter']
                c.write("""4) Ring of winter (allows you to travel in the coldest parts of the
  world without any trouble. Ice and snow will not slow you down any more. The
  ring can only exist in COLD places, unless coupled with a ring of summer.)\n  """)
                c.text(5,offset,'Ring of winter',flowers['4'].color)
                offset+=3
            if '5' in flowers:
                possible['5']=[{'summerwalk':1},'ring of summer']
                c.write("""5) Ring of summer (allows you to travel in the hottest parts of the
  world without any trouble. Sands will not slow you down any more. The
  ring can only exist in HOT places, unless coupled with a ring of winter.)\n  """)
                c.text(5,offset,'Ring of summer',flowers['5'].color)
                offset+=3
        if 'fairy3' in ch.tool_tags:
            c.write("""6) Dress of the fae. The most beautifull expression of a fairy's soul,
  this gown (or robe, when made for male fairies) makes all faerie magicks
  linger for eternity. In addition, all who strike at the fairy suffer greatly
  as their minds witness the destruction of such beauty. (Needs 50 wild
  flowers and one of each rare flower (rare, noon, midnight, frost and desert)
  in your bag!)\n""")
            c.text(5,offset,'Dress of the fae',12)
            c.text(64,offset+3,'50',12)
            if len(flowers)==5:
                possible['6']=[{'fairyland':1},'dress of the fae']
        i=msvcrt.getch()
        if i in possible:
            if i!='6':
                creation.color=flowers[i].color
                flowers[i].lose_item(1)
            else:
                found=0
                for i1 in ch.inventory:
                    if i1.name=='wild flowers' and i1.qty>=50:
                        found=1
                        i1.lose_item(50)
                        creation.color=12
                        for each in flowers:
                            flowers[each].lose_item(1)
                if not found:
                    message_message('flower_dress')
                    return creation
            if i in ['4','5']:
                creation.name=possible[i][1]
                creation.type=[['Right ring','Left ring'][['4','5'].index(i)]]
            elif i=='6':
                creation.name=possible[i][1]
                creation.type=['Chest']
            else:
                creation.name=possible[i][1]+' '+creation.name
            creation.effect=possible[i][0]
        return creation
    else:
        return creation

def create(ground_items):
    metal_chosen='a'
    if 'dwarf3' in ch.tool_tags:
        c.page()
        c.write('''\n  As a dwarf you now can choose the kind of metal you want to use for
  your items. If the chosen metal is not available at your location you will
  not be able to craft anything. Various metals may give different properties
  to the created items...

   a) Iron
   b) Copper
   c) Silver
   d) Gold''')
        metal_chosen=msvcrt.getch()
    if -1<ord(metal_chosen)-97<4:
        metal_chosen=['iron','copper','silver','gold'][ord(metal_chosen)-97]
    else:
        metal_chosen='iron'
    mats={}
    ground_tools=[]
    for i in ground_items:
        if i[:2]==ch.xy:
            if 'craftmat' in i[2].type:
                if i[2].effect['craft'] in mats:
                    mats[i[2].effect['craft']]+=i[2].qty
                else:
                    mats[i[2].effect['craft']]=i[2].qty
            if 'tool' in i[2].type:
                ground_tools+=i[2].tool_tag
    mat_keys=mats.keys()
    selected_recipes={}
    tools_needed={}
    the_build=''
    for recipe_group in CrR:
        for r in CrR[recipe_group][ch.attr['Cre']]:
            if recipe_group not in selected_recipes:
                selected_recipes[recipe_group]={}
                tools_needed[recipe_group]=[]
            all_in=1
            needed_mats=craft_recipes[recipe_group][r][3].copy()
            if metal_chosen!='iron' and 'iron' in needed_mats:
                needed_mats[metal_chosen]=needed_mats['iron']
                del(needed_mats['iron'])
            needed_tools=[]
            for t in craft_recipes[recipe_group][r][1]:
                if t not in tools_needed[recipe_group]:
                    tools_needed[recipe_group].append(t)
                if t not in ch.tool_tags[:] and t not in ground_tools:
                    needed_tools.append(t)
            if mats:
                for t in mats:
                    if t in needed_mats and mats[t]>=needed_mats[t]:
                        out=needed_mats.pop(t)
                    elif t in needed_mats:
                        needed_mats[t]-=mats[t]
            if needed_mats:
                all_in=0
            if metal_chosen!='iron':
                if all_in:
                    selected_recipes[recipe_group][metal_chosen+' '+r]=needed_tools[:]
                else:
                    selected_recipes[recipe_group][metal_chosen+' '+r]=''.join(['%s ' %(x) *needed_mats[x] for x in needed_mats]).strip().split()
            else:
                if all_in:
                    selected_recipes[recipe_group][r]=needed_tools[:]
                else:
                    selected_recipes[recipe_group][r]=''.join(['%s ' %(x) *needed_mats[x] for x in needed_mats]).strip().split()
    i=''
    the_keys=selected_recipes.keys()
    while i!=' ':# and not '0'<i<=str(len(the_keys)):
        c.page()
        c.pos(1,0)
        c.write('''These are the items you can craft. YOU MUST PUT ALL THE NEEDED MATERIALS
 ON THE GROUND AT THE SPOT YOU WANT TO CRAFT ON, AND HAVE THE TOOLS IN YOUR
 INVENTORY (not the forge and anvil...)! (1-9 to craft, SPACE to exit)

 You have:                  You can build:\n''')
        for i1 in range(len(mat_keys)):
            print '   %s x %d' %(mat_keys[i1].capitalize(),mats[mat_keys[i1]])
        if selected_recipes:
            line=0
            for r in the_keys:
                c.text(28,line+5,'%d) %s' %(line/2+1,r.capitalize()))
                line+=2
        i=msvcrt.getch()
        try:
            craft_group=the_keys[int(i)-1]
            break
        except:
            redraw_screen()
            return ground_items
    i=''
    the_keys=selected_recipes[craft_group].keys()
    while i!=' ':
        c.page()
        c.pos(1,0)
        c.write('''These are the items you can craft. YOU MUST PUT ALL THE NEEDED MATERIALS
 ON THE GROUND AT THE SPOT YOU WANT TO CRAFT ON, AND HAVE THE TOOLS IN YOUR
 INVENTORY (not the forge and anvil...)! (1-9 to craft, SPACE to exit)
 May need:%s
 You have:                  You can build:\n''' %(', '.join(tools_needed[craft_group])))
        for i1 in range(len(mat_keys)):
            print '   %s x %d' %(mat_keys[i1].capitalize(),mats[mat_keys[i1]])
        line=0
        for r in the_keys:
            c.text(28,line+5,'%d) %s' %(line/2+1,r.capitalize()))
            if selected_recipes[craft_group][r]:
                c.text(29,line+6,'%s' %(','.join(['%d %s' %(selected_recipes[craft_group][r].count(x),x.capitalize()) for x in set(selected_recipes[craft_group][r])])),12)
            else:
                c.text(29,line+6,"Press %d to build!" %(line/2+1),10)
            line+=2
        i=msvcrt.getch()
        if '0'<i<='9' and int(i)<=len(the_keys):
                break
    if '0'<i<='9' and not selected_recipes[craft_group][the_keys[int(i)-1]]:
        building,build_name=craft_item(craft_group,the_keys[int(i)-1])
        redraw_screen()
        if building == 1:
            c.pos(1,0)
            c.write('You craft a %s.' %(build_name))
            if the_keys[int(i)-1].split()[0] in ['copper','silver','gold']:
                used_mats=craft_recipes[craft_group][' '.join(the_keys[int(i)-1].split()[1:])][3].copy()
            else:
                used_mats=craft_recipes[craft_group][the_keys[int(i)-1]][3].copy()
            if metal_chosen!='iron' and 'iron' in used_mats:
                used_mats[metal_chosen]=used_mats['iron']
                del(used_mats['iron'])
            new_ground_items=[]
            for m in ground_items:
                if m[:2]==ch.xy and 'craftmat' in m[2].type and m[2].effect['craft'] in used_mats and used_mats[m[2].effect['craft']]>0:
                    if m[2].qty>used_mats[m[2].effect['craft']]:
                        m[2].qty-=used_mats[m[2].effect['craft']]
                        new_ground_items.append(m)
                    else:
                        used_mats[m[2].effect['craft']]=used_mats[m[2].effect['craft']]-m[2].qty
                else:
                    new_ground_items.append(m)
            return new_ground_items
        elif building == -2:
            message_emotion('not_tough')
        elif building == -1:
            message_emotion('tired')
        elif building == -4:
            message_emotion('exhausted')
        elif building == -3:
            message_emotion('hostiles')
        return ground_items
    else:
        redraw_screen()
        return ground_items

def dryad_grow():
    if T[land[ch.xy[1]-1][ch.xy[0]-21]].id == 'T':
        c.page()
        si=[None,None]
        i=''
        i1=''
        while i!=' ':
            c.pos(0,0)
            c.write('''\n  You touch the tree next to you and feel it shudder. Under your quiet
  chanting a new branch grows out of the trunk and forms into the shape
  of your choosing (SPACE to exit):

  1) Weapons and ammunition
  2) Living wood armour''')
            i=msvcrt.getch()
            if i in ['1','2']:
                si[0]=int(i)-1
                break
            elif i==' ':
                i1=' '
        while i1!=' ':
            c.page()
            if i=='1':
                c.pos(0,0)
                c.write('''\n  You touch the tree next to you and feel it shudder. Under your quiet
  chanting a new branch grows out of the trunk and forms into the shape
  of your choosing (SPACE to exit):

  1) A totem staff
  2) A dryad bow
  3) 20 living wood arrows''')
                i1=msvcrt.getch()
                if i1 in ['1','2','3']:
                    si[1]=int(i1)-1
                    break
            elif i=='2':
                c.pos(0,0)
                c.write('''\n  You touch the tree next to you and feel it shudder. Under your quiet
  chanting a new branch grows out of the trunk and forms into the shape
  of your choosing (SPACE to exit):

  1) Cloak of leaves
  2) Living wood boots
  3) Living wood chestplate
  4) Living wood pants
  5) Living wood gloves
  6) Living wood helm
  7) Living wood belt''')
                i1=msvcrt.getch()
                if int(i1) in range(1,8):
                    si[1]=int(i1)-1
                    break
        if si[0]!=None and si[1]!=None:
            c.write('''\n\n  The bark breaks open and you take the item. You will need to repay
  Nature for this gift and restore your standing as a dryad.''')
            msvcrt.getch()
            make_list=[[50,56,1318],[604,606,600,601,603,605,602]]
            if si==[0,2]:
                amount=20
            else:
                amount=1
            weap_names=['totem staff','dryad bow','living wood arrow']
            if si[0]==0:
                grown_item=I[make_list[si[0]][si[1]]].duplicate(amount,weap_names[si[1]])
            else:
                grown_item=I[make_list[si[0]][si[1]]].duplicate(amount)
            ground_items.append([ch.xy[0],ch.xy[1],grown_item])
            effect('force',{'Nature':{'dryad':-1.}})
    else:
        message_message('dryad_song')
        msvcrt.getch()
        if ch.energy>100:
            effect('dryad song',1)
            ch.energy=0
    redraw_screen()

def degrade_terr(old_ter, xy, c_x, c_y):
    ok = 0
    if ((ch.hunger > 79) or (ch.thirst > 79)) and T[old_ter].degr_mess[ch.mode]!='forage':
        return -4
    while 1:
        if (ch.energy < T[old_ter].tire[ch.mode]) and (ch.work == 0):
            if ch.max_energy < T[old_ter].tire[ch.mode]:
                return -2
            else:
                return -1
        elif ok != 1:
            ch.work = T[old_ter].tire[ch.mode]
        for i in T[old_ter].degrade_tool[ch.mode]:
            if i in ch.tool_tags:
                ok = 1
                if 'dryad2' in ch.tool_tags and T[old_ter].id==':' and ch.mode=='Nature':
                    message_message('dryad_heal_tree')
                else:
                    message_message(T[old_ter].degr_mess[ch.mode])
                hostiles=game_time('0')
                if hostiles==2:
                    ch.work=0
                    return -3
                if ch.work == 0:
                    if T[land[xy[1]-1][xy[0]-21]].degradable:
                        if 'dryad2' in ch.tool_tags and T[old_ter].id==':' and ch.mode=='Nature':
                            land[xy[1]-1] = land[xy[1]-1][:xy[0]-21] + 'T' + land[xy[1]-1][xy[0]-20:]
                        else:
                            land[xy[1]-1] = land[xy[1]-1][:xy[0]-21] + T[old_ter].degrade_to[ch.mode] + land[xy[1]-1][xy[0]-20:]
                    found_loot=0
                    if xy not in ch.worked_places[ch.mode] or T[old_ter].id=='m':
                        effect('force',T[old_ter].force_effects[ch.mode],xy,T[old_ter].char)
                        if 'dryad2' in ch.tool_tags and T[old_ter].id==':' and ch.mode=='Nature':
                            effect('force',T[old_ter].force_effects[ch.mode],xy,T[old_ter].char)
                        ch.worked_places[ch.mode].append(xy[:])
                        if 'gnome2' in ch.tool_tags and T[old_ter].id in ['%','n','m'] and ch.mode=='Nature':
                            found_loot+=put_item([['gnome_touch',5,1,1]], xy)
                            if found_loot:
                                message_message('gnome_touch')
                        elif 'fairy1' in ch.tool_tags and T[old_ter].id in ['g','O'] and ch.mode=='Nature':
                            found_loot+=put_item([['fairy_flowers',5,1,1]], xy)
                            if found_loot:
                                message_message('fairy_flowers')
                        if T[land[xy[1]-1][xy[0]-21]].pass_through:
                            found_loot+=put_item(T[old_ter].loot[ch.mode], xy)
                        else:
                            found_loot+=put_item(T[old_ter].loot[ch.mode], [c_x,c_y])
                    if not found_loot:
                        c.scroll((xy[0],xy[1],xy[0]+1,xy[1]+1), 1, 1, T[land[xy[1]-1][xy[0]-21]].colour, T[land[xy[1]-1][xy[0]-21]].char)
                    draw_items(xy)
                    return 1
                elif ((ch.hunger > 79) or (ch.thirst > 79)) and T[old_ter].degr_mess[ch.mode]!='forage':
                    ch.work = 0
                    return -4
        if ok == 0:
            ch.work = 0
            return 0

def work(i):
    message_message('')
    try:
        md = {'1':[-1,1], '2':[0,1], '3':[1,1], '4':[-1,0], '5':[0,0],
              '6':[1,0], '7':[-1,-1], '8':[0,-1], '9':[1,-1], '0':[0,0]}
        xy = ch.xy[:]
        x = xy[0]
        y = xy[1]
        for a in range(2):
                xy[a] = xy[a] + md[i][a]
        if T[land[xy[1]-1][xy[0]-21]].workable:
            d = degrade_terr(land[xy[1]-1][xy[0]-21], xy, x, y)
            if d == 1:
                xy[0] = x
                xy[1] = y
                draw_move(ch, x, y)
            elif d == -2:
                message_emotion('not_tough')
                xy[0] = x
                xy[1] = y
            elif d == -1:
                message_emotion('tired')
                xy[0] = x
                xy[1] = y
            elif d == -4:
                message_emotion('exhausted')
                xy[0] = x
                xy[1] = y
            elif d == -3:
                message_emotion('hostiles')
                xy[0] = x
                xy[1] = y
            else:
                message_tool_msg('no_tool',T[land[xy[1]-1][xy[0]-21]].degrade_tool[ch.mode])
                xy[0] = x
                xy[1] = y
        else:
            message_message('cant_work')
            xy[0] = x
            xy[1] = y
    except KeyError:
        message_message('direction')

def draw_inv(put_in=None, container=None):
    c.page()
    c.pos(0,0)
    if put_in:
        c.write('\n What do you want to put in the container?\n\n\n')
    else:
        c.write('\n You open your backpack:\n (e)view equipment (q)eat/drink (d)drop item (u)use item\n\n')
    for i in range(len(ch.inventory)):
        print ' '+chr(i+97)+')  ', ch.inventory[i].name.capitalize()+', %d x %s stones' %(ch.inventory[i].qty,
                                                                                  str(ch.inventory[i].weight))
        c.text(4,i+4,ch.inventory[i].tag,ch.inventory[i].color)
    print '\n Carrying: %s/%s. You can fit %s more in your bag.' %(str(ch.weight), str(ch.max_weight),
                                                                   str(ch.backpack))
    i1 = ' '
    i1 = msvcrt.getch()
    try:
        if put_in and ch.inventory[ord(i1)-97] != container:
            space = I[container.id].weight*7 - container.weight
            drop = ch.inventory[ord(i1)-97].drop_item('',space)
            if not drop:
                message_message('cant_fit_in_container')
                msvcrt.getch()
            return drop
        elif put_in and ch.inventory[ord(i1)-97] == container:
            message_message('cant_fit_container')
            msvcrt.getch()
            return None
    except IndexError:
        return None
    if i1 == 'q':
        c.rectangle((0,0,79,1))
        c.pos(0,0)
        c.write(' What do you want to eat or drink?')
        while 1:
            if msvcrt.kbhit():
                eat = msvcrt.getch()
                break
        c.rectangle((0,0,79,1))
        try:
            ch.inventory[ord(eat)-97].eat()
        except IndexError:
            pass
        draw_inv()
    if i1 == 'd':
        c.rectangle((0,0,79,1))
        c.pos(0,0)
        c.write(' Which item do you want to drop?')
        while 1:
            if msvcrt.kbhit():
                dr = msvcrt.getch()
                break
        c.rectangle((0,0,79,1))
        try:
            drop = ch.inventory[ord(dr)-97].drop_item('',10000)
            dropped = 0
            for item in ground_items:
                if item[:2] == ch.xy and item[2].id == drop.id and item[2].stackable and item[2].name == drop.name:
                    item[2].qty += drop.qty
                    dropped = 1
            if not dropped:
                ground_items.append([ch.xy[0], ch.xy[1],drop])
        except:
            pass
        draw_inv()
    if i1 == 'e':
        draw_equip()
        return 1
    if i1 == 'u':
        c.rectangle((0,0,79,1))
        c.pos(0,0)
        c.write(' Which item do you want to use?')
        use = msvcrt.getch()
        c.rectangle((0,0,79,1))
        try:
            ty = ch.inventory[ord(use)-97].type
            if 'container' in ch.inventory[ord(use)-97].type:
                open_container(ch.inventory[ord(use)-97])
            elif ch.inventory[ord(use)-97].effect != {} and ('armour' not in ty and 'weapon' not in ty and 'tool' not in ty):
                ch.inventory[ord(use)-97].use_item()
            if ch.spell_cast or ch.turn in ch.land_effects:
                return 0
        except IndexError:
            pass
        draw_inv()
        
def draw_equip():
    c.page()
    c.pos(0,0)
    c.write('\n You check your equipment:\n (a-p)take off/equip item (1)view inventory\n\n')
    for i in range(len(ch.equipment)):
        if ch.equipment[ch.equip_tags[i]] != []:
            item_effs = ''
            try:
                item_effs = []
                done = [item_effs.extend(x) for x in ch.equipment[ch.equip_tags[i]].effect['temp_attr']]
                if item_effs:
                    item_effs = '['+' '.join([str(x) for x in item_effs])+']'
                else:
                    item_effs = ''
            except KeyError:
                item_effs = ''
            engrav = ''
            if 'engraving' in ch.equipment[ch.equip_tags[i]].effect:
                engrav = '"'+ch.equipment[ch.equip_tags[i]].effect['engraving']+'"'
            if 'two_handed' in ch.equipment[ch.equip_tags[i]].type:
                print ' '+chr(i+97)+')  ', ch.equip_tags[i]+': %s (two hands), %d x %s stones %s %s' %(ch.equipment[ch.equip_tags[i]].name.capitalize(),
                                                                                          ch.equipment[ch.equip_tags[i]].qty,
                                                                                          str(ch.equipment[ch.equip_tags[i]].weight), item_effs,
                                                                                                            engrav)
            else:
                print ' '+chr(i+97)+')  ', ch.equip_tags[i]+': %s, %d x %s stones %s %s' %(ch.equipment[ch.equip_tags[i]].name.capitalize(),
                                                                                          ch.equipment[ch.equip_tags[i]].qty,
                                                                                          str(ch.equipment[ch.equip_tags[i]].weight),item_effs,
                                                                                             engrav)
            c.text(4,i+4,ch.equipment[ch.equip_tags[i]].tag,ch.equipment[ch.equip_tags[i]].color)
        else:
            print ' '+chr(i+97)+')  ', ch.equip_tags[i]+':'
    i1 = ' '
    i1 = msvcrt.getch()
    if i1 == '1':
        draw_inv()
        return 1
    if ord(i1)-97 in range(19):
        if ch.equipment[ch.equip_tags[ord(i1)-97]] == []:
            two = 0
            if ch.equip_tags[ord(i1)-97] == 'Right hand' and ch.equipment['Left hand'] != []:
                if 'two_handed' in ch.equipment['Left hand'].type:
                    two = 1
                    ch.take_off(ch.equip_tags.index('Left hand'))
            elif ch.equip_tags[ord(i1)-97] == 'Left hand' and ch.equipment['Right hand'] != []:
                if 'two_handed' in ch.equipment['Right hand'].type:
                    two = 1
                    ch.take_off(ch.equip_tags.index('Right hand'))
            if not two:
                ch.find_equipment(ord(i1)-97)
        else:
            if ch.equip_tags[ord(i1)-97] == 'Backpack':
                print ' Do you really want to drop your bag to the ground?\n You will be able to carry only one item per free hand at most! (y/n)'
                b1 = msvcrt.getch()
                if b1.lower() != 'y':
                    draw_equip()
                    return
            ch.take_off(ord(i1)-97)
        draw_equip()

def character():
    atts = ['Str','Dex','End','Int','Cre','Mnd']
    races = {'Nature':['elf','gnome','spirit of nature','dryad','water elemental','fairy'],
             'Chaos':['ork','troll','spirit of chaos','goblin','kraken','imp'],
             'Order':['human','dwarf','spirit of order']}
    all_races = ['elf','gnome','spirit of nature','dryad','water elemental','fairy','human','dwarf','spirit of order',
              'ork','troll','spirit of chaos','goblin','kraken','imp']
    c.page()
    c.pos(0,0)
    c.text(2,1,'%s' %(ch.name),7)
    i = 10
    if (ch.life < (ch.max_life*0.7)) and (ch.life > (ch.max_life*0.2)):
        i = 14
    elif (ch.life <= (ch.max_life*0.2)):
        i = 12
    c.text(2,3,'Life %d/%d' %(ch.life,ch.max_life),i)
    for x in atts:
        c.text(2,atts.index(x)+5,'%s  %d' %(x,ch.attr[x]),ch.attr_colors[x])
    c.text(13,3,'Armour %d' %(ch.armour),9)
    c.text(13,5,'Wg %.2f/%d' %(ch.weight, ch.max_weight),7)
    c.text(13,6,'Free bag %.2f' %(ch.backpack),7)
    c.text(13,7,'Free hands %d' %(ch.free_hands),9)
    c.text(13,8,'Turn %d' %(ch.turn),7)
    c.text(29,3,'Weapon skills',12)
    current_weapons=[]
    right_hand_weapon=''
    if ch.equipment['Right hand'] and 'weapon' in ch.equipment['Right hand'].type:
        current_weapons.append(ch.equipment['Right hand'].weapon_type.capitalize())
        right_hand_weapon=ch.equipment['Right hand'].weapon_type.capitalize()
    if ch.equipment['Left hand'] and 'weapon' in ch.equipment['Left hand'].type:
        current_weapons.append(ch.equipment['Left hand'].weapon_type.capitalize())
    if not current_weapons:
        current_weapons=['Unarmed']
    for s in ch.weapon_skills:
        if s in current_weapons:
            if s==right_hand_weapon or len(current_weapons)==1:
                c.text(29,ch.weapon_skills.keys().index(s)+5,'%-12s:%6.2f' %(s,ch.weapon_skill),10)
            else:
                c.text(29,ch.weapon_skills.keys().index(s)+5,'%-12s:%6.2f' %(s,ch.weapon_skills[s]),10)
        else:
            c.text(29,ch.weapon_skills.keys().index(s)+5,'%-12s:%6.2f' %(s,ch.weapon_skills[s]),7)
    c.text(49,1,'NATURE %17.2f' %ch.forces['Nature']+'%',10)
    the_line=3
    for race in races['Nature']:
        if race==ch.locked_race:
            col=2
        else:
            col=7
        c.text(50,the_line,'%s) %-16s:%6.2f' %(chr(all_races.index(race)+97),race.capitalize(),ch.races['Nature'][race])+'%',col)
        the_line+=1
    c.text(49,the_line+1,'ORDER  %17.2f' %ch.forces['Order']+'%',9)
    the_line+=3
    for race in races['Order']:
        if race==ch.locked_race:
            col=2
        else:
            col=7
        c.text(50,the_line,'%s) %-16s:%6.2f' %(chr(all_races.index(race)+97),race.capitalize(),ch.races['Order'][race])+'%',col)
        the_line+=1
    c.text(49,the_line+1,'CHAOS  %17.2f' %ch.forces['Chaos']+'%',12)
    the_line+=3
    for race in races['Chaos']:
        if race==ch.locked_race:
            col=2
        else:
            col=7
        c.text(50,the_line,'%s) %-16s:%6.2f' %(chr(all_races.index(race)+97),race.capitalize(),ch.races['Chaos'][race])+'%',col)
        the_line+=1
    c.pos(2,15)
    if ch.emotion == 2:
        c.text(2,20,'Tired',7)
    if ch.sit == True:
        c.text(2,23,'Sitting',7)
    colour = 7
    if ch.hunger > 60:
        sign = 'Hungry'
        if 80 < ch.hunger < 100:
            colour = 12
            sign = 'HUNGRY'
        if ch.hunger == 100:
            if ch.turn%2 == 1:
                colour = 14
            else:
                colour = 12
            sign = 'STARVING!'
        c.text(2,21,sign,colour)
    colour = 7
    if ch.thirst > 60:
        sign = 'Thirsty'
        if 80 < ch.thirst < 100:
            colour = 12
            sign = 'THIRSTY'
        if ch.thirst == 100:
            if ch.turn%2 == 0:
                colour = 14
            else:
                colour = 12
            sign = 'DYING OF THIRST!'
        c.text(2,22,sign,colour)
    waiting=msvcrt.getch()
    if ord(waiting) in range(97,len(all_races)+97):
        ch.locked_race=all_races[ord(waiting)-97]
        character()

def research():
    races = {'Nature':['elf','gnome','spirit of nature','dryad','water elemental','fairy'],
             'Chaos':['ork','troll','spirit of chaos','goblin','kraken','imp'],
             'Order':['human','dwarf','spirit of order']}
    all_races = ['elf','gnome','spirit of nature','dryad','water elemental','fairy','human','dwarf','spirit of order',
              'ork','troll','spirit of chaos','goblin','kraken','imp']
    c.page()
    c.pos(1,1)
    c.write('''      RESEARCHING FORCES AND RACES

 As a highly attuned human you have the ability
 to study the world that surrounds you. This
 gives you the chance to learn skills and
 abilities that belong to the other races of
 Order, and even the races of Nature and Chaos!
 To begin studying a race you need to select
 them to the right, and then spend time in the
 respective environment observing it.
 Take note that the maximum total force
 knowledge of all three forces can be 100%,
 and the maximum total race knowledge in a
 force can't be more than the force knowledge
 itself (like your own attunement). If you want
 to stop studying and fix the numbers the way
 they are, simply select human as a study race.
 
 IF YOU LOSE YOUR HIGH HUMAN ATTUNEMENT (90%)
 YOU WILL LOSE ALL COLLECTED KNOWLEDGE!''')

    c.text(1,22,'Researching: %s -> %s' %(ch.research_force,ch.research_race.capitalize()))
    c.text(49,1,'NATURE %17.2f' %ch.research_forces['Nature']+'%',10)
    the_line=3
    for race in races['Nature']:
        if race==ch.research_race:
            col=2
        else:
            col=7
        c.text(50,the_line,'%s) %-16s:%6.2f' %(chr(all_races.index(race)+97),race.capitalize(),ch.research_races['Nature'][race])+'%',col)
        the_line+=1
    c.text(49,the_line+1,'ORDER  %17.2f' %ch.research_forces['Order']+'%',9)
    the_line+=3
    for race in races['Order']:
        if race==ch.research_race:
            col=2
        else:
            col=7
        c.text(50,the_line,'%s) %-16s:%6.2f' %(chr(all_races.index(race)+97),race.capitalize(),ch.research_races['Order'][race])+'%',col)
        the_line+=1
    c.text(49,the_line+1,'CHAOS  %17.2f' %ch.research_forces['Chaos']+'%',12)
    the_line+=3
    for race in races['Chaos']:
        if race==ch.research_race:
            col=2
        else:
            col=7
        c.text(50,the_line,'%s) %-16s:%6.2f' %(chr(all_races.index(race)+97),race.capitalize(),ch.research_races['Chaos'][race])+'%',col)
        the_line+=1
    waiting=msvcrt.getch()
    if ord(waiting) in range(97,len(all_races)+97):
        ch.research_race=all_races[ord(waiting)-97]
        for r in races:
            if all_races[ord(waiting)-97] in races[r]:
                ch.research_force=r
                break
        research()

def tame(animal):
    diff=animal.attr['tame'][1]
    if animal.attr['tame'][2] not in [i.id for i in ch.inventory]:
        message_use('taming_item',I[animal.attr['tame'][2]])
        return 0
    chance=random.randint(1,100)
    if chance+ch.forces['Nature']>=diff:
        message_creature('tame_success',animal)
        if animal.random:
            animal.random=False
            animal.appearance=100
            animal.name='friendly '+animal.name
        else:
            animal.appearance+=100
            if animal.appearance>=1000 and 'tame' not in animal.name:
                animal.name='tame '+animal.name[9:]
                animal.mode='follow'
                animal.attr['area']=''
                animal.attr['target']=[]
                animal.food=50
                animal.farm=0
                ch.followers.append(animal)
    else:
        message_creature('tame_fail',animal)
        animal.appearance-=10
        if animal.appearance<=0:
            animal.random=True
            for a in game_creatures:
                if a.id==animal.id:
                    animal.name=a.name
                    break

def command_tamed(animal):
    message_message('')
    c.text(1,0,'Choose command:   a)change mode   b)manipulate',7)
    choice=msvcrt.getch()
    if choice.lower()=='a':
        message_message('')
        c.text(1,0,'Choose mode:   a)follow   b)stay   c)guard',7)
        ch_mode=msvcrt.getch()
        if ch_mode.lower()=='a':
            message_message('')
            animal.mode='follow'
            message_creature('command_follow',animal)
        elif ch_mode.lower()=='b':
            message_message('')
            animal.mode='standing'
            animal.attr['area']=current_area
            message_creature('command_stay',animal)
        elif ch_mode.lower()=='c':
            message_message('')
            if animal.attr['tame'][0]=='guard':
                animal.mode='guarding'
                message_creature('command_guard',animal)
            else:
                message_message('cant_guard')
        else:
            message_message('')
    elif choice.lower()=='b':
        message_message('')
        c.text(1,0,'Choose action:   a)feed   b)farm   c)ride',7)
        ch_action=msvcrt.getch()
        message_message('')
        if ch_action.lower()=='a':
            chosen_food=0
            for i in ch.inventory:
                if i.id == animal.attr['tame'][2]:
                    chosen_food=i
                    break
            if chosen_food and animal.food<100:
                message_creature('feed',animal)
                i.lose_item(1)
                animal.food=min([animal.food+random.randint(10,20),100])
            elif chosen_food and animal.food==100:
                message_message('full_animal')
            else:
                message_use('feed_item',I[animal.attr['tame'][2]])
        elif ch_action.lower()=='b':
            message_message('')
            if animal.attr['tame'][0]=='farm':
                if animal.farm:
                    if 'container' in I[animal.attr['tame'][3]].effect:
                        needed=I[I[animal.attr['tame'][3]].effect['container']]
                        found=0
                        for cont in ch.inventory:
                            if cont.id==needed.id and cont.name==needed.name:
                                cont.lose_item(1)
                                found=1
                                break
                        if not found:
                            message_use('needed_container',needed)
                            return 0
                    creation=I[animal.attr['tame'][3]].duplicate(1)
                    ground_items.append([ch.xy[0],ch.xy[1],creation])
                    ch.pick_up(ground_items)
                    message_use('farm_harvest',creation)
                    animal.farm-=1
                else:
                    message_message('nothing_to_farm')
            else:
                message_message('cant_farm')
        elif ch_action.lower()=='c':
            message_message('')
            if animal.attr['tame'][0]=='ride' and not ch.ride and not ch.possessed:
                ch.followers.remove(animal)
                ch.ride.append(animal)
                ch.backpack += animal.attr['Str']*2
                hide(animal)
                animal.xy=[1,1]
                animal.mode='follow'
                message_creature('mount',animal)
                if animal.food<25:
                    message_message('hungry_mount')
                elif animal.food<75:
                    message_message('normal_mount')
                else:
                    message_message('well_fed_mount')
            else:
                if ch.ride:
                    message_message('cant_ride_two')
                else:
                    message_message('cant_ride')

def possess(animal,tr=''):
    message_message('')
    chance=float(ch.attr['Mnd'])/(ch.attr['Mnd']+animal.attr['Mnd'])
    tried=random.random()
    if tried<chance or tr:
        ch.possessed=[animal]
        for x in ch.attr:
            ch.attr[x]=animal.attr[x]
        ch.life+=animal.life
        ch.max_life+=animal.life
        if tr=='trans':
            message_creature('transform_into',animal)
        else:
            message_creature('possessed_animal',animal)
            hide(animal)
            animal.xy=[1,1]
            animal.mode='follow'
            if 'spirit of nature3' in ch.tool_tags:
                the_slot=''
                if ch.equipment['Right hand'] and ch.equipment['Right hand'].id==50 and \
                   (ch.equipment['Right hand'].effect=={} or 'totem' in ch.equipment['Right hand'].type):
                    the_slot='Right hand'
                elif ch.equipment['Left hand'] and ch.equipment['Left hand'].id==50 and \
                     (ch.equipment['Left hand'].effect=={} or 'totem' in ch.equipment['Left hand'].type):
                    the_slot='Left hand'
                if the_slot:
                    if 'totem' in ch.equipment[the_slot].type:
                        if 'temp_attr' in ch.equipment[the_slot].effect:
                            del(ch.equipment[the_slot].effect['temp_attr'])
                        if 'transform' not in ch.equipment[the_slot].effect and ch.equipment[the_slot].name[:-6]==animal.name:
                            ch.equipment[the_slot].effect['transform']=animal.duplicate(1,1,10000,animal.force,
                                                                                               animal.race,rand=False)
                            ch.equipment[the_slot].effect['transform'].mode='temp'
                    else:
                        ch.equipment[the_slot].type.append('totem')
                        ch.equipment[the_slot].type.remove('weapon')
                        ch.equipment[the_slot].effect[animal.name]=0.
                        ch.equipment[the_slot].effect['transform']=animal.duplicate(1,1,10000,animal.force,
                                                                                            animal.race,rand=False)
                        ch.equipment[the_slot].effect['transform'].mode='temp'
                        ch.equipment[the_slot].name='%s totem' %(animal.name)
    elif tried>.95:
        animal.mode='hostile'
        message_creature('anger_animal',animal)

def pickpocket(target):
    target_awareness=(target.attr['Int']+target.attr['Mnd'])/2.
    if 'stealthy' in ch.tool_tags:
        picking_skill=(ch.attr['Int']+ch.attr['Dex'])/1.5
    else:
        picking_skill=(ch.attr['Int']+ch.attr['Dex'])/2.
    chance=picking_skill/(target_awareness+picking_skill)
    if random.random()<chance:
        if len(target.attr['loot'])==1 and 'picked_dry' not in target.attr:
            put_item([[1000,75,1,10]],ch.xy)
            target.attr['picked_dry']=1
            message_creature('pilfer_last',target)
        elif len(target.attr['loot'])>1:
            put_item([target.attr['loot'][1]],ch.xy)
            target.attr['loot']=[target.attr['loot'][0]]+target.attr['loot'][2:]
            message_creature('pilfer',target)
        elif len(target.attr['loot'])==1 and 'picked_dry' in target.attr:
            message_creature('no_pilfer',target)
    else:
        target.mode='hostile'
        message_creature('steal_failed',target)

def talk(target):
    race_answers={'fairy':{'learn':
"""  Being a fairy isn't hard at all! You just go around cleaning the wells,
  decorating walls with pretty clay you find around the wells, hanging
  flowers on the fences of farmers and the doors of their houses. A fairy
  does best around humans, because their villages can always be made much
  more beautiful. If you are lighthearted enough to be a fairy go
  %s of here, where you will find a human village.

  Oh, and don't forget that if you are at least one third a fairy, grass will
  grow magically under your feet, making you even more powerful, and if you
  find some rare flowers you can make a magical flower crown and other pretty
  things!
  
  Do what I taught you and return sometimes to tell me of what you have seen
  and done!""",'trade':"""\n  I can only give you food and water, or some pretty flowers. What else
  would a fairy need?\n\n"""},'elf':{'learn':
"""  The elves are the warriors of the forest, they protect Nature from the
  teeth of trolls and the axes of men! Animals do not attack elves, and woe
  to the elf that strikes down an innocent creature without need. Elves tend
  to ailing grasses and fruit-giving bushes and trees, living off the land's
  gifts.

  The bow is the greatest possession of an elf. When you are surrounded by
  the forest and every tiny sound of moving leaves and breaking twigs resounds
  in your ears, you can feel other living things without seeing them.
  And when you smell an ork from a hundred paces you can put an arrow through
  his neck in a heartbeat, without making a sound. So practice your bow, give
  Nature its due, and you may become an elf one day...%s""",'trade':'''\n  If you have some food or water I can barter arrows or even a spare bow,
  if I have one.\n\n'''},'gnome':{'learn':
"""  Oh, so you want to be a gnome? Well, I'll tell you what a gnome is then.
  He's a fairy with a dwarf's beard, hahahaha! No, I'm serious, a gnome has a
  dwarf's love of stone and gems, but shows it much like a fairy's love for
  grasses and flowers. A dwarf breaks the stone to build a house, while we
  tend and nurture it, and live directly in it. We can find the gems hidden
  in the stone just by looking inside! These gems are our magic, the way we
  wield the force of Nature. Every gem can be used under certain conditions
  to a certain effect, which you'll have to find for yourself.

  I'll only share this one piece of gem-lore with you: use a lapis lazuli to
  enter the world of stone, the gnomes' homeland.\n%s""",'trade':'''\n  I am only interested in shiny stones, but you will need to give me
  a lot of food for one of them!\n\n'''},
    'spirit of nature':{'learn':
"""  A spirit connects with the environment in any place he visits.
  He tends to the grass and burries the remains of creatures so they can
  become one with Nature again. He heals the ground wherever he steps and
  he can possess animals that do not attack him. If you are a strong enough
  spirit you can make a totem of the animal from a staff when you control
  it. The totem will accumulate the essence of the animal and allow you to
  use it as you wish. If your totem is strong enough it will allow you to
  assume the form of the creature once until you possess it again.

  You can get a totem staff from me if you need one...\n\n%s""",
'trade':'''\n  I can only give you food and water, or a staff you can use for a totem.\n\n'''},
    'dryad':{'learn':
"""  A dryad must show commitment to Nature. We are the creators, the ones
  that push the growth of trees and woods so that Nature can claim a place
  properly. We channel our living energy in saplings and dead trees alike,
  so that the force of Nature runs strong in them. With enough time we can
  turn even the most barren desert into a forest, or create pieces of living
  wooden armour, which the warriors of Nature use to defend themselves from
  the fury of chaotic beasts and the axes of men. We can also make bows for
  the elves and totem staffs for the spirits of Nature.\n%s""","trade":
"""\n  Yes, I can trade some of the things I create with you... But only if
  you use them to protect Nature!\n\n"""},
    'water elemental':{'learn':
"""  To understand a water elemental you have to think like one. We have a
  phylosophy that water is the most important thing in Nature. Nothing lives
  without water, and we are the bringers and protectors of water. In return
  water protects and sustains us. We can melt into water, becoming truly
  invisible. If you care for water long enough you do not need food anymore,
  and being surrounded by water is enough to sate your hunger. It's only
  logical that polluted waters are poisonous to us - our first task is to
  clean them of the taint of Chaos.

  The ultimate gift of water can make us nearly immortal for a time, and
  magical springs can help us reform our physical bodies. Thus, we value
  those magical places above all else.%s""",'trade':""""""}}
    c.page()
    try:
        the_name=target.name
        gender=target.gender
        c.write('''\n  %s greets you.
  What do you want to talk about with %s?\n\n  ''' %(the_name,gender[2]))
    except AttributeError:
        the_name=random_name(target.force)
        target.name=the_name
        gender=random.choice([['he','his','him'],['she','her','her']])
        target.gender=gender
        c.write('''\n  The %s presents %sself as %s.
  What do you want to talk about with %s?\n\n  ''' %(target.race,gender[2],the_name,gender[2]))
    c.write('''1) Learning how to be a %s
  2) Trade
  3) Rumours\n\n''' %(target.race))
    i=msvcrt.getch()
    if i=='1':
        if target.race in race_answers:
            dirs=''
            if target.race=='fairy':
                town=find_place('Order','Population')
                curr_coords=[int(current_area[4:])/map_size,int(current_area[4:])%map_size]
                NS=cmp(curr_coords[0],town[0])
                WE=cmp(curr_coords[1],town[1])
                if NS:
                    dirs+='%d hour%s %s' %(abs(curr_coords[0]-town[0]),['','s'][cmp(abs(curr_coords[0]-town[0]),1)],['south','north'][max([NS,0])])
                if WE:
                    if dirs:
                        dirs+=' and '
                    dirs+='%d hour%s %s' %(abs(curr_coords[1]-town[1]),['','s'][cmp(abs(curr_coords[0]-town[0]),1)],['east','west'][max([NS,0])])
            c.write('%s' %(race_answers[target.race]['learn']) %(dirs))
    elif i=='2':
        if target.race in race_answers:
            trade_goods={'fairy':{'buy':[[1305,100,1,13],[3,100,1,3],[1301,100,1,3]],'sell':['food','drink','flowers']},
                         'elf':{'buy':[[1313,100,1,3],[3,100,1,3],[1318,100,5,10],[56,60,1,1]],'sell':['food','drink','Ammunition']},
                         'gnome':{'buy':[[1301,100,1,3],[1311,80,1,3],[3,100,1,3],['gnome_touch',20]],'sell':['food','drink','cookmat','gem']},
                         'spirit of nature':{'buy':[[50,100,1,1],[3,100,1,3],[1301,100,1,3]],'sell':['food','drink','cookmat','weapon']},
                         'dryad':{'buy':[[1311,80,1,1],[3,100,1,3],[1301,100,1,3],['dryad',100],['dryad',100]],'sell':['food','drink','cookmat','weapon','armour','Ammunition']}}
            offering=set([])
            for y in trade_goods[target.race]['sell']:
                for x in ch.inventory:
                    if y in x.type:
                        offering.add(x)
            offering=list(offering)
            getting=[]
            if 'trade_goods' in target.attr and target.attr['trade_timer']+600>ch.turn:
                getting=target.attr['trade_goods'][:]
                target.attr['trade_timer']+=100
            else:
                for x in trade_goods[target.race]['buy']:
                    the_goods=put_item([x])
                    if the_goods:
                        getting.append(the_goods)
                target.attr['trade_goods']=getting[:]
                target.attr['trade_timer']=ch.turn
            i=''
            chosen={}
            balance=0
            while i!=' ':
                c.page()
                c.write(race_answers[target.race]['trade'])
                c.write('  You can offer:                   Chosen:  You can get:\n\n')
                for x in offering:
                    c.text(1,6+offering.index(x),'%s)%-15s %d at %.2f cp'
                           %(chr(97+offering.index(x)),x.name.capitalize()[:15],x.qty,get_price(x,target,1)))
                    if x in chosen:
                        c.text(36,6+offering.index(x),str(chosen[x]))
                for x in getting:
                    c.text(43,6+getting.index(x),'%s)%-15s %d at %.2f cp'
                           %(chr(65+getting.index(x)),x.name.capitalize()[:15],x.qty,get_price(x,target,0)))
                    if x in chosen:
                        c.text(39,6+getting.index(x),str(chosen[x]))
                c.text(2,22,'a..z/A..Z - select items; trade with SPACE; exit with !; reset with 0.')
                c.text(2,23,'Trade balance: %.2f' %(balance),[10,12,10][cmp(0,balance)])
                c.pos(72,22)
                i=msvcrt.getch()
                if 'A'<=i<chr(65+len(getting)):
                    old=chosen.get(getting[ord(i)-65],0)
                    chosen[getting[ord(i)-65]]=min([chosen.get(getting[ord(i)-65],0)+1,getting[ord(i)-65].qty])
                    if old!=chosen[getting[ord(i)-65]]:
                        balance-=get_price(getting[ord(i)-65],target,0)
                elif 'a'<=i<chr(97+len(offering)):
                    old=chosen.get(offering[ord(i)-97],0)
                    chosen[offering[ord(i)-97]]=min([chosen.get(offering[ord(i)-97],0)+1,offering[ord(i)-97].qty])
                    if old!=chosen[offering[ord(i)-97]]:
                        balance+=get_price(offering[ord(i)-97],target,1)
                elif i=='!':
                    break
                elif i=='0':
                    chosen={}
                    balance=0
                elif i==' ':
                    if balance>=0 and chosen:
                        for x in chosen.keys():
                            if x in ch.inventory:
                                x.lose_item(chosen[x])
                                added=0
                                for y in getting:
                                    if y.id==x.id and y.name==x.name:
                                        y.qty+=chosen[x]
                                        added=1
                                        break
                                if not added:
                                    getting.append(x.duplicate(chosen[x]))
                            elif x in getting:
                                if chosen[x]==x.qty:
                                    getting.remove(x)
                                else:
                                    x.qty-=chosen[x]
                                ground_items.append([ch.xy[0], ch.xy[1], x.duplicate(chosen[x])])
                        target.attr['trade_goods']=getting[:]
                    else:
                        i=''
    if i=='1':
        msvcrt.getch()
    redraw_screen()

def get_price(x,merch,sell):
    item_types={'tool':5,'weapon':20,'container':20,'talisman':30,'armour':20,'craftmat':2,'cookmat':2,
                'food':10,'drink':10,'treasure':100,'ancient':1000,'seed':5,'ore':3,'Ammunition':5,'spice':10}
    materials={'wood':5,'iron':5,'copper':1,'silver':10,'gold':100,'leather':8,'ivory':50,'cloth':3,
               'diamond':1000,'emerald':750,'sapphire':750,'ruby':750,'pearl':750,'amethyst':750,'topaz':500,
               'tourmaline':500,'garnet':500,'aquamarine':500,'opal':750,'turquoise':500,'lapis lazuli':500,
               'paper':100,'feather':5,'bone':5}
    price=max([x.weight,0.01])*max([materials.get(y,1) for y in x.type])*max([item_types.get(z,1) for z in x.type])
    m=(float(merch.attr['Int']+merch.attr['Cre'])/(merch.attr['Int']+merch.attr['Cre']+ch.attr['Int']+ch.attr['Cre'])-.5)/2
    if sell:
        price-=price*m
    else:
        price+=price*m
    return price
                        

def find_place(a,b):
    good_coords=[]
    max_score=0
    for x in range(len(T_matrix)):
        for y in range(len(T_matrix)):
            if x==0 and y==0:
                continue
            else:
                if T_matrix[x][y][a]+T_matrix[x][y][b]>max_score:
                    max_score=T_matrix[x][y][a]+T_matrix[x][y][b]
                    good_coords=[x,y]
    return good_coords

def random_name(f):
    engraving = ''
    vowel = {'Nature':'aoeiuy','Order':'aoeiuy','Chaos':'eiuy'}
    consonant = {'Nature':'lkhgfdscvbnm','Order':'rtplkhgfdszxcvbnmw','Chaos':'rtplkhgfdszxvbnmw'}
    cap = 1
    syllables = random.randint(1,5)
    for y in range(syllables):
        chars=[consonant[f],vowel[f]]
        random.shuffle(chars,random=random.random)
        for z in chars:
            if cap:
                engraving+=random.choice(z).upper()
                cap = 0
            else:
                engraving+=random.choice(z)
    return engraving

def game_over():
    c.page()
    c.pos(30,14)
    c.write('Your life is 0! GAME OVER!')
    c.text(35,17,'(q)uit',7)
    i = ''
    while 1:
        if msvcrt.kbhit():
            i = msvcrt.getch()
            if i == 'q' or i == 'Q':
                return 0

def drink(xy):
    if T[land[xy[1]-1][xy[0]-21]].drink != {}:
        if ch.thirst == 0:
            message_use('over_drink',T[land[xy[1]-1][xy[0]-21]])            
            return 1
        message_use('drink',T[land[xy[1]-1][xy[0]-21]])
        if T[land[xy[1]-1][xy[0]-21]].id=='t' and 'goblin1' in ch.tool_tags:
            for k,v in {'energy':10,'thirst':5}.items():
                effect(k,v)
        else:
            for k,v in T[land[xy[1]-1][xy[0]-21]].drink.items():
                effect(k,v)
    elif ch.possessed:
        if ch.thirst>20 or ch.hunger>20:
            to_eat={'wild horse':'gb','squirrel':'T','snake':'b','poison snake':'b','camel':'Tb','giant lizard':'.,',
                    'penguin':'wW','monkey':'T','polar bear':'wW','bear':'b','cattle':'gb','chicken':'g.','fish':'wW',
                    'plant':'.g'}
            if T[land[xy[1]-1][xy[0]-21]].id in to_eat.get(ch.possessed[0].race,''):
                if ch.equipment['Right hand'] and ch.possessed[0].name in ch.equipment['Right hand'].effect:
                    ch.equipment['Right hand'].effect[ch.possessed[0].name]\
                                               =min([100,ch.equipment['Right hand'].effect[ch.possessed[0].name]+0.1])
                elif ch.equipment['Left hand'] and ch.possessed[0].name in ch.equipment['Left hand'].effect:
                    ch.equipment['Left hand'].effect[ch.possessed[0].name]\
                                               =min([100,ch.equipment['Left hand'].effect[ch.possessed[0].name]+0.1])
                if ch.xy not in ch.worked_places[ch.mode]:
                    for k,v in {'energy':10,'thirst':5,'hunger':5}.items():
                        effect(k,v)
                    message_message('eating_%s' %(ch.possessed[0].race.replace(' ','_')))
                    if ch.possessed[0].race!='plant':
                        ch.worked_places[ch.mode].append(xy[:])
                else:
                    message_message('no_food_%s' %(ch.possessed[0].race.replace(' ','_')))
            elif ch.possessed[0].race in ['grizzly','wolf','dog','polar wolf','hyena']:
                found_meat=0
                for x in ground_items:
                    if [x[0],x[1]]==ch.xy and 'meat' in x[2].name:
                        found_meat=1
                        for k,v in {'energy':10,'thirst':10,'hunger':25}.items():
                            effect(k,v)
                        break
                if found_meat:
                    if x[2].qty>1:
                        x[2].qty-=1
                    else:
                        ground_items.remove(x)
                    message_message('eating_carnivore')
                    if ch.equipment['Right hand'] and ch.possessed[0].name in ch.equipment['Right hand'].effect:
                        ch.equipment['Right hand'].effect[ch.possessed[0].name]\
                                                   =min([100,ch.equipment['Right hand'].effect[ch.possessed[0].name]+0.1])
                    elif ch.equipment['Left hand'] and ch.possessed[0].name in ch.equipment['Left hand'].effect:
                        ch.equipment['Left hand'].effect[ch.possessed[0].name]\
                                                   =min([100,ch.equipment['Left hand'].effect[ch.possessed[0].name]+0.1])
                else:
                    message_message('no_food_carnivore')
            else:
                message_message('no_food_%s' %(ch.possessed[0].race.replace(' ','_')))
        else:
            message_message('not_hungry')
    else:
        message_message('no_drink')

def find_to_open(xy):
    md = {1:[-1,1], 2:[0,1], 3:[1,1], 4:[-1,0], 5:[0,0],
          6:[1,0], 7:[-1,-1], 8:[0,-1], 9:[1,-1]}
    doors = []
    containers = []
    for i in range(1, 10):
        search = [xy[0]+md[i][0], xy[1]+md[i][1]]
        if 'door_' in T[land[search[1]-1][search[0]-21]].world_name:
            doors.append(search[:])
        for bag in ground_items:
            if search == bag[:2] and 'container' in bag[2].type:
                containers.append(bag)
    if len(doors)+len(containers) == 0:
        message_message('no_open')
        return 0
    elif len(doors)+len(containers) == 1:
        if len(doors):
            if T[land[doors[0][1]-1][doors[0][0]-21]].world_name.endswith('_c'):
                open_door(doors[0], land[doors[0][1]-1][doors[0][0]-21])
            elif T[land[doors[0][1]-1][doors[0][0]-21]].world_name.endswith('_o'):
                close_door(doors[0], land[doors[0][1]-1][doors[0][0]-21])
            return 0
        else:
            success = open_container(containers[0][2])
            return success
    else:
        message_message('which_open')
        i = msvcrt.getch()
        try:
            message_message('')
            try:
                i = int(i)
            except ValueError:
                message_message('direction')
                return 0
            target = [xy[0]+md[i][0], xy[1]+md[i][1]]
            if target in doors:
                if T[land[target[1]-1][target[0]-21]].world_name.endswith('_c'):
                    open_door(target, land[target[1]-1][target[0]-21])
                elif T[land[target[1]-1][target[0]-21]].world_name.endswith('_o'):
                    close_door(target, land[target[1]-1][target[0]-21])
                return 0
            else:
                nothing = 1
                for cont in containers:
                    if target == cont[:2]:
                        nothing = 0
                        break
                if nothing:
                    message_message('no_open')
                    return 0
                else:
                    success = open_container(cont[2])
                    return success
        except KeyError:
            message_message('direction')
            return 0

def open_container(chest):
    if 'locked' in chest.type: ##Lockpicking se uchi samo kogato uspeesh!
        if 'lockpick' in ch.tool_tags:
            lock_atts = (ch.attr['Dex']+ch.attr['Int'])/2.0
            if 'lockpicking' not in ch.skills:
                ch.skills['lockpicking'] = float(ch.attr['Dex'])
            if random.random() < ch.skills['lockpicking']/chest.effect['lock_strength']:
                learn = random.uniform(0,100)
                if learn <= (lock_atts - ch.skills['lockpicking']/5)/lock_atts*100:
                    ch.skills['lockpicking'] += 0.1
                chest.type.remove('locked')
                message_message('success_lockpick')
                msvcrt.getch()
            else:
                if ch.skills['lockpicking'] < chest.effect['lock_strength']/10:
                    learn = random.uniform(0,100)
                    if learn <= (lock_atts - ch.skills['lockpicking']/5)/lock_atts*100:
                        ch.skills['lockpicking'] += 0.01
                message_message('failed_lockpick')
                msvcrt.getch()
                return 0
        else:
            message_use('no_lockpick',chest)
            msvcrt.getch()
            return 0
    c.page()
    print ' You open the %s and look inside.\n (t) take item (p) put item\n' %(chest.name)
    for i in range(len(chest.effect['contains'])):
        print ' %s)   %s %d x %s stones' %(chr(i+97),chest.effect['contains'][i].name.capitalize(),chest.effect['contains'][i].qty,
                                         str(chest.effect['contains'][i].weight))
        c.text(4,i+3,chest.effect['contains'][i].tag,chest.effect['contains'][i].color)
    print '\n You can carry %s more stones, %s more will fit in your backpack.' %(str(ch.max_weight-ch.weight),
                                                                                  str(ch.backpack))
    i1 = msvcrt.getch()
    i1 = i1.lower()
    if i1 == 't' and len(chest.effect['contains']):
        c.rectangle((0,0,79,1))
        c.pos(0,0)
        c.write(' Which item do you want to take out?')
        while 1:
            if msvcrt.kbhit():
                take = msvcrt.getch()
                break
        c.rectangle((0,0,79,1))
        try:
            item = chest.effect['contains'][ord(take)-97]
            if item.qty > 1 and ch.equipment['Backpack'] != []:
                message_message('pickup')                    
                a = ''
                i = ' '
                while ord(i) != 13:
                    i = msvcrt.getch()
                    if ord(i) in range(48,58):
                        c.write(i)
                        a += i
                message_message('')
                if a =='':
                    open_container(chest)
                    return 1
                a=int(a)
            else:
                a = 1
            if a > item.qty:
                a = item.qty
            if chest in ch.inventory:
                ch.weight -= item.weight*a
                ch.backpack += item.weight * item.qty
            if ch.weight+item.weight*a <= ch.max_weight and item.weight*a <= ch.backpack and ch.equipment['Backpack'] != []:
                item.get_item(a,item.name)
                chest.weight -= item.weight*a
                if a == item.qty:
                    chest.effect['contains'].remove(item)
                else:
                    item.qty -= a
                if 'talisman' in chest.type and 'talisman' in item.effect:
                    for tal in item.effect['talisman']:
                        for tal_add in item.effect['talisman'][tal]:
                            chest.effect[tal].remove(tal_add)
            elif ch.weight+item.weight*a > ch.max_weight:
                message_use('cant_carry', item)
                msvcrt.getch()
            elif item.weight*a > ch.backpack:
                if ch.equipment['Backpack'] == []:
                    if 'two_handed' in item.type:
                        needed_hands = 2
                    else:
                        needed_hands = 1
                    if ch.free_hands >= needed_hands:
                        item.get_item()
                        chest.weight -= item.weight*a
                        ch.free_hands -= needed_hands
                        if 1 < item.qty:
                            item.qty -= 1
                        else:
                            chest.effect['contains'].remove(item)
                        ch.backpack = 0
                    else:
                        message_message('drop_first')
                        msvcrt.getch()
                else:
                    message_use('cant_fit_in_backpack', item)
                    msvcrt.getch()
        except IndexError:
            pass
        open_container(chest)
    elif i1 == 'p':
        item = draw_inv(1, chest)
        if item:
            dropped = 0
            for i in chest.effect['contains']:
                if i.name == item.name and i.id == item.id and item.stackable:
                    i.qty += item.qty
                    message_message('ch')
                    dropped = 1
            if not dropped:
                chest.effect['contains'].append(item)
            chest.weight += item.weight * item.qty
            if chest in ch.inventory:
                ch.weight += item.weight * item.qty
                ch.backpack -= item.weight * item.qty
            if 'talisman' in chest.type and 'talisman' in item.effect:
                for tal in item.effect['talisman']:
                    if tal not in chest.effect:
                        chest.effect[tal]=item.effect['talisman'][tal][:]
                    else:
                        chest.effect[tal] += item.effect['talisman'][tal][:]
        open_container(chest)
    return 1

def open_door(xy, door_id):
    land[xy[1]-1] = land[xy[1]-1][:xy[0]-21] + T[door_id].degrade_to['door'] + land[xy[1]-1][xy[0]-20:]
    c.scroll((xy[0],xy[1],xy[0]+1,xy[1]+1), 1, 1, T[land[xy[1]-1][xy[0]-21]].colour, T[land[xy[1]-1][xy[0]-21]].char)
    message_message('open_door')
    
def creature_open_door(xy, door_id):
    land[xy[1]-1] = land[xy[1]-1][:xy[0]-21] + T[door_id].degrade_to['door'] + land[xy[1]-1][xy[0]-20:]
    c.scroll((xy[0],xy[1],xy[0]+1,xy[1]+1), 1, 1, T[land[xy[1]-1][xy[0]-21]].colour, T[land[xy[1]-1][xy[0]-21]].char)

def close_door(xy, door_id):
    blocked = 0
    for cr in all_beings:
        if cr.xy == xy:
            blocked = 1
    for i in ground_items:
        if i[:2] == xy:
            blocked = 1
    if blocked:
        message_message('blocked_door')
    else:
        land[xy[1]-1] = land[xy[1]-1][:xy[0]-21] + T[door_id].degrade_to['door'] + land[xy[1]-1][xy[0]-20:]
        c.scroll((xy[0],xy[1],xy[0]+1,xy[1]+1), 1, 1, T[land[xy[1]-1][xy[0]-21]].colour, T[land[xy[1]-1][xy[0]-21]].char)
        message_message('close_door')

def cook():
    mats=[]
    selected_mats=[]
    for i in ch.inventory:
        if 'cookmat' in i.type:
            mats.append(i.duplicate(i.qty))
            selected_mats.append(i.duplicate(0))
    selected_recipes={}
    selected_tags=[]
    the_meal=''
    i=''
    while i!=' ':
        c.page()
        c.pos(1,1)
        c.write('''You have the following ingredients for cooking. Select the ones you want to
 use and take note of the other things you need for the desired meal on the
 right. (exit with SPACE, decrease with SHIFT)

 You have:                   Using:     You can make:\n''')
        for i in range(len(mats)):
            print ' %s)   %s x %d' %(chr(i+97),mats[i].name,mats[i].qty)
            c.text(4,i+6,mats[i].tag,mats[i].color)
            c.text(31,i+6,str(selected_mats[i].qty))
        if selected_recipes:
            line=0
            for r in selected_recipes:
                c.text(40,line+6,'%s' %(r.capitalize()))
                if selected_recipes[r]:
                    c.text(40,line+7,' Needs: %s' %(','.join(['%d %s' %(selected_recipes[r].count(x),x.capitalize()) for x in set(selected_recipes[r])])))
                else:
                    c.text(40,line+7,' Press SPACE to make!')
                line+=2
        i=msvcrt.getch()
        if ord(i)-97 in range(len(mats)):
            if mats[ord(i)-97].qty>0:
                selected_mats[ord(i)-97].qty+=1
                selected_tags.append(mats[ord(i)-97].effect['cook'])
                mats[ord(i)-97].qty-=1
        if ord(i)-65 in range(len(mats)):
            if selected_mats[ord(i)-65].qty>0:
                selected_mats[ord(i)-65].qty-=1
                selected_tags.remove(mats[ord(i)-65].effect['cook'])
                mats[ord(i)-65].qty+=1
        if selected_tags:
            selected_recipes={}
            for r in CR[ch.attr['Cre']]:
                all_in=1
                needed_tags=cook_recipes[r][3:]
                for t in selected_tags:
                    if t in needed_tags:
                        needed_tags.remove(t)
                    else:
                        all_in=0
                        break
                for t in cook_recipes[r][1]:
                    full_tools=ch.tool_tags[:]
                    for gi in ground_items:
                        if gi[:2]==ch.xy:
                            full_tools+=gi[2].tool_tag
                    if t not in full_tools:
                        needed_tags.append(t)
                if all_in:
                    selected_recipes[r]=needed_tags[:]
                    if not needed_tags:
                        the_meal=r
        else:
            selected_recipes={}
        if the_meal not in selected_recipes:
            the_meal=''
    if the_meal:
        for m in selected_mats:
            if m.qty!=0:
                for x in ch.inventory:
                    if x.id==m.id and x.name==m.name:
                        x.lose_item(m.qty)
                        if the_meal=='get seeds':
                            veg_name=m.name
        creation=I[cook_recipes[the_meal][2]].duplicate(1)
        ## Za semena se izpolzva SAMO iztochnika (zelenchuk/cvete)
        if the_meal=='get seeds':
            creation.qty=3
            creation.name=veg_name+' seed'
            medium=creation.effect.pop('plant_vegetable')
            creation.effect['plant_specific']=[medium,veg_name]
        ground_items.append([ch.xy[0],ch.xy[1],creation])
        ch.pick_up(ground_items)
        c.rectangle((0,0,80,1))
        c.pos(1,0)

def choose_spell():
    c.page()
    if ch.spells == []:
        c.write('''
  You do not know any spells, you have to create some!''')
        i = msvcrt.getch()
    else:
        c.write('''
  Choose your spell:\n\n  ''')
        for x in ch.spells.keys():
            c.write('%d) %s  Ingredients:%s\n  ' %(ch.spells.keys().index(x)+1,x,[x.name for x in ch.spells[x]['ingredients']]))
        i = msvcrt.getch()
        try:
            i = int(i)-1
            if i in range(len(ch.spells)):
                cast_spell(ch.spells.keys()[i])
        except ValueError:
            pass

def cast_spell(name):
    in_stock = {}
    needed = {}
    for x in ch.inventory:
        in_stock[x.id] = x.qty
    for x in ch.spells[name]['ingredients']:
        needed[x.id] = needed.get(x.id,0) + 1
    for x in needed:
        if needed[x]>in_stock[x]:
            c.write("  You don't have the needed ingredients!")
            i = msvcrt.getch()
            return 0
    for x in ch.inventory:
        if x.id in needed:
            x.lose_item(needed[x.id])
    if len(ch.spells[name]) == 1:
        c.write('''  You cast the spell and nothing happens - you must have made a mistake in
  the incantation! Your ingredients are wasted and you throw away your useless
  writings on the spell. You will have to start over with the creation.''')
        del(ch.spells[name])
        i = msvcrt.getch()
    else:
        if ch.spells[name]['effect'] == 'Fizzle':
            c.write('''  You cast the spell and feel the energy spread around you without any purpose
  - the spell was useless! Your ingredients are wasted.''')
            del(ch.spells[name])
            i = msvcrt.getch()
        elif ch.spells[name]['effect'] == 'Damage/Healing':
            if ch.spells[name]['target'] == 'Self':
                act = {'-':'destructive','+':'healing'}
                c.write('''\n  The %s energy of the spell focuses on you!''' %act[ch.spells[name]['action']])
                ch.life += eval('%s%d' %(ch.spells[name]['action'],ch.spells[name]['strength']))
                if ch.life > ch.max_life:
                    ch.life = ch.max_life
                i = msvcrt.getch()
            else:
                ch.spell_cast = name
        elif ch.spells[name]['effect'] == 'Invisibility':
            if ch.spells[name]['target'] == 'Self':
                if ch.spells[name]['action'] == '+':
                    ch.effects['invisible']=ch.spells[name]['strength']+5
                    c.write('''\n  You cast the spell and feel the energy fill you up. You become invisible!''')
                    ch.emotion=1
                    i = msvcrt.getch()
                else:
                    c.write('''  You cast the spell and feel the energy spread around you without any purpose
 - the spell was useless! Your ingredients are wasted.''')
                    del(ch.spells[name])
                    i = msvcrt.getch()
            else:
                ch.spell_cast = name

def execute_spell(buff):
    ## Tuk se razreshavat efektite nasocheni kum drugi sushtestva i mesta. Tezi kum igracha sa v cast_spell()
    all_targets = []
    for x in all_creatures:
        if x.mode != 'not_appeared' and max([abs(x.xy[0]-ch.xy[0]),abs(x.xy[1]-ch.xy[1])])<=ch.attr['Mnd'] and clear_los(direct_path(ch.xy,x.xy)):
            all_targets.append(x)
    if len(all_targets):
        message_message('choose_target')
        i=msvcrt.getch()
        l = len(all_targets)
        i = ' '
        current = 0
        while 1:
            target = all_targets[current]
            current += 1
            if current == l:
                current = 0
            old_tag = target.tag
            old_emotion = target.emotion
            target.tag = '*'
            target.emotion = 14
            redraw_screen()
            message_creature('current_target',target)
            target.tag = old_tag
            target.emotion = old_emotion
            i = msvcrt.getch()
            if ord(i) == 13:
                break
        if ch.spells[ch.spell_cast]['effect'] == 'Damage/Healing':
            target.life += eval('%s%d' %(ch.spells[ch.spell_cast]['action'],ch.spells[ch.spell_cast]['strength']))
            if ch.spells[ch.spell_cast]['action'] == '-':
                target.mode = 'hostile'
                message_mode = 'spell_damage'
            else:
                message_mode = 'spell_healing'
            message_creature('%s' %message_mode,target,ch.spells[ch.spell_cast]['strength'])
        elif ch.spells[ch.spell_cast]['effect'] == 'Invisibility':
            target.attr['invisible']=ch.spells[ch.spell_cast]['strength']+5
    else:
        message_message('no_target')
            

def devise_spell():
    c.page()
    c.write('''
  Do you want to choose one of your known spells or create a new one?

  a) Choose spell.
  b) Create a new spell.''')
    i=msvcrt.getch()
    if i == 'a':
        choose_spell()
        return 0
    elif i == 'b':
        strength=0
        target='None'
        effect='unknown effect'
        action=''
        targets={'@':'Self','?':'Other'}
        effects={'a':'Damage/Healing','l':'Invisibility'}
        i1=''
        while strength==0 or target=='None' or effect=='unknown effect' or action=='' or ord(i1)!=13:
            c.page()
            c.write('''
  Choose the effect, strength (1-9) and target of your spell and press ENTER:

   Target:  @) Self.   ?) Other.        Action: +) Positive.  -) Negative.
         
   Effect:  a) Damage/Healing           g) Spirit (affects Cre & End)
            b) Fire (lighting, burning) h) Body (Str & Dex)
            c) Ice (freezing)           i) Mind (Mnd & Int)
            d) Water                    j) Life
            e) Earth                    k) Death
            f) Air (flying, wind)       l) Invisibility

   Effect: %s Strength: %d Target: %s Action: %s''' %(effect,strength,target,action))
            i1 = msvcrt.getch()
            if i1 in 'al':
                effect = effects[i1]
            elif i1 in '123456789':
                strength = float(i1)
            elif i1 in '@?':
                target = targets[i1]
            elif i1 in '-+':
                action = i1
        effect_diffs = {'Damage/Healing':1.0,'Fizzle':0.0,'Invisibility':9.0}
        target_diff = 5.0
        action_diff = 5.0
        total_diff = effect_diffs[effect]+target_diff+action_diff+strength
        if ch.attr['Int']/total_diff > random.random():
            if (ch.attr['Mnd']/target_diff)*.95-ch.attr['Mnd']/total_diff < random.random():
                if target == 'Self':
                    target = 'Other'
                else:
                    target = 'Self'
            if (ch.attr['Mnd']/action_diff)*.95-ch.attr['Mnd']/total_diff < random.random():
                if action == '-':
                    action = '+'
                else:
                    action = '-'
            if (ch.attr['Mnd']/(strength*2))*.95-ch.attr['Mnd']/total_diff < random.random():
                strength = random.randint(1,max([1,strength-1]))
            if (ch.attr['Mnd']/effect_diffs[effect])*.95-ch.attr['Mnd']/total_diff < random.random():
                possible = []
                for x in effect_diffs:
                    if effect_diffs[x] < effect_diffs[effect]:
                        possible.append(x)
                effect = random.choice(possible)
            create_spell(total_diff,effect,strength,target,action)
        else:
            create_spell(total_diff,0)

def create_spell(total_diff,effect,strength=0,target='',action=''):
    c.page()
    c.write('''
  Write the name for your new spell. If you repeat the name of an
  existing spell the old one will be overwritten! ''')
    name = raw_input()
    all_ings = herbs
    ings = []
    n = int(total_diff)/5
    for x in range(n):
        ings.append(random.choice(all_ings))
    if effect == 0:
        ch.spells[name]={'ingredients':ings}
    else:
        ch.spells[name]={'ingredients':ings,'effect':effect,'strength':strength,'target':target,'action':action}

def look():
    key = ' '
    c.pos(*ch.xy)
    xy = ch.xy[:]
    changed=1
    while ord(key) != 13:
        if ch.target and changed:
            changed=0
            redraw_screen()
            highlight_path(direct_path(ch.xy,ch.target))
            c.scroll((ch.target[0],ch.target[1],ch.target[0]+1,ch.target[1]+1),1,1,236,'X')
            c.pos(*xy)
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key=='t':
                changed=1
                ch.target=xy[:]
            md = {'1':[-1,1], '2':[0,1], '3':[1,1], '4':[-1,0], '5':[0,0],
              '6':[1,0], '7':[-1,-1], '8':[0,-1], '9':[1,-1], '0':[0,0]}
            a = 0
            try:
                for a in range(2):
                    xy[a] += md[key][a]
                if (xy[0] == 20) or (xy[0] == 79) or (xy[1] == 0) or (xy[1] == 24):
                    xy[0] -= md[key][0]
                    xy[1] -= md[key][1]
                message_message('')
                c.pos(*xy)
                message_look(xy, all_beings, T, ch.known_areas)
                c.pos(*xy)
            except:
                pass

def change_place(area,direction):
    if area!='areaB':
        run_away = {'Dex':0,'End':0,'Int':0,'Cre':0}
        hostiles = 0
        character_run = 0
        for thing in all_creatures:
            ## Broqt se samo gadinite koito sa na 7 i po malko razstoqnie ot igracha
            if thing.mode == 'hostile' and max([abs(thing.xy[0]-ch.xy[0]),abs(thing.xy[1]-ch.xy[1])])<8 and clear_los(direct_path(thing.xy,ch.xy)):
                hostiles += 1
                for x in run_away:
                    run_away[x] = max([run_away[x],thing.attr[x]])
                    if hostiles == 1:
                        character_run += ch.attr[x]
        if hostiles and 'invisible' not in ch.effects:
            difficulty = sum(run_away.values()+[hostiles])
            chance = 50.0*character_run/difficulty
            if random.randint(1,100) < chance:
                message_message('ran_away')
                msvcrt.getch()
            else:
                message_creature('no_escape',0)
                return 0
    if area != 'area0':
        old_temp=current_place['Temperature']
        places = open('%s//%s_dir//new_%s.dat'%(curdir,ch.name,current_area), 'w')
        pickle.dump(ground_items, places)
        pickle.dump(current_place, places)
        pickle.dump(terrain_type, places)
        pickle.dump(current_area, places)
        pickle.dump(directions, places)
        pickle.dump(land, places)
        pickle.dump(map_coords, places)
        creatures_left=[]
        for creature in all_creatures:
            if creature not in ch.followers+ch.ride+ch.possessed:
                creatures_left.append(creature)
        pickle.dump(creatures_left, places)
        if current_area not in ch.known_areas:
            ch.known_areas.append(current_area)
        places.close()
        new_terr(area,direction)
        draw_hud()
        ch.worked_places={'Nature':[],'Chaos':[],'Order':[]}
        ch.target=[]
        draw_move(ch, ch.xy[0], ch.xy[1])
        if old_temp<33<=current_place['Temperature']:
            for thing in ch.inventory:
                if thing.name=='ring of winter':
                    thing.name+=' (melted)'
                    del(thing.effect['winterwalk'])
        elif current_place['Temperature']<66<=old_temp:
            for thing in ch.inventory:
                if thing.name=='ring of summer':
                    thing.name+=' (withered)'
                    del(thing.effect['summerwalk'])
        for x in all_creatures:
            if x not in hidden and clear_los(direct_path(ch.xy,x.xy)):
                draw_move(x, x.xy[0], x.xy[1])
        c.pos(*ch.xy)
        return 1
    else:
        return 0

def world(current_area):
    entered = -1
    if current_area != 'world':
        data = []
        data.append(terrain_type+' '+current_area+' '+' '.join(directions)+'\n')
        for i in range(23):
            data.append(land[i]+'\n')
        data.append(map_coords)
        creatures_number = 0
        for i in all_creatures:
            if not i.random:
                creatures_number += 1
        data.append(str(creatures_number)+'\n')
        for thing in all_creatures:
            if not thing.random:
                data.append(str(thing.id)+' '+str(thing.xy[0])+' '+str(thing.xy[1])+' '+str(thing.game_id)+' '+str(thing.appearance)+'\n')
            else:
                data.append(str(thing.id)+' '+str(thing.xy[0])+' '+str(thing.xy[1])+' '+str(thing.game_id)+' '+str(ch.turn)+'\n')
        if current_area not in ch.known_areas:
            ch.known_areas.append(current_area)
        places = open(current_area+'.dat', 'w')
        for i in data:
            places.write(i)
        pickle.dump(ground_items, places)

        places.close()
        t = world()
        current_area = 'world'
        ch.place_time = 100
    else:
        for x in world_places:
            if world_places[x] == ch.xy:
                change_place(x, 0)
                current_area = x
                ch.place_time = 1
                entered = 1
                break
        if entered == -1:
            entered = 0
    return current_area, entered

################################ INIT_SCREEN ^^^ ######################
################################ LOAD          #########################

## Load-va savenat fail
def load_terr(f):
    try:
        terr = open(f, 'r')
    except:
        print 'No such file!'
        terr = msvcrt.getch()
        return 0,0
    c.page()
    land = []
    for i in range(23):
        land.append(terr.read(58))
        terr.read(1)
    for x in range(1,24):
        c.pos(21, x)
        for y in range(21,79):
            c.scroll((y,x,y+1,x+1), 1, 1, T[land[x-1][y-21]].colour, T[land[x-1][y-21]].char)
    ch = pickle.load(terr)
    ch.inventory = pickle.load(terr)
    ch.equipment = pickle.load(terr)
    ch.skills = pickle.load(terr)
    ch.spells = pickle.load(terr)
    ch.forces = pickle.load(terr)
    ch.races = pickle.load(terr)
    ch.effects = pickle.load(terr)
    ch.land_effects = pickle.load(terr)
    ch.known_areas = pickle.load(terr)
    ch.weapon_skills = pickle.load(terr)
    ch.attr_colors = pickle.load(terr)
    all_creatures = pickle.load(terr)
    max_id=0
    creature_coords=[]
    for c in all_creatures:
        max_id=max([max_id,c.game_id])
        creature_coords.append(c.xy)
    for fol in ch.followers+ch.ride+ch.possessed:
        if fol.mode!='standing':
            all_beings.append(fol)
            all_creatures.append(fol)
            fol.game_id=max_id+1
            max_id+=1
        if fol.mode=='standing' and fol.attr['area']==area:
            all_beings.append(fol)
            all_creatures.append(fol)
            fol.game_id=max_id+1
            max_id+=1
    hidden = pickle.load(terr)
    for one in hidden:
        for two in all_creatures:
            if one.game_id == two.game_id:
                all_creatures.remove(two)
                all_creatures.append(one)
                break
    all_beings = all_creatures + [ch]
    ground_items = pickle.load(terr)
    directions = pickle.load(terr)
    world_places = pickle.load(terr)
    top_world_places = pickle.load(terr)
    place_descriptions = pickle.load(terr)
    map_coords = pickle.load(terr)
    current_area = pickle.load(terr)
    current_place = pickle.load(terr)
    treasure_modifier = pickle.load(terr)
    lTm = pickle.load(terr)
    terr.close()
    return 1,lTm

## Load-va nachalnata mestnost
def draw_terr(start_force):
    ## Generation of terrain matrix
    for x in range(map_size):
        T_matrix.append([])
        for y in range(map_size):
            T_matrix[x].append({'Nature':33,'Chaos':33,'Order':33,'Population':0,'Treasure':1,'Temperature':0,
                                'Water':10})
    force_points={}
    for each in ['Nature','Chaos','Order','Population','Water']:
        force_points[each]=[]
        for i in range(map_size/2):
            fx = random.randint(0,map_size-1)
            fy = random.randint(0,map_size-1)
            if each=='Population':
                amplitude = random.choice([35,45,60])
            else:
                amplitude = random.choice([10,20,30,40,50])
            for x in range(map_size):
                for y in range(map_size):
                    if abs(x-fx)+abs(y-fy)<amplitude/10:
                        if each in ['Nature','Chaos','Order']:
                            rest=amplitude-(abs(x-fx)+abs(y-fy))*10
                            T_matrix[x][y][each] = min([T_matrix[x][y][each]+rest,100])
                            restf=list(set(['Nature','Chaos','Order'])-set([each]))
                            while rest>0 and not (T_matrix[x][y][restf[0]]==0 and T_matrix[x][y][restf[1]]==0):
                                T_matrix[x][y][restf[0]] -= 1
                                if T_matrix[x][y][restf[0]]>=0:
                                    rest-=1
                                else:
                                    T_matrix[x][y][restf[0]]=0
                                T_matrix[x][y][restf[1]] -= 1
                                if T_matrix[x][y][restf[1]]>=0:
                                    rest-=1
                                else:
                                    T_matrix[x][y][restf[1]]=0
                        elif each=='Population' or each=='Water':
                            T_matrix[x][y][each] = min([T_matrix[x][y][each]+(amplitude-(abs(x-fx)+abs(y-fy))*10),100])
                    if T_matrix[x][y]["Nature"]+T_matrix[x][y]['Order']+T_matrix[x][y]['Chaos']>100:
                        print "Mapping Error:",T_matrix[x][y]["Nature"],T_matrix[x][y]['Order'],T_matrix[x][y]['Chaos']
                        raw_input()
                        raise
    temp_borders=[random.randint(0,30),random.randint(70,100)]
    temp_step=(temp_borders[1]-temp_borders[0])/map_size
    temp_direction=random.choice([[0,1],[1,-1]])
    for x in range(map_size):
        the_temp=temp_borders[temp_direction[0]]+x*temp_direction[1]*temp_step
        for y in range(map_size):
            T_matrix[x][y]['Temperature']+=the_temp
            T_matrix[x][y]['Water']=max([T_matrix[x][y]['Water']-max([the_temp-66,0]),1])
            chance=random.randint(-90,10)
            if chance>0:
                T_matrix[x][y]['Treasure']+=chance
            if T_matrix[x][y][start_force]>max([T_matrix[x][y][f] for f in (set(['Nature','Chaos','Order'])-set([start_force]))]):
                force_points[start_force].append([T_matrix[x][y][start_force],x,y])

    ##Generation of starting terrain - terrain generation procedure
    starter=force_points[start_force][:]
    starter.sort()
    if starter:
        starting_point=starter[-1][1:]
    else:
        starting_point=[random.randint(1,mapsize),random.randint(1,mapsize)]
    direction = 2
    if T_matrix[starting_point[0]][starting_point[1]]['Population']<60:
        T_matrix[starting_point[0]][starting_point[1]]['Population']=60
    current_place=T_matrix[starting_point[0]][starting_point[1]]
    unknown_terrain(starting_point,direction)

    place_descriptions = {'world':'Your country.'}
    area_number=starting_point[0]*map_size+starting_point[1]
    place_descriptions['area%s' %(area_number)] = 'A place of %s.' %(start_force)
    world_places = {'world':[0,0]}
    top_world_places = {}
    return 1

def unknown_terrain(coords,direction):
    c.page()
    land = []
    directions = []
    area_number=coords[0]*map_size+coords[1]
    current_area = 'area%s' %(area_number)
    treasure_modifier = T_matrix[coords[0]][coords[1]]['Treasure']
    if area_number+map_size>(map_size*map_size-1):
        down_dir=0
    else:
        down_dir=area_number+map_size
    if area_number%map_size==0:
        left_dir=0
    else:
        left_dir=area_number-1
    if (area_number+1)%map_size==0:
        right_dir=0
    else:
        right_dir=area_number+1
    directions = [max([0,area_number-map_size]),down_dir,left_dir,right_dir,0,0]
    for x in range(len(directions)):
        directions[x]=str(directions[x])
    land=generate_terr(coords)
    for x in range(1,24):
        for y in range(21,79):
            c.scroll((y,x,y+1,x+1), 1, 1, T[land[x-1][y-21]].colour, T[land[x-1][y-21]].char)
    map_coords = '47 22;47 2;77 12;22 12;0 0;0 0'
    new_coords = map_coords.split(';')
    for i in range(6):
        new_coords[i] = new_coords[i].split(' ')
    spot=[int(new_coords[direction][0]),int(new_coords[direction][1])]
    while not T[land[spot[1]-1][spot[0]-21]].pass_through:
        if direction==0:
            spot[1]-=1
        elif direction==1:
            spot[1]+=1
        elif direction==2:
            spot[0]-=1
        elif direction==3:
            spot[1]+=1
    for i in range(2):
        ch.xy[i] = spot[i]
        
def unknown_Bterrain(coords,direction):
    ## The direction sets the spot in which the character appears, according to his race
    current_place={'Nature':33,'Chaos':33,'Order':33,'Population':0,'Treasure':50,'Temperature':0,'Water':10,
                               'Nspirit':0,'Ospirit':0,'Cspirit':0,'Npop':0,'Opop':0,'Cpop':0}
    for x in range(map_size):
        for y in range(map_size):
            current_place['Nature']=max([T_matrix[x][y]['Nature'],current_place['Nature']])
            current_place['Order']=max([T_matrix[x][y]['Order'],current_place['Order']])
            current_place['Chaos']=max([T_matrix[x][y]['Chaos'],current_place['Chaos']])
            if not T_matrix[x][y]['Nature']==T_matrix[x][y]['Order']==T_matrix[x][y]['Chaos']:
                predominant_f={T_matrix[x][y]['Nature']:'Nature',T_matrix[x][y]['Order']:'Order',
                               T_matrix[x][y]['Chaos']:'Chaos'}
                if predominant_f.keys().count(max(predominant_f.keys()))==1:
                    the_force=predominant_f[max(predominant_f.keys())]
                    the_power=T_matrix[x][y][the_force]-(100-T_matrix[x][y][the_force])/2
                    if T_matrix[x][y]['Population']>20:
                        current_place['%spop' %(the_force[0])]+=the_power
                    else:
                        current_place['%sspirit' %(the_force[0])]+=the_power
##                    else:
    c.page()
    land = []
    directions = []
    area_number=coords[0]*map_size+coords[1]
    current_area = 'area%s' %(area_number)
    treasure_modifier = T_matrix[coords[0]][coords[1]]['Treasure']
    if area_number+map_size>(map_size*map_size-1):
        down_dir=0
    else:
        down_dir=area_number+map_size
    if area_number%map_size==0:
        left_dir=0
    else:
        left_dir=area_number-1
    if (area_number+1)%map_size==0:
        right_dir=0
    else:
        right_dir=area_number+1
    directions = [max([0,area_number-map_size]),down_dir,left_dir,right_dir,0,0]
    for x in range(len(directions)):
        directions[x]=str(directions[x])
    land=generate_terr(coords)
    for x in range(1,24):
        for y in range(21,79):
            c.scroll((y,x,y+1,x+1), 1, 1, T[land[x-1][y-21]].colour, T[land[x-1][y-21]].char)
    map_coords = '47 22;47 2;77 12;22 12;0 0;0 0'
    new_coords = map_coords.split(';')
    for i in range(6):
        new_coords[i] = new_coords[i].split(' ')
    spot=[int(new_coords[direction][0]),int(new_coords[direction][1])]
    while not T[land[spot[1]-1][spot[0]-21]].pass_through:
        if direction==0:
            spot[1]-=1
        elif direction==1:
            spot[1]+=1
        elif direction==2:
            spot[0]-=1
        elif direction==3:
            spot[1]+=1
    for i in range(2):
        ch.xy[i] = spot[i]

##Random terrain generation
def generate_terr(starting_point):
    tp=T_matrix[starting_point[0]][starting_point[1]]
    temp_select = min([tp['Temperature']/33,2])
    terrain_selection={}
    swamp_add=[]
    if tp['Water']>60:
        swamp_add=['~']
    for f in force_terrains:
        if tp[f]<33:
            terrain_selection[f]=force_terrains[f][temp_select][:2]+swamp_add
        elif tp[f]<66:
            terrain_selection[f]=force_terrains[f][temp_select][:-1]+swamp_add
        else:
            terrain_selection[f]=force_terrains[f][temp_select][1:]+swamp_add
    lands=[]
    all_land=''
    done_lands=0
    for f in terrain_selection:
        amount=(1334*tp[f])/100
        for x in range(amount):
            add_terr=random.choice(range(len(terrain_selection[f])))
            if not T[terrain_selection[f][add_terr]].pass_through and random.random()>0.25:
                other_terr=terrain_selection[f][:]
                other_terr.remove(terrain_selection[f][add_terr])
                add_terr=random.choice(other_terr)
                all_land+=add_terr
                done_lands+=1
            elif T[terrain_selection[f][add_terr]].pass_through:
                if random.random()>(add_terr+tp['Population']/10)/10.:
                    all_land+=terrain_selection[f][add_terr]
                    done_lands+=1
                else:
                    all_land+=terrain_selection[f][0]
                    done_lands+=1
            else:
                if terrain_selection[f][add_terr]=='%' and random.random()<0.15:
                    all_land+='m'
                else:
                    all_land+=terrain_selection[f][add_terr]
                done_lands+=1

    if 1334>done_lands:
        for x in range(1334-done_lands):
            add_terr=random.choice(terrain_selection[random.choice(terrain_selection.keys())])
            all_land+=add_terr
    all_land=list(all_land)
    random.shuffle(all_land)
    all_land=''.join(all_land)
    for x in range(0,1334,58):
        lands.append(all_land[x:x+58])
    ##Dobavqne na fermi, kushti, kladenci, ezera
    land_features={}
    game_ids=[]
    creature_coords=[ch.xy[:]]
    if random.random()<tp['Water']/100.:
        terrain_type='w'
        size=random.randint(7,min([15,max([7,tp['Water']/5])]))
        spot=[random.randint(3,19-size),random.randint(3,53-size)]
        land_features[tuple(spot)]=size
        filling=['w','f','%','~']
        for f in terrain_selection:
            filling.append(terrain_selection[f][0])
        for x in range(size):
            to_add=''
            add_x=abs(float(x)-size/2)
            for y in range(size):
                add_y=abs(float(y)-size/2)
                total_add=0
                if x==0 or x==1 or x==size-2 or x==size-1:
                    total_add+=add_x
                if y==0 or y==1 or y==size-2 or y==size-1:
                    total_add+=add_y
                if random.random()>total_add/5.:
                    check_water=random.random()
                    if check_water<(0.05*tp['Treasure']):
                        to_add+='W'
                    elif check_water+tp['Chaos']/100.>0.95:
                        to_add+='t'
                    else:
                        to_add+='w'
                else:
                    to_add+=random.choice(filling)
            lands[spot[0]+x]=lands[spot[0]+x][:spot[1]]+to_add+lands[spot[0]+x][spot[1]+size:]
        creatures = random.randint(0,2)
        if creatures:
            for i in range(creatures):
                ID = random.choice(water_creatures)
                for thing in game_creatures:
                    if ID == thing.id:
                        break
                game_id = i+1
                x = random.randint(21,78)
                y = random.randint(1,23)
                while [x,y] in creature_coords or not T[lands[y-1][x-21]].pass_through or T[lands[y-1][x-21]].id in thing.terr_restr:
                    x = random.randint(21,78)
                    y = random.randint(1,23)
                creation = thing.duplicate(x,y,game_id,thing.force,thing.race,True)
                creature_coords.append(creation.xy[:])
                all_creatures.append(creation)
                game_ids.append(game_id)
    else:
        terrain_type=''
    if tp['Population']>19:
        if land_features=={}:
            wells=random.randint(0,max([tp['Temperature']/30,1]))
            for x in range(wells):
                spot=[random.randint(3,19),random.randint(3,53)]
                land_features[tuple(spot)]=1
                lands[spot[0]]=lands[spot[0]][:spot[1]]+'O'+lands[spot[0]][spot[1]+1:]
        if  tp['Order']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
            farms=random.randint(1,2)
            for x in range(farms):
                size=random.randint(5,min([max([6,tp['Temperature']/8]),10]))
                good_spot=0
                tries=0
                while not good_spot and tries<2000:
                    tries+=1
                    good_spots=0
                    spot=[random.randint(3,19-size),random.randint(3,53-size)]
                    center=[spot[0]+size/2,spot[1]+size/2]
                    if land_features=={}:
                        good_spot=1
                    for s in land_features:
                        center_s=[s[0]+land_features[s]/2,s[1]+land_features[s]/2]
                        min_distance=size/2+size%2+land_features[s]/2+land_features[s]%2+1
                        if max([abs(center[0]-center_s[0]),abs(center[1]-center_s[1])]) > min_distance:
                            good_spots+=1
                    if good_spots==len(land_features):
                        good_spot=1
                if good_spot:
                    land_features[tuple(spot)]=size
                    door=random.randint(0,size-1)
                    for y in range(size):
                        if y==0 or y==size-1:
                            to_add='o'*size
                            if door==y:
                                to_add=to_add[:-3]+'+'
                                to_add=list(to_add)
                                random.shuffle(to_add)
                                to_add=''.join(to_add)
                                to_add='o'+to_add+'o'
                            lands[spot[0]+y]=lands[spot[0]+y][:spot[1]]+to_add+lands[spot[0]+y][spot[1]+size:]
                        else:
                            to_add='a'*(size-2)
                            the_fence=['o','o']
                            if door==y:
                                the_fence[random.randint(0,1)]='+'
                            lands[spot[0]+y]=lands[spot[0]+y][:spot[1]]+the_fence[0]+to_add+the_fence[1]+lands[spot[0]+y][spot[1]+size:]
        creatures = random.randint(0,tp['Population']/10)
        if creatures:
            resident_type=[]
            if  tp['Order']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
                resident_type.append('Order')
            if  tp['Nature']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
                resident_type.append('Nature')
            if  tp['Chaos']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
                resident_type.append('Chaos')
            if game_ids:
                add_id=max(game_ids)
            else:
                add_id=1
            for i in range(creatures):
                c_force=random.choice(resident_type)
                c_race=random.choice(ch.races[c_force].keys())
                ID = 1
                game_id = i+add_id+1
                game_ids.append(game_id)
                x = random.randint(21,78)
                y = random.randint(1,23)
                while [x,y] in creature_coords or not T[lands[y-1][x-21]].pass_through or T[lands[y-1][x-21]].id in wood.terr_restr:
                    x = random.randint(21,78)
                    y = random.randint(1,23)
                creation = wood.duplicate(x,y,game_id,c_force,c_race,True)
                creature_coords.append(creation.xy[:])
                all_creatures.append(creation)
    if random.randint(0,100)<100-tp['Population']:
        creatures = random.randint(0,3)
        if creatures:
            if game_ids:
                add_id=max(game_ids)
            else:
                add_id=1
            for i in range(creatures):
                c_force=random.choice(['Nature']*tp['Nature']+['Order']*tp['Order']+['Chaos']*tp['Chaos'])
                if tp['Temperature']<34:
                    c_temp='cold'
                elif tp['Temperature']<66:
                    c_temp='warm'
                else:
                    c_temp='hot'
                ID = random.choice(random_by_force[c_force][c_temp])
                for thing in game_creatures:
                    if ID == thing.id:
                        break
                game_id = i+add_id+1
                game_ids.append(game_id)
                x = random.randint(21,78)
                y = random.randint(1,23)
                while [x,y] in creature_coords or not T[lands[y-1][x-21]].pass_through or \
                      (T[lands[y-1][x-21]].id in thing.terr_restr and thing.race!='plant') or \
                      T[lands[y-1][x-21]].id in ['pa']:
                    x = random.randint(21,78)
                    y = random.randint(1,23)
                creation = thing.duplicate(x,y,game_id,thing.force,thing.race,True)
                creature_coords.append(creation.xy[:])
                all_creatures.append(creation)
                
    if tp['Population']>35:
        village_type=[]
        if  tp['Order']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
            village_type.append('Order')
        if  tp['Nature']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
            village_type.append('Nature')
        if  tp['Chaos']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
            village_type.append('Chaos')
        houses=random.randint(1,(tp['Population']-25)/5)
        add_ons=list(house_generated[:])
        for x in range(houses):
            house_type=random.choice(village_type)
            if house_type=='Nature' or house_type=='Chaos':
                add_on=cauldron
            else:
                if add_ons:
                    add_on=random.choice(add_ons)
                    add_ons.remove(add_on)
                else:
                    add_on=cauldron
            good_spot=0
            tries=0
            while not good_spot and tries<2000:
                tries+=1
                good_spots=0
                size=min([15,random.randint(4, 4+(tp['Population']-35)/5)])
                if house_type=='Nature' and size<5:
                    size=5
                spot=[random.randint(3,19-size),random.randint(3,53-size)]
                center=[spot[0]+size/2,spot[1]+size/2]
                if land_features=={}:
                    good_spot=1
                for s in land_features:
                    center_s=[s[0]+land_features[s]/2,s[1]+land_features[s]/2]
                    min_distance=size/2+size%2+land_features[s]/2+land_features[s]%2+1
                    if max([abs(center[0]-center_s[0]),abs(center[1]-center_s[1])]) > min_distance:
                        good_spots+=1
                if good_spots==len(land_features):
                    good_spot=1
            if good_spot:
                for person in range(size/4):
                    if game_ids:
                        add_id=max(game_ids)
                    else:
                        add_id=1
                    c_force=house_type
                    c_race=random.choice(ch.races[c_force].keys())
                    ID = 2
                    game_id = 1+add_id
                    game_ids.append(game_id)
                    x = random.randint(21,78)
                    y = random.randint(1,23)
                    while [x,y] in creature_coords or not T[lands[y-1][x-21]].pass_through or T[lands[y-1][x-21]].id in wood.terr_restr:
                        x = random.randint(21,78)
                        y = random.randint(1,23)
                    creation = wood_perm.duplicate(x,y,game_id,c_force,c_race,False)
                    creature_coords.append(creation.xy[:])
                    all_creatures.append(creation)
                ground_items.append([center[1]+21,center[0]+1,add_on.duplicate(1)])
                land_features[tuple(spot)]=size
                door=random.randint(0,size-1)
                for y in range(size):
                    if house_type=='Order':
                        if y==0 or y==size-1:
                            to_add='#'*size
                            if door==y:
                                to_add=to_add[:-3]+'+'
                                to_add=list(to_add)
                                random.shuffle(to_add)
                                to_add=''.join(to_add)
                                to_add='#'+to_add+'#'
                            lands[spot[0]+y]=lands[spot[0]+y][:spot[1]]+to_add+lands[spot[0]+y][spot[1]+size:]
                        else:
                            to_add='p'*(size-2)
                            the_wall=['#','#']
                            if door==y:
                                the_wall[random.randint(0,1)]='+'
                            lands[spot[0]+y]=lands[spot[0]+y][:spot[1]]+the_wall[0]+to_add+the_wall[1]+lands[spot[0]+y][spot[1]+size:]
                    elif house_type=='Nature':
                        if door==1:
                            door=0
                        elif door==size-2:
                            door=size-1
                        if y==0 or y==size-1:
                            to_add='g'+'J'*(size-2)+'g'
                            if door==y:
                                to_add='J'*(size-5)+'b'
                                to_add=list(to_add)
                                random.shuffle(to_add)
                                to_add=''.join(to_add)
                                to_add='gJ'+to_add+'Jg'
                            lands[spot[0]+y]=lands[spot[0]+y][:spot[1]]+to_add+lands[spot[0]+y][spot[1]+size:]
                        elif y==1 or y==size-2:
                            to_add='JJ'+'g'*(size-4)+'JJ'
                            lands[spot[0]+y]=lands[spot[0]+y][:spot[1]]+to_add+lands[spot[0]+y][spot[1]+size:]
                        else:
                            to_add='g'*(size-2)
                            the_wall=['J','J']
                            if door==y:
                                the_wall[random.randint(0,1)]='b'
                            lands[spot[0]+y]=lands[spot[0]+y][:spot[1]]+the_wall[0]+to_add+the_wall[1]+lands[spot[0]+y][spot[1]+size:]
                    elif house_type=='Chaos':
                        if y==0 or y==size-1:
                            to_add='#'*size
                            if door==y:
                                to_add=to_add[:-3]+'+'
                                to_add=list(to_add)
                                random.shuffle(to_add)
                                to_add=''.join(to_add)
                                to_add='#'+to_add+'#'
                            lands[spot[0]+y]=lands[spot[0]+y][:spot[1]]+to_add+lands[spot[0]+y][spot[1]+size:]
                        else:
                            bone_add=random.randint(1,2)*'B'
                            to_add='.'*(size-2-len(bone_add))+bone_add
                            to_add=list(to_add)
                            random.shuffle(to_add)
                            to_add=''.join(to_add)
                            the_wall=['#','#']
                            if door==y:
                                the_wall[random.randint(0,1)]='+'
                            lands[spot[0]+y]=lands[spot[0]+y][:spot[1]]+the_wall[0]+to_add+the_wall[1]+lands[spot[0]+y][spot[1]+size:]

    all_beings += all_creatures
    return lands

## Loads terrain when traveling
def new_terr(area,direction,f=''):
    if area in ch.known_areas:
        try:
            f = curdir+'//%s_dir//new_%s.dat' %(ch.name,area)
            terr = open(f, 'r')
        except IOError:
            f = curdir+'//%s_dir//%s.dat' %(ch.name,area)
            try:
                terr = open(f, 'r')
            except IOError:
                ch.known_areas.remove(area)
                new_terr(area,direction)
                return 0
        ground_items = pickle.load(terr)
        current_place = pickle.load(terr)
        tp=current_place
        c.page()

        terrain_type = pickle.load(terr)
        current_area = pickle.load(terr)
        directions = pickle.load(terr)
        if terrain_type=='w':
            waters=36
        else:
            waters=0
        land = pickle.load(terr)
        map_coords = pickle.load(terr)
        all_creatures = pickle.load(terr)
        for x in range(1,24):
            for y in range(21,79):
                c.scroll((y,x,y+1,x+1), 1, 1, T[land[x-1][y-21]].colour, T[land[x-1][y-21]].char)
##        map_coords = terr.readline()
##        new_coords = map_coords[:len(map_coords)-1].split(';')
                
        new_coords = map_coords.split(';')
        
        for i in range(6):
            new_coords[i] = new_coords[i].split(' ')
        spot=[int(new_coords[direction][0]),int(new_coords[direction][1])]
        while not T[land[spot[1]-1][spot[0]-21]].pass_through:
            if direction==0:
                spot[1]-=1
            elif direction==1:
                spot[1]+=1
            elif direction==2:
                spot[0]-=1
            elif direction==3:
                spot[1]+=1
        ch.xy = spot[:]
        treasure_modifier = current_place['Treasure']
        hidden = []
        all_beings = [ch]
        creature_coords=[ch.xy[:]]
        game_ids = []

        randoms=0
        if len(all_creatures):
            to_remove=[]
            for each_creature in all_creatures:
                if each_creature.random:
                    appear = 100-min([99,ch.turn-each_creature.appearance])
                    if random.randint(1,100)<=appear:
                        randoms=1
                        all_beings.append(each_creature)
                        creature_coords.append(each_creature.xy[:])
                        game_ids.append(each_creature.game_id)
                    else:
                        to_remove.append(each_creature)
                else:
                    if each_creature.appearance == 0:
                        all_beings.append(each_creature)
                        creature_coords.append(each_creature.xy[:])
                        game_ids.append(each_creature.game_id)
                    else: #if each_creature.id not in random_creatures:
                        if random.randint(1,1000)>each_creature.appearance:
                            each_creature.mode = 'not_appeared'
                            hidden.append(each_creature)
                        else:
                            all_beings.append(each_creature)
                            creature_coords.append(each_creature.xy[:])
                            game_ids.append(each_creature.game_id)
            for rem in to_remove:
                all_creatures.remove(rem)
        if not randoms:
            if current_place['Population']<20:
                creatures = random.randint(0,2)
                if creatures:
                    if game_ids:
                        add_id=max(game_ids)
                    else:
                        add_id=1
                    for i in range(creatures):
                        c_force=random.choice(['Nature']*tp['Nature']+['Order']*tp['Order']+['Chaos']*tp['Chaos'])
                        if tp['Temperature']<34:
                            c_temp='cold'
                        elif tp['Temperature']<66:
                            c_temp='warm'
                        else:
                            c_temp='hot'
                        ID = random.choice(random_by_force[c_force][c_temp])
                        for thing in game_creatures:
                            if ID == thing.id:
                                break
                        game_id = i+add_id+1
                        game_ids.append(game_id)
                        x = random.randint(21,78)
                        y = random.randint(1,23)
                        while [x,y] in creature_coords or not T[land[y-1][x-21]].pass_through or \
                              (T[land[y-1][x-21]].id in thing.terr_restr and thing.race!='plant') or \
                              T[land[y-1][x-21]].id in ['pa']:
                            x = random.randint(21,78)
                            y = random.randint(1,23)
                        creation = thing.duplicate(x,y,game_id,thing.force,thing.race,True)
                        creature_coords.append(creation.xy[:])
                        all_creatures.append(creation)
            else:
                creatures = random.randint(0,tp['Population']/10)
                if creatures:
                    resident_type=[]
                    if  tp['Order']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
                        resident_type.append('Order')
                    if  tp['Nature']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
                        resident_type.append('Nature')
                    if  tp['Chaos']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
                        resident_type.append('Chaos')
                    if game_ids:
                        add_id=max(game_ids)
                    else:
                        add_id=1
                    for i in range(creatures):
                        c_force=random.choice(resident_type)
                        c_race=random.choice(ch.races[c_force].keys())
                        ID = 1
                        game_id = i+add_id+1
                        game_ids.append(game_id)
                        x = random.randint(21,78)
                        y = random.randint(1,23)
                        while [x,y] in creature_coords or not T[land[y-1][x-21]].pass_through or T[land[y-1][x-21]].id in wood.terr_restr:
                            x = random.randint(21,78)
                            y = random.randint(1,23)
                        creation = wood.duplicate(x,y,game_id,c_force,c_race,True)
                        creature_coords.append(creation.xy[:])
                        all_creatures.append(creation)
            if waters>35:
                creatures = random.randint(0,2)
                if creatures:
                    if game_ids:
                        add_id=max(game_ids)
                    else:
                        add_id=1
                    for i in range(creatures):
                        ID = random.choice(water_creatures)
                        for thing in game_creatures:
                            if ID == thing.id:
                                break
                        game_id = i+add_id+1
                        game_ids.append(game_id)
                        x = random.randint(21,78)
                        y = random.randint(1,23)
                        while [x,y] in creature_coords or not T[land[y-1][x-21]].pass_through or T[land[y-1][x-21]].id in thing.terr_restr:
                            x = random.randint(21,78)
                            y = random.randint(1,23)
                        creation = thing.duplicate(x,y,game_id,thing.force,thing.race,True)
                        creature_coords.append(creation.xy[:])
                        all_creatures.append(creation)
                            
        all_beings += all_creatures
        draw_items()
        terr.close()
    else:
        an=area[4:]
        if an=='B':
            coords=[0,0]
            all_creatures = []
            hidden = []
            ground_items = []
            all_beings = [ch]
            unknown_Bterrain(coords,direction)
            predominant_f={current_place['Nature']:'Nature',current_place['Order']:'Order',
                           current_place['Chaos']:'Chaos'}
            place_descriptions['area%s' %(an)] = 'A place of %s.' %(predominant_f[max(predominant_f.keys())])
        else:
            an=int(an)
            coords=[an/map_size,an%map_size]
            current_place=T_matrix[coords[0]][coords[1]]
            all_creatures = []
            hidden = []
            ground_items = []
            all_beings = [ch]
            unknown_terrain(coords,direction)
            predominant_f={T_matrix[coords[0]][coords[1]]['Nature']:'Nature',T_matrix[coords[0]][coords[1]]['Order']:'Order',
                           T_matrix[coords[0]][coords[1]]['Chaos']:'Chaos'}
            place_descriptions['area%s' %(an)] = 'A place of %s.' %(predominant_f[max(predominant_f.keys())])
    max_id=0
    creature_coords=[]
    for c in all_creatures:
        max_id=max([max_id,c.game_id])
        creature_coords.append(c.xy)
    for fol in ch.followers+ch.ride+ch.possessed:
        if fol.mode!='standing':
            all_beings.append(fol)
            all_creatures.append(fol)
            fol.game_id=max_id+1
            max_id+=1
            if fol in ch.ride or fol in ch.possessed:
                x = 1
                y = 1
            else:
                x = random.randint(max([ch.xy[0]-3,21]),min([78,ch.xy[0]+3]))
                y = random.randint(max([ch.xy[1]-3,1]),min([23,ch.xy[1]+3]))
                while [x,y] in creature_coords or not T[land[y-1][x-21]].pass_through or T[land[y-1][x-21]].id in fol.terr_restr:
                    x = random.randint(max([ch.xy[0]-3,21]),min([78,ch.xy[0]+3]))
                    y = random.randint(max([ch.xy[1]-3,1]),min([23,ch.xy[1]+3]))
            fol.xy=[x,y]
        if fol.mode=='standing' and fol.attr['area']==area:
            all_beings.append(fol)
            all_creatures.append(fol)
            fol.game_id=max_id+1
            max_id+=1
    return 1

def world():
    f = 'dat'
    terr = open(f, 'r')
    c.page()
    land = []
    places = {}
    place_descriptions = {}
    line = ''
    while 'world' not in line:
        line = terr.readline()
    directions = line[:len(line)-1].split(' ')[1:]
    for i in range(23):
        land.append(terr.read(58))
        terr.read(1)

    areas = terr.readline()
    if int(areas):
        for i in range(int(areas)):
            line = terr.readline()
            chop = line[:len(line)-1].split(':')
            xy = [int(chop[1]),int(chop[2])]
            if current_area == 'area'+chop[0]:
                ch.xy[0] = xy[0]
                ch.xy[1] = xy[1]
            world_places['area'+chop[0]] = xy
            if not chop[4]:
                top_world_places[str(xy)] = chop[3]
            place_descriptions['area'+chop[0]] = chop[3]

    ground_items = []
    all_beings = [ch]
    all_creatures = []
    hidden = []

    terr.close()
    return 1

################################ LOAD ^^^ #########################
################################ MESSAGE #########################

def message_message(x):
    md = {'wall':'You hit a wall!', '?':'What?', 'wait':'You wait.', 'tree':'You walk under a tree.',
          'rock':'You can\'t go through rocks!', 'break_rock':'You smash the rock to pieces!', 'q':'Save the game? (y/n)',
          'ch':'  CHECK!', 'break_wall':'You break down the wall!', 'cut_tree':'You cut the tree down.',
          'log':'A tree log lays here.', 
          'water':'You splash into the water.', 'magic_water':'You step into the sparkling water.',
          'no_drink':'There\'s nothing here to drink!','no_pickup':'There\'s nothing here to pick up!',
          'work':'What do you want to interact with?(direction)','direction':'That is not a direction!',
          'how_much':'How much do you want to drop?','pickup':' How much do you want to take?',
          'sit':'You sit down.','look':"You look around. (press 't' to target)",'unequipable':'That can not be equipped!',
          'takeoff_first':'You have to unequip something first!','cant_work':"You can't work on that.",
          'no_fill':'There is nothing to fill the container with.','nowhere_togo':'You have nowhere to go in that direction.',
          'up_stair':'There is a stair going up here.','down_stair':'There is a stair going down here.',
          'going_down':'You go down the stairs...','going_up':'You go up the stairs...',
          'no_stairs':'There are no stairs here!','no_exit':'You have to go in the open to leave this place!',
          'open_door':'You open the door.','close_door':'You close the door.','no_open':'There is nothing to open here.',
          'blocked_door':'The door is blocked!','which_open':'What do you want to open or close?(direction)',
          'cut_log':'You chop the log to smaller pieces.','drop_first':'You have to drop something first!',
          'no_sit':"You can't sit down here!",'drown':'You are drowning!','ran_away':'You escape the area safely!',
          'no_gather':" You can't gather any herbs here.",'failed_gather':" You did not find any herbs.",
          'choose_target':"Choose the target for your spell.",'no_target':"There is no valid target near you.",
          'failed_lockpick':"You failed to pick the lock!",'success_lockpick':"You successfully open the lock!",
          'dig_earth':'You dig in the earth.','need_dirt':' You have to uncover some dirt before planting seeds!',
          'plant_seed':' You plant the seed in the ground!','cant_fit_in_container':' There is no place for this in there!',
          'jungle':"You can't pass through the undergrowth!",'bush':'You press forward through the bushes.',
          'lichen':'You step on the thick lichen cover.','ice':'You try not to slip on the ice!',
          'ice_block':"You can't pass through the thick ice!",
          'd_tree':'You pass under a sickly looking tree.','frozen_tree':'You walk under a frozen tree.',
          'lava':"You can't walk through the lava!",'movement_error':'ERROR IN MOVEMENT MODULE!',
          'leave_world':'You are at the borders of your world. Nothing is beyond this point.',
          'well_pass':"You pass near a waterwell.",'walk_bones':'Bones crunch under your feet.',
          'dig_bones':'You dig through the remains.','fence':'You bump in a fence.','break_fence':'You tear the fence down.',
          'swamp':'The swamp drags your feet down.','clean_grass':'You clean the grass from twigs and rocks.',
          'stomp_grass':'You stomp the grass and leave it dying.','propose_plant':'You can plant a seed here if you have one.',
          'cover_bones':'You bury the gruesome remains.','clean_tree':'You remove the old leaves and branches from the tree.',
          'fire_tree':'You set the tree on fire!','heal_grass':'You treat the soil with some herbs and the grass shows improvement.',
          'fire_grass':'You purify the diseased grass with fire!','heal_tree':'You apply some medicine on the tree.',
          'thaw_tree':'You carefully remove the ice from the tree with fire.','tear_tree':'You tear the tree down!',
          'forage':'You search for food.','root_bushes':'You uproot the bush from the ground.',
          'fire_bush':'You set fire to the bushes!','ravage_lichen':'You destroy the beautiful lichens!',
          'call_the_seed':'You call forward the core around which the lichen has formed!',
          'touch_rock':"You caress the surface of the rock and feel Nature's power through it.",
          'clean_well':'You clean the well from rocks and weeds.','crush_well':'You destroy the well!',
          'paint_wall':'You try to freshen the wall with some colorful clay.',
          'strenghten_wall':'You fill the cracks in the wall with some clay.',
          'paint_fence':'You hang some flowers on the fence.','strenghten_fence':'You make sure the fence is firmly attached to the ground.',
          'remove_pavement':'You pry the cobblestones from the ground.','repair_pavement':'You fix some shaky stones in the pavement.',
          'destroy_pavement':'You break the stones and scatter the remains around.','dig_sand':'You dig in the sand.',
          'lay_earth':'You lay some earth over the sands.','remove_swamp':'You dig some canals and the water drains away.',
          'remove_snow':'You shovel away the snow.','thaw_ice':'You melt the ice with fire.','break_ice':'You break the ice.',
          'care_log':'You check the log for new shoots and clean the space around them.','clean_water':'You clean the water from junk and dead fish.',
          'search_water':'You search the bottom.','contaminate_water':'You throw some foul junk in the water.',
          'honor_water':'You observe the sparkling water, silently thanking Nature for this gift.','stop_waterfall':'You dig a ditch and reroute the water.',
          'destroy_waterfall':'You crush the rocks and destroy the waterfall.',
          'ritual_calm_fire':'You sit near the lava and call on the forces of Earth to accept it back.',
          'ritual_suppress_fire':'You stand near the lava and call on the forces of Earth to subdue it!',
          'ritual_awaken_fire':'You dance around the lava and call on the forces of Fire to give you power!',
          'need_farm':'You need to soften the earth before planting this seed.',
          'need_human3':'You have to be 90% human to study other races.','clear_build_site':'You have to clear the junk away before building!',
          'need_human1&dwarf1':'You have to be 30% human or dwarf to build!','break_door':'You break the door down!',
          'paint_door':'You hang some flowers on the door.','strenghten_door':'You make some minor repairs to the door.',
          'good_water':'The water drains your hunger away.','bad_water':'The dirty water makes you sick to your stomach!',
          'not_in_waterform':"You can't do that right now, you are water in the ground!",
          'reform_waterform':'The magical water sparkles as your new body forms out of it!',
          'target_first':'You have to choose a target first!','need_ranged_weapon':'You have to equip a ranged weapon to shoot!',
          'need_ammo':"You've got no ammo equipped.",'wrong_ammo':'Your ammunition is the wrong type!',
          'cant_hit_with_bow':'You are holding a ranged weapon!','day_troll':'The sun slows you down!',
          'cant_guard':'This is not a guard animal!','full_animal':"The animal doesn't want to eat any more.",
          'cant_farm':'This animal does not produce anything useful.','nothing_to_farm':'You have to wait a bit to do that.',
          'cant_ride':'You can not ride this animal.','no_riding_fighting':"You can't fight while riding!",
          'save_failed':'Save failed!','hungry_mount':"It looks hungry and won't run fast at all.",
          'normal_mount':"It doesn't look hungry and will run fast for some time.",'well_fed_mount':"It looks well fed and can run for a long time.",
          'dismount':'You jump down from your mount.','kraken_move':'You move swiftly through the murky water.',
          'gnome_move':'Your body mixes with the stone as you push through.','found_gem':'You break the rock and a precious stone shines between the pieces!',
          'failed_smelt':'You put the ore in the fire but nothing usefull comes out.','found_metal':'Shiny streaks of metal combine into an ingot in the forge!',
          'chaos_spirit_move':'Plants around you wither from the force of chaos!','goblin_move':'Your filth is left in the water you pass through!',
          'nature_spirit_move':'The sickly grass under your feet grows green again!','fairy_move':'Grass grows from the soil at your touch!',
          'dryad_move':'Living energy streams up the tree from your lightest touch!','dryad_heal_tree':'You channel the power of Nature through the fallen trunk as it regrows!',
          'cant_fit_container':'You cannot put this in itself!','need_dryad3':'You have to be 90% dryad to grow trees and items!',
          'dryad_song':'You sing to the saplings and seeds. Nature around you awakens slowly.',
          'gnome_touch':'You feel a gem under the surface of the rock!','fairy_flowers':'You find a rare flower!',
          'fairy_snowmove':'You step graciously on the surface of the snow.','fairy_icemove':\
          'Snowflakes swirl around you as you walk over the slippery ice.','fairy_sandmove':\
          'Not a grain of sand moves under your feet as you walk through the dunes.',
          'flower_dress':'You need 50 wild flowers in your bag and 15 on the ground to make this!',
          'not_when_possessed':'You cannot do this while possessing a creature!','cant_ride_two':'You cannot ride two mounts at once!',
          'not_hungry':'You are not hungry yet.','eating_wild_horse':'You find some nice grass to graze on.',
          'no_food_wild_horse':'There is no good grass to eat here...','eating_cattle':'You find some nice grass to graze on.',
          'no_food_cattle':'There is no good grass to eat here...','eating_squirrel':'You climb up the tree and eat what seeds and nuts you find.',
          'no_food_squirrel':'There is nothing for a squirrel to eat here...','eating_snake':'You slither through the tall grass and find a birds nest with eggs. Yummy!',
          'no_food_snake':'There is nothing for a snake to eat here...','eating_poison_snake':'You slither through the tall grass and find a birds nest with eggs. Yummy!',
          'no_food_poison_snake':'There is nothing for a snake to eat here...','eating_camel':'You chew on some low leaves and branches.',
          'no_food_camel':'There is nothing for a camel to eat here...','eating_giant_lizard':'You use your flickering tongue to search for insects in the dirt.',
          'no_food_giant_lizard':'There is nothing for a lizard to eat here...','eating_penguin':'You dive in the water and chase a school of fish until you catch one.',
          'no_food_penguin':'There is no fish around here...','eating_polar_bear':'You splash in the water and catch a fish.',
          'no_food_polar_bear':'There is no fish around here...','eating_monkey':'You climb up the tree and fing some fruit.',
          'no_food_monkey':'There is nothing to eat here...','eating_bear':'You rummage in the bushes for some berries.',
          'no_food_bear':'There is nothing for a bear here...','eating_chicken':'You cluck and pick some seeds fron the ground.',
          'no_food_chicken':'There is nothing to peck here...','eating_fish':'You nibble at some weeds in the water.',
          'no_food_fish':'The water here is dirty and lifeless...','eating_plant':'Your roots pierce the ground and collect water and minerals.',
          'no_food_plant':'The ground is rocky and dry...','eating_carnivore':'You tear a piece of meat and eat it!',
          'no_food_carnivore':'There is no meat here...','diamond_mess':'You drop the diamond and it disappears in the depths with a sparkle.',
          'cant_use_gem':'The gem sparkles in your hand.','topaz_mess':'The topaz glows and melts into your palm, filling you with energy!',
          'emerald_mess':'The blades of grass at your feet glitter with life that flows into you!',
          'garnet_mess':'The gem flashes and disappears with a loud crack!','opal_mess':'The rock around you swirls and you melt in it, appearing somewhere else!',
          'turquoise_mess':'The gem dissolves in a wave of glittering motes and the water around clears     like a crystal!',
          'tourmaline_mess':'The ground shakes and a slab of stone shoots up, engulfing you as it goes!',
          'aquamarine_mess':'A trickle of water breaks the ground at your feet and forms a pond!',
          'sapphire_mess':'The sapprire glows and bathes your surroundings in ice blue light! ',
          'ruby_mess':"The ruby reflects the fire's light and emits a wave of heat! ",
          'lapis_mess':'The stone sucks you in and you are transported somewhere else!',
          'amethyst0':"You remove the mark from the stone.",'amethyst1':"The amethyst shines brightly and marks the stone around you"}
    c.pos(0,0)
    try:
        if x not in ['work','no_fill','which_open','how_much','q','pickup','look','ran_away','need_human1&dwarf1','need_dryad3',
                     'no_riding_fighting','save_failed','break_rock','found_gem','found_metal','failed_smelt','clear_build_site',
                     'cant_fit_container','?','dryad_song','need_human3','not_when_possessed','no_gather','failed_gather']:
            combat_buffer+=' '+md[x]
        else:
            c.write(md[x])
    except:
        c.rectangle((0,0,80,1))

def message_tool_msg(x,t):
    md={'no_tool':'You don\'t have the appropriate tool! (%s)',}
    c.pos(0,0)
    try:
        c.write(md[x] %(', '.join(t)))
    except:
        c.rectangle((0,0,80,1))

def message_emotion(x,t=0):
    md = {'tired':'You are too tired!', 'not_tired':'You are no longer tired.',
          'exhausted':'You are too exhausted to work, you need sustenance!',
          'not_tough':'You are not tough enough to work effectively, increase your endurance!',
          'hostiles':"You can't focus on this, you are under attack!",
          'gain_waterform':'You drain in the ground! You have %d turns to find magic water to reform!'}
    c.pos(0,0)
    try:
        if x=='gain_waterform':
            print md[x] %(t)
        else:
            print md[x]
    except:
        c.rectangle((0,0,80,1))

def message_creature(x, a, dmg=0,d=''):
    md = {'bump':'You bump into %s.','hit':'You hit the %s for %d!','crit':'You crit the %s for %d!',
          'kill':'You slay the %s!','creature_hit':'The %s hits you for %d!','miss':'You miss the %s!',
          'creature_miss':'The %s misses you!','no_escape':'You fail to lose your pursuers! ',
          'current_target':"Current target: %s.",'spell_damage':"Your spell hits the %s for %d!",
          'crit_kill':'You finish the %s off with deadly precision!','spell_healing':"Your magic heals the %s for %d!",
          'talk':'Do you want to talk to the %s? (y/n)','attack':'Do you want to attack the %s? (y/n)',
          'elf_kill':"You drive an arrow through the %s's eye!",'dodged':'The %s dodges your arrow!',
          'creature_dodged':"You dodge the %s's projectile!",'creature_hits_creature':'The %s hits the %s for %d!',
          'tame':'Will you try taming the %s? (y/n)','tamed_use':'Do you want to give the %s a command? (y/n)',
          'tame_success':'The %s looks friendlier.','tame_fail':"You fail to catch the %s's attention.",
          'command_follow':'The %s starts following you.','command_stay':"The %s holds it's ground.",
          'command_guard':'The %s will protect you now.','feed':'You feed the %s.','mount':"You mount the %s.",
          "kraken_death":'You twist around the %s and drag it under the surface of the water!',
          'steal':"Do you want to pick the %s's pocket? (y/n)",'steal_failed':'The %s notices you and attacks!',
          'pilfer':"The %s doesn't notice your attempt.",'pilfer_last':"You find some coppers in the %s's pocket.",
          'no_pilfer':"There's nothing more in the %s's pockets!",'fairyland_hit':'The %s cries in agony (%d) as its weapon tears through your beauty!',
          'possess':'Do you want to try and possess the %s? (y/n)','anger_animal':'The %s suddenly attacks you!',
          'possessed_animal':'You dissipate and melt into the %s.','unpossess':'Your spirit drifts out of the %s and reforms.',
          'transform_into':'You turn into a %s!','transform_outof':'You reform back and no longer resemble a %s.',
          'sapphired':{0:'The %s is covered with ice!',1:'The %s is covered with frost!',2:'The %s starts trembling from the cold!'},
          'rubied':{0:'The %s is lit on fire!',1:"The %s's clothes turn to cinders!",2:'The %s screams in pain as the wave engulfs it!'}}
    c.pos(0,0)
    try:
        if x == 'hit' or x == 'crit' or x == 'creature_hit' or x == 'spell_damage' or x=='fairyland_hit':
            mess = md[x] %(a.race,dmg)
            combat_buffer += mess+' '
        elif  x == 'kill' or x == 'elf_kill' or x == 'crit_kill' or x == 'miss' or x == 'creature_miss':
            mess = md[x] %(a.race)
            combat_buffer += mess+' '
        elif x == 'no_escape':
            combat_buffer += md[x]
        elif x == 'creature_hits_creature':
            combat_buffer += md[x] %(a.race,d.name,dmg)
        elif x in ['talk','attack','tame','tamed_use','command_follow','command_stay','command_guard','steal','possess']:
            print md[x] %(a.race)
        elif x == 'sapphired':
            if a.life<1:
                combat_buffer += 'The %s falls frozen to the ground!' %(a.race)+' '
            elif a.life/5>2:
                combat_buffer += 'The %s shrugs off the cold wave.' %(a.race)+' '
            else:
                combat_buffer += md[x][int(a.life/5)] %(a.race)+' '
        elif x == 'rubied':
            if a.life<1:
                combat_buffer += 'The %s falls to the ground charred!' %(a.race)+' '
            elif a.life/5>2:
                combat_buffer += 'The %s grunts as the heat washes over it.' %(a.race)+' '
            else:
                combat_buffer += md[x][int(a.life/5)] %(a.race)+' '
        else:
            combat_buffer += md[x] %a.name
    except:
        c.rectangle((0,0,80,1))

def message_creatures(x, a, b, dmg=0):
    md = {'miss_attack':'The %s jumps at the %s and misses!','good_attack':'The %s hits the %s for %d!',
          'kill':'The %s finishes the %s off!'}
    c.pos(0,0)
    try:
        if x=='miss_attack' or x=='kill':
            combat_buffer += md[x] %(a.race, b.race)
        else:
            combat_buffer += md[x] %(a.race, b.race, dmg)
    except:
        c.rectangle((0,0,80,1))

def message_use(x, a, qty=1, xy=[]):
    md = {'drink':'You drink from the %s.','over_drink':'You can\'t drink the %s, you are full!',
          'over_eat':'You can\'t eat the %s, you are full!','cant_carry':'You can\'t carry the %s, it\'s too heavy!',
          'gr_item':'There is %s here.','pickup':'You take the %s.','create_drop':'You can\'t carry the %s and drop it.',
          'cant_fit_in_backpack':'There is no place in your backpack for the %s!','no_lockpick':"The %s is locked and you don't have a lockpick.",
          'taming_item':'You need some %ss to try and tame that animal.','feed_item':'You need some %ss to feed that animal.',
          'farm_harvest':'You get some %s.','needed_container':'You need a %s to do that!','craft_item':'You craft a %s.',
          'pickup_melt':'The %s melts as you pick it up!','pickup_dry':'The %s withers as you pick it up!'}
    c.pos(0,0)
    try:
        if x == 'gr_item':
            items = []
            for item in ground_items:
                if item[:2] == xy:
                    items.append(item[2:])
            if len(items) > 1:
                print 'You see several items on the ground.'
            else:
                message('')
                if qty == 1 and a.name[0].lower() in 'aieo':
                    print md[x] %('an ' + a.name)
                elif qty == 1 and a.name[0].lower() not in 'aieo':
                    print md[x] %('a ' + a.name)
                else:
                    print md[x] %(a.name+'('+str(qty)+')')
        elif x == 'craft_item':
            combat_buffer += md[x] %(a.name)
        else:
            print md[x] %a.name
    except:
        c.rectangle((0,0,80,1))

def message_look(xy, creatures, T, known_areas):
    try:
        added_thing=''
        if current_area == 'world':
            things = 'You see: ' + T[land[xy[1]-1][xy[0]-21]].world_name + '.'
            for place in world_places:
                if world_places[place] == xy and place in known_areas:
                    things = 'You see: ' + top_world_places[str(xy)]
        else:
            things = 'You see: ' + T[land[xy[1]-1][xy[0]-21]].name + '.'
            for one in creatures:
                if one.xy == xy:
                    if one in ch.followers:
                        if one.food<30:
                            added_thing='(hungry)'
                        elif one.food>75:
                            added_thing='(well fed)'
                    if one.id==0:
                        things += ' You stand here.'
                        break
                    else:
                        if one.race!=one.name and one.t=='sentient':
                            things += ' %s stands here.%s' %(one.name.capitalize(),added_thing)
                        elif one.race[0].lower() in 'aieo':
                            things += ' An %s stands here.%s%d' %(one.race,added_thing,one.life)
                            break
                        else:
                            things += ' A %s stands here.%s%d' %(one.race,added_thing,one.life)
                            break
            for piece in ground_items:
                if piece[:2] == xy:
                    things += ' There are items here.'
                    break
                
        c.text(0,0,things,7)
    except:
        c.rectangle((0,0,80,1))

def message_choice(x):
    md = {'leave_area':'Do you wish to leave this area? (y/n)'}
    c.pos(0,0)
    try:
        print md[x]
        answer = msvcrt.getch()
        if answer == 'y' or answer == 'Y':
            return 1
        else:
            c.rectangle((0,0,80,1))
            return 0
    except:
        c.rectangle((0,0,80,1))
        return 0

def message_combat_buffer():
    if combat_buffer:
        c.rectangle((0,0,80,1))
        combat_buffer = combat_buffer.strip()
        while combat_buffer:
            pause = 0
            if len(combat_buffer) > 79:
                pause = 1
            c.text(0,0,combat_buffer[:79],7)
            combat_buffer = combat_buffer[79:]
            if pause:
                press = msvcrt.getch()
                c.rectangle((0,0,80,1))

################################ MESSAGE ^^^ #########################
################################ MOVEMENT    #########################

def force_attack(attacker,defender):
    ## Force effects based on mode and enemy
    if attacker.mode=='Nature':
        if defender.force=='Nature':
            if attacker.hunger>60 and defender.t=='animal':
                effect('force',{'Nature':{'force':0.01,'elf':0.01},'Chaos':{'all':-0.01},'Order':{'all':-0.01}})
            else:
                effect('force',{'Nature':{'all':-0.02},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
        elif defender.force=='Order':
            if current_place['Chaos']>=current_place['Nature']:
                effect('force',{'Nature':{'force':0.01,'elf':0.01,'terrain':0.05},'Chaos':{'all':-0.01},'Order':{'all':-0.01}})
            else:
                effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
        elif defender.force=='Chaos':
            effect('force',{'Nature':{'force':0.01,'elf':0.01,'terrain':0.05},'Chaos':{'all':-0.01},'Order':{'force':0.01}})
    elif attacker.mode=='Chaos':
        if defender.force=='Nature':
            effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
        elif defender.force=='Order':
            effect('force',{'Nature':{'all':-0.01},'Chaos':{'force':0.01,'ork':0.01,'terrain':0.05},'Order':{'all':-0.01}})
        elif defender.force=='Chaos':
            effect('force',{'Chaos':{'ork':0.01}})
    elif attacker.mode=='Order':
        if defender.force=='Nature':
            if defender.t=='animal':
                effect('force',{'Nature':{'all':-0.01},'Order':{'force':0.01,'human':0.01,'terrain':0.05},'Chaos':{'all':-0.01}})
            else:
                if current_place['Chaos']>=current_place['Order']:
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

def attack(attacker,defender):
    if attacker.tag == '@' or defender.tag == '@':
        if attacker.tag == '@' and (ch.equipment['Right hand'] and 'ranged' in ch.equipment['Right hand'].type) or (ch.equipment['Left hand'] and 'ranged' in ch.equipment['Left hand'].type):
            message_message('cant_hit_with_bow')
            return 0
        if ch.weapon_weight < 6:
            att_att = 'Dex'
            def_att = 'Dex'
            battle_att = ch.attr['Dex']
        elif ch.weapon_weight < 10:
    ## Ako orujieto e sredno maksimalnata stoinost na umenieto stava 100 pri balans na Dex i Str
            the_max=max([ch.attr['Dex'],ch.attr['Str']])
            the_min=min([ch.attr['Dex'],ch.attr['Str']])
            battle_att = min([the_max+(the_min-the_max*2/3),20])
            att_att = 'Str'
            def_att = 'Dex'
        elif ch.weapon_weight >= 10:
            battle_att = ch.attr['Str']
            att_att = 'Str'
            def_att = 'Str'
    ## Uchi se orujieto ako umenieto e pod 100. Pri Atribut = 20 shansa da se vdigne poveche ot 100 e 0.
    ## Pri Atribut = 1 max-skill=5 => po 5 tochki na tochka Atribut
    ## Ako se bie s dve orujiq tova v lqvata ruka se uchi dva puti po-bavno
        if attacker.tag == '@':
            against = float(defender.weapon_skill)
        else:
            against = float(attacker.weapon_skill)
        learn = random.uniform(0,100)
        if learn <= (battle_att - ch.weapon_skill/5)/battle_att*100:
            ch.weapon_skill += 0.1*max([against/ch.weapon_skill,0.1])
        if ch.equiped_weaps == 2:
            learn = random.uniform(1,100)
            if learn <= (battle_att - ch.weapon_skill/5)/battle_att*50:
                if ch.equipment['Left hand'].weapon_type==ch.equipment['Right hand'].weapon_type:
                    ch.weapon_skill += 0.1*max([against/ch.weapon_skill,0.1])
                else:
                    ch.weapon_skills[ch.equipment['Left hand'].weapon_type.capitalize()] += 0.1*max([against/ch.weapon_skill,0.1])
    if attacker.tag == '@':
        force_attack(attacker,defender)
        ## Ako bronqta teji poveche ot polovinata maksimalno teglo se namalqva efektivnoto umenie
        if attacker.armour_weight:
            armour_mod = min([float(attacker.max_weight)/attacker.armour_weight, 2]) - 1
        else:
            armour_mod = 1
        if attacker.equiped_weaps == 2:
##  Ako se bie s dve orujiq e po vajna Dex, obshtiq sbor e maksimum 90
            att = attacker.attr[att_att]/2.0 + (attacker.attr[att_att]/25.0)*attacker.weapon_skill*armour_mod + random.randint(-5,5)
        else:
##  Ako se bie s edno orujie obshtiq sbor e maksimum 120
            att = float(attacker.attr[att_att]) + attacker.weapon_skill*armour_mod + random.randint(-5,5)
    else:
        att = float(attacker.attr['Dex']) + attacker.weapon_skill + random.randint(-5,5)
    if defender.tag == '@':
        if defender.armour_weight:
            armour_mod = min([float(defender.max_weight)/defender.armour_weight, 2]) - 1
        else:
            armour_mod = 1
        defence = float(defender.attr[def_att]) + defender.weapon_skill*armour_mod + random.randint(-5,5)
    else:
        defence = float(defender.attr['Dex']) + defender.weapon_skill + random.randint(-5,5)
    if att < 0:
        defence -= att
        att = 1
    if defence < 0:
        att -= defence
        defence = 1
    chance = att/(att+defence) * 100
    hit = random.uniform(0,100)
    if chance > hit:
        return 1
    else:
        return 0

def shoot(attacker):
    if attacker.energy > 50:
        attacker.energy-=10
        if attacker.tag=='@':
            if 'invisible' in ch.effects:
                del(ch.effects['invisible'])
            bullet=ch.equipment['Ammunition'].duplicate(1)
            found=0
            for item in ch.inventory:
                if item.id==bullet.id and item.name==bullet.name:
                    found=1
                    item.lose_item(1)
            if not found:
                ch.equipment['Ammunition']=[]
                ch.weight-=bullet.weight
            shot_length=len(direct_path(ch.xy,ch.target))-1
            learn = random.uniform(0,100)
            if learn <= (ch.attr['Dex'] - ch.weapon_skill/5)/ch.attr['Dex']*100 and shot_length>=ch.attr['Dex']*3/4:
                ch.weapon_skill += 0.1*min([0.5,max([(shot_length*5)/ch.weapon_skill,0.1])])
        else:
            attacker.target=ch.xy[:]
            bullet=attacker.attr['shoot'].duplicate(1)
            shot_length=len(direct_path(attacker.xy,ch.xy))-1
        shot_chance=75*attacker.weapon_skill/float(attacker.attr['Dex']*5)+(attacker.attr['Dex']-shot_length)*10
        chance=random.randint(0,100)
        if chance<=shot_chance:
            fall_spot=attacker.target[:]
        else:
            fall_spot=[x+random.randint(1,max([1,(chance-int(shot_chance))/20]))*random.choice([-1,1]) for x in attacker.target]
            if (fall_spot[0] <= 20):
                fall_spot[0]=21
            if (fall_spot[0] >= 79):
                fall_spot[0] = 78
            if (fall_spot[1] <= 0):
                fall_spot[1] = 1
            if (fall_spot[1] >= 24):
                fall_spot[1] = 23
        attack_path=direct_path(attacker.xy,fall_spot)[1:]
        for spot in attack_path:
            if T[land[spot[1]-1][spot[0]-21]].id in "i:wWtL`S.gBaTdDFblOop,~'":
                for creature in all_beings:
                    if creature not in hidden and creature.xy==spot:
                        dodge_chance=creature.attr['Dex']*attack_path.index(spot)/2
                        if attacker.tag=='@' and creature.mode!='hostile':
                            dodge_chance-=20
                        if not clear_los(direct_path(attacker.xy,creature.xy)):
                            dodge_chance-=100
                            if (attacker.tag!='@' and 'elf3' in ch.tool_tags) or (attacker.tag=='@' and current_place['Nature']>90):
                                dodge_chance+=80
                        if random.randint(1,100)>dodge_chance:
                            if attacker.tag=='@':
                                force_attack(attacker,creature)
                                creature.mode='hostile'
                            add_dmg = 0
                            crit = random.randint(1,100)
                            if crit <= attacker.attr['Dex']:
                                add_dmg = attacker.attr['Dex']/10 + 1
                            if attacker.tag=='@':
                                if 'elf3' in ch.tool_tags and spot==attack_path[-1]:
                                    kill_chance=current_place['Chaos']/4
                                    if current_place['Nature']>=33 and current_place['Temperature']>=33:
                                        kill_chance+=25
                                    if random.randint(1,100)<=kill_chance:
                                        add_dmg+=creature.life+5
                                        if kill_chance>12 and current_place['Chaos']>0:
                                            current_place['Chaos']-=1
                                            if current_place['Nature']<100:
                                                current_place['Nature']+=1
                                if add_dmg<creature.life+5:
                                    for each_other in all_creatures:
                                        if each_other.force==creature.force and (creature.t=='sentient' and each_other.t=='sentient') and not (creature.force=='Chaos' and ch.mode=='Chaos'):
                                            each_other.mode='hostile'
                            chance = random.uniform(1,500)
                            ## Kategorii na resisted damage ot bronqta. Pri bronq 500 vinagi ima namalenie na shtetite
                            cats = {5:[1,11],4:[11,26],3:[26,46],2:[46,71],1:[71,101]}
                            resisted = 0
                            if chance < creature.armour: 
                                    cat = int(100*chance/creature.armour)
                                    cat = max([cat, 1])
                                    for x in cats:
                                            if cat in range(*cats[x]):
                                                    resisted = x
                                                    break
                            if ((creature.tag=='@' and 'troll2' in ch.tool_tags) or (creature.tag!='@' and creature.race=='troll' and current_place['Chaos']>=60)) and (ch.turn%2400>=1200):
                                resisted+=2
                            damage = random.randint(0,max([1,attacker.attr['Dex']/5]))+attacker.weapon_dmg+add_dmg+bullet.dmg-resisted
                            if damage < 1:
                                damage = 0
                            if attacker.tag=='@':
                                if add_dmg>=creature.life+5:
                                    message_creature('elf_kill',creature)
                                elif add_dmg:
                                    message_creature('crit',creature,damage)
                                else:
                                    message_creature('hit',creature,damage)
                            else:
                                if creature.tag=='@':
                                    message_creature('creature_hit',attacker,damage)
                                else:
                                    message_creature('creature_hits_creature',attacker,damage,creature)
                            creature.life -= damage
                            if attacker.tag=='@':
                                creature.attr['loot'].append([bullet.id,75,1,1])
                                if creature.life<=0:
                                    defender_dead(creature,add_dmg,attacker)
                            return 1
                        else:
                            if attacker.tag=='@':
                                message_creature('dodged',creature)
                            elif creature.tag=='@':
                                message_creature('creature_dodged',attacker)
                x=spot[0]
                y=spot[1]
                c.scroll((x, y, x+1, y+1), 1, 1, bullet.color,bullet.tag)
                sleep(.04)
                if spot==attack_path[-1]:
                    ground_items.append([attack_path[attack_path.index(spot)][0],attack_path[attack_path.index(spot)][1],bullet])
                    return 0
                else:
                    c.scroll((x, y, x+1, y+1), 1, 1, T[land[spot[1]-1][spot[0]-21]].colour,T[land[spot[1]-1][spot[0]-21]].char)
                    for be in all_beings:
                        if be.xy==spot:
                            draw_move(be,be.xy[0],be.xy[1])
                            break
                if T[land[spot[1]-1][spot[0]-21]].id in 'TDFboO':
                    chance=random.randint(0,100)-(attacker.attr['Dex']-attack_path.index(spot))*10
                    if chance>shot_chance:
                        ground_items.append([spot[0],spot[1],bullet])
                        return 0
            else:
                ground_items.append([attack_path[attack_path.index(spot)-1][0],attack_path[attack_path.index(spot)-1][1],bullet])
                return 0

def defender_dead(defender,add_dmg,attacker):
    if attacker.tag=='@':
        if defender.race=='dwarf':
            effect('force',{'Chaos':{'troll':0.02}})
        elif defender.race=='troll':
            effect('force',{'Order':{'dwarf':0.02}})
        elif defender.race=='spirit of order':
            effect('force',{'Chaos':{'spirit of chaos':0.02}})
        elif defender.race=='spirit of chaos':
            effect('force',{'Order':{'spirit of order':0.02}})
        elif defender.race=='spirit of nature':
            effect('force',{'Chaos':{'goblin':0.02}})
        elif defender.race=='dryad':
            effect('force',{'Chaos':{'goblin':0.02}})
        elif defender.race=='fairy':
            effect('force',{'Chaos':{'goblin':0.02}})
        elif defender.race=='kraken':
            effect('force',{'Nature':{'water elemental':0.02}})
        elif defender.race=='water elemental':
            effect('force',{'Chaos':{'kraken':0.02}})
        c.scroll((defender.xy[0], defender.xy[1], defender.xy[0]+1, defender.xy[1]+1), 1, 1,
                             T[land[defender.xy[1]-1][defender.xy[0]-21]].colour,
                             T[land[defender.xy[1]-1][defender.xy[0]-21]].char)
        if add_dmg:
            message_creature('crit_kill',defender)
        else:
            message_creature('kill',defender)
    else:
        message_creatures('kill',attacker,defender)
    found_item=put_item(defender.attr['loot'],defender.xy)
    if found_item:
        draw_items()
    all_creatures.remove(defender)
    all_beings.remove(defender)
    if defender in ch.followers:
        ch.followers.remove(defender)


def combat(attacker,defender,second_swing=0):
    if attacker.tag=='@' or defender.tag=='@':
        if 'invisible' in ch.effects:
            del(ch.effects['invisible'])
        if ch.possessed and 'spirit of nature3' in ch.tool_tags:
            if ch.equipment['Right hand'] and ch.possessed[0].name in ch.equipment['Right hand'].effect:
                ch.equipment['Right hand'].effect[ch.possessed[0].name]\
                                           =min([66,ch.equipment['Right hand'].effect[ch.possessed[0].name]+0.1])
            elif ch.equipment['Left hand'] and ch.possessed[0].name in ch.equipment['Left hand'].effect:
                ch.equipment['Left hand'].effect[ch.possessed[0].name]\
                                           =min([66,ch.equipment['Left hand'].effect[ch.possessed[0].name]+0.1])
    if attacker.energy > 50:
        if attack(attacker, defender):
            add_dmg = 0
            crit = random.randint(1,100)
            if crit <= attacker.attr['Dex']:
                add_dmg = attacker.attr['Dex']/10 + 1
                
            chance = random.uniform(1,500)
            ## Kategorii na resisted damage ot bronqta. Pri bronq 500 vinagi ima namalenie na shtetite
            cats = {5:[1,11],4:[11,26],3:[26,46],2:[46,71],1:[71,101]}
            resisted = 0
            if chance < defender.armour: 
                cat = int(100*chance/defender.armour)
                cat = max([cat, 1])
                for x in cats:
                    if cat in range(*cats[x]):
                        resisted = x
                        break
            if ((defender.tag=='@' and 'troll2' in ch.tool_tags) or (defender.tag!='@' and defender.race=='troll' and current_place['Chaos']>=60)) and (ch.turn%2400>=1200):
                resisted+=2
            damage = random.randint(1,attacker.dmg) + attacker.weapon_dmg + add_dmg - resisted
            if damage < 1:
                damage = 0
            if attacker.tag == '@':
                if 'kraken2' in attacker.tool_tags and \
                       T[land[attacker.xy[1]-1][attacker.xy[0]-21]].id in "wWt" and \
                       T[land[defender.xy[1]-1][defender.xy[0]-21]].id in "wWt" and \
                       ch.turn%2400>1200:
                    damage += defender.life+5
                    message_creature('kraken_death',defender)
                elif add_dmg:
                    message_creature('crit',defender,damage)
                else:
                    message_creature('hit',defender,damage)
            elif defender.tag == '@':
                message_creature('creature_hit',attacker,damage)
                if 'fairyland' in ch.effects:
                    fairy_magick=set(['fairyland','summerwalk','winterwalk','midnight fears','sun armour','invisible'])
                    fairy_dmg=1+len(fairy_magick&set(ch.effects.keys()))
                    attacker.life-=fairy_dmg
                    message_creature('fairyland_hit',attacker,fairy_dmg)
                    if attacker.life<1:
                        defender_dead(attacker,0,defender)
            else:
                message_creatures('good_attack',attacker,defender,damage)
            defender.life -= damage
        else:
            if attacker.tag == '@':
                message_creature('miss',defender)
            elif defender.tag == '@':
                message_creature('creature_miss',attacker)
            else:
                message_creatures('miss_attack',attacker,defender)
        attacker.energy -= 20
        if defender.life <= 0:
            if defender.tag =='@':
                pass
            else:
                defender_dead(defender,add_dmg,attacker)
        if attacker.tag == '@' and not second_swing and defender.life > 0:
            if attacker.equiped_weaps == 2:
                combat(attacker,defender,1)

def check_passage(xy, x, y, riding=0):
    if (xy[0] == 20) or (xy[0] == 79) or (xy[1] == 0) or (xy[1] == 24):
        if (xy[0] == 20):
            direction = 2
        elif (xy[0] == 79):
            direction = 3
        elif (xy[1] == 0):
            direction = 0
        elif (xy[1] == 24):
            direction = 1
        if not int(directions[direction]) and current_area != 'world':
            message_message('leave_world')
            xy[0] = x
            xy[1] = y
            return 1
##       ##World movement disabled!
##            else:
##                current_area, entered = world(current_area)
##                redraw_screen()
        elif not int(directions[direction]) and current_area == 'world':
            xy[0] = x
            xy[1] = y
            message_message('nowhere_togo')
        else:
            xy[0] = x
            xy[1] = y
            travel = change_place('area%s' %(directions[direction]),direction)
        return 1
    elif (T[land[xy[1]-1][xy[0]-21]].pass_through or \
         ('spirit of order1' in ch.tool_tags and T[land[xy[1]-1][xy[0]-21]].id in '#o+`sS') or \
         ('spirit of chaos1' in ch.tool_tags and T[land[xy[1]-1][xy[0]-21]].id in '#o+`sS') or \
         ('gnome1' in ch.tool_tags and T[land[xy[1]-1][xy[0]-21]].id in 'nmA%') or \
         'waterform' in ch.effects) and \
         not (ch.possessed and T[land[xy[1]-1][xy[0]-21]].id in ch.possessed[0].terr_restr):
        if 'waterform' in ch.effects:
            return 0
        for a in all_creatures:
            if (a.xy == xy) and (a not in hidden):
                if a.mode in ['hostile','standing_hostile']:
                    if not riding:
                        if not ch.ride:
                            combat(ch, a)
                        else:
                            message_message('no_riding_fighting')
                    else:
                        message_message('no_riding_fighting')
                    xy[0] = x
                    xy[1] = y
                    return 1
                else:
                    if a.t=='sentient' and not ch.possessed:
                        message_creature('talk',a)
                        answer=msvcrt.getch()
                        if answer.lower()=='y':
                            xy[0] = x
                            xy[1] = y
                            talk(a)
                            return 1
                        else:
                            message_message('')
                            if 'goblin1' in ch.tool_tags:
                                message_creature('steal',a)
                                answer=msvcrt.getch()
                                if answer.lower()=='y':
                                    effect('force',{'Chaos':{'force':0.02,'goblin':0.02},'Nature':{'all':-.01},'Order':{'all':-.01}})
                                    xy[0] = x
                                    xy[1] = y
                                    pickpocket(a)
                                    return 1
                                else:
                                    message_message('')
                    elif 'tame' in a.attr and 'tame' not in a.name and 'human2' in ch.tool_tags\
                          and not ch.possessed:
                        message_creature('tame',a)
                        answer=msvcrt.getch()
                        if answer.lower()=='y':
                            effect('force',{'Order':{'force':0.02,'human':0.02}})
                            tame(a)
                            xy[0] = x
                            xy[1] = y
                            return 1
                        else:
                            message_message('')
                    elif a in ch.followers and 'human2' in ch.tool_tags\
                          and not ch.possessed:
                        message_creature('tamed_use',a)
                        answer=msvcrt.getch()
                        if answer.lower()=='y':
                            effect('force',{'Order':{'force':0.01,'human':0.01}})
                            command_tamed(a)
                            xy[0] = x
                            xy[1] = y
                            return 1
                        else:
                            message_message('')
                    elif 'spirit of nature2' in ch.tool_tags and not ch.possessed and not ch.ride:
                        message_creature('possess',a)
                        answer=msvcrt.getch()
                        if answer.lower()=='y':
                            effect('force',{'Nature':{'force':0.03,'spirit of nature':0.03}})
                            possess(a)
                            xy[0] = x
                            xy[1] = y
                            return 1
                        else:
                            message_message('')
                    if not ch.ride:
                        message_creature('attack',a)
                        answer=msvcrt.getch()
                        if answer.lower()=='y':
                            a.mode='hostile'
                            for each_other in all_creatures:
                                if each_other.force==a.force and (a.t=='sentient' and each_other.t=='sentient') and not (a.force=='Chaos' and (ch.mode=='Chaos' or ('spirit of order3' in ch.tool_tags and random.randint(1,30)>each_other.attr['Mnd']))):
                                    each_other.mode='hostile'
                            combat(ch, a)
                        else:
                            message_message('')
                    xy[0] = x
                    xy[1] = y
                    return 1
        if (T[land[xy[1]-1][xy[0]-21]].tire_move > ch.energy) and not \
           ('kraken1' in ch.tool_tags and T[land[xy[1]-1][xy[0]-21]].id in 'wWt~') and not \
           ('winterwalk' in ch.effects and T[land[xy[1]-1][xy[0]-21]].id in "'i") and not \
           ('summerwalk' in ch.effects and T[land[xy[1]-1][xy[0]-21]].id in ",") and not \
           (ch.possessed and ch.possessed[0].race=='fish' and T[land[xy[1]-1][xy[0]-21]].id in 'wWt'):
            message_emotion('tired')
            if T[land[ch.xy[1]-1][ch.xy[0]-21]].id in drowning:
                ch.life -= 1
                message_message('drown')
            xy[0] = x
            xy[1] = y
        elif not (ch.possessed and ch.possessed[0].race=='fish' and T[land[xy[1]-1][xy[0]-21]].id in 'wWt'):
            if ('kraken1' in ch.tool_tags and T[land[xy[1]-1][xy[0]-21]].id in 'wWt~'):
                message_message('kraken_move')
            elif ('winterwalk' in ch.effects and T[land[xy[1]-1][xy[0]-21]].id in "'i"):
                message_message('fairy_%smove' %(T[land[xy[1]-1][xy[0]-21]].name))
            elif ('summerwalk' in ch.effects and T[land[xy[1]-1][xy[0]-21]].id in ","):
                message_message('fairy_%smove' %(T[land[xy[1]-1][xy[0]-21]].name))
            elif ('gnome1' in ch.tool_tags and T[land[xy[1]-1][xy[0]-21]].id in 'nmA%'):
                ch.energy -= T[land[xy[1]-1][xy[0]-21]].tire_move
                if T[land[xy[1]-1][xy[0]-21]].id != 'n':
                    land[xy[1]-1]=land[xy[1]-1][:xy[0]-21]+'n'+land[xy[1]-1][xy[0]-20:]
                    effect('force',{'Nature':{'force':0.01,'gnome':0.01,'terrain':0.4},'Chaos':{'all':-.01},'Order':{'all':-.01}})
                message_message('gnome_move')
            elif ('spirit of nature1' in ch.tool_tags and T[land[xy[1]-1][xy[0]-21]].id in 'd'):
                ch.energy -= T[land[xy[1]-1][xy[0]-21]].tire_move
                land[xy[1]-1]=land[xy[1]-1][:xy[0]-21]+'g'+land[xy[1]-1][xy[0]-20:]
                effect('force',{'Nature':{'force':0.01,'spirit of nature':0.01,'terrain':0.4},'Chaos':{'all':-.01},'Order':{'all':-.01}})
                message_message('nature_spirit_move')
            elif ('fairy1' in ch.tool_tags and T[land[xy[1]-1][xy[0]-21]].id in '.a'):
                ch.energy -= T[land[xy[1]-1][xy[0]-21]].tire_move
                land[xy[1]-1]=land[xy[1]-1][:xy[0]-21]+'g'+land[xy[1]-1][xy[0]-20:]
                effect('force',{'Nature':{'force':0.01,'fairy':0.01,'terrain':0.4},'Chaos':{'all':-.01},'Order':{'all':-.01}})
                message_message('fairy_move')
            elif ('dryad1' in ch.tool_tags and T[land[xy[1]-1][xy[0]-21]].id in 'D'):
                ch.energy -= T[land[xy[1]-1][xy[0]-21]].tire_move
                land[xy[1]-1]=land[xy[1]-1][:xy[0]-21]+'T'+land[xy[1]-1][xy[0]-20:]
                effect('force',{'Nature':{'force':0.01,'dryad':0.01,'terrain':0.4},'Chaos':{'all':-.01},'Order':{'all':-.01}})
                message_message('dryad_move')
            elif ('goblin2' in ch.tool_tags and T[land[xy[1]-1][xy[0]-21]].id in 'wW'):
                ch.energy -= T[land[xy[1]-1][xy[0]-21]].tire_move
                land[xy[1]-1]=land[xy[1]-1][:xy[0]-21]+'t'+land[xy[1]-1][xy[0]-20:]
                effect('force',{'Chaos':{'force':0.01,'goblin':0.01,'terrain':0.4},'Nature':{'all':-.01},'Order':{'all':-.01}})
                message_message('goblin_move')
            elif ('spirit of chaos2' in ch.tool_tags and T[land[xy[1]-1][xy[0]-21]].id in 'gT'):
                ch.energy -= T[land[xy[1]-1][xy[0]-21]].tire_move
                if T[land[xy[1]-1][xy[0]-21]].id=='g':
                    land[xy[1]-1]=land[xy[1]-1][:xy[0]-21]+'d'+land[xy[1]-1][xy[0]-20:]
                elif T[land[xy[1]-1][xy[0]-21]].id=='T':
                    land[xy[1]-1]=land[xy[1]-1][:xy[0]-21]+'D'+land[xy[1]-1][xy[0]-20:]
                effect('force',{'Chaos':{'force':0.01,'spirit of chaos':0.01,'terrain':0.4},'Nature':{'all':-.01},'Order':{'all':-.01}})
                message_message('chaos_spirit_move')
            else:
                ch.energy -= T[land[xy[1]-1][xy[0]-21]].tire_move
                message_message(T[land[xy[1]-1][xy[0]-21]].mess)
            for item in ground_items:
                if item[:2] == xy:
                    message_use('gr_item',item[2],item[2].qty,xy)
                    break
    elif 'door_' in T[land[xy[1]-1][xy[0]-21]].world_name:
        open_door(xy, land[xy[1]-1][xy[0]-21])
        xy[0] = x
        xy[1] = y
    else:
        if not T[land[xy[1]-1][xy[0]-21]].pass_through:
            message_message(T[land[xy[1]-1][xy[0]-21]].mess)
        xy[0] = x
        xy[1] = y

def creature_passage(ch, x, y):
    if (ch.area != []):
        if (ch.xy[0] < ch.area[0]) or (ch.xy[0] > ch.area[2]) or (ch.xy[1] < ch.area[1]) or (ch.xy[1] > ch.area[3]):
            ch.xy[0] = x
            ch.xy[1] = y
            return 1
    if (ch.xy[0] == 20) or (ch.xy[0] == 79) or (ch.xy[1] == 0) or (ch.xy[1] == 24):
        ch.xy[0] = x
        ch.xy[1] = y
        return 1
    elif T[land[ch.xy[1]-1][ch.xy[0]-21]].id in ch.terr_restr and not ch.mode=='standing_hostile':
        ch.xy[0] = x
        ch.xy[1] = y
        return 1
    elif T[land[ch.xy[1]-1][ch.xy[0]-21]].pass_through or (ch.race=='spirit of order' and current_place['Order']>30 and T[land[ch.xy[1]-1][ch.xy[0]-21]].id in '#o+`sS') or (ch.race=='spirit of chaos' and current_place['Chaos']>30 and T[land[ch.xy[1]-1][ch.xy[0]-21]].id in '#o+`sS') or (ch.race=='gnome' and current_place['Nature']>30 and T[land[ch.xy[1]-1][ch.xy[0]-21]].id in 'nmA%'):
        for a in all_beings:
            if a.xy == ch.xy and a.game_id != ch.game_id:
                ch.xy[0] = x
                ch.xy[1] = y
                if (ch.mode=='guarding' and a.mode=='hostile') or (a.mode=='guarding' and ch.mode=='hostile') or (a.xy == ch.xy and ch.mode in ['hostile','standing_hostile'] and 'waterform' not in ch.effects):
                    combat(ch,a)
                return 1
        if T[land[ch.xy[1]-1][ch.xy[0]-21]].tire_move>ch.energy:
            if T[land[ch.xy[1]-1][ch.xy[0]-21]].id in drowning and ch.race!='fish':
                ch.life -= 1
            ch.xy[0] = x
            ch.xy[1] = y
        elif not (ch.race=='kraken' and current_place['Chaos']>30 and T[land[ch.xy[1]-1][ch.xy[0]-21]].id in 'wWt~')\
             and not (ch.race=='fairy' and current_place['Nature']>60 and T[land[ch.xy[1]-1][ch.xy[0]-21]].id in "'i,")\
             and not (ch.race=='fish' and T[land[ch.xy[1]-1][ch.xy[0]-21]].id in "Wwt~"):
            ch.energy-=T[land[ch.xy[1]-1][ch.xy[0]-21]].tire_move
        if ch.mode=='standing_hostile':
            ch.xy[0] = x
            ch.xy[1] = y
    elif 'door_' in T[land[ch.xy[1]-1][ch.xy[0]-21]].world_name:
        creature_open_door(ch.xy, land[ch.xy[1]-1][ch.xy[0]-21])
        ch.xy[0] = x
        ch.xy[1] = y
    else:
          ch.xy[0] = x
          ch.xy[1] = y
##  elif T[land[ch.xy[1]-1][ch.xy[0]-21]].degradable:
##        d = degrade_terr(land[ch.xy[1]-1][ch.xy[0]-21], ch.xy)
##        if d == 1:
##            ch.xy[0] = x
##            ch.xy[1] = y
##        elif d == -1:
##            message_emotion('tired')
##            ch.xy[0] = x
##            ch.xy[1] = y
##        else:
##            message_message('no_tool')
##            ch.xy[0] = x
##            ch.xy[1] = y
##            

def move(key,ch,riding=0):
    md = {'1':[-1,1], '2':[0,1], '3':[1,1], '4':[-1,0], '5':[0,0],
          '6':[1,0], '7':[-1,-1], '8':[0,-1], '9':[1,-1], '0':[0,0]}
    x = ch.xy[0]
    y = ch.xy[1]
    a = 0
##    try:
    if (key == '0'):
        return 1
    if 'troll2' in ch.tool_tags and ch.turn%2 and ch.turn%2400<1200:
        message_message('day_troll')
        return 1
    if (key == '5'):
        message_message('')
        message_message('wait')
        if (ch.energy < ch.max_energy) and not (ch.hunger>79 or ch.thirst>79):
            ch.energy += 1
    elif ch.possessed and 'spirit of nature3' in ch.tool_tags:
        if ch.equipment['Right hand'] and ch.possessed[0].name in ch.equipment['Right hand'].effect:
            ch.equipment['Right hand'].effect[ch.possessed[0].name]\
                                       =min([33,ch.equipment['Right hand'].effect[ch.possessed[0].name]+0.01])
        elif ch.equipment['Left hand'] and ch.possessed[0].name in ch.equipment['Left hand'].effect:
            ch.equipment['Left hand'].effect[ch.possessed[0].name]\
                                       =min([33,ch.equipment['Left hand'].effect[ch.possessed[0].name]+0.01])
    for a in range(2):
        ch.xy[a] = ch.xy[a] + md[key][a]
    check_passage(ch.xy, x, y, riding)
    draw_move(ch, x, y)
##    except KeyError:
##        message_message('movement_error')

def creature_move(ch):
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
    x = ch.xy[0]
    y = ch.xy[1]
    a = 0
    key = '0'
    mode = ch.mode
    creature_sight=direct_path(ch.xy, ch.xy)
    creature_los = clear_los(creature_sight)
    player_los = clear_los(direct_path(ch.xy,ch.xy))
    if ch.t=='sentient':
        if float(ch.fear)/(ch.fear+(ch.attr['Int']+ch.attr['Mnd'])*10)>random.random():
            mode='fearfull'
    if ch.race=='troll' and current_place['Chaos']>=60 and ch.turn%2 and ch.turn%2400<1200:
        ch.path=[]
        mode='wander'
    if mode in ['follow','hostile','fearfull_hide','fearfull'] and ('invisible' in ch.effects or not creature_los):
        mode = 'wander'
    if mode in ['hostile','fearfull_hide','fearfull'] and 'elf1' in ch.tool_tags and ch.t=='animal':
        mode = 'wander'
    if mode in ['hostile','standing_hostile','fearfull_hide','fearfull'] and 'stealthy' in ch.tool_tags and creature_los:
        hide_chance=ch.attr['Dex']*3+ch.attr['Int']-ch.attr['Int']+len(creature_sight)
        if random.randint(1,100)<hide_chance:
            if mode=='standing_hostile':
                mode='standing'
            else:
                mode='wander'
    if 'ork1' in ch.tool_tags and ch.mode=='hostile' and creature_los:
        if 'human3' in ch.tool_tags:
            if random.random()<ch.research_races['Chaos']['ork']/(2*(max([current_place['Order'],current_place['Nature']])+ch.research_races['Chaos']['ork'])):
                mode='fearfull'
        else:
            if random.random()<ch.races['Chaos']['ork']/(2*(max([current_place['Order'],current_place['Nature']])+ch.races['Chaos']['ork'])):
                mode='fearfull'
    ## wander, follow, hostile, fearfull_hide, standing_hostile, standing, guarding, fearfull
    if mode == 'guarding':
        fighting=0
        if 'target' in ch.attr and ch.attr['target']!=[] and ch.attr['target'] in all_creatures:
            if len(direct_path(ch.attr['target'].xy,ch.xy))<5:
                fighting=1
                ch.path=direct_path(ch.xy,ch.attr['target'].xy)
            else:
                ch.attr['target']=[]
        if not fighting:
            for enemy in all_creatures:
                if enemy.mode=='hostile' and len(direct_path(enemy.xy,ch.xy))<3 and clear_los(direct_path(ch.xy,enemy.xy)):
                    fighting=1
                    ch.attr['target']=enemy
                    ch.path=direct_path(ch.xy,ch.attr['target'].xy)
        if not fighting:
            mode='follow'
    if mode == 'wander':
        if ch.path:
            try:
                if good_place(ch,ch.path[1]):
                    ch.xy = ch.path[1]
                    ch.path = ch.path[1:]
                else:
                    ch.path=[]
            except IndexError:
                ch.path=[]
            key = '5'
        else:
            if ch.race=='troll' and current_place['Chaos']>=60 and ch.turn%2 and ch.turn%2400<1200: 
                key='5'
            else:
                key = str(random.randint(1,9))
    if mode == 'follow' or mode == 'hostile' or mode=='standing_hostile' or mode=='guarding':
        if mode != 'guarding':
            ch.path = direct_path(ch.xy, ch.xy)
        shot=0
        if mode=='hostile' and 'shoot' in ch.attr:
            if random.randint(1,40)<ch.attr['Dex'] and len(ch.path)>2:
                shoot(ch)
                key='5'
                shot=1
        if not shot:
            try:
                if good_place(ch,ch.path[1]):
                    ch.xy = ch.path[1]
                    ch.path = ch.path[1:]
                    key = '5'
                else:
                    direction=[ch.path[1][0]-ch.xy[0],ch.path[1][1]-ch.xy[1]]
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
                        if good_place(ch,[ch.xy[a]+md[key][a] for a in range(2)]):
                            found_good=1
                        else:
                            the_key=key
            except IndexError:
                key = str(random.randint(1,9))
    if mode == 'fearfull':
        ch.xy[0] -= cmp(ch.xy[0],x)
        ch.xy[1] -= cmp(ch.xy[1],y)
        key='0'
    if mode == 'fearfull_hide':
        if (abs(ch.xy[0]-x) + abs(ch.xy[1]-y)) < 7:
            ch.xy[0] += cmp(ch.area[4],x)
            ch.xy[1] += cmp(ch.area[5],y)
            if ((cmp(ch.area[4],x) == 0) and (cmp(ch.area[5],y) == 0)) and (ch not in hidden):
                hidden.append(ch)
            key = '0'
        else:
            key = str(random.randint(1,9))
        if (ch in hidden) and ([x,y] != ch.area[4:]):
            hidden.remove(ch)
    if mode == 'standing':
        key='5'
    for a in range(2):            
        ch.xy[a] = ch.xy[a] + md[key][a]
    creature_passage(ch, x, y)
    if (ch in hidden):
        if (ch.xy != ch.xy):
            hide(ch)
    else:
        if player_los or (current_place['Nature']>=33 and current_place['Temperature']>=33 and 'elf2' in ch.tool_tags):
            draw_move(ch, x, y)
        if ch.race=='water elemental' and T[land[ch.xy[1]-1][ch.xy[0]-21]].id in 'wWt':
            ch.attr['invisible']=2
        if 'invisible' in ch.attr:
            hide(ch)
            ch.attr['invisible']-=1
            if ch.attr['invisible']==0:
                del(ch.attr['invisible'])

def create_path(path, a, b, change,times,direction = [1,1]): ## Ne se izpolzva v momenta
    borders = [[21,79],[1,24]]
    new_path = path[:]
    for i in range(1,len(path)-1):
        if not good_place(a, path[i]):
            if times == 0:
                if abs(path[0][0]-path[len(path)-1][0]) > abs(path[0][1]-path[len(path)-1][1]):
                    change = 1
                else:
                    change = 0
            for step in new_path[1:len(new_path)-1]:       ## mrudvame stupkite do dobri pozicii
                rounds = 0
                while not good_place(a, step):
                    step[change] += direction[change]
                    if step[change] not in range(*borders[change]):
                        step[change] -= direction[change]
                        direction[change] = -1*direction[change]
                        rounds += 1
                    if rounds == 2:
                        path = []
                        return path
            step_index = 0
            second_path = new_path[:]
            index_diff = 0
            for step_index in range(len(new_path)-1):       ## svurzvame mrudnatite stupki
                if abs(new_path[step_index][0] - new_path[step_index+1][0]) > 1 or abs(new_path[step_index][1] - new_path[step_index+1][1]) > 1:
                    addition = direct_path(new_path[step_index], new_path[step_index+1])
                    second_path = second_path[:step_index+index_diff+1]+addition[1:len(addition)-1][:]+new_path[step_index+1:]
                    index_diff = len(second_path)-len(new_path)
            last_path = second_path[:]
            index_diff = 0
            for step_index in range(len(second_path)-2):  ## izrqzvame izlishnite parcheta ot putq
                connection=0
                for step_index2 in range(step_index+2, len(second_path)):
                    if clear_path(a,second_path[step_index],second_path[step_index2]):
                        connection = step_index2
                if connection > step_index:
                    addition = direct_path(second_path[step_index], second_path[connection])
                    if len(addition) == 1:
                        last_path = last_path[:step_index+index_diff]+second_path[connection+1:]
                    else:
                        last_path = last_path[:step_index+index_diff+1]+addition[1:len(addition)-1][:]+second_path[connection:]
                    index_diff = len(last_path)-len(second_path)

    if not good_path(a, new_path):
        if change:
            path = create_path(new_path, a, b, 0, 1)
        else:
            path = create_path(new_path, a, b, 1, 1)
    return path
    
##    changes = [0,0]
##    for step in path[1:len(path)-1]:
##        step_record = step[:]
##        if (step != a.xy) and (step != b):
##            no_pass = 0
##            for creature in all_beings:
##                if creature.xy == step:
##                    no_pass = 1
##                    break
##            if T[land[step[1]-1][step[0]-21]].pass_through and not no_pass:
##                pass
##            else:
##                if path[path.index(step)-1][0]-path[path.index(step)+1][0]<path[path.index(step)-1][1]-path[path.index(step)+1][1]:
##                    change = 0
##                else:
##                    change = 1
##                while not T[land[step[1]-1][step[0]-21]].pass_through or no_pass:
##                    if changes[0] > 1:
##                        change = 1
##                        step = step_record[:]
##                    elif changes[1] > 1:
##                        change = 0
##                        step = step_record[:]
##                    step[change] += direction[change]
##                    no_pass = 0
##                    for creature in all_beings:
##                        if creature.xy == step:
##                            no_pass =1
##                            break
##                    if (step[0] == 79) or (step[0] == 20):
##                        step[0] -= 1
##                        direction[0] = -1*direction[0]
##                        changes[0] += 1
##                    if (step[1] == 24) or (step[1] == 0):
##                        step[1] -= 1
##                        direction[1] = -1*direction[1]
##                        changes[1] += 1
##                    if changes[0] > 0 and changes[1] > 0:
##                        path = []
##                        return path
##    for step in path[:len(path)-1]:
##        if (abs(step[0] - path[path.index(step)+1][0]) > 1) or (abs(step[1] - path[path.index(step)+1][1]) > 1):
##            addition = direct_path(step,path[path.index(step)+1])
##            path = path[:path.index(step)+1]+addition[1:len(addition)-1][:]+path[path.index(step)+1:]
##    for step in path[:len(path)-1]:
##        connection=0
##        step_index = path.index(step)+1
##        for i in range(step_index, len(path)):
##            if clear_path(a,step,path[i]):
##                connection = i
##        if connection > step_index:
##            addition = direct_path(step, path[connection])
##            if len(addition) == 1:
##                path = path[:step_index]+path[connection+1:]
##            else:
##                path = path[:path.index(step)+1]+addition[1:len(addition)-1][:]+path[connection:]
##            break
##    again = 0
##    for step in path[1:len(path)-1]:
##        no_pass = 0
##        for creature in all_beings:
##            if creature.xy == step and creature.game_id != a.game_id:
##                no_pass = 1
##                break
##        if (not T[land[step[1]-1][step[0]-21]].pass_through or no_pass):
##            again = 1
##            times += 1
##            break
##    if change:
##        change = 0
##    else:
##        change = 1
##    if times > 10:
##        times = 0
##        direction[0] = -1*direction[0]
##        direction[1] = -1*direction[1]
##    if again:
##        path = create_path(path,a,b,change,times,direction)
##    return path    

def clear_path(thing,a,b):
    xy = a[:]
    no_pass = 0
    for creature in all_beings:
        if creature.xy == xy and creature.game_id != thing.game_id:
            no_pass = 1
            break
    if not T[land[xy[1]-1][xy[0]-21]].pass_through or no_pass or T[land[xy[1]-1][xy[0]-21]].id in thing.terr_restr:
        return 0
    while xy != b:
        xy[0] += cmp(b[0],xy[0])
        xy[1] += cmp(b[1],xy[1])
        no_pass = 0
        for creature in all_beings:
            if creature.xy == xy and creature.game_id != thing.game_id:
                no_pass = 1
                break
        if not T[land[xy[1]-1][xy[0]-21]].pass_through or no_pass or T[land[xy[1]-1][xy[0]-21]].id in thing.terr_restr:
            return 0
    return 1

def good_path(thing,path):
##    broken = 0
##    for step_index in range(len(path)-1):
##        if abs(path[step_index][0] - path[step_index+1][0]) > 1 or abs(path[step_index][1] - path[step_index+1][1]) > 1:
##            broken = 1
    for xy in path[:len(path)-1]:
        no_pass = 0
        for creature in all_beings:
            if creature.xy == xy and creature.game_id != thing.game_id:
                no_pass = 1
                break
        if (not T[land[xy[1]-1][xy[0]-21]].pass_through or no_pass or T[land[xy[1]-1][xy[0]-21]].id in thing.terr_restr) and not (thing.race=='spirit of order' and current_place['Order']>30 and T[land[xy[1]-1][xy[0]-21]].id in '#o+`sS') and not (thing.race=='spirit of chaos' and current_place['Chaos']>30 and T[land[xy[1]-1][xy[0]-21]].id in '#o+`sS') and not (thing.race=='gnome' and current_place['Nature']>30 and T[land[xy[1]-1][xy[0]-21]].id in 'nmA%'):
            return 0
    return 1

def clear_los(path):
    if len(path)>2:
        for xy in path[1:-1]:
            if T[land[xy[1]-1][xy[0]-21]].id in 'T%m#f+s><DFJbnI':
                return 0
    if T[land[path[-1][1]-1][path[-1][0]-21]].id=='#':
        return 0
    return 1

def good_place(thing,place):
    no_pass = 0
    for creature in all_creatures:
        if creature.xy == place and not (creature.mode=='hostile' and thing.mode=='guarding') and not (thing.mode=='hostile' and creature.mode=='guarding'):
            no_pass = 1
            break
    if (not T[land[place[1]-1][place[0]-21]].pass_through or no_pass or (T[land[place[1]-1][place[0]-21]].id in thing.terr_restr and thing.mode!='standing_hostile')) and not (thing.race=='spirit of order' and current_place['Order']>30 and T[land[place[1]-1][place[0]-21]].id in '#o+s') and not (thing.race=='spirit of chaos' and current_place['Chaos']>30 and T[land[place[1]-1][place[0]-21]].id in '#o+s') and not (thing.race=='gnome' and current_place['Nature']>30 and T[land[place[1]-1][place[0]-21]].id in 'nmA%') and not ('door_' in T[land[place[1]-1][place[0]-21]].world_name and thing.t=='sentient'):
        return 0
    return 1

def direct_path(a,b):
    path=[a[:]]
    dif=[abs(a[0]-b[0]),abs(a[1]-b[1])]
    dirxy=[0,0]
    if abs(a[0]-b[0]):
        dirxy[0]=(b[0]-a[0])/abs(a[0]-b[0])
    if abs(a[1]-b[1]):
        dirxy[1]=(b[1]-a[1])/abs(a[1]-b[1])
    longer=dif.index(max(dif))
    shorter=[0,1]
    shorter.remove(longer)
    shorter=shorter[0]
    if dif[longer]:
        floater=float(dif[shorter])/dif[longer]
    else:
        return [a[:],b[:]]
    for x in range(dif[longer]):
        point=a[:]
        point[longer]+=(x+1)*dirxy[longer]
        point[shorter]+=int(round((x+1)*floater))*dirxy[shorter]
        path.append(point[:])
    return path
    
##    path = [a[:]]
##    xy = a[:]
##    d_x = abs(a[0]-b[0])
##    d_y = abs(a[1]-b[1])
##    if d_y:
##        div_x = float(d_x)/d_y
##    else:
##        div_x = d_x
##    if d_x:
##        div_y = float(d_y)/d_x
##    else:
##        div_y = d_y
##    to_do = [0,0]
##    added = [0,0]
##    while xy != b:
##        if to_do[0] < 1:
##            to_do[0]+=div_x
##        if to_do[1] < 1:
##            to_do[1]+=div_y
##        for z in range(int(max(to_do))):
####        while to_do[0] >= 1 or to_do[1] >= 1:
##            if to_do[0] >= 1:
##                xy[0] += cmp(b[0],xy[0])
##                to_do[0] -= 1
##                added[0] += 1
##            if to_do[1] >= 1:
##                xy[1] += cmp(b[1],xy[1])
##                to_do[1] -= 1
##                added[1] += 1
##            path.append(xy[:])
##            if not added[0]:
##                to_do[0]+=div_x
##            if not added[1]:
##                to_do[1]+=div_y
##            added = [0,0]
##            if [abs(xy[p]-b[p]) for p in [0,1]] == [1,1]:
##                path.append(b[:])
##                xy = b
##                break
##    return path

def highlight_path(way):
    if way != []:
        for step in way[1:]:
            x = step[0]
            y = step[1]
            if way.index(step)<=ch.attr['Dex']:
                c.scroll((x, y, x+1, y+1), 1, 1, 14,'*')
            else:
                c.scroll((x, y, x+1, y+1), 1, 1, 4,'*')
##    check = msvcrt.getch()
##    redraw_screen()

################################ MOVEMENT ^^^ #########################
################################ PLAYER       #########################

def make_player(race,f):
    pl = Player([0, 0],race,f)
    return pl



##['Backpack','Head','Neck','Chest','Jewel','Back','Arms','Right hand','Left hand','On hands',
## 'Left ring','Right ring','Belt','Legs','Feet','Sheath','Belt tool 1','Belt tool 2','Quiver/stone pouch']



def take_effect():
    ch.max_weight = ch.attr['Str']*10
    ch.max_weaps = ch.attr['Str']
    ch.max_energy = ch.attr['End']*100
    ch.max_life = ch.attr['End'] + ch.attr['End']/4
    ch.dmg = max([ch.attr['Str'] / 5, 1])

def take_force_effect(ch):
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
                take_force_effect(ch)
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
                        combat_buffer+=' The lava recedes down in the earth. With a last flicker a spark flies up and   lands near your feet. You have received a Seed of Life!'
                        land[xy[1]-1] = land[xy[1]-1][:xy[0]-21]+'.'+land[xy[1]-1][xy[0]-20:]
                        put_item([[1307,100,1,1]], xy)
                ## Rituala na reda e po-lesen (50% pri 100 i 100), no ako se provali izbuhva
                elif y=='suppress_lava':
                    chance=max(ch.races['Order'].values())+ch.forces['Order']-v[x][y]
                    check=random.randint(0,100)
                    if check<chance:
                        msvcrt.getch()
                        combat_buffer+=' The lava bubles and dances, and then slowly turns darker - you managed to tame the power of the fire! With a last "BLOP!" the nearly black surface breaks and  in the last flickers you see something shiny. Maybe you can pry it out?'
                        land[xy[1]-1] = land[xy[1]-1][:xy[0]-21]+'A'+land[xy[1]-1][xy[0]-20:]
                    else:
                        msvcrt.getch()
                        combat_buffer+=' The lava errupts violently!'
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
                        combat_buffer+=' The lava bursts out of the earth and sprays the space around you! On the bottom of the smoking hole lies a small piece of black rock, emanating dread and      coldness.'
                        land[xy[1]-1] = land[xy[1]-1][:xy[0]-21]+'.'+land[xy[1]-1][xy[0]-20:]
                        put_item([[1309,100,1,1]], xy)
                        for x1 in range(max([1,xy[1]-14]),min([24,xy[1]+14])):
                            for y1 in range(max([21,xy[0]-14]),min([79,xy[0]+14])):
                                if random.choice([0,1,2,3]):
                                    effect('force',{'Chaos':{'lava_fire':15}},[y1,x1])
                    else:
                        msvcrt.getch()
                        combat_buffer+=' The lava errupts violently!'
                        for x1 in range(max([1,xy[1]-14]),min([24,xy[1]+14])):
                            for y1 in range(max([21,xy[0]-14]),min([79,xy[0]+14])):
                                if random.choice([0,1,2,3]):
                                    effect('force',{'Chaos':{'lava_fire':15}},[y1,x1])
                elif y=='fire_up':
                    spot_id=ot
                    spot_color=T[land[xy[1]-1][xy[0]-21]].colour
                    ch.land_effects[ch.turn]=[v[x][y],'on_fire',current_area,xy[:],spot_id,spot_color,2]
                elif y=='lava_fire':
                    spot_id=T[land[xy[1]-1][xy[0]-21]].char
                    spot_color=T[land[xy[1]-1][xy[0]-21]].colour
                    if land[xy[1]-1][xy[0]-21] in ['T','g',':','J']:
                        land[xy[1]-1] = land[xy[1]-1][:xy[0]-21]+'.'+land[xy[1]-1][xy[0]-20:]
                    if ch.land_effects.keys():
                        if max(ch.land_effects.keys())<ch.turn:
                            ch.land_effects[ch.turn]=[v[x][y]+random.randint(0,6),'on_fire',current_area,xy[:],spot_id,spot_color,6]
                        else:
                            ch.land_effects[max(ch.land_effects.keys())+1]=[v[x][y]+random.randint(0,6),'on_fire',current_area,xy[:],spot_id,spot_color,6]
                    else:
                        ch.land_effects[ch.turn]=[v[x][y]+random.randint(0,6),'on_fire',current_area,xy[:],spot_id,spot_color,6]
                ## Izpolzva se za uvelichavane!
                elif y=='terrain':
                    if random.random()<v[x][y]:
                        if current_place[x]<100:
                            current_place[x]+=1
                        restf=['Nature','Chaos','Order']
                        restf.remove(x)
                        random.shuffle(restf)
                        if current_place[restf[0]]>0:
                            current_place[restf[0]]-=1
                        elif current_place[restf[1]]>0:
                            current_place[restf[1]]-=1
                        predominant_f={current_place['Nature']:'Nature',current_place['Order']:'Order',
                                       current_place['Chaos']:'Chaos'}
                        place_descriptions[current_area] = 'A place of %s.' %(predominant_f[max(predominant_f.keys())])
                ## Izpolzva se za uvelichavane!
                elif y=='population':
                    current_place['Population']=max([0,min([100,current_place['Population']+v[x][y]])])
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
                    take_force_effect(ch)
    elif k=='mass destruction':
        ch.land_effects[ch.turn]=[1,'mass destruction',current_area]
    elif k=='dryad song':
        ch.land_effects[ch.turn]=[1,'dryad song',current_area,ch.energy/100+1]
    elif k == 'thirst':
        ch.thirst -= v
        if ch.thirst < 0:
            ch.thirst = 0
    elif k == 'hunger':
        ch.hunger -= v
        if ch.hunger < 0:
            ch.hunger = 0
    elif k == 'container':
        I[v].create_item()
    elif k == 'fill':
        try:
            I[v[land[ch.xy[1]-1][ch.xy[0]-21]]].create_item()
        except KeyError:
            message_message('no_fill')
            i = msvcrt.getch()
            return 0
    elif k == 'gather':
        try:
            ## Izbira sluchaina bilka ot spisuka za suotvetniq teren i opredelq dali e namerena.
            choice = random.choice(v[land[ch.xy[1]-1][ch.xy[0]-21]])
            found = random.randint(1,100)
            if found <= choice.effect['chance']*ch.attr['Int']:
                choice.create_item()
            else:
                message_message('failed_gather')
                i = msvcrt.getch()
        except KeyError:
            message_message('no_gather')
            i = msvcrt.getch()
            return 0
    elif k=='transform':
        possess(v,'trans')
    elif k=='devise_spell':
        devise_spell()
    elif k=='plant_seed':
        if land[ch.xy[1]-1][ch.xy[0]-21] in ['.','a','g']:
            message_message('plant_seed')
            ch.land_effects[ch.turn]=[int(1200*(1-.5*(current_place['Nature']/100.))),'plant',current_area,random.choice(v),ch.xy[:]]
        else:
            message_message('need_dirt')
            return 0
    elif k=='plant_vegetable':
        if land[ch.xy[1]-1][ch.xy[0]-21]== 'a':
            message_message('plant_seed')
            ch.land_effects[ch.turn]=[int(1200*(1-.5*(current_place['Nature']/100.))),'plant',current_area,random.choice(v),ch.xy[:]]
        else:
            message_message('need_farm')
            return 0
    ## Za veche opredeleni semena na zelenchuci
    elif k=='plant_specific':
        if land[ch.xy[1]-1][ch.xy[0]-21]== 'a':
            message_message('plant_seed')
            ch.land_effects[ch.turn]=[int(1200*(1-.5*(current_place['Nature']/100.))),'plant',current_area,random.choice(v[0]),ch.xy[:],v[1]]
        else:
            message_message('need_farm')
            return 0
    elif k=='break_rock':
        if 'hammer' in ch.tool_tags:
            effect('force',{'Order':{'force':0.01,'dwarf':0.01},'Nature':{'all':-.01}})
            if random.random()<0.05 or ('dwarf3' in ch.tool_tags and random.random()<0.15):
                the_turn=ch.turn+1
                while the_turn in ch.land_effects:
                    the_turn+=1
                ch.land_effects[the_turn]=[1,'plant',current_area,random.choice(v),ch.xy[:]]
                message_message('found_gem')
            else:
                message_message('break_rock')
            msvcrt.getch()
        else:
            message_tool_msg('no_tool',['hammer'])
            msvcrt.getch()
            return 0
    elif k=='smelt_ore':
        if 'hammer' in ch.tool_tags:
            smelted=0
            for i in ground_items:
                if i[:2]==ch.xy and i[2].id==505:
                    effect('force',{'Order':{'force':0.01,'dwarf':0.01},'Nature':{'all':-.01},'Chaos':{'all':-.01}})
                    if random.random()<(0.05*ch.attr['Cre']):
                        the_turn=ch.turn+1
                        while the_turn in ch.land_effects:
                            the_turn+=1
                        if random.random()<0.08 or ('dwarf3' in ch.tool_tags and random.random()<0.25):
                            ch.land_effects[the_turn]=[50,'plant',current_area,v[1],ch.xy[:],
                                                      random.choice(['copper ingot','gold ingot','silver ingot'])]
                        else:
                            ch.land_effects[the_turn]=[50,'plant',current_area,v[0],ch.xy[:]]
                        message_message('found_metal')
                        msvcrt.getch()
                    else:
                        message_message('failed_smelt')
                        msvcrt.getch()
                        return 0
                    smelted=1
                    break
            if not smelted:
                message_tool_msg('no_tool',['forge'])
                msvcrt.getch()
                return 0
        else:
            message_tool_msg('no_tool',['hammer'])
            msvcrt.getch()
            return 0
    elif k=='gnome_gem':
        if T[land[ch.xy[1]-1][ch.xy[0]-21]].id in v[0] and 'gnome2' in ch.tool_tags:
            if 'ruby' not in v[1] and 'sapphire' not in v[1] and 'amethyst' not in v[1]:
                message_message(v[1])
            if 'topaz' in v[1]:
                effect('energy',ch.max_energy-ch.energy)
            elif 'emerald' in v[1]:
                effect('energy',ch.max_energy-ch.energy+100*(ch.max_life-ch.life))
            elif 'diamond' in v[1]:
                current_place['Treasure']+=1
                treasure_modifier -=1
            elif 'garnet' in v[1]:
                for x in all_creatures:
                    if x.mode != 'not_appeared' and x.t=='animal':
                        x.mode='fearfull'
            elif 'opal' in v[1]:
                mossy_coords=[]
                for y in range(len(land)):
                    for x in range(len(land[y])):
                        if land[y][x]=='n' and [x+21,y+1] != ch.xy:
                            mossy_coords.append([x+21,y+1])
                ch.xy=random.choice(mossy_coords)
            elif 'turquoise' in v[1]:
                land[ch.xy[1]-1] = land[ch.xy[1]-1][:ch.xy[0]-21]+'W'+land[ch.xy[1]-1][ch.xy[0]-20:]
                effect('force',{'Nature':{'terrain':1}})
            elif 'tourmaline' in v[1]:
                land[ch.xy[1]-1] = land[ch.xy[1]-1][:ch.xy[0]-21]+'n'+land[ch.xy[1]-1][ch.xy[0]-20:]
                effect('force',{'Nature':{'terrain':1}})
            elif 'aquamarine' in v[1]:
                land[ch.xy[1]-1] = land[ch.xy[1]-1][:ch.xy[0]-21]+'w'+land[ch.xy[1]-1][ch.xy[0]-20:]
                effect('force',{'Nature':{'terrain':1}})
            elif 'sapphire' in v[1]:
                for x in all_creatures:
                    if x.mode=='hostile':
                        if clear_los(direct_path(ch.xy,x.xy)):
                            x.life-=max([(ch.races['Nature']['gnome']-60)/4,1])
                            message_creature('sapphired',x)
            elif 'ruby' in v[1]:
                found_fire=0
                for x in ch.land_effects.keys():
                    if ch.land_effects[x][2]==current_area and ch.land_effects[x][1]=='on_fire' \
                       and ch.land_effects[x][3]==ch.xy:
                        message_message(v[1])
                        found_fire=1
                        for x in all_creatures:
                            if x.mode=='hostile':
                                if clear_los(direct_path(ch.xy,x.xy)):
                                    x.life-=max([(ch.races['Nature']['gnome']-60)/2,1])
                                    message_creature('rubied',x)
                        break
                if not found_fire:
                    message_message('cant_use_gem')
                    return 0
            elif 'amethyst' in v[1]:
                if ch.marked_stone and current_area==ch.marked_stone[0] and ch.xy==ch.marked_stone[1]:
                    ch.marked_stone=[]
                    message_message('amethyst0')
                else:
                    ch.marked_stone=[current_area,ch.xy[:]]
                    message_message('amethyst1')
            elif 'lapis' in v[1]:
                change_place('areaB','gnome')
            effect('force',{'Nature':{'force':0.03,'gnome':0.03},'Chaos':{'all':-.03},'Order':{'all':-.03}})
        else:
            message_message('cant_use_gem')
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
            move(i,ch)
            if 'human3' in ch.tool_tags and ch.research_race!='human':
                if current_place[ch.research_force]==max([current_place['Chaos'],current_place['Order'],current_place['Nature'],]) and current_place[ch.research_force]>=ch.research_forces[ch.research_force]:
                    effect('research',{ch.research_force:{'force':0.01}})
            if ch.possessed and ch.possessed[0].mode=='temp':
                effect('force',{'Nature':{'terrain':0.1}})
        if ch.spell_cast:
            execute_spell(combat_buffer)
            ch.spell_cast = 0
        for x in all_creatures:
            if x.mode != 'not_appeared':
                if x.life < 1:
                    c.scroll((x.xy[0], x.xy[1], x.xy[0]+1, x.xy[1]+1), 1, 1,
                                         T[land[x.xy[1]-1][x.xy[0]-21]].colour,
                                         T[land[x.xy[1]-1][x.xy[0]-21]].char)
                    all_creatures.remove(x)
                    all_beings.remove(x)
        for x in all_creatures:
            if not (x in ch.followers and x.xy==ch.xy) or (x in ch.possessed and x.xy==[1,1]):
                hide(x)
            if x.mode != 'not_appeared':
                if x in ch.ride or x in ch.possessed or (x in ch.followers and x.xy==ch.xy):
                    continue
                creature_move(x)
            if clear_los(direct_path(ch.xy,x.xy)):
                if x.mode=='hostile':
                    hostile_in_sight=2
                if 'human3' in ch.tool_tags and ch.research_race!='human':
                    if x.race==ch.research_race and i!=0 and i!=5 and x.learning>0:
                        effect('research',{ch.research_force:{ch.research_race:0.01}})
                        x.learning-=0.01
            elif x.t=='sentient' and 'midnight fears' in ch.effects and x.mode=='hostile':
                x.fear+=int(ch.races['Nature']['fairy']/10)-abs(600-max([0,ch.turn%2400-1200])%1200)/100
        draw_items()
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
        if (ch.life < ch.max_life) and current_area != 'world' and ch.life!=0:
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
        draw_hud()
        if 'water elemental1' in ch.tool_tags and T[land[ch.xy[1]-1][ch.xy[0]-21]].id in 'wWt':
            if 'waterform' not in ch.effects:
                ch.effects['invisible']=2
                if 'water elemental2' in ch.tool_tags:
                    if T[land[ch.xy[1]-1][ch.xy[0]-21]].id in 'wW':
                        ch.hunger=max([0,ch.hunger-1])
                        ch.thirst=max([0,ch.thirst-1])
                        message_message('good_water')
                    elif T[land[ch.xy[1]-1][ch.xy[0]-21]].id=='t':
                        ch.hunger=min([100,ch.hunger+10])
                        ch.thirst=min([100,ch.thirst+10])
                        message_message('bad_water')
            elif T[land[ch.xy[1]-1][ch.xy[0]-21]].id=='W' and 'waterform' in ch.effects:
                ch.life=1
                ch.hunger=90
                ch.thirst=90
                del(ch.effects['waterform'])
                del(ch.effects['invisible'])
                message_message('reform_waterform')
                msvcrt.getch()
        if (current_place['Nature']>=33 and current_place['Temperature']>=33 and 'elf2' in ch.tool_tags) \
           or ('goblin1' in ch.tool_tags and ch.turn%2400>1200):
            if 'stealthy' not in ch.tool_tags:
                ch.tool_tags.append('stealthy')
        else:
            if 'stealthy' in ch.tool_tags:
                ch.tool_tags.remove('stealthy')
        if 'stealthy' in ch.tool_tags:
            ch.emotion=8
        for x in ch.effects.keys():
            if not (ch.equipment['Right ring'] and ch.equipment['Right ring'].name=='ring of winter' and (current_place['Temperature']<33 or 'summerwalk' in ch.effects) and x=='winterwalk')\
               and not (ch.equipment['Left ring'] and ch.equipment['Left ring'].name=='ring of summer' and (current_place['Temperature']>=66 or 'winterwalk' in ch.effects) and x=='summerwalk')\
               and not (x in ['fairyland','summerwalk','winterwalk','midnight fears','sun armour','invisible'] and 'fairyland' in ch.effects):
                ch.effects[x] -= 1
            if ch.effects[x]==0:
                if x=='waterform':
                    msvcrt.getch()
                    over = game_over()
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
            if ch.land_effects[x][2]==current_area:
                if ch.land_effects[x][1]=='mass destruction':
                    combat_buffer+=' You unleash the power of the chaos rock! The world crumbles around you!'
                    message_combat_buffer()
                    msvcrt.getch()
                    for i1 in range(8):
                        effect('force',{'Chaos':{'terrain':1}})
                        for i2 in range(100):
                            place=[random.randint(22,78),random.randint(2,23)]
                            dest=T[land[place[1]-1][place[0]-21]].degrade_to['Chaos']
                            if dest in ['`','+','s','S']:
                                dest='.'
                            land[place[1]-1] = land[place[1]-1][:place[0]-21]+dest+land[place[1]-1][place[0]-20:]
                            c.scroll((place[0],place[1],place[0]+1,place[1]+1), 1, 1, T[land[place[1]-1][place[0]-21]].colour, T[land[place[1]-1][place[0]-21]].char)
                        msvcrt.getch()
                if ch.land_effects[x][1]=='dryad song':
                    effect('force',{'Nature':{'dryad':.01,'terrain':.4,'force':.01},'Chaos':{'all':-0.02},'Order':{'all':-0.01}})
                    combat_buffer+=' Leaves rustle, wood creaks, in your steps the grass grows higher!'
                    for i1 in range(30):
                        place=[random.randint(22,78),random.randint(2,23)]
                        growing={'.':'g','B':'g','g':'b','a':'g','T':'J','F':'T','b':'T','%':'n','m':'n','#':'n','o':'b',
                                 'p':'g',',':'g','~':'b','+':'T','`':'T',}
                        dest=T[land[place[1]-1][place[0]-21]].id
                        if dest in growing:
                            dest=growing[dest]
                        land[place[1]-1] = land[place[1]-1][:place[0]-21]+dest+land[place[1]-1][place[0]-20:]
                        c.scroll((place[0],place[1],place[0]+1,place[1]+1), 1, 1, T[land[place[1]-1][place[0]-21]].colour, T[land[place[1]-1][place[0]-21]].char)
                        if ch.land_effects[x][3]>1:
                            ch.land_effects[ch.turn]=[1,'dryad song',current_area,ch.land_effects[x][3]-2]
                if ch.land_effects[x][1]=='plant':
                    if ch.land_effects[x][0]==0:
##                        put_item([[ch.land_effects[x][3].id,100,1,1]],ch.land_effects[x][4])
                        if len(ch.land_effects[x])==5:
                            put_item([[ch.land_effects[x][3].id,100,1,1]],ch.land_effects[x][4])
                        ## Za opredeleni zelenchuci
                        elif len(ch.land_effects[x])==6:
                            new_veg=ch.land_effects[x][3].duplicate(1,ch.land_effects[x][5])
                            ground_items.append([ch.land_effects[x][4][0],ch.land_effects[x][4][1],new_veg])
                if ch.land_effects[x][1]=='on_fire':
                    fxy=ch.land_effects[x][3]
                    if ch.land_effects[x][0]==0:
                        c.scroll((fxy[0],fxy[1],fxy[0]+1,fxy[1]+1), 1, 1, T[land[fxy[1]-1][fxy[0]-21]].colour, T[land[fxy[1]-1][fxy[0]-21]].char)
                    else:
                        for cr in all_creatures:
                            if cr.mode != 'not_appeared':
                                if cr.xy==fxy:
                                    cr.life-=ch.land_effects[x][6]
                                if cr.life < 1:
                                    c.scroll((cr.xy[0], cr.xy[1], cr.xy[0]+1, cr.xy[1]+1), 1, 1,
                                                         T[land[cr.xy[1]-1][cr.xy[0]-21]].colour,
                                                         T[land[cr.xy[1]-1][cr.xy[0]-21]].char)
                                    all_creatures.remove(cr)
                                    all_beings.remove(cr)
                                    combat_buffer+=' The %s dies in the flames!' %(cr.name)
                        fire_color=random.choice([4,12,14])
                        c.scroll((fxy[0],fxy[1],fxy[0]+1,fxy[1]+1), 1, 1, fire_color*16+ch.land_effects[x][5],ch.land_effects[x][4])
                        if ch.xy==fxy:
                            ch.life-=ch.land_effects[x][6]
                            combat_buffer+=' You get burnt by the fire!'
            if ch.land_effects[x][0]==0:
                del(ch.land_effects[x])

        message_combat_buffer()

        if ch.life <= 0:
            if 'water elemental3' in ch.tool_tags and 'waterform' not in ch.effects:
                ch.effects['waterform']=100+int(100*(ch.races['Nature']['water elemental']-90))
                ch.effects['invisible']=100+int(100*(ch.races['Nature']['water elemental']-90))
                message_emotion('gain_waterform',ch.effects['waterform'])
            elif 'waterform' in ch.effects:
                message_emotion('gain_waterform',ch.effects['waterform'])
            else:
                msvcrt.getch()
                over = game_over()
                return over
    else:
        message_message('?')
    ##Can't be 0 - ends the game
    return hostile_in_sight

################################ PLAYER ^^^ #########################
################################ MAIN       #########################


if __name__=='__main__':

    ## TERRAIN INSTANCES
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

    treasure1 = Terrain(id='treasure1',loot=100)
    mechka = Terrain(id='mechka',random_creatures=[[4,500]])

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
                                            'Chaos':{'force':0.03,'imp':0.03,'terrain':0.2,'fire_up':25}}})
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
                                            'Chaos':{'force':0.01,'imp':0.01,'terrain':0.05,'fire_up':25}}})
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
                                            'Chaos':{'force':0.05,'troll':0.05,'terrain':0.05}}})
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
                                            'Chaos':{'force':0.02,'imp':0.02,'terrain':0.2,'fire_up':50}}})
    bush = Terrain('bush', '', 'b', 10, '#','bush',degrade_to = {'Nature':'b','Order':'.','Chaos':'.'},
                    degr_mess = {'Nature':'forage','Order':'root_bushes','Chaos':'fire_bush'},
                    degrade_tool = {'Nature':['inherent'],'Order':['inherent'],'Chaos':['fire']},
                    tire={'Nature':20,'Order':30,'Chaos':10},tire_move = 15,
                    loot = {'Nature':[['forage',40,1,2]],'Order':[],'Chaos':[]},
                    force_effects={'Nature':{'Nature':{'force':0.02,'elf':0.02},'Chaos':{'all':-.02}},
                                   'Order':{'Nature':{'all':-.02},'Order':{'force':0.02,'human':0.02,'terrain':0.2}},
                                   'Chaos':{'Nature':{'all':-.02},'Order':{'all':-.02},
                                            'Chaos':{'force':0.02,'imp':0.02,'terrain':0.2,'fire_up':15}}})
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
                                   'Chaos':{'Nature':{'all':-.05},'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2}}})
    well = Terrain('well', 'mountains', 'O', 1, 'O', 'well_pass', True, True, True,
                   degrade_to = {'Nature':'O','Order':'O','Chaos':'.'},
                    degr_mess = {'Nature':'clean_well','Order':'clean_well','Chaos':'crush_well'},
                    degrade_tool = {'Nature':['inherent'],'Order':['inherent'],'Chaos':['pickaxe','pick','big hammer']},
                    tire={'Nature':10,'Order':10,'Chaos':150},drink = {'energy':20, 'thirst':20},
                    loot = {'Nature':[[1303,40,2,4],[1304,30,1,2]],'Order':[[1306,40,1,2]],'Chaos':[[4,100,1,4]]},
                    force_effects={'Nature':{'Nature':{'force':0.01,'fairy':0.01},'Chaos':{'all':-.01}},
                                   'Order':{'Chaos':{'all':-.01},'Order':{'force':0.01,'spirit of order':0.01}},
                                   'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                            'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2,'population':-2}}})
    mossy_rock = Terrain('mossy rock', 'mountains', 'n', 10, '%', 'rock', False, True, True,
                   degrade_to = {'Nature':'n','Order':'.','Chaos':'.'},
                    degr_mess = {'Nature':'touch_rock','Order':'break_rock','Chaos':'break_rock'},
                    degrade_tool = {'Nature':['inherent'],'Order':['pickaxe','pick','big hammer'],'Chaos':['pickaxe','pick','big hammer']},
                    tire={'Nature':0,'Order':150,'Chaos':150},tire_move=10,
                    loot = {'Nature':[[1304,30,1,2]],'Order':[[4,100,3,8],[5,5,1,2]],'Chaos':[[4,100,1,5]]},
                    force_effects={'Nature':{'Nature':{'force':0.01,'gnome':0.01},'Chaos':{'all':-.01},'Order':{'all':-.01}},
                                   'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05,'terrain':0.2}},
                                   'Chaos':{'Nature':{'all':-.05},'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2}}})
    mine_rock = Terrain('rock', 'mountains', 'm', 8, '%', 'rock', False, False, True,
                   degrade_to = {'Nature':'m','Order':'.','Chaos':'.'},
                    degr_mess = {'Nature':'touch_rock','Order':'break_rock','Chaos':'break_rock'},
                    degrade_tool = {'Nature':['inherent'],'Order':['pickaxe','pick','big hammer'],'Chaos':['pickaxe','pick','big hammer']},
                    tire={'Nature':0,'Order':150,'Chaos':150},tire_move=20,
                    loot = {'Nature':[[1304,30,1,2]],'Order':[[4,100,3,8],[5,60,1,3]],'Chaos':[[4,100,1,5]]},
                    force_effects={'Nature':{'Nature':{'force':0.01,'gnome':0.01},'Chaos':{'all':-.01},'Order':{'all':-.01}},
                                   'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05}},
                                   'Chaos':{'Nature':{'all':-.05},'Chaos':{'force':0.05,'troll':0.05}}})
    wall = Terrain('wall', 'wall???', '#', 7, '#', 'wall', False, True, True,
                   degrade_to = {'Nature':'#','Order':'#','Chaos':'.'},
                    degr_mess = {'Nature':'paint_wall','Order':'strenghten_wall','Chaos':'break_wall'},
                    degrade_tool = {'Nature':['color clay'],'Order':['clay'],'Chaos':['pickaxe','pick','big hammer']},
                    tire={'Nature':20,'Order':20,'Chaos':150},tire_move=20,
                    loot = {'Nature':[],'Order':[],'Chaos':[[4,100,1,4]]},
                    force_effects={'Nature':{'Nature':{'force':0.02,'fairy':0.02,'expend':'color clay'},'Chaos':{'all':-.02}},
                                   'Order':{'Chaos':{'all':-.02},'Order':{'force':0.02,'dwarf':0.02,'expend':'clay'}},
                                   'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                            'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2,'population':-1}}})
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
                                   'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},'Chaos':{'force':0.07,'kraken':0.07,'terrain':0.05}}})
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
                                   'Chaos':{'Nature':{'water elemental':-0.05},'Chaos':{'force':0.05,'kraken':0.05,'terrain':0.05}}})
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
                                            'Chaos':{'force':0.03,'kraken':0.03,'terrain':0.2}}})
    dirty_water = Terrain('dirty water', 'sea','t',8,'~','water',degrade_to = {'Nature':'w','Order':'t','Chaos':'t'},
                    degr_mess = {'Nature':'clean_water','Order':'search_water','Chaos':'contaminate_water'},
                    degrade_tool = {'Nature':['inherent'],'Order':['inherent'],'Chaos':['inherent']},
                    tire={'Nature':50,'Order':250,'Chaos':10},tire_move=35,drink = {'energy':5, 'thirst':-5},
                    loot = {'Nature':[],'Order':[['treasure',0.8,'small',False],['treasure',0.4,'medium',False],['treasure',0.2,'large',False],
                          ['treasure',0.16,'small',True],['treasure',0.08,'medium',True],['treasure',0.04,'large',True]],'Chaos':[]},
                    force_effects={'Nature':{'Nature':{'force':0.03,'water elemental':0.03,'terrain':.3},'Chaos':{'all':-.03}},
                                   'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05,'terrain':0.05}},
                                   'Chaos':{'Nature':{'all':-.03},'Order':{'all':-.03},
                                            'Chaos':{'force':0.03,'kraken':0.03,'terrain':0.05}}})
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
                                            'Chaos':{'force':0.03,'kraken':0.03,'terrain':0.2}}})
    waterfall = Terrain('waterfall', 'river','f',11,'~',pass_through=False,
                          degrade_to = {'Nature':'f','Order':'%','Chaos':'w'},
                    degr_mess = {'Nature':'clean_water','Order':'stop_waterfall','Chaos':'destroy_waterfall'},
                    degrade_tool = {'Nature':['inherent'],'Order':['shovel'],'Chaos':['pickaxe','pick','big hammer']},
                    tire={'Nature':50,'Order':250,'Chaos':250},
                    loot = {'Nature':[],'Order':[],'Chaos':[]},
                    force_effects={'Nature':{'Nature':{'force':0.03,'water elemental':0.03,'terrain':.05},'Chaos':{'all':-.03}},
                                   'Order':{'Nature':{'all':-.05},'Order':{'force':0.05,'dwarf':0.05,'terrain':0.2}},
                                   'Chaos':{'Nature':{'all':-.05},'Order':{'all':-.05},
                                            'Chaos':{'force':0.05,'kraken':0.05,'terrain':0.2}}})
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
                                            'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2,'population':-1}}})
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
                                            'Chaos':{'force':0.05,'troll':0.05,'terrain':0.2,'population':-1}}})
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
    up_stair = Terrain('staircase going up','','>',7,'>','up_stair',True,False,False)
    down_stair = Terrain('staircase going down','','<',7,'<','down_stair',True,False,False)

    unsittable = ('w','W','O','~','t') ## ID na terenite na koito ne moje da se sedi,no moje da se minava prez tqh
    drowning = ('w','t')

    ## ***************************************UPDATE LOS TOO!*********************************************
    all = (dirt,grass,tree,rock,mine_rock,wall,pavement,sand,snow,log,water,magic_water,waterfall,up_stair,down_stair,mechka,
           wood_door_c,wood_door_o,stone_door_o,stone_door_c,treasure1,mossy_rock,bush,lichen,jungle,ice,ice_block,
           frozen_tree,d_grass,d_tree,lava,bones,well,farmland,wooden_fence,swamp,dirty_water,lava_rock)
    T = {}
    for i in all:
        T[i.id] = (i)

    ###### ITEM INSTANCES

    ## weight,[type],[tool_tag],'weap_type',armour,dmg,name, id, stackable=False, qty=1, effect={}, color=7, tag='?'
    ## Za napitki butilkata(id) e vuv efektite( 'container':id_na_praznata_butilka; 'fill':{'teren':id_na_pulnata_butilka} )!
    ## Slojnostta na kliuchalkata e vuv efektite {'lock_strength':XX}
    ## Za konteineri (torbi i sanduci) sudurjanieto e v efektite, 'contains':[[predmet]...]
    ## Nadpisite (engraving) sa v efektite {'engraving':'...'}
    ## V type se pishat slotovete (VSICHKI SLOTOVE!!!) v equipment koito moje da zaema neshtoto
    ## VSICHKI predmeti imat damage, zashtoto vsichki mogat da se durjat v ruka!!!
    ## Materialite koito mogat da se poluchat ot predmeta se pishat v TYPE!
    ## Tagove:
    ## tool, armour, weapon, two_handed (DA NE SE SLAGA NA INSTRUMENTI!), food, drink, material, ammunition, bottle,
    ## container, seed, backpack, treasure, herb_set, magic_book,lockpick,locked,goods,flower
    ## material tagove:
    ## m-long|m-short(forma)  m-connect(funkciq)
    ## 'leather','wood','paper','rock','ore','spice','heavy_fabric','cloth','iron','steel','copper','silver','gold','enameled',
    ## +imenata na skupocennite kamuni.
    ## , - food
    ## * - material,herb,flowers
    ## . - seeds
    ## = - container
    ## / - weapons
    ## ~ - rope/strings
    ## ) - cloaks/gloves/armguards
    ## [ - chest armour
    ## ( - pants
    ## - - belt
    ## ^ - hat/cap/helmet
    ## $ - treasure
    ## IMENA ZA RANDOM EQUIPMENT:
    ## traveler's, scholar's, working, merchant's, razlichni cvetove (zapisvat se v duplicate funkciqta!)

    spike_shield = item(9,['armour','Right hand','Left hand','leather','iron'],[],'',30,1,'spiked shield',10,False,1,{'temp_attr':[['Dex',1]]},8,'}')

    ## Tools, IDs 1,500-
    pick = item(8, ['tool','weapon','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['pick'],'pick',0, 1, 'pick', id=1,tag='/')
    shovel = item(5, ['tool','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['shovel'],'',0, 1, 'shovel', id=500,tag='/')
    pickaxe = item(8, ['tool','weapon','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['pickaxe'],'pick',0, 1, 'pickaxe', id=501,tag='/')
    tinderbox = item(1, ['tool','iron','wood'],['fire'],'',0,0,'tinder-box',502,color=8,tag='=')
    cauldron = item(50, ['tool','iron'],['cauldron'],'',0,0,'cauldron',503,color=8,tag='O')
    anvil = item(250, ['tool','iron'],['anvil'],'',0,0,'anvil',504,color=8,tag='-')
    forge = item(1500, ['tool','iron'],['forge'],'',0,0,"blacksmith's forge",505,color=12,tag='O')
    working_table = item(200, ['tool','wood'],['work_table'],'',0,0,'work table',506,color=6,tag='-')
    hammer = item(3, ['tool','weapon','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['hammer'],'hammer',0, 1, 'hammer', id=507,tag='/')
    saw = item(3, ['tool','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['saw'],'',0, 1, 'saw', id=508,tag='/')
    chisel = item(1.5, ['tool','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['chisel'],'',0, 1, 'chisel', id=509,tag='/')
    pliers = item(1.5, ['tool','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['pliers'],'',0, 0, 'pliers', id=510,tag='/')
    needle = item(0.02, ['tool','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['needle'],'',0, 0, 'needle', id=511,tag='/')

    tools = (pick,shovel,pickaxe,tinderbox,cauldron,anvil,forge,working_table,hammer,saw,chisel,pliers,needle)
    human_tools=(pick,shovel,pickaxe,tinderbox,hammer,saw,chisel,pliers,needle)
    house_generated=(cauldron,anvil,forge,working_table)

    ## Containers, IDs 11,17,18-
    wooden_chest = item(50,['container','two_handed','locked','wood'],[],'',0,1,'wooden chest',11,False,1,{'contains':[],'lock_strength':15},6,'=')
    small_backpack = item(4,['container','Backpack','leather'],[],'',0,0,'small backpack',17,False,1,{'contains':[]},7,'=')
    shoulder_bag = item(2,['container','Backpack','leather'],[],'',0,0,'shoulder bag',18,False,1,{'contains':[]},7,'=')
    small_chest = item(20,['container','two_handed','wood'],[],'',0,1,'small chest',19,False,1,{'contains':[],'lock_strength':15},6,'=')
    wooden_box = item(8,['container','two_handed','wood'],[],'',0,0,'wooden box',20,False,1,{'contains':[]},7,'=')
    talisman_pouch = item(0.01,['talisman','container','leather','Neck'],[],'',0,0,'talisman pouch',21,False,1,{'contains':[]},7,'=')
    ivory_box = item(8,['container','two_handed','ivory'],[],'',0,0,'ivory box',22,False,1,{'contains':[]},7,'=')
    medium_backpack = item(7,['container','Backpack','leather'],[],'',0,0,'medium backpack',23,False,1,{'contains':[]},7,'=')
    large_backpack = item(10,['container','Backpack','leather'],[],'',0,0,'large backpack',24,False,1,{'contains':[]},7,'=')

    tiny_containers = (talisman_pouch,)
    small_containers = (shoulder_bag,small_backpack)
    medium_containers = (small_chest,wooden_box,ivory_box,medium_backpack,large_backpack)
    large_containers = (wooden_chest,)

    ## Weapons, IDs 12,13,15,50-
    ## light <5
    ## medium <10
    ## heavy >=10
    ## weapon types: long sword, club, axe, staff, dagger, big hammer, short sword, bow, crossbow, sling, hammer, pick
    long_sword = item(6, ['weapon','Right hand','Left hand','iron'],['cutting'],'long sword',0,2,'long sword',12,tag='/')
    axe = item(6, ['tool','weapon','Belt tool 1','Belt tool 2','Right hand','Left hand','iron'],['axe'],'axe',0, 2, 'axe', id=13,tag='/')
    club = item(6, ['weapon','Right hand','Left hand','wood'],['crude hammer'],'club',0, 2, 'club', 15,tag='/')
    light_staff = item(3, ['weapon','two_handed','Right hand','Left hand','wood'],['leverage'],'staff',0, 1, 'light wooden staff', 50,color=6,tag='/')
    dagger = item(2, ['weapon','Right hand','Left hand','iron'],['cutting'],'dagger',0,1,'dagger',51,color=7,tag='/')
    sceptre = item(10, ['weapon','two_handed','Right hand','Left hand','iron'],['big hammer'],'big hammer',0,3,'sceptre', 52,tag='/')
    heavy_hammer = item(12, ['weapon','two_handed','Right hand','Left hand','iron'],['big hammer'],'big hammer',0,3,'heavy hammer', id=53,tag='/')
    giant_club = item(12, ['weapon','two_handed','Right hand','Left hand','wood'],['big hammer'],'big hammer',0,3,'giant club', id=54,tag='/')
    short_sword = item(4, ['weapon','Right hand','Left hand','iron'],['cutting'],'short sword',0,2,'short sword',55,tag='/')
    bow = item(3, ['weapon','two_handed','Right hand','Left hand','wood','ranged'],[],'bow',0, 2, 'bow', 56,effect={'shoot':'arrow'},color=6,tag='{')
    crossbow = item(6, ['weapon','two_handed','Right hand','Left hand','wood','iron','ranged'],[],'crossbow',0, 2, 'crossbow', 57,effect={'shoot':'bolt'},color=7,tag='{')
    sling = item(1, ['weapon','two_handed','Right hand','Left hand','leather','ranged'],[],'sling',0, 1, 'sling', 58,effect={'shoot':'stone'},color=8,tag='{')

    light_weapons = (light_staff,dagger,short_sword)
    medium_weapons = (long_sword,axe,club)
    heavy_weapons = (sceptre,heavy_hammer,giant_club)
    ranged_weapons = (bow,sling,crossbow)

    ## Cloth armour(armour 14,wgt 0.7), IDs 100-
    cloth_pants = item(0.1, ['armour','Legs','cloth'],[],'',2, 0, 'pants', id=100, color=15, tag='(')
    cloth_belt = item(0.1, ['armour','Belt','cloth'],[],'',2, 0, 'belt', id=101, color=15, tag='-')
    cloth_gloves = item(0.1, ['armour','On hands','cloth'],[],'',2, 0, 'cloth gloves', id=102, color=15, tag=')')
    cloth_cloak = item(0.1, ['armour','Back','cloth'],[],'',2, 0, 'cloth cloak', id=103, color=15, tag=')')
    cloth_shirt = item(0.1, ['armour','Chest','cloth'],[],'',2, 0, 'shirt', id=104, color=15, tag='[')
    cloth_hat = item(0.1, ['armour','Head','cloth'],[],'',2, 0, 'hat', id=105, color=15, tag='^')
    cloth_robe = item(0.2, ['armour','Chest','cloth'],[],'',3, 0, 'robe', id=106, color=15, tag='[')
    cloth_shoes = item(0.1, ['armour','Feet','cloth','wood'],[],'',2, 0, 'shoes', id=107, color=15, tag='_')
    flower_crown = item(0.05, ['armour','Head'],[],'',1, 0, 'flower crown', id=108, color=5, tag='*')

    cloth_armour = (cloth_pants,cloth_cloak,cloth_belt,cloth_gloves,cloth_shirt,cloth_hat,cloth_shoes,cloth_robe,flower_crown)

    ## Leather armour(armour 180,wgt 25.5), IDs 8, 200-
    leather_vest = item(7,['armour','Chest','leather'],[],'',50,0,'leather vest',8,False,1,{},8,'[')
    leather_pants = item(6, ['armour','Legs','leather'],[],'',50, 0, 'leather pants', id=200, color=8, tag='(')
    leather_belt = item(2, ['armour','Belt','leather'],[],'',10, 0, 'leather belt', id=201, color=8, tag='-')
    leather_gloves = item(1.5, ['armour','On hands','leather'],[],'',15, 0, 'leather gloves', id=202, color=8, tag=')')
    leather_cloak = item(5, ['armour','Back','leather'],[],'',30, 0, 'leather cloak', id=203, color=8, tag=')')
    leather_hat = item(1, ['armour','Head','leather'],[],'',10, 0, 'leather hat', id=204, color=8, tag='^')
    leather_boots = item(3, ['armour','Feet','leather','wood'],[],'',15, 0, 'leather boots', id=205, color=8, tag='_')

    leather_armour = (leather_pants,leather_vest,leather_cloak,leather_belt,leather_gloves,leather_hat,leather_boots)

    ## Chain armour(armour 360,wgt 48), IDs 300-
    chain_vest = item(15,['armour','Chest','iron','leather'],[],'',100,0,'chain vest',300,False,1,{},7,'[')
    chain_pants = item(12, ['armour','Legs','iron','leather'],[],'',100, 0, 'chain pants', id=301, color=7, tag='(')
    chain_belt = item(3, ['armour','Belt','iron','leather'],[],'',20, 0, 'chain belt', id=302, color=7, tag='-')
    chain_gloves = item(2, ['armour','On hands','iron'],[],'',30, 0, 'chain gloves', id=303, color=7, tag=')')
    chain_cloak = item(10, ['armour','Back','iron','leather'],[],'',60, 0, 'chain cloak', id=304, color=7, tag=')')
    chain_hat = item(2, ['armour','Head','iron'],[],'',20, 0, 'chain coif', id=305, color=7, tag='^')
    chain_boots = item(4, ['armour','Feet','iron','leather','wood'],[],'',30, 0, 'chain boots', id=306, color=7, tag='_')

    chain_armour = (chain_pants,chain_vest,chain_cloak,chain_belt,chain_gloves,chain_hat,chain_boots)

    ## Plate armour(armour 520,wgt 88), IDs 400-
    plate_chest= item(40,['armour','Chest','iron','leather'],[],'',200,0,'chestplate',400,False,1,{},8,'[')
    plate_pants = item(25, ['armour','Legs','iron','leather'],[],'',150, 0, 'greaves', id=401, color=8, tag='(')
    plate_belt = item(6, ['armour','Belt','iron','leather'],[],'',30, 0, 'plate belt', id=402, color=8, tag='-')
    plate_gloves = item(5, ['armour','On hands','iron','leather'],[],'',40, 0, 'plate gloves', id=403, color=8, tag=')')
    plate_helm = item(3, ['armour','Head','iron'],[],'',40, 0, 'plate helm', id=404, color=8, tag='^')
    plate_boots = item(9, ['armour','Feet','iron'],[],'',60, 0, 'plate boots', id=405, color=8, tag='_')

    plate_armour = (plate_pants,plate_chest,plate_belt,plate_gloves,plate_helm,plate_boots)

    ## Wooden armour(armour 270,wgt 35), IDs 600-
    wood_vest = item(10,['armour','Chest','wood'],[],'',80,0,'living wood chestplate',600,False,1,{},10,'[')
    wood_pants = item(9, ['armour','Legs','wood'],[],'',80, 0, 'living wood pants', id=601, color=10, tag='(')
    wood_belt = item(2, ['armour','Belt','wood'],[],'',15, 0, 'living wood belt', id=602, color=10, tag='-')
    wood_gloves = item(2, ['armour','On hands','wood'],[],'',20, 0, 'living wood gloves', id=603, color=10, tag=')')
    wood_cloak = item(8, ['armour','Back','wood'],[],'',40, 0, 'cloak of leaves', id=604, color=10, tag=')')
    wood_hat = item(1, ['armour','Head','wood'],[],'',15, 0, 'living wood helm', id=605, color=10, tag='^')
    wood_boots = item(3, ['armour','Feet','wood'],[],'',20, 0, 'living wood boots', id=606, color=10, tag='_')

    wood_armour = (wood_pants,wood_vest,wood_cloak,wood_belt,wood_gloves,wood_hat,wood_boots)

    ##Herbs&Flowers, IDs 900-
    ##Po spisuci se razpredelqt i se zapisvat v 'gather' na herb set-ovete za localizaciq po tereni
    ##Chance dava vuzmojnostta da se nameri bilkata v %, koito se umnojava po Int na geroq
    herb = item(0.01,['herb','material','cookmat'],[],'',0, 0, 'herb',900,True,1,{'chance':5,'cook':'herb'},10,'*')
    flower = item(0.2,['expendable','material','craftmat','flowers'],['flowers'],'',0,0,'flower',901,True,1,{'craft':'flowers','force':{'Nature':{'force':0.01}}},192,'*')
    vegetable = item(0.5, ['food','cookmat'],[],'',0,0,'vegetable',902,True,1,{'hunger':20,'thirst':5,'energy':20,'cook':'vegetable'},2,tag=',')
    rare_flower = item(0.2,['material','expendable','craftmat','rare flower'],[],'',0,0,'rare flower',903,True,1,{'craft':'rare flowers',},192,'*')

    vegetables = (vegetable,)
    flowers = (flower,)
    herbs = (herb,)

    ##Treasure, IDs 1000-
    coins_copper = item(0.01,['treasure','coin','copper'],[],'',0,0,'copper coins', id=1000, stackable=True, color=6, tag='$')
    coins_silver = item(0.01,['treasure','coin','silver'],[],'',0,0,'silver coins', 1001, stackable=True, color=15, tag='$')
    coins_gold = item(0.01,['treasure','coin','gold'],[],'',0,0,'gold coins', 1002, stackable=True, color=14, tag='$')
    coins_ancient_copper = item(0.01,['treasure','coin','ancient','copper'],[],'',0,0,'ancient copper coins', id=1003, stackable=True, color=6, tag='$')
    coins_ancient_silver = item(0.01,['treasure','coin','ancient','silver'],[],'',0,0,'ancient silver coins', 1004, stackable=True, color=15, tag='$')
    coins_ancient_gold = item(0.01,['treasure','coin','ancient','gold'],[],'',0,0,'ancient gold coins', 1005, stackable=True, color=14, tag='$')
    jewel_ring = item(0.01,['treasure','jewel','ring','Left ring','Right ring'],[],'',0,0,'ring', 1006, stackable=False, color=7, tag='$')
    jewel_crown = item(1,['treasure','jewel','crown','Head'],[],'',0,0,'crown', 1007, stackable=False, color=7, tag='$')
    jewel_bracelet = item(0.3,['treasure','jewel','bracelet','Jewel'],[],'',0,0,'bracelet', 1008, stackable=False, color=7, tag='$')
    jewel_necklace = item(0.3,['treasure','jewel','necklace','Neck'],[],'',0,0,'necklace', 1009, stackable=False, color=7, tag='$')
    jewel_earring = item(0.03,['treasure','jewel','earring','Jewel'],[],'',0,0,'earring', 1010, stackable=False, color=7, tag='$')
    jewel_chain = item(0.5,['treasure','jewel','chain','Neck','Jewel'],[],'',0,0,'chain', 1011, stackable=False, color=7, tag='$')
    jewel_pendant = item(0.5,['treasure','jewel','pendant','Jewel'],[],'',0,0,'pendant', 1012, stackable=False, color=7, tag='$')
    jewel_brooch = item(0.2,['treasure','jewel','brooch','Jewel'],[],'',0,0,'brooch', 1013, stackable=False, color=7, tag='$')
    jewel_hairpin = item(0.05,['treasure','jewel','hairpin','Jewel'],[],'',0,0,'hairpin', 1014, stackable=False, color=7, tag='$')
    jewel_tiara = item(0.8,['treasure','jewel','tiara','Head'],[],'',0,0,'tiara', 1015, stackable=False, color=7, tag='$')
    jewel_diadem = item(0.5,['treasure','jewel','diadem','Head'],[],'',0,0,'diadem', 1016, stackable=False, color=7, tag='$')
    tumi = item(1, ['treasure','jewel','Jewel'],['cutting'],'',0, 0, 'tumi', 1017,False,effect={'temp_attr':[['Dex',+1]]},color=7,tag='/')
    the_golden_stool = item(5, ['treasure','furniture','UNIQUE','gold','wood'],[],'',0, 0, 'The Golden Stool', 1018,False,color=14,tag='-')
    gem_diamond = item(0.02,['treasure','gem','diamond'],[],'',0,0,'diamond', 1019, stackable=True, effect={'gnome_gem':['wWO','diamond_mess'],'talisman':{'temp_attr':[['Cre',2]]}}, color=15, tag='$')
    gem_emerald = item(0.02,['treasure','gem','emerald'],[],'',0,0,'emerald', 1020, stackable=True, effect={'gnome_gem':['g','emerald_mess'],'talisman':{'temp_attr':[['End',1]]}}, color=10, tag='$')
    gem_sapphire = item(0.02,['treasure','gem','sapphire'],[],'',0,0,'sapphire', 1021, stackable=True, effect={'gnome_gem':["F'i",'sapphire_mess'],'talisman':{'temp_attr':[['Cre',1]]}}, color=1, tag='$')
    gem_ruby = item(0.02,['treasure','gem','ruby'],[],'',0,0,'ruby', 1022, stackable=True, effect={'gnome_gem':[".,+><aAbBdDfFgiIJlLmnoOpsStTwW%#`'~:",'ruby_mess'],'talisman':{'temp_attr':[['End',2]]}}, color=4, tag='$')
    gem_pearl = item(0.02,['treasure','gem','pearl'],[],'',0,0,'stone pearl', 1023, stackable=True, effect={'gnome_gem':['wWO','diamond_mess'],'talisman':{'temp_attr':[['Mnd',2]]}}, color=7, tag='$')
    gem_amethyst = item(0.02,['treasure','gem','amethyst'],[],'',0,0,'amethyst', 1024, stackable=True, effect={'gnome_gem':['n','amethyst_mess'],'talisman':{'temp_attr':[['Dex',2]]}}, color=5, tag='$')
    gem_topaz = item(0.02,['treasure','gem','topaz'],[],'',0,0,'topaz', 1025, stackable=True, effect={'gnome_gem':[".,+><aAbBdDfFgiIJlLmnoOpsStTwW%#`'~:",'topaz_mess'],'talisman':{'temp_attr':[['Dex',1]]}}, color=14, tag='$')
    gem_tourmaline = item(0.02,['treasure','gem','tourmaline'],[],'',0,0,'tourmaline', 1026, stackable=True, effect={'gnome_gem':["g.adDFp,~'i:",'tourmaline_mess'],'talisman':{'temp_attr':[['Str',1]]}}, color=2, tag='$')
    gem_garnet = item(0.02,['treasure','gem','garnet'],[],'',0,0,'garnet', 1027, stackable=True, effect={'gnome_gem':[".,+><aAbBdDfFgiIJlLmnoOpsStTwW%#`'~:",'garnet_mess'],'talisman':{'temp_attr':[['Str',2]]}}, color=12, tag='$')
    gem_aquamarine = item(0.02,['treasure','gem','aquamarine'],[],'',0,0,'aquamarine', 1028, stackable=True, effect={'gnome_gem':["g.adDFp,~'i:",'aquamarine_mess'],'talisman':{'temp_attr':[['Mnd',1]]}}, color=3, tag='$')
    gem_opal = item(0.02,['treasure','gem','opal'],[],'',0,0,'opal', 1029, stackable=True, effect={'gnome_gem':['n','opal_mess'],'talisman':{'temp_attr':[['Int',2]]}}, color=154, tag='$')
    gem_turquoise = item(0.02,['treasure','gem','turquoise'],[],'',0,0,'turquoise', 1030, stackable=True, effect={'gnome_gem':['tw','turquoise_mess'],'talisman':{'temp_attr':[['Int',1]]}}, color=11, tag='$')
    gem_lapis_lazuli = item(0.02,['treasure','gem','lapis lazuli'],[],'',0,0,'lapis lazuli', 1031, stackable=True, effect={'gnome_gem':['n','lapis_mess'],'talisman':{'temp_attr':[['Dex',1],['End',1]]}}, color=9, tag='$')
    ##coins_copper = item(0.05,['treasure','coin','copper'],[],'',0,0,'copper coins', 1003, stackable=True, color=14, tag='$')
    ##coins_copper = item(0.05,['treasure','coin','copper'],[],'',0,0,'copper coins', 1004, stackable=True, color=14, tag='$')
    ##coins_copper = item(0.05,['treasure','coin','copper'],[],'',0,0,'copper coins', 1005, stackable=True, color=14, tag='$')

    treasure_money = (coins_copper,coins_silver,coins_gold,coins_ancient_copper,coins_ancient_silver,coins_ancient_gold)
    gems = (gem_diamond,gem_emerald,gem_sapphire,gem_ruby,gem_pearl,gem_amethyst,gem_topaz,gem_tourmaline,gem_garnet,
            gem_aquamarine,gem_opal,gem_turquoise,gem_lapis_lazuli)
    small_treasure = (jewel_hairpin,jewel_brooch,jewel_pendant,jewel_earring,jewel_bracelet,jewel_ring)
    medium_treasure = (jewel_diadem,jewel_tiara,jewel_chain,jewel_necklace,tumi)
    large_treasure = (jewel_crown,)
    unique_treasure = (the_golden_stool,)

    ##Misc equipment, IDs 1200-
    herb_set = item(1,['herb_set','wood'],['herb_set'],'',0,0,'herb collecting set',1200,False,1,{'gather':{'g':herbs}},7,'"')
    magic_book = item(2,['magic_book','paper'],['magic_book'],'',0,0,'book of magical theory',1201,False,1,{'devise_spell':'devise'},12,'"')
    lockpicks = item(1,['lockpick','iron'],['lockpick'],'',0,0,'lockpick set',1202,False,1,{},7,'"')
    nature_heal_set = item(1,['heal_set','wood'],['nature healing set'],'',0,0,"nature healer's set",1203,False,1,{},7,'"')

    not_included= (magic_book,)
    misc_equipment = (herb_set,lockpicks,nature_heal_set)

    ##Goods (trading and materials), IDs 2,3,4,5,6,7,9,14,16,1300-
    ## Razlichni semena davat razlichni efekti - ako sa cvetq,hrasti,durveta,treva - Nature, ako sa kulturni sortove - Red,
    ## ako sa trunlivi hrasti ili nqkakvi mutanti - Chaos
    bread = item(1, ['food','cookmat'],[],'',0,-2,'bread',2,True,1,{'hunger':30,'thirst':0,'energy':20,'cook':'bread'},2,tag=',')
    bottle_water = item(1, ['drink','cookmat'],['water'],'',0,0,'full waterskin',3,True,1,{'cook':'water','hunger':0,'thirst':30,'energy':20,'container':7},2,tag=',')
    rock = item(3, ['craftmat','buildmat','material','rock','Right hand','Left hand'],['crude hammer','rock'],'',0,1,'rock',4,True,1,{'build':'rock','break_rock':gems,'craft':'rock'},tag='*')
    dust = item(3, ['material'],[],'',0,0,'dust',6,True,1,{},color=5,tag='*')
    bottle = item(0.5,['material','m-short','bottle'],['bottle'],'',0,0,'empty waterskin',7,True,1,{'fill':{'w':3,'O':3}},7,',')
    flower_seed = item(0,['seed'],['seed'],'',0,0,'flower seed',9,True,1,
                       {'plant_seed':flowers,'force':{'Nature':{'force':0.01,'elf':0.01,'terrain':.05},'Chaos':{'all':-.01}}},10,'.')
    tree_log = item(2, ['craftmat','expendable','buildmat','material', 'two_handed','m-long','wood'],['wood'],'',0, 2,'piece of wood',14,True,1,{'build':'wood','craft':'wood'},color=6,tag='|')
    string = item(0,['material','m-connect','Right hand','Left hand'],[],'',0,0,'string',16,True,1,{},7,'~')
    common_spices = item(1,['goods','spice','cookmat'],['common spices'],'',0,0,'common spices',1300,True,1,{'cook':'spice'},14,'"')
    fruit = item(1, ['food','cookmat'],[],'',0,-2,'fruit',1301,True,1,{'hunger':20,'thirst':5,'energy':20,'cook':'fruit'},12,tag=',')
    berries = item(1, ['food','cookmat'],[],'',0,-2,'berries',1302,True,1,{'hunger':20,'thirst':5,'energy':20,'cook':'fruit'},5,tag=',')
    earth = item(3, ['expendable','material'],['earth'],'',0,0,'earth',1303,True,1,{'force':{'Nature':{'force':0.01}}},color=6,tag='*')
    color_clay = item(3, ['expendable','buildmat','material','clay'],['color clay','clay'],'',0,0,'colorful clay',1304,True,1,{'build':'clay','force':{'Nature':{'force':0.01}}},color=13,tag='*')
    wild_flowers = item(0.01, ['expendable','craftmat','material','flowers'],['flowers'],'',0,0,'wild flowers',1305,True,1,{'craft':'flowers','force':{'Nature':{'force':0.01}}},color=5,tag='*')
    clay = item(3, ['expendable','buildmat','material','clay'],['clay'],'',0,0,'clay',1306,True,1,{'build':'clay','force':{'Order':{'force':0.01}}},color=6,tag='*')
    seed_life = item(0,['seed','treasure'],['seed of life'],'',0,0,'Seed of Life',1307,True,1,
                       {'plant_seed':flowers,'force':{'Nature':{'force':0.5,'elf':0.5,'terrain':1},'Chaos':{'all':-.5}}},12,'*')
    earth_ore = item(5, ['material','ore','m-short','ammunition','tool','weapon','Right hand','Left hand'],['crude hammer'],'',0,1,'earth ore',1308,True,1,{},color=6,tag='*')
    chaos_rock = item(5, ['material'],[],'',0,1,'chaos rock',1309,True,1,
                      {'mass destruction':10,'force':{'Chaos':{'force':12,'ork':2,'goblin':2,'kraken':2,'imp':2,'spirit of chaos':2,'troll':2},'Nature':{'all':-10},'Order':{'all':-10}}},color=128,tag='*')
    raw_meat = item(1, ['raw meat','cookmat'],[],'',0,-2,'raw meat',1310,True,1,{'force':{'Chaos':{'force':0.03,'ork':0.03},'Nature':{'all':-0.5},'Order':{'all':-0.5}},'hunger':30,'thirst':0,'energy':20,'cook':'raw meat'},4,tag=',')
    sweet_bread = item(1, ['food','cookmat'],[],'',0,-2,'sweet bread',1311,True,1,{'hunger':50,'thirst':0,'energy':120,'cook':'sweet bread'},12,tag=',')
    fruit_juice = item(1, ['drink','cookmat'],[],'',0,0,'bottle of juice',1312,True,1,{'cook':'juice','hunger':0,'thirst':50,'energy':70,'container':7},12,tag=',')
    roasted_meat = item(1, ['food'],[],'',0,0,'roasted meat',1313,True,1,{'hunger':50,'thirst':0,'energy':100},6,tag=',')
    skin = item(2, ['craftmat','material','skin','leather'],[],'',0,0,'skin',1314,True,1,{'craft':'leather'},6,tag='~')
    vegetable_seed = item(0,['seed'],['seed'],'',0,0,'vegetable seed',1315,True,1,
                       {'plant_vegetable':vegetables,'force':{'Order':{'force':0.01,'human':0.01,'terrain':.05},
                                                                'Chaos':{'all':-.01}}},10,'.')
    vegetable_soup = item(1, ['drink'],[],'',0,0,'bottle of soup',1316,True,1,{'hunger':20,'thirst':60,'energy':100,'container':7},10,tag=',')
    iron_ingot = item(5, ['craftmat','buildmat','material','iron'],['iron'],'',0,1,'iron ingot',1317,True,1,{'craft':'iron','build':'iron'},color=7,tag='-')
    wood_arrow = item(0.1,['Ammunition','wood'],[],'',0,1,'wooden arrow',1318,True,1,{'shoot':'arrow'},6,'|')
    wood_bolt = item(0.1,['Ammunition','wood'],[],'',0,1,'wooden bolt',1319,True,1,{'shoot':'bolt'},8,'|')
    stone = item(0.1,['Ammunition','rock'],[],'',0,1,'stone',1320,True,1,{'shoot':'stone'},8,'*')
    raw_egg = item(.1, ['raw egg','cookmat'],[],'',0,-2,'raw egg',1321,True,1,{'cook':'raw egg'},15,tag=',')
    milk = item(1, ['drink','cookmat'],[],'',0,0,'milk',1322,True,1,{'cook':'milk','thirst':30,'energy':20,'container':7},15,tag=',')
    feather = item(.05, ['craftmat','feather'],[],'',0,-2,'feather',1323,True,1,{'craft':'feather'},7,tag='~')
    boiled_egg = item(.1, ['boiled egg','cookmat','food'],[],'',0,-2,'boiled egg',1324,True,1,{'hunger':15,'energy':20,'cook':'boiled egg'},15,tag=',')
    metal_ingot = item(3, ['craftmat','material'],[],'',0,1,'ingot',1325,True,1,{},color=7,tag='-')
    ore = item(5, ['material','ore','m-short','Right hand','Left hand'],['crude hammer'],'',0,1,'ore',5,True,1,{'smelt_ore':[iron_ingot,metal_ingot]},color=8,tag='*')
    bone = item(.2, ['craftmat','bone'],[],'',0,0,'bone',1326,True,1,{'craft':'bone'},15,tag='~')

    foraged=(berries,fruit)
    goods = (rock,ore,dust,tree_log,string,common_spices,bread,bottle_water,bottle,fruit,berries,flower_seed,earth,color_clay,
             wild_flowers,clay,seed_life,earth_ore,chaos_rock,raw_meat,sweet_bread,fruit_juice,roasted_meat,skin,vegetable_seed,
             vegetable_soup,iron_ingot,wood_arrow,wood_bolt,stone,raw_egg,milk,feather,boiled_egg,metal_ingot,bone,rare_flower)

    all_items =(spike_shield,)+tools+tiny_containers+small_containers+medium_containers+large_containers+treasure_money+gems+small_treasure+medium_treasure+large_treasure+unique_treasure+goods+misc_equipment+cloth_armour+leather_armour+chain_armour+plate_armour+wood_armour+light_weapons+medium_weapons+heavy_weapons+ranged_weapons+herbs+flowers+vegetables

    ################################ LIVING INSTANCES #########################
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


    ## VARIABLES
    all_beings = []
    all_creatures = []
    hidden = [] ## Sudurja skritite sushtestva i tezi koito ne sa se poqvili, no se poqvqvat po princip v mestnostta i sa
                ## unikalni (ne random) i imat mode = 'not_appeared'!!!


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
    ch = 0
    c = Console.getconsole()
    c.title("Balance")
    c.cursor(1)
    land = []
    directions = []
    map_coords = ''
    current_area = ''
    current_place={}
    treasure_modifier = 1
    terrain_type = ''
    world_places = {'world':[0,0]}
    top_world_places = {}
    place_descriptions = {'world':'Your country.'}
    ground_items = []
    combat_buffer = ''
    I = {}
    for i in all_items:
        I[i.id] = (i)

    map_size=10
    T_matrix = []
    force_terrains={'Nature':[["'","'",'.','g','l'],['g','g','b','g','T','n'],[',','b','g','g','g','T','J']],
                     'Chaos':[['i','.','I','F','%'],['.','d','d','D','%','B'],[',',',','.','L','B','%']],
                     'Order':[["'","'",'.','g','%'],['.','g',':','g','%','g'],[',',',',':','g','%']]}

    
    game=Game()
    game.main_loop()

################################ MAIN ^^^ #########################
