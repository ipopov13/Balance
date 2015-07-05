# -*- coding: cp1251 -*-
import player
import msvcrt
import message
import random

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

    def start_item(self,qty=1,name=''):
        item = self.duplicate(qty,name)
        player.ch.inventory.append(item)
        if player.ch.equipment['Backpack'] == []:
            player.ch.free_hands -= 1
        else:
            player.ch.backpack -= item.weight * qty
        player.ch.tool_tags += item.tool_tag
        player.ch.weight += item.weight * qty
            
    def get_item(self,qty=1,name=''):
        if name == '':
            name = self.name
        found=0
        if name == 'ring of winter' and init_screen.current_place['Temperature']>=33:
            if player.ch.equipment['Left ring']:
                if player.ch.equipment['Left ring'].name=='ring of summer':
                    found=1
                else:
                    for it in player.ch.inventory:
                        if it.name=='ring of summer':
                            found=1
                            break
            if not found:
                name+=' (melted)'
                del(self.effect['winterwalk'])
                message.use('pickup_melt', self)
            else:
                message.use('pickup', self)
        elif name == 'ring of summer' and init_screen.current_place['Temperature']<66:
            if player.ch.equipment['Right ring']:
                if player.ch.equipment['Right ring'].name=='ring of winter':
                    found=1
                else:
                    for it in player.ch.inventory:
                        if it.name=='ring of winter':
                            found=1
                            break
            if not found:
                name+=' (withered)'
                del(self.effect['summerwalk'])
                message.use('pickup_dry', self)
            else:
                message.use('pickup', self)
        else:
            message.use('pickup', self)
        has_it = 0
        for x in player.ch.inventory:
            if self.id == x.id and self.name == x.name:
                has_it = 1
                break
        if self.stackable and has_it == 1:
            x.qty += qty
            player.ch.weight += x.weight * qty
            player.ch.backpack -= x.weight * qty
        else:
            player.ch.inventory.append(self.duplicate(qty,name))
            player.ch.tool_tags += self.tool_tag
            player.ch.weight += self.weight * qty
            player.ch.backpack -= self.weight * qty

    def create_item(self,qty=1,name=''):
        has_it = 0
        if not name:
            name = self.name
        for x in player.ch.inventory:
            if self.id==x.id and name == x.name:
                has_it = 1
                break
        if (player.ch.weight + self.weight*qty <= player.ch.max_weight and self.weight*qty <= player.ch.backpack) or player.ch.equipment['Backpack'] == []:
            if self.stackable and has_it == 1:
                x.qty += qty
            else:
                player.ch.inventory.append(self.duplicate(qty,name))
                for tt in self.tool_tag:
                    player.ch.tool_tags.append(tt)
            player.ch.weight += self.weight * qty
            if player.ch.equipment['Backpack'] != []:
                player.ch.backpack -= self.weight * qty
            else:
                player.ch.free_hands -= 1
        else:
            drop = self.duplicate(qty,name)
            dropped = 0
            message.use('create_drop',drop)
            wait = msvcrt.getch()
            for item in init_screen.ground_items:
                if item[:2] == player.ch.xy and item[2].id == drop.id and item[2].name == drop.name and item[2].stackable:
                    item[2].qty += drop.qty
                    dropped = 1
            if not dropped:
                init_screen.ground_items.append([player.ch.xy[0], player.ch.xy[1],drop])

    def lose_item(self,i=1):
        if (i < self.qty):
            self.qty -= i
        else:
            if (i > self.qty):
                i = self.qty
            player.ch.inventory.remove(self)
            if self.tool_tag:
                for tag in self.tool_tag:
                    player.ch.tool_tags.remove(tag)
        player.ch.weight -= self.weight * i
        if player.ch.equipment['Backpack'] != []:
            player.ch.backpack += self.weight * i
        else:
            player.ch.free_hands += i
            if 'two_handed' in self.type:
                player.ch.free_hands += 1
        return i

    def drop_item(self,forced='',s=None):
        if self.qty >1 and not forced:
            message.message('how_much')
            a = ''
            i = ' '
            while ord(i) != 13:        
                i = msvcrt.getch()
                if ord(i) in range(48,58):
                    init_screen.c.write(i)
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
        if 'food' in self.type or ('raw meat' in self.type and 'ork2' in player.ch.tool_tags):
            if (player.ch.hunger > 0):
                self.lose_item()
                for k,v in self.effect.items():
                    player.effect(k,v)
            else:
                message.use('over_eat',self)
                i = msvcrt.getch()
        if ('drink' in self.type):
            if player.ch.thirst > 0:
                self.lose_item()
                for k,v in self.effect.items():
                    player.effect(k,v)
            else:
                message.use('over_drink',self)
                i = msvcrt.getch()

    def use_item(self,ex=''):
        if ('food' in self.type) or ('drink' in self.type) or ('raw meat' in self.type and 'ork2' in player.ch.tool_tags):
            self.eat()
        elif (ex=='expend' and 'expendable' in self.type):
            self.lose_item()
        elif (ex=='' and 'expendable' not in self.type):
            used=0
            for k,v in self.effect.items():
                if k!='temp_attr':
                    used1 = player.effect(k,v)
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
                if 'herbalism' not in player.ch.skills:
                    player.ch.skills['herbalism'] = float(player.ch.attr['Int'])
                else:
                    learn = random.uniform(0,100)
                    if learn <= (player.ch.attr['Int'] - player.ch.skills['herbalism']/5)/player.ch.attr['Int']*100:
                        player.ch.skills['herbalism'] += 0.05

def put_item(loot,xy=None):
    found_some=0
    for l in loot:
        chance = random.randint(0,10000)
        chance = chance/100.
        if l[0] == 'treasure':
            if init_screen.treasure_modifier:
                chance = chance/init_screen.treasure_modifier
            else:
                chance=100.
        elif l[0]== 'ntreasure' or l[0] == 'wtreasure':
            if player.ch.forces['Chaos']==0 and int(player.ch.forces['Nature']/10)+init_screen.treasure_modifier>0:
                chance=chance/((player.ch.forces['Nature']/10.)+init_screen.treasure_modifier)
            else:
                chance=100.
        if chance <= l[1]:
            if l[0] == 'treasure':
                creation = random_treasure(l[2],l[3])
                if l[3]==True:
                    init_screen.current_place['Treasure']-=1
                    init_screen.treasure_modifier -=1
            elif l[0] == 'ntreasure':
                if player.ch.forces['Nature']<40:
                    treasure_type=False
                    treasure_size=random.choice(['small','medium'])
                elif player.ch.forces['Nature']<75:
                    treasure_type=False
                    treasure_size=random.choice(['small','medium','large'])
                elif player.ch.forces['Nature']>75:
                    treasure_type=random.choice([False,True])
                    treasure_size=random.choice(['small','medium','large'])
                if treasure_type==True:
                    init_screen.current_place['Treasure']=max(-int(player.ch.forces['Nature']/10.),
                                                              init_screen.current_place['Treasure']-1)
                    init_screen.treasure_modifier = max(-int(player.ch.forces['Nature']/10.),
                                                        init_screen.treasure_modifier-1)
                init_screen.land[xy[1]-1] = init_screen.land[xy[1]-1][:xy[0]-21]+'.'+init_screen.land[xy[1]-1][xy[0]-20:]
                creation = random_treasure(treasure_size,treasure_type)
            elif l[0] == 'wtreasure':
                if player.ch.forces['Nature']<40:
                    treasure_type=False
                    treasure_size=random.choice(['small','medium'])
                elif player.ch.forces['Nature']<75:
                    treasure_type=False
                    treasure_size=random.choice(['small','medium','large'])
                elif player.ch.forces['Nature']>75:
                    treasure_type=random.choice([False,True])
                    treasure_size=random.choice(['small','medium','large'])
                if treasure_type==True:
                    init_screen.current_place['Treasure']=max(-int(player.ch.forces['Nature']/10.),
                                                              init_screen.current_place['Treasure']-1)
                    init_screen.treasure_modifier = max(-int(player.ch.forces['Nature']/10.),
                                                        init_screen.treasure_modifier-1)
                init_screen.land[xy[1]-1] = init_screen.land[xy[1]-1][:xy[0]-21]+'W'+init_screen.land[xy[1]-1][xy[0]-20:]
                creation = random_treasure(treasure_size,treasure_type)
            elif l[0] in player.race_attrs.keys():
                ## Can have main loot and additional items, added separately in the ground_items here
                ## Roll for quality for the main loot
                if l[0]=='ork':
                    quality=random.randint(0,100)<init_screen.current_place['Chaos']/5+init_screen.current_place['Treasure']
                    creation = random.choice(medium_weapons+heavy_weapons).duplicate(1)
                    if quality:
                        creation.name='orkish '+creation.name
                        creation.dmg=creation.dmg+1
                    if chance<=l[1]/4:
                        bonus = random.choice(plate_armour).duplicate(1)
                        init_screen.ground_items.append([xy[0], xy[1], bonus])
                    elif chance<=l[1]/2:
                        bonus = random.choice(chain_armour).duplicate(1)
                        init_screen.ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='troll':
                    quality=random.randint(0,100)<init_screen.current_place['Chaos']/5+init_screen.current_place['Treasure']
                    creation = random.choice(heavy_weapons).duplicate(1)
                    if chance<=l[1]/2:
                        if quality:
                            bonus = random.choice(gems).duplicate(1)
                            init_screen.ground_items.append([xy[0], xy[1], bonus])
                        else:
                            bonus = random.choice(treasure_money).duplicate(1)
                            init_screen.ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='spirit of chaos':
                    quality=random.randint(0,100)<init_screen.current_place['Chaos']/5+init_screen.current_place['Treasure']
                    creation = random.choice(cloth_armour).duplicate(1)
                    if quality:
                        creation.name='chaos '+creation.name
                        creation.armour=creation.armour+10
                        creation.color=12
                    if chance<=l[1]/4:
                        bonus = random.choice(misc_equipment).duplicate(1)
                        init_screen.ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='goblin':
                    quality=random.randint(0,100)<init_screen.current_place['Chaos']/5+init_screen.current_place['Treasure']
                    creation = random.choice(light_weapons).duplicate(1)
                    if quality:
                        creation.name='wicked '+creation.name
                        creation.dmg=creation.dmg+1
                    if chance<=l[1]/4:
                        bonus = random_treasure('medium')
                        init_screen.ground_items.append([xy[0], xy[1], bonus])
                    elif chance<=l[1]/2:
                        bonus = random_treasure()
                        init_screen.ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='kraken':
                    quality=random.randint(0,100)<init_screen.current_place['Chaos']/5+init_screen.current_place['Treasure']
                    creation = random.choice(leather_armour).duplicate(1)
                    if quality:
                        creation.name='sealskin '+creation.name.split()[-1]
                        creation.armour=creation.armour+10
                        creation.color=7
                elif l[0]=='imp':
                    quality=random.randint(0,100)<init_screen.current_place['Chaos']/5+init_screen.current_place['Treasure']
                    if chance<=l[1]/1:
                        creation = light_staff.duplicate(1)
                        if quality:
                            creation.name='staff of fire'
                            creation.tool_tag.append('fire')
                    else:
                        continue
                elif l[0]=='human':
                    quality=random.randint(0,100)<init_screen.current_place['Order']/5+init_screen.current_place['Treasure']
                    creation = random.choice(human_tools).duplicate(1)
                    if chance<=l[1]/2:
                        if quality:
                            bonus = random.choice([medium_backpack,large_backpack]).duplicate(1)
                            init_screen.ground_items.append([xy[0], xy[1], bonus])
                        else:
                            bonus = random.choice(small_containers).duplicate(1)
                            init_screen.ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='dwarf':
                    quality=random.randint(0,100)<init_screen.current_place['Order']/5+init_screen.current_place['Treasure']
                    creation = random.choice([pick,shovel,pickaxe]).duplicate(1)
                    if quality:
                        creation.name='dwarven '+creation.name
                        creation.tool_tag=['shovel','pick','pickaxe']
                        if 'weapon' not in creation.type:
                            creation.type.append('weapon')
                        creation.dmg=2
                        creation.color=6
                elif l[0]=='spirit of order':
                    quality=random.randint(0,100)<init_screen.current_place['Order']/5+init_screen.current_place['Treasure']
                    creation = random.choice(cloth_armour).duplicate(1)
                    if quality:
                        creation.name='order '+creation.name
                        creation.armour=creation.armour+10
                        creation.color=9
                    if chance<=l[1]/4:
                        bonus = random.choice(misc_equipment).duplicate(1)
                        init_screen.ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='elf':
                    quality=random.randint(0,100)<init_screen.current_place['Nature']/5+init_screen.current_place['Treasure']
                    creation = random.choice(leather_armour).duplicate(1)
                    if quality:
                        creation.name='elven '+creation.name
                        creation.armour=creation.armour+15
                        creation.color=15
                    if chance<=l[1]/2:
                        bonus = random.choice(flowers+(flower_seed,)).duplicate(1)
                        init_screen.ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='gnome':
                    quality=random.randint(0,100)<init_screen.current_place['Nature']/5+init_screen.current_place['Treasure']
                    creation = random.choice(gems).duplicate(1)
                    if quality:
                        bonus = color_clay.duplicate(5)
                        init_screen.ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='spirit of nature':
                    quality=random.randint(0,100)<init_screen.current_place['Nature']/5+init_screen.current_place['Treasure']
                    creation = flower_seed.duplicate(1)
                    if quality:
                        bonus = random.choice(gems).duplicate(1)
                        init_screen.ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='dryad':
                    quality=random.randint(0,100)<init_screen.current_place['Nature']/5+init_screen.current_place['Treasure']
                    creation = random.choice(wood_armour).duplicate(1)
                    if quality:
                        creation.name='masterwork '+creation.name
                        creation.armour=creation.armour+15
                        creation.color=2
                    if chance<=l[1]/3:
                        bonus = random.choice(light_weapons).duplicate(1)
                        init_screen.ground_items.append([xy[0], xy[1], bonus])
                elif l[0]=='water elemental':
                    quality=random.randint(0,100)<init_screen.current_place['Nature']/5+init_screen.current_place['Treasure']
                    creation = bottle_water.duplicate(1)
                    if quality:
                        creation.name='bottle of pure water'
                        creation.effect={'cook':'water','thirst':60,'energy':60,'container':7}
                elif l[0]=='fairy':
                    quality=random.randint(0,100)<init_screen.current_place['Nature']/5+init_screen.current_place['Treasure']
                    creation = random.choice(flowers+herbs).duplicate(1)
                    if chance<=l[1]/3:
                        if quality:
                            bonus = random_treasure('medium')
                            init_screen.ground_items.append([xy[0], xy[1], bonus])
                        else:
                            bonus = random_treasure()
                            init_screen.ground_items.append([xy[0], xy[1], bonus])
            elif l[0] == 'forage':
                qty = random.randint(l[2],l[3])
                creation = random.choice(foraged).duplicate(qty)
            elif l[0] == 'gnome_touch':
                creation = random.choice(gems).duplicate(1)
            elif l[0] == 'fairy_flowers':
                creation = rare_flower.duplicate(1)
                if 'fairy2' in player.ch.tool_tags:
                    if 550<player.ch.turn%2400<650:
                        creation.name='noon flower'
                        creation.color=190#224
                    elif 1750<player.ch.turn%2400<1850:
                        creation.name='midnight flower'
                        creation.color=30#208
                    elif init_screen.current_place['Temperature']<33 and random.random()>init_screen.current_place['Temperature']/33.:
                        creation.name='frost flower'
                        creation.color=155#144
                    elif init_screen.current_place['Temperature']>=66 and random.random()<init_screen.current_place['Temperature']-65/35.:
                        creation.name='desert flower'
                        creation.color=206
            elif 'skin' in str(l[0]):
                qty = random.randint(l[2],l[3])
                creation = skin.duplicate(qty)
                creation.name=l[0]
            else:
                qty = random.randint(l[2],l[3])
                creation = init_screen.I[l[0]].duplicate(qty)
            if xy:
                found_it=0
                for existing in init_screen.ground_items:
                    if existing[:2]==xy and existing[2].id==creation.id and existing[2].name==creation.name:
                        existing[2].qty+=creation.qty
                        found_it=1
                        break
                if not found_it:
                    init_screen.ground_items.append([xy[0], xy[1], creation])
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
magic_book = item(2,['magic_book','paper'],['magic_book'],'',0,0,'book of magical theory',1201,False,1,{},12,'"')
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
