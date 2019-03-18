import msvcrt
import random

class Item:
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

    def duplicate(self,i=1,name=''):
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
            if type(self.effect[key]) is list:
                ef[key]=self.effect[key][:]
            else:
                ef[key]=self.effect[key]
        if 'ingot' in name:
            if 'craft' not in ef:
                ef['craft']='%s' %(name.split()[0])
        ## The dictionary links names and colours
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
        ## Jewelery metal type is added so they can be smelted
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
        return Item(self.weight, t, self.tool_tag, self.weapon_type, self.armour, self.dmg, name,
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
        self.game.player.inventory.append(item)
        if self.game.player.equipment['Backpack'] == []:
            self.game.player.free_hands -= 1
        else:
            self.game.player.backpack -= item.weight * qty
        self.game.player.tool_tags += item.tool_tag
        self.game.player.weight += item.weight * qty
            
    def get_item(self,qty=1,name=''):
        if name == '':
            name = self.name
        found=0
        if name == 'ring of winter' and self.game.current_place['Temperature']>=33:
            if self.game.player.equipment['Left ring']:
                if self.game.player.equipment['Left ring'].name=='ring of summer':
                    found=1
                else:
                    for it in self.game.player.inventory:
                        if it.name=='ring of summer':
                            found=1
                            break
            if not found:
                name+=' (melted)'
                del(self.effect['winterwalk'])
                self.game.message.use('pickup_melt', self)
            else:
                self.game.message.use('pickup', self)
        elif name == 'ring of summer' and self.game.current_place['Temperature']<66:
            if self.game.player.equipment['Right ring']:
                if self.game.player.equipment['Right ring'].name=='ring of winter':
                    found=1
                else:
                    for it in self.game.player.inventory:
                        if it.name=='ring of winter':
                            found=1
                            break
            if not found:
                name+=' (withered)'
                del(self.effect['summerwalk'])
                self.game.message.use('pickup_dry', self)
            else:
                self.game.message.use('pickup', self)
        else:
            self.game.message.use('pickup', self)
        has_it = 0
        for x in self.game.player.inventory:
            if self.id == x.id and self.name == x.name:
                has_it = 1
                break
        if self.stackable and has_it == 1:
            x.qty += qty
            self.game.player.weight += x.weight * qty
            self.game.player.backpack -= x.weight * qty
        else:
            self.game.player.inventory.append(self.duplicate(qty,name))
            self.game.player.tool_tags += self.tool_tag
            self.game.player.weight += self.weight * qty
            self.game.player.backpack -= self.weight * qty

    def create_item(self,qty=1,name=''):
        has_it = 0
        if not name:
            name = self.name
        for x in self.game.player.inventory:
            if self.id==x.id and name == x.name:
                has_it = 1
                break
        if (self.game.player.weight + self.weight*qty <= self.game.player.max_weight and self.weight*qty <= self.game.player.backpack) or \
           self.game.player.equipment['Backpack'] == []:
            if self.stackable and has_it == 1:
                x.qty += qty
            else:
                self.game.player.inventory.append(self.duplicate(qty,name))
                for tt in self.tool_tag:
                    self.game.player.tool_tags.append(tt)
            self.game.player.weight += self.weight * qty
            if self.game.player.equipment['Backpack'] != []:
                self.game.player.backpack -= self.weight * qty
            else:
                self.game.player.free_hands -= 1
        else:
            drop = self.duplicate(qty,name)
            dropped = 0
            self.game.message.use('create_drop',drop)
            msvcrt.getch()
            for item in self.game.ground_items:
                if item[:2] == self.game.player.xy and item[2].id == drop.id and item[2].name == drop.name and item[2].stackable:
                    item[2].qty += drop.qty
                    dropped = 1
            if not dropped:
                self.game.ground_items.append([self.game.player.xy[0], self.game.player.xy[1],drop])

    def lose_item(self,i=1):
        if (i < self.qty):
            self.qty -= i
        else:
            if (i > self.qty):
                i = self.qty
            self.game.player.inventory.remove(self)
            if self.tool_tag:
                for tag in self.tool_tag:
                    self.game.player.tool_tags.remove(tag)
        self.game.player.weight -= self.weight * i
        if self.game.player.equipment['Backpack'] != []:
            self.game.player.backpack += self.weight * i
        else:
            self.game.player.free_hands += i
            if 'two_handed' in self.type:
                self.game.player.free_hands += 1
        return i

    def drop_item(self,forced=False,space_needed=100000):
        if self.qty >1 and not forced:
            self.game.message.message('how_much')
            a = ''
            i = ' '
            while ord(i) != 13:        
                i = msvcrt.getch()
                if ord(i) in range(48,58):
                    self.game.c.write(i)
                    a += i
            if self.weight*min([self.qty,int(a)]) > space_needed or int(a)==0:
                return None
            i = self.lose_item(int(a))
            duplica = self.duplicate(i)
            return duplica
        else:
            i = self.lose_item(self.qty)
            return self

    def eat(self):      
        if 'food' in self.type or ('raw meat' in self.type and 'ork2' in self.game.player.tool_tags):
            if self.game.player.hunger > 0:
                self.lose_item()
                for k,v in self.effect.items():
                    self.game.effect(k,v)
            else:
                self.game.message.use('over_eat',self)
                msvcrt.getch()
        if 'drink' in self.type:
            if self.game.player.thirst > 0:
                self.lose_item()
                for k,v in self.effect.items():
                    self.game.effect(k,v)
            else:
                self.game.message.use('over_drink',self)
                msvcrt.getch()

    def use_item(self,ex=''):
        if 'food' in self.type or 'drink' in self.type or ('raw meat' in self.type and 'ork2' in self.game.player.tool_tags):
            self.eat()
        elif ex=='expend' and 'expendable' in self.type:
            self.lose_item()
        elif ex=='' and 'expendable' not in self.type:
            used=0
            for k,v in self.effect.items():
                if k!='temp_attr':
                    used1 = self.game.effect(k,v)
                    if k=='transform':
                        del(self.effect['transform'])
                    if used1==None:
                        used+=1
##                    elif used1==0:
##                        used=0
            if used == 0:
                return 0
            if 'herb_set' not in self.tool_tag and 'magic_book' not in self.tool_tag\
                and 'totem' not in self.type and self.name!='lapis lazuli':
                self.lose_item()
            if 'herb_set' in self.tool_tag:
                if 'herbalism' not in self.game.player.skills:
                    self.game.player.skills['herbalism'] = float(self.game.player.attr['Int'])
                else:
                    learn = random.uniform(0,100)
                    if learn <= (self.game.player.attr['Int'] - self.game.player.skills['herbalism']/5)/self.game.player.attr['Int']*100:
                        self.game.player.skills['herbalism'] += 0.05

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

spike_shield = Item(9,['armour','Right hand','Left hand','leather','iron'],[],'',30,1,'spiked shield',10,False,1,{'temp_attr':[['Dex',1]]},8,'}')

## Tools, IDs 1,500-
pick = Item(8, ['tool','weapon','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['pick'],'pick',0, 1, 'pick', id=1,tag='/')
shovel = Item(5, ['tool','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['shovel'],'',0, 1, 'shovel', id=500,tag='/')
pickaxe = Item(8, ['tool','weapon','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['pickaxe'],'pick',0, 1, 'pickaxe', id=501,tag='/')
tinderbox = Item(1, ['tool','iron','wood'],['fire'],'',0,0,'tinder-box',502,color=8,tag='=')
cauldron = Item(50, ['tool','iron'],['cauldron'],'',0,0,'cauldron',503,color=8,tag='O')
anvil = Item(250, ['tool','iron'],['anvil'],'',0,0,'anvil',504,color=8,tag='-')
forge = Item(1500, ['tool','iron'],['forge'],'',0,0,"blacksmith's forge",505,color=12,tag='O')
working_table = Item(200, ['tool','wood'],['work_table'],'',0,0,'work table',506,color=6,tag='-')
hammer = Item(3, ['tool','weapon','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['hammer'],'hammer',0, 1, 'hammer', id=507,tag='/')
saw = Item(3, ['tool','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['saw'],'',0, 1, 'saw', id=508,tag='/')
chisel = Item(1.5, ['tool','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['chisel'],'',0, 1, 'chisel', id=509,tag='/')
pliers = Item(1.5, ['tool','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['pliers'],'',0, 0, 'pliers', id=510,tag='/')
needle = Item(0.02, ['tool','Belt tool 1','Belt tool 2','Right hand','Left hand','wood','iron'],['needle'],'',0, 0, 'needle', id=511,tag='/')

tools = (pick,shovel,pickaxe,tinderbox,cauldron,anvil,forge,working_table,hammer,saw,chisel,pliers,needle)
human_tools=(pick,shovel,pickaxe,tinderbox,hammer,saw,chisel,pliers,needle)
house_generated=(cauldron,anvil,forge,working_table)

## Containers, IDs 11,17,18-
wooden_chest = Item(50,['container','two_handed','locked','wood'],[],'',0,1,'wooden chest',11,False,1,{'contains':[],'lock_strength':15},6,'=')
small_backpack = Item(4,['container','Backpack','leather'],[],'',0,0,'small backpack',17,False,1,{'contains':[]},7,'=')
shoulder_bag = Item(2,['container','Backpack','leather'],[],'',0,0,'shoulder bag',18,False,1,{'contains':[]},7,'=')
small_chest = Item(20,['container','two_handed','wood'],[],'',0,1,'small chest',19,False,1,{'contains':[],'lock_strength':15},6,'=')
wooden_box = Item(8,['container','two_handed','wood'],[],'',0,0,'wooden box',20,False,1,{'contains':[]},7,'=')
talisman_pouch = Item(0.01,['talisman','container','leather','Neck'],[],'',0,0,'talisman pouch',21,False,1,{'contains':[]},7,'=')
ivory_box = Item(8,['container','two_handed','ivory'],[],'',0,0,'ivory box',22,False,1,{'contains':[]},7,'=')
medium_backpack = Item(7,['container','Backpack','leather'],[],'',0,0,'medium backpack',23,False,1,{'contains':[]},7,'=')
large_backpack = Item(10,['container','Backpack','leather'],[],'',0,0,'large backpack',24,False,1,{'contains':[]},7,'=')

tiny_containers = (talisman_pouch,)
small_containers = (shoulder_bag,small_backpack)
medium_containers = (small_chest,wooden_box,ivory_box,medium_backpack,large_backpack)
large_containers = (wooden_chest,)

## Weapons, IDs 12,13,15,50-
## light <5
## medium <10
## heavy >=10
## weapon types: long sword, club, axe, staff, dagger, big hammer, short sword, bow, crossbow, sling, hammer, pick
long_sword = Item(6, ['weapon','Right hand','Left hand','iron'],['cutting'],'long sword',0,2,'long sword',12,tag='/')
axe = Item(6, ['tool','weapon','Belt tool 1','Belt tool 2','Right hand','Left hand','iron'],['axe'],'axe',0, 2, 'axe', id=13,tag='/')
club = Item(6, ['weapon','Right hand','Left hand','wood'],['crude hammer'],'club',0, 2, 'club', 15,tag='/')
light_staff = Item(3, ['weapon','two_handed','Right hand','Left hand','wood'],['leverage'],'staff',0, 1, 'light wooden staff', 50,color=6,tag='/')
dagger = Item(2, ['weapon','Right hand','Left hand','iron'],['cutting'],'dagger',0,1,'dagger',51,color=7,tag='/')
sceptre = Item(10, ['weapon','two_handed','Right hand','Left hand','iron'],['big hammer'],'big hammer',0,3,'sceptre', 52,tag='/')
heavy_hammer = Item(12, ['weapon','two_handed','Right hand','Left hand','iron'],['big hammer'],'big hammer',0,3,'heavy hammer', id=53,tag='/')
giant_club = Item(12, ['weapon','two_handed','Right hand','Left hand','wood'],['big hammer'],'big hammer',0,3,'giant club', id=54,tag='/')
short_sword = Item(4, ['weapon','Right hand','Left hand','iron'],['cutting'],'short sword',0,2,'short sword',55,tag='/')
bow = Item(3, ['weapon','two_handed','Right hand','Left hand','wood','ranged'],[],'bow',0, 2, 'bow', 56,effect={'shoot':'arrow'},color=6,tag='{')
crossbow = Item(6, ['weapon','two_handed','Right hand','Left hand','wood','iron','ranged'],[],'crossbow',0, 2, 'crossbow', 57,effect={'shoot':'bolt'},color=7,tag='{')
sling = Item(1, ['weapon','two_handed','Right hand','Left hand','leather','ranged'],[],'sling',0, 1, 'sling', 58,effect={'shoot':'stone'},color=8,tag='{')

light_weapons = (light_staff,dagger,short_sword)
medium_weapons = (long_sword,axe,club)
heavy_weapons = (sceptre,heavy_hammer,giant_club)
ranged_weapons = (bow,sling,crossbow)

## Cloth armour(armour 14,wgt 0.7), IDs 100-
cloth_pants = Item(0.1, ['armour','Legs','cloth'],[],'',2, 0, 'pants', id=100, color=15, tag='(')
cloth_belt = Item(0.1, ['armour','Belt','cloth'],[],'',2, 0, 'belt', id=101, color=15, tag='-')
cloth_gloves = Item(0.1, ['armour','On hands','cloth'],[],'',2, 0, 'cloth gloves', id=102, color=15, tag=')')
cloth_cloak = Item(0.1, ['armour','Back','cloth'],[],'',2, 0, 'cloth cloak', id=103, color=15, tag=')')
cloth_shirt = Item(0.1, ['armour','Chest','cloth'],[],'',2, 0, 'shirt', id=104, color=15, tag='[')
cloth_hat = Item(0.1, ['armour','Head','cloth'],[],'',2, 0, 'hat', id=105, color=15, tag='^')
cloth_robe = Item(0.2, ['armour','Chest','cloth'],[],'',3, 0, 'robe', id=106, color=15, tag='[')
cloth_shoes = Item(0.1, ['armour','Feet','cloth','wood'],[],'',2, 0, 'shoes', id=107, color=15, tag='_')
flower_crown = Item(0.05, ['armour','Head'],[],'',1, 0, 'flower crown', id=108, color=5, tag='*')

cloth_armour = (cloth_pants,cloth_cloak,cloth_belt,cloth_gloves,cloth_shirt,cloth_hat,cloth_shoes,cloth_robe,flower_crown)

## Leather armour(armour 180,wgt 25.5), IDs 8, 200-
leather_vest = Item(7,['armour','Chest','leather'],[],'',50,0,'leather vest',8,False,1,{},8,'[')
leather_pants = Item(6, ['armour','Legs','leather'],[],'',50, 0, 'leather pants', id=200, color=8, tag='(')
leather_belt = Item(2, ['armour','Belt','leather'],[],'',10, 0, 'leather belt', id=201, color=8, tag='-')
leather_gloves = Item(1.5, ['armour','On hands','leather'],[],'',15, 0, 'leather gloves', id=202, color=8, tag=')')
leather_cloak = Item(5, ['armour','Back','leather'],[],'',30, 0, 'leather cloak', id=203, color=8, tag=')')
leather_hat = Item(1, ['armour','Head','leather'],[],'',10, 0, 'leather hat', id=204, color=8, tag='^')
leather_boots = Item(3, ['armour','Feet','leather','wood'],[],'',15, 0, 'leather boots', id=205, color=8, tag='_')

leather_armour = (leather_pants,leather_vest,leather_cloak,leather_belt,leather_gloves,leather_hat,leather_boots)

## Chain armour(armour 360,wgt 48), IDs 300-
chain_vest = Item(15,['armour','Chest','iron','leather'],[],'',100,0,'chain vest',300,False,1,{},7,'[')
chain_pants = Item(12, ['armour','Legs','iron','leather'],[],'',100, 0, 'chain pants', id=301, color=7, tag='(')
chain_belt = Item(3, ['armour','Belt','iron','leather'],[],'',20, 0, 'chain belt', id=302, color=7, tag='-')
chain_gloves = Item(2, ['armour','On hands','iron'],[],'',30, 0, 'chain gloves', id=303, color=7, tag=')')
chain_cloak = Item(10, ['armour','Back','iron','leather'],[],'',60, 0, 'chain cloak', id=304, color=7, tag=')')
chain_hat = Item(2, ['armour','Head','iron'],[],'',20, 0, 'chain coif', id=305, color=7, tag='^')
chain_boots = Item(4, ['armour','Feet','iron','leather','wood'],[],'',30, 0, 'chain boots', id=306, color=7, tag='_')

chain_armour = (chain_pants,chain_vest,chain_cloak,chain_belt,chain_gloves,chain_hat,chain_boots)

## Plate armour(armour 520,wgt 88), IDs 400-
plate_chest= Item(40,['armour','Chest','iron','leather'],[],'',200,0,'chestplate',400,False,1,{},8,'[')
plate_pants = Item(25, ['armour','Legs','iron','leather'],[],'',150, 0, 'greaves', id=401, color=8, tag='(')
plate_belt = Item(6, ['armour','Belt','iron','leather'],[],'',30, 0, 'plate belt', id=402, color=8, tag='-')
plate_gloves = Item(5, ['armour','On hands','iron','leather'],[],'',40, 0, 'plate gloves', id=403, color=8, tag=')')
plate_helm = Item(3, ['armour','Head','iron'],[],'',40, 0, 'plate helm', id=404, color=8, tag='^')
plate_boots = Item(9, ['armour','Feet','iron'],[],'',60, 0, 'plate boots', id=405, color=8, tag='_')

plate_armour = (plate_pants,plate_chest,plate_belt,plate_gloves,plate_helm,plate_boots)

## Wooden armour(armour 270,wgt 35), IDs 600-
wood_vest = Item(10,['armour','Chest','wood'],[],'',80,0,'living wood chestplate',600,False,1,{},10,'[')
wood_pants = Item(9, ['armour','Legs','wood'],[],'',80, 0, 'living wood pants', id=601, color=10, tag='(')
wood_belt = Item(2, ['armour','Belt','wood'],[],'',15, 0, 'living wood belt', id=602, color=10, tag='-')
wood_gloves = Item(2, ['armour','On hands','wood'],[],'',20, 0, 'living wood gloves', id=603, color=10, tag=')')
wood_cloak = Item(8, ['armour','Back','wood'],[],'',40, 0, 'cloak of leaves', id=604, color=10, tag=')')
wood_hat = Item(1, ['armour','Head','wood'],[],'',15, 0, 'living wood helm', id=605, color=10, tag='^')
wood_boots = Item(3, ['armour','Feet','wood'],[],'',20, 0, 'living wood boots', id=606, color=10, tag='_')

wood_armour = (wood_pants,wood_vest,wood_cloak,wood_belt,wood_gloves,wood_hat,wood_boots)

##Herbs&Flowers, IDs 900-
##Po spisuci se razpredelqt i se zapisvat v 'gather' na herb set-ovete za localizaciq po tereni
##Chance dava vuzmojnostta da se nameri bilkata v %, koito se umnojava po Int na geroq
herb = Item(0.01,['herb','material','cookmat'],[],'',0, 0, 'herb',900,True,1,{'chance':5,'cook':'herb'},10,'*')
flower = Item(0.2,['expendable','material','craftmat','flowers'],['flowers'],'',0,0,'flower',901,True,1,{'craft':'flowers','force':{'Nature':{'force':0.01}}},192,'*')
vegetable = Item(0.5, ['food','cookmat'],[],'',0,0,'vegetable',902,True,1,{'hunger':20,'thirst':5,'energy':20,'cook':'vegetable'},2,tag=',')
rare_flower = Item(0.2,['material','expendable','craftmat','rare flower'],[],'',0,0,'rare flower',903,True,1,{'craft':'rare flowers',},192,'*')

vegetables = (vegetable,)
flowers = (flower,)
herbs = (herb,)

##Treasure, IDs 1000-
coins_copper = Item(0.01,['treasure','coin','copper'],[],'',0,0,'copper coins', id=1000, stackable=True, color=6, tag='$')
coins_silver = Item(0.01,['treasure','coin','silver'],[],'',0,0,'silver coins', 1001, stackable=True, color=15, tag='$')
coins_gold = Item(0.01,['treasure','coin','gold'],[],'',0,0,'gold coins', 1002, stackable=True, color=14, tag='$')
coins_ancient_copper = Item(0.01,['treasure','coin','ancient','copper'],[],'',0,0,'ancient copper coins', id=1003, stackable=True, color=6, tag='$')
coins_ancient_silver = Item(0.01,['treasure','coin','ancient','silver'],[],'',0,0,'ancient silver coins', 1004, stackable=True, color=15, tag='$')
coins_ancient_gold = Item(0.01,['treasure','coin','ancient','gold'],[],'',0,0,'ancient gold coins', 1005, stackable=True, color=14, tag='$')
jewel_ring = Item(0.01,['treasure','jewel','ring','Left ring','Right ring'],[],'',0,0,'ring', 1006, stackable=False, color=7, tag='$')
jewel_crown = Item(1,['treasure','jewel','crown','Head'],[],'',0,0,'crown', 1007, stackable=False, color=7, tag='$')
jewel_bracelet = Item(0.3,['treasure','jewel','bracelet','Jewel'],[],'',0,0,'bracelet', 1008, stackable=False, color=7, tag='$')
jewel_necklace = Item(0.3,['treasure','jewel','necklace','Neck'],[],'',0,0,'necklace', 1009, stackable=False, color=7, tag='$')
jewel_earring = Item(0.03,['treasure','jewel','earring','Jewel'],[],'',0,0,'earring', 1010, stackable=False, color=7, tag='$')
jewel_chain = Item(0.5,['treasure','jewel','chain','Neck','Jewel'],[],'',0,0,'chain', 1011, stackable=False, color=7, tag='$')
jewel_pendant = Item(0.5,['treasure','jewel','pendant','Jewel'],[],'',0,0,'pendant', 1012, stackable=False, color=7, tag='$')
jewel_brooch = Item(0.2,['treasure','jewel','brooch','Jewel'],[],'',0,0,'brooch', 1013, stackable=False, color=7, tag='$')
jewel_hairpin = Item(0.05,['treasure','jewel','hairpin','Jewel'],[],'',0,0,'hairpin', 1014, stackable=False, color=7, tag='$')
jewel_tiara = Item(0.8,['treasure','jewel','tiara','Head'],[],'',0,0,'tiara', 1015, stackable=False, color=7, tag='$')
jewel_diadem = Item(0.5,['treasure','jewel','diadem','Head'],[],'',0,0,'diadem', 1016, stackable=False, color=7, tag='$')
tumi = Item(1, ['treasure','jewel','Jewel'],['cutting'],'',0, 0, 'tumi', 1017,False,effect={'temp_attr':[['Dex',+1]]},color=7,tag='/')
the_golden_stool = Item(5, ['treasure','furniture','UNIQUE','gold','wood'],[],'',0, 0, 'The Golden Stool', 1018,False,color=14,tag='-')
gem_diamond = Item(0.02,['treasure','gem','diamond'],[],'',0,0,'diamond', 1019, stackable=True, effect={'gnome_gem':['wWO','diamond_mess'],'talisman':{'temp_attr':[['Cre',2]]}}, color=15, tag='$')
gem_emerald = Item(0.02,['treasure','gem','emerald'],[],'',0,0,'emerald', 1020, stackable=True, effect={'gnome_gem':['g','emerald_mess'],'talisman':{'temp_attr':[['End',1]]}}, color=10, tag='$')
gem_sapphire = Item(0.02,['treasure','gem','sapphire'],[],'',0,0,'sapphire', 1021, stackable=True, effect={'gnome_gem':["F'i",'sapphire_mess'],'talisman':{'temp_attr':[['Cre',1]]}}, color=1, tag='$')
gem_ruby = Item(0.02,['treasure','gem','ruby'],[],'',0,0,'ruby', 1022, stackable=True, effect={'gnome_gem':[".,+><aAbBdDfFgiIJlLmnoOpsStTwW%#`'~:",'ruby_mess'],'talisman':{'temp_attr':[['End',2]]}}, color=4, tag='$')
gem_pearl = Item(0.02,['treasure','gem','pearl'],[],'',0,0,'stone pearl', 1023, stackable=True, effect={'gnome_gem':['wWO','diamond_mess'],'talisman':{'temp_attr':[['Mnd',2]]}}, color=7, tag='$')
gem_amethyst = Item(0.02,['treasure','gem','amethyst'],[],'',0,0,'amethyst', 1024, stackable=True, effect={'gnome_gem':['n','amethyst_mess'],'talisman':{'temp_attr':[['Dex',2]]}}, color=5, tag='$')
gem_topaz = Item(0.02,['treasure','gem','topaz'],[],'',0,0,'topaz', 1025, stackable=True, effect={'gnome_gem':[".,+><aAbBdDfFgiIJlLmnoOpsStTwW%#`'~:",'topaz_mess'],'talisman':{'temp_attr':[['Dex',1]]}}, color=14, tag='$')
gem_tourmaline = Item(0.02,['treasure','gem','tourmaline'],[],'',0,0,'tourmaline', 1026, stackable=True, effect={'gnome_gem':["g.adDFp,~'i:",'tourmaline_mess'],'talisman':{'temp_attr':[['Str',1]]}}, color=2, tag='$')
gem_garnet = Item(0.02,['treasure','gem','garnet'],[],'',0,0,'garnet', 1027, stackable=True, effect={'gnome_gem':[".,+><aAbBdDfFgiIJlLmnoOpsStTwW%#`'~:",'garnet_mess'],'talisman':{'temp_attr':[['Str',2]]}}, color=12, tag='$')
gem_aquamarine = Item(0.02,['treasure','gem','aquamarine'],[],'',0,0,'aquamarine', 1028, stackable=True, effect={'gnome_gem':["g.adDFp,~'i:",'aquamarine_mess'],'talisman':{'temp_attr':[['Mnd',1]]}}, color=3, tag='$')
gem_opal = Item(0.02,['treasure','gem','opal'],[],'',0,0,'opal', 1029, stackable=True, effect={'gnome_gem':['n','opal_mess'],'talisman':{'temp_attr':[['Int',2]]}}, color=154, tag='$')
gem_turquoise = Item(0.02,['treasure','gem','turquoise'],[],'',0,0,'turquoise', 1030, stackable=True, effect={'gnome_gem':['tw','turquoise_mess'],'talisman':{'temp_attr':[['Int',1]]}}, color=11, tag='$')
gem_lapis_lazuli = Item(0.02,['treasure','gem','lapis lazuli'],[],'',0,0,'lapis lazuli', 1031, stackable=True, effect={'gnome_gem':['n','lapis_mess'],'talisman':{'temp_attr':[['Dex',1],['End',1]]}}, color=9, tag='$')
##coins_copper = Item(0.05,['treasure','coin','copper'],[],'',0,0,'copper coins', 1003, stackable=True, color=14, tag='$')
##coins_copper = Item(0.05,['treasure','coin','copper'],[],'',0,0,'copper coins', 1004, stackable=True, color=14, tag='$')
##coins_copper = Item(0.05,['treasure','coin','copper'],[],'',0,0,'copper coins', 1005, stackable=True, color=14, tag='$')

treasure_money = (coins_copper,coins_silver,coins_gold,coins_ancient_copper,coins_ancient_silver,coins_ancient_gold)
gems = (gem_diamond,gem_emerald,gem_sapphire,gem_ruby,gem_pearl,gem_amethyst,gem_topaz,gem_tourmaline,gem_garnet,
        gem_aquamarine,gem_opal,gem_turquoise,gem_lapis_lazuli)
small_treasure = (jewel_hairpin,jewel_brooch,jewel_pendant,jewel_earring,jewel_bracelet,jewel_ring)
medium_treasure = (jewel_diadem,jewel_tiara,jewel_chain,jewel_necklace,tumi)
large_treasure = (jewel_crown,)
unique_treasure = (the_golden_stool,)

##Misc equipment, IDs 1200-
herb_set = Item(1,['herb_set','wood'],['herb_set'],'',0,0,'herb collecting set',1200,False,1,{'gather':{'g':herbs}},7,'"')
magic_book = Item(2,['magic_book','paper'],['magic_book'],'',0,0,'book of magical theory',1201,False,1,{},12,'"')
lockpicks = Item(1,['lockpick','iron'],['lockpick'],'',0,0,'lockpick set',1202,False,1,{},7,'"')
nature_heal_set = Item(1,['heal_set','wood'],['nature healing set'],'',0,0,"nature healer's set",1203,False,1,{},7,'"')

not_included= (magic_book,)
misc_equipment = (herb_set,lockpicks,nature_heal_set)

##Goods (trading and materials), IDs 2,3,4,5,6,7,9,14,16,1300-
## Razlichni semena davat razlichni efekti - ako sa cvetq,hrasti,durveta,treva - Nature, ako sa kulturni sortove - Red,
## ako sa trunlivi hrasti ili nqkakvi mutanti - Chaos
bread = Item(1, ['food','cookmat'],[],'',0,-2,'bread',2,True,1,{'hunger':30,'thirst':0,'energy':20,'cook':'bread'},2,tag=',')
bottle_water = Item(1, ['drink','cookmat'],['water'],'',0,0,'full waterskin',3,True,1,{'cook':'water','hunger':0,'thirst':30,'energy':20,'container':7},2,tag=',')
rock = Item(3, ['craftmat','buildmat','material','rock','Right hand','Left hand'],['crude hammer','rock'],'',0,1,'rock',4,True,1,{'build':'rock','break_rock':gems,'craft':'rock'},tag='*')
dust = Item(3, ['material'],[],'',0,0,'dust',6,True,1,{},color=5,tag='*')
bottle = Item(0.5,['material','m-short','bottle'],['bottle'],'',0,0,'empty waterskin',7,True,1,{'fill':{'w':3,'O':3}},7,',')
flower_seed = Item(0,['seed'],['seed'],'',0,0,'flower seed',9,True,1,
                   {'plant_seed':flowers,'force':{'Nature':{'force':0.01,'elf':0.01,'terrain':.05},'Chaos':{'all':-.01}}},10,'.')
tree_log = Item(2, ['craftmat','expendable','buildmat','material', 'two_handed','m-long','wood'],['wood'],'',0, 2,'piece of wood',14,True,1,{'build':'wood','craft':'wood'},color=6,tag='|')
string = Item(0,['material','m-connect','Right hand','Left hand'],[],'',0,0,'string',16,True,1,{},7,'~')
common_spices = Item(1,['goods','spice','cookmat'],['common spices'],'',0,0,'common spices',1300,True,1,{'cook':'spice'},14,'"')
fruit = Item(1, ['food','cookmat'],[],'',0,-2,'fruit',1301,True,1,{'hunger':20,'thirst':5,'energy':20,'cook':'fruit'},12,tag=',')
berries = Item(1, ['food','cookmat'],[],'',0,-2,'berries',1302,True,1,{'hunger':20,'thirst':5,'energy':20,'cook':'fruit'},5,tag=',')
earth = Item(3, ['expendable','material'],['earth'],'',0,0,'earth',1303,True,1,{'force':{'Nature':{'force':0.01}}},color=6,tag='*')
color_clay = Item(3, ['expendable','buildmat','material','clay'],['color clay','clay'],'',0,0,'colorful clay',1304,True,1,{'build':'clay','force':{'Nature':{'force':0.01}}},color=13,tag='*')
wild_flowers = Item(0.01, ['expendable','craftmat','material','flowers'],['flowers'],'',0,0,'wild flowers',1305,True,1,{'craft':'flowers','force':{'Nature':{'force':0.01}}},color=5,tag='*')
clay = Item(3, ['expendable','buildmat','material','clay'],['clay'],'',0,0,'clay',1306,True,1,{'build':'clay','force':{'Order':{'force':0.01}}},color=6,tag='*')
seed_life = Item(0,['seed','treasure'],['seed of life'],'',0,0,'Seed of Life',1307,True,1,
                   {'plant_seed':flowers,'force':{'Nature':{'force':0.5,'elf':0.5,'terrain':1},'Chaos':{'all':-.5}}},12,'*')
earth_ore = Item(5, ['material','ore','m-short','ammunition','tool','weapon','Right hand','Left hand'],['crude hammer'],'',0,1,'earth ore',1308,True,1,{},color=6,tag='*')
chaos_rock = Item(5, ['material'],[],'',0,1,'chaos rock',1309,True,1,
                  {'mass destruction':10,'force':{'Chaos':{'force':12,'ork':2,'goblin':2,'kraken':2,'imp':2,'spirit of chaos':2,'troll':2},'Nature':{'all':-10},'Order':{'all':-10}}},color=128,tag='*')
raw_meat = Item(1, ['raw meat','cookmat'],[],'',0,-2,'raw meat',1310,True,1,{'force':{'Chaos':{'force':0.03,'ork':0.03},'Nature':{'all':-0.5},'Order':{'all':-0.5}},'hunger':30,'thirst':0,'energy':20,'cook':'raw meat'},4,tag=',')
sweet_bread = Item(1, ['food','cookmat'],[],'',0,-2,'sweet bread',1311,True,1,{'hunger':50,'thirst':0,'energy':120,'cook':'sweet bread'},12,tag=',')
fruit_juice = Item(1, ['drink','cookmat'],[],'',0,0,'bottle of juice',1312,True,1,{'cook':'juice','hunger':0,'thirst':50,'energy':70,'container':7},12,tag=',')
roasted_meat = Item(1, ['food'],[],'',0,0,'roasted meat',1313,True,1,{'hunger':50,'thirst':0,'energy':100},6,tag=',')
skin = Item(2, ['craftmat','material','skin','leather'],[],'',0,0,'skin',1314,True,1,{'craft':'leather'},6,tag='~')
vegetable_seed = Item(0,['seed'],['seed'],'',0,0,'vegetable seed',1315,True,1,
                   {'plant_vegetable':vegetables,'force':{'Order':{'force':0.01,'human':0.01,'terrain':.05},
                                                            'Chaos':{'all':-.01}}},10,'.')
vegetable_soup = Item(1, ['drink'],[],'',0,0,'bottle of soup',1316,True,1,{'hunger':20,'thirst':60,'energy':100,'container':7},10,tag=',')
iron_ingot = Item(5, ['craftmat','buildmat','material','iron'],['iron'],'',0,1,'iron ingot',1317,True,1,{'craft':'iron','build':'iron'},color=7,tag='-')
wood_arrow = Item(0.1,['Ammunition','wood'],[],'',0,1,'wooden arrow',1318,True,1,{'shoot':'arrow'},6,'|')
wood_bolt = Item(0.1,['Ammunition','wood'],[],'',0,1,'wooden bolt',1319,True,1,{'shoot':'bolt'},8,'|')
stone = Item(0.1,['Ammunition','rock'],[],'',0,1,'stone',1320,True,1,{'shoot':'stone'},8,'*')
raw_egg = Item(.1, ['raw egg','cookmat'],[],'',0,-2,'raw egg',1321,True,1,{'cook':'raw egg'},15,tag=',')
milk = Item(1, ['drink','cookmat'],[],'',0,0,'milk',1322,True,1,{'cook':'milk','thirst':30,'energy':20,'container':7},15,tag=',')
feather = Item(.05, ['craftmat','feather'],[],'',0,-2,'feather',1323,True,1,{'craft':'feather'},7,tag='~')
boiled_egg = Item(.1, ['boiled egg','cookmat','food'],[],'',0,-2,'boiled egg',1324,True,1,{'hunger':15,'energy':20,'cook':'boiled egg'},15,tag=',')
metal_ingot = Item(3, ['craftmat','material'],[],'',0,1,'ingot',1325,True,1,{},color=7,tag='-')
ore = Item(5, ['material','ore','m-short','Right hand','Left hand'],['crude hammer'],'',0,1,'ore',5,True,1,{'smelt_ore':[iron_ingot,metal_ingot]},color=8,tag='*')
bone = Item(.2, ['craftmat','bone'],[],'',0,0,'bone',1326,True,1,{'craft':'bone'},15,tag='~')

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
