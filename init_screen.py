import Console
from terrain import T
import player
import msvcrt
import pickle
import message
import inventory
import random
import load
from os import curdir
from os import mkdir

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
for i in inventory.all_items:
    I[i.id] = (i)


##def reinitialize():
##    player.ch = player.Player([0, 0],attr = {'Str':10, 'End':5,'Dex':10})
##    player.ch.inventory = []
##    for tag in player.ch.equip_tags:
##        player.ch.equipment[tag] = []
##    player.all_beings = [player.ch]
##    player.all_creatures = []
##    player.hidden = []
    
def draw_items(the_spot=[]):
    for x in ground_items:
        if the_spot and x[:2]!=the_spot:
            continue
        i = 0
        for thing in player.all_beings:
            if (thing.xy[0] == x[0]) and (thing.xy[1] == x[1]) and thing not in player.hidden and thing.life>0:
                i += 1
                break
        if i == 0:
            c.scroll((x[0], x[1], x[0]+1, x[1]+1), 1, 1, x[2].color, x[2].tag)

def draw_mode():
    c.rectangle((15,16,20,19))
    mode_mod=['Nature','Order','Chaos'].index(player.ch.mode)
    c.text(15,mode_mod+16,'***',[10,9,12][mode_mod])

def draw_hud():
    c.rectangle((0,1,20,25))
    c.text(0,1,'%s' %(player.ch.name),7)
    for tag in player.ch.equip_tags:
        if player.ch.equipment[tag] != []:
            c.text(1+player.ch.equip_tags.index(tag),2,player.ch.equipment[tag].tag,player.ch.equipment[tag].color)
        else:
            c.text(1+player.ch.equip_tags.index(tag),2,' ',7)
    i = 10
    if (player.ch.life < (player.ch.max_life*0.7)) and (player.ch.life > (player.ch.max_life*0.2)):
        i = 14
    elif (player.ch.life <= (player.ch.max_life*0.2)):
        i = 12
    c.text(0,3,'Life %d/%d' %(player.ch.life,player.ch.max_life),i)
    try:
        if player.ch.sun_armour:
            c.text(0,4,'Armour ' + str(player.ch.armour),9+224)
        else:
            c.text(0,4,'Armour ' + str(player.ch.armour),9)
    except AttributeError:
        c.text(0,4,'Armour ' + str(player.ch.armour),9)
    c.text(0,5,'Str  ' + str(player.ch.attr['Str']),player.ch.attr_colors['Str'])
    c.text(0,6,'Dex  ' + str(player.ch.attr['Dex']),player.ch.attr_colors['Dex'])
    c.text(0,7,'End  ' + str(player.ch.attr['End']),player.ch.attr_colors['End'])
    c.text(0,8,'Int  ' + str(player.ch.attr['Int']),player.ch.attr_colors['Int'])
    c.text(0,9,'Cre  ' + str(player.ch.attr['Cre']),player.ch.attr_colors['Cre'])
    c.text(0,10,'Mnd  ' + str(player.ch.attr['Mnd']),player.ch.attr_colors['Mnd'])
    if player.ch.equipment['Ammunition']:
        c.text(11,4,'Ammo:',4)
        ammo_col=10
        ammo=1
        for am in player.ch.inventory:
            if am.id==player.ch.equipment['Ammunition'].id and am.name==player.ch.equipment['Ammunition'].name:
                ammo+=am.qty
                break
        if ammo<5:
            ammo_col=12
        elif ammo<11:
            ammo_col=14
        c.text(17,4,str(ammo),ammo_col)
    if player.ch.ride:
        c.text(11,6,'Mount:',7)
        if player.ch.ride[0].food<25:
            c.text(11,7,'Hungry!',12)
        elif player.ch.ride[0].food<75:
            c.text(11,7,'Normal',7)
        else:
            c.text(11,7,'Fresh',10)
    c.text(0,11,'Wg %.2f/%d' %(player.ch.weight, player.ch.max_weight),7)
    if player.ch.equipment['Backpack']:
        c.text(0,12,'Bag %.2f/%.2f' %(player.ch.equipment['Backpack'].weight*6-player.ch.backpack,player.ch.equipment['Backpack'].weight*6),7)
    else:
        c.text(0,12,'Bag --/--',7)
    if 'dwarf1' in player.ch.tool_tags:
        c.text(0,13,'Treasure feeling ' + str(current_place['Treasure']),13)
    daytime=player.ch.turn%2400
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
    c.text(0,16,'Nature %6.2f' %(player.ch.forces['Nature'])+'%',10)
    c.text(0,17,'Order  %6.2f' %(player.ch.forces['Order'])+'%',9)
    c.text(0,18,'Chaos  %6.2f' %(player.ch.forces['Chaos'])+'%',12)
##    try:
##        c.text(0,23,'%d' %(player.ch.hunger),7)
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

    if 'invisible' in player.ch.effects:
        c.text(0,19,'Invisible',7)
    if 'stealthy' in player.ch.tool_tags:
        c.text(10,19,'Stealth',7)
    if player.ch.emotion == 2:
        c.text(0,20,'Tired',7)
    if player.ch.sit == True:
        c.text(0,23,'Sitting',7)
    colour = 7
    if player.ch.hunger > 60:
        sign = 'Hungry'
        if 80 < player.ch.hunger < 100:
            colour = 12
            sign = 'HUNGRY'
        if player.ch.hunger == 100:
            if player.ch.turn%2 == 1:
                colour = 14
            else:
                colour = 12
            sign = 'STARVING!'
        c.text(0,21,sign,colour)
    colour = 7
    if player.ch.thirst > 60:
        sign = 'Thirsty'
        if 80 < player.ch.thirst < 100:
            colour = 12
            sign = 'THIRSTY'
        if player.ch.thirst == 100:
            if player.ch.turn%2 == 0:
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
    for x in player.ch.land_effects.keys():
        if player.ch.land_effects[x][1]=='on_fire':
            fxy=player.ch.land_effects[x][3]
            if player.ch.land_effects[x][0]==0:
                c.scroll((fxy[0],fxy[1],fxy[0]+1,fxy[1]+1), 1, 1, T[land[fxy[1]-1][fxy[0]-21]].colour, T[land[fxy[1]-1][fxy[0]-21]].char)
                continue
            fire_color=random.choice([4,12,14])
            c.scroll((fxy[0],fxy[1],fxy[0]+1,fxy[1]+1), 1, 1, fire_color*16+player.ch.land_effects[x][5],player.ch.land_effects[x][4])
    draw_hud()
    draw_items()
    for creature in player.all_creatures:
        if creature not in player.hidden and (clear_los(direct_path(player.ch.xy,creature.xy)) or (current_place['Nature']>=33 and current_place['Temperature']>=33 and 'elf2' in player.ch.tool_tags)):
            draw_move(creature, creature.xy[0], creature.xy[1])
    
    if current_area == 'world':
        for place in world_places:
            if place != 'world' and place in player.ch.known_areas and str(world_places[place]) in top_world_places:
                x = world_places[place][0]
                y = world_places[place][1]
                c.scroll((x, y, x+1, y+1), 1, 1, 11, '?')
    draw_move(player.ch, player.ch.xy[0], player.ch.xy[1])
    c.pos(*player.ch.xy)

def draw_move(ch, x, y):
##    try:
    c.scroll((x, y, x+1, y+1), 1, 1, T[land[y-1][x-21]].colour, T[land[y-1][x-21]].char)
##    except:
##        print x, y, land[y-1][x-21]
    if current_area == 'world':
        if str([x, y]) in top_world_places and [x,y] in [world_places[a] for a in player.ch.known_areas]:
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
    if player.ch.hunger>79 or player.ch.thirst>79:
        return -4
    while 1:
        if (player.ch.energy < inventory.build_recipes[new_ter][4]) and (player.ch.work == 0):
            if player.ch.max_energy < inventory.build_recipes[new_ter][4]:
                return -2
            else:
                return -1
        elif ok!=1:
            player.ch.work = inventory.build_recipes[new_ter][4]
            ok=1
        hostiles=player.game_time('0')
        if hostiles==2:
            player.ch.work=0
            return -3
        if player.ch.work == 0:
            player.effect('force',inventory.build_recipes[new_ter][5])
            if 'str' in str(type(inventory.build_recipes[new_ter][2])):
                land[player.ch.xy[1]-1] = land[player.ch.xy[1]-1][:player.ch.xy[0]-21] + inventory.build_recipes[new_ter][2] + land[player.ch.xy[1]-1][player.ch.xy[0]-20:]
            elif 'int' in str(type(inventory.build_recipes[new_ter][2])):
                creation=I[inventory.build_recipes[new_ter][2]].duplicate()
                ground_items.append([player.ch.xy[0],player.ch.xy[1],creation])
            return 1
        elif player.ch.hunger>79 or player.ch.thirst>79:
            player.ch.work = 0
            return -4

def build(ground_items):
    mats={}
    for i in ground_items:
        if i[:2]==player.ch.xy:
            if 'buildmat' in i[2].type:
                if i[2].effect['build'] in mats:
                    mats[i[2].effect['build']]+=i[2].qty
                else:
                    mats[i[2].effect['build']]=i[2].qty
            else:
                message.message('clear_build_site')
                return ground_items
    mat_keys=mats.keys()
    selected_recipes={}
    the_build=''
    for r in inventory.BR[player.ch.attr['Cre']]:
        all_in=1
        needed_mats=inventory.build_recipes[r][3]
        needed_tools=[]
        for t in inventory.build_recipes[r][1]:
            if t not in player.ch.tool_tags[:]:
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
                if m[:2]!=player.ch.xy or (inventory.build_recipes[the_build][2] in I and\
                   m[2].id==I[inventory.build_recipes[the_build][2]].id):
                    new_ground_items.append(m)
            return new_ground_items
        elif building == -2:
            message.emotion('not_tough')
        elif building == -1:
            message.emotion('tired')
        elif building == -4:
            message.emotion('exhausted')
        elif building == -3:
            message.emotion('hostiles')
        return ground_items
    else:
        redraw_screen()
        return ground_items

def craft_item(item_type,new_item):
    the_name=new_item
    if new_item.split()[0] in ['copper','silver','gold']:
        new_item=' '.join(new_item.split()[1:])
    ok = 0
    if player.ch.hunger>79 or player.ch.thirst>79:
        return -4,0
    while 1:
        if (player.ch.energy < inventory.craft_recipes[item_type][new_item][4]) and (player.ch.work == 0):
            if player.ch.max_energy < inventory.craft_recipes[item_type][new_item][4]:
                return -2,0
            else:
                return -1,0
        elif ok!=1:
            player.ch.work = inventory.craft_recipes[item_type][new_item][4]
            ok=1
        hostiles=player.game_time('0')
        if hostiles==2:
            player.ch.work=0
            return -3,0
        if player.ch.work == 0:
            player.effect('force',inventory.craft_recipes[item_type][new_item][5])
            creation=I[inventory.craft_recipes[item_type][new_item][2]].duplicate(name=the_name)
            if 'dwarf2' in player.ch.tool_tags:
                creation=add_gems(creation)
            elif 'fairy1' in player.ch.tool_tags and creation.name=='flower crown':
                creation=add_flowers(creation)
            ground_items.append([player.ch.xy[0],player.ch.xy[1],creation])
            return 1,creation.name
        elif player.ch.hunger>79 or player.ch.thirst>79:
            player.ch.work = 0
            return -4,0

def add_gems(creation):
    gems=[]
    for x in player.ch.inventory:
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
    for fls in player.ch.inventory:
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
        if 'fairy2' in player.ch.tool_tags:
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
        if 'fairy3' in player.ch.tool_tags:
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
                for i1 in player.ch.inventory:
                    if i1.name=='wild flowers' and i1.qty>=50:
                        found=1
                        i1.lose_item(50)
                        creation.color=12
                        for each in flowers:
                            flowers[each].lose_item(1)
                if not found:
                    message.message('flower_dress')
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
    if 'dwarf3' in player.ch.tool_tags:
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
        if i[:2]==player.ch.xy:
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
    for recipe_group in inventory.CrR:
        for r in inventory.CrR[recipe_group][player.ch.attr['Cre']]:
            if recipe_group not in selected_recipes:
                selected_recipes[recipe_group]={}
                tools_needed[recipe_group]=[]
            all_in=1
            needed_mats=inventory.craft_recipes[recipe_group][r][3].copy()
            if metal_chosen!='iron' and 'iron' in needed_mats:
                needed_mats[metal_chosen]=needed_mats['iron']
                del(needed_mats['iron'])
            needed_tools=[]
            for t in inventory.craft_recipes[recipe_group][r][1]:
                if t not in tools_needed[recipe_group]:
                    tools_needed[recipe_group].append(t)
                if t not in player.ch.tool_tags[:] and t not in ground_tools:
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
                used_mats=inventory.craft_recipes[craft_group][' '.join(the_keys[int(i)-1].split()[1:])][3].copy()
            else:
                used_mats=inventory.craft_recipes[craft_group][the_keys[int(i)-1]][3].copy()
            if metal_chosen!='iron' and 'iron' in used_mats:
                used_mats[metal_chosen]=used_mats['iron']
                del(used_mats['iron'])
            new_ground_items=[]
            for m in ground_items:
                if m[:2]==player.ch.xy and 'craftmat' in m[2].type and m[2].effect['craft'] in used_mats and used_mats[m[2].effect['craft']]>0:
                    if m[2].qty>used_mats[m[2].effect['craft']]:
                        m[2].qty-=used_mats[m[2].effect['craft']]
                        new_ground_items.append(m)
                    else:
                        used_mats[m[2].effect['craft']]=used_mats[m[2].effect['craft']]-m[2].qty
                else:
                    new_ground_items.append(m)
            return new_ground_items
        elif building == -2:
            message.emotion('not_tough')
        elif building == -1:
            message.emotion('tired')
        elif building == -4:
            message.emotion('exhausted')
        elif building == -3:
            message.emotion('hostiles')
        return ground_items
    else:
        redraw_screen()
        return ground_items

def dryad_grow():
    if T[land[player.ch.xy[1]-1][player.ch.xy[0]-21]].id == 'T':
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
            ground_items.append([player.ch.xy[0],player.ch.xy[1],grown_item])
            player.effect('force',{'Nature':{'dryad':-1.}})
    else:
        message.message('dryad_song')
        msvcrt.getch()
        if player.ch.energy>100:
            player.effect('dryad song',1)
            player.ch.energy=0
    redraw_screen()

def degrade_terr(old_ter, xy, c_x, c_y):
    ok = 0
    if ((player.ch.hunger > 79) or (player.ch.thirst > 79)) and T[old_ter].degr_mess[player.ch.mode]!='forage':
        return -4
    while 1:
        if (player.ch.energy < T[old_ter].tire[player.ch.mode]) and (player.ch.work == 0):
            if player.ch.max_energy < T[old_ter].tire[player.ch.mode]:
                return -2
            else:
                return -1
        elif ok != 1:
            player.ch.work = T[old_ter].tire[player.ch.mode]
        for i in T[old_ter].degrade_tool[player.ch.mode]:
            if i in player.ch.tool_tags:
                ok = 1
                if 'dryad2' in player.ch.tool_tags and T[old_ter].id==':' and player.ch.mode=='Nature':
                    message.message('dryad_heal_tree')
                else:
                    message.message(T[old_ter].degr_mess[player.ch.mode])
                hostiles=player.game_time('0')
                if hostiles==2:
                    player.ch.work=0
                    return -3
                if player.ch.work == 0:
                    if T[land[xy[1]-1][xy[0]-21]].degradable:
                        if 'dryad2' in player.ch.tool_tags and T[old_ter].id==':' and player.ch.mode=='Nature':
                            land[xy[1]-1] = land[xy[1]-1][:xy[0]-21] + 'T' + land[xy[1]-1][xy[0]-20:]
                        else:
                            land[xy[1]-1] = land[xy[1]-1][:xy[0]-21] + T[old_ter].degrade_to[player.ch.mode] + land[xy[1]-1][xy[0]-20:]
                    found_loot=0
                    if xy not in player.ch.worked_places[player.ch.mode] or T[old_ter].id=='m':
                        player.effect('force',T[old_ter].force_effects[player.ch.mode],xy,T[old_ter].char)
                        if 'dryad2' in player.ch.tool_tags and T[old_ter].id==':' and player.ch.mode=='Nature':
                            player.effect('force',T[old_ter].force_effects[player.ch.mode],xy,T[old_ter].char)
                        player.ch.worked_places[player.ch.mode].append(xy[:])
                        if 'gnome2' in player.ch.tool_tags and T[old_ter].id in ['%','n','m'] and player.ch.mode=='Nature':
                            found_loot+=inventory.put_item([['gnome_touch',5,1,1]], xy)
                            if found_loot:
                                message.message('gnome_touch')
                        elif 'fairy1' in player.ch.tool_tags and T[old_ter].id in ['g','O'] and player.ch.mode=='Nature':
                            found_loot+=inventory.put_item([['fairy_flowers',5,1,1]], xy)
                            if found_loot:
                                message.message('fairy_flowers')
                        if T[land[xy[1]-1][xy[0]-21]].pass_through:
                            found_loot+=inventory.put_item(T[old_ter].loot[player.ch.mode], xy)
                        else:
                            found_loot+=inventory.put_item(T[old_ter].loot[player.ch.mode], [c_x,c_y])
                    if not found_loot:
                        c.scroll((xy[0],xy[1],xy[0]+1,xy[1]+1), 1, 1, T[land[xy[1]-1][xy[0]-21]].colour, T[land[xy[1]-1][xy[0]-21]].char)
                    draw_items(xy)
                    return 1
                elif ((player.ch.hunger > 79) or (player.ch.thirst > 79)) and T[old_ter].degr_mess[player.ch.mode]!='forage':
                    player.ch.work = 0
                    return -4
        if ok == 0:
            player.ch.work = 0
            return 0

def work(i):
    message.message('')
    try:
        md = {'1':[-1,1], '2':[0,1], '3':[1,1], '4':[-1,0], '5':[0,0],
              '6':[1,0], '7':[-1,-1], '8':[0,-1], '9':[1,-1], '0':[0,0]}
        xy = player.ch.xy[:]
        x = xy[0]
        y = xy[1]
        for a in range(2):
                xy[a] = xy[a] + md[i][a]
        if T[land[xy[1]-1][xy[0]-21]].workable:
            d = degrade_terr(land[xy[1]-1][xy[0]-21], xy, x, y)
            if d == 1:
                xy[0] = x
                xy[1] = y
                draw_move(player.ch, x, y)
            elif d == -2:
                message.emotion('not_tough')
                xy[0] = x
                xy[1] = y
            elif d == -1:
                message.emotion('tired')
                xy[0] = x
                xy[1] = y
            elif d == -4:
                message.emotion('exhausted')
                xy[0] = x
                xy[1] = y
            elif d == -3:
                message.emotion('hostiles')
                xy[0] = x
                xy[1] = y
            else:
                message.tool_msg('no_tool',T[land[xy[1]-1][xy[0]-21]].degrade_tool[player.ch.mode])
                xy[0] = x
                xy[1] = y
        else:
            message.message('cant_work')
            xy[0] = x
            xy[1] = y
    except KeyError:
        message.message('direction')

def draw_inv(put_in=None, container=None):
    c.page()
    c.pos(0,0)
    if put_in:
        c.write('\n What do you want to put in the container?\n\n\n')
    else:
        c.write('\n You open your backpack:\n (e)view equipment (q)eat/drink (d)drop item (u)use item\n\n')
    for i in range(len(player.ch.inventory)):
        print ' '+chr(i+97)+')  ', player.ch.inventory[i].name.capitalize()+', %d x %s stones' %(player.ch.inventory[i].qty,
                                                                                  str(player.ch.inventory[i].weight))
        c.text(4,i+4,player.ch.inventory[i].tag,player.ch.inventory[i].color)
    print '\n Carrying: %s/%s. You can fit %s more in your bag.' %(str(player.ch.weight), str(player.ch.max_weight),
                                                                   str(player.ch.backpack))
    i1 = ' '
    i1 = msvcrt.getch()
    try:
        if put_in and player.ch.inventory[ord(i1)-97] != container:
            space = I[container.id].weight*7 - container.weight
            drop = player.ch.inventory[ord(i1)-97].drop_item('',space)
            if not drop:
                message.message('cant_fit_in_container')
                msvcrt.getch()
            return drop
        elif put_in and player.ch.inventory[ord(i1)-97] == container:
            message.message('cant_fit_container')
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
            player.ch.inventory[ord(eat)-97].eat()
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
            drop = player.ch.inventory[ord(dr)-97].drop_item('',10000)
            dropped = 0
            for item in ground_items:
                if item[:2] == player.ch.xy and item[2].id == drop.id and item[2].stackable and item[2].name == drop.name:
                    item[2].qty += drop.qty
                    dropped = 1
            if not dropped:
                ground_items.append([player.ch.xy[0], player.ch.xy[1],drop])
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
            ty = player.ch.inventory[ord(use)-97].type
            if 'container' in player.ch.inventory[ord(use)-97].type:
                open_container(player.ch.inventory[ord(use)-97])
            elif player.ch.inventory[ord(use)-97].effect != {} and ('armour' not in ty and 'weapon' not in ty and 'tool' not in ty):
                player.ch.inventory[ord(use)-97].use_item()
            if player.ch.spell_cast or player.ch.turn in player.ch.land_effects:
                return 0
        except IndexError:
            pass
        draw_inv()
        
def draw_equip():
    c.page()
    c.pos(0,0)
    c.write('\n You check your equipment:\n (a-p)take off/equip item (1)view inventory\n\n')
    for i in range(len(player.ch.equipment)):
        if player.ch.equipment[player.ch.equip_tags[i]] != []:
            item_effs = ''
            try:
                item_effs = []
                done = [item_effs.extend(x) for x in player.ch.equipment[player.ch.equip_tags[i]].effect['temp_attr']]
                if item_effs:
                    item_effs = '['+' '.join([str(x) for x in item_effs])+']'
                else:
                    item_effs = ''
            except KeyError:
                item_effs = ''
            engrav = ''
            if 'engraving' in player.ch.equipment[player.ch.equip_tags[i]].effect:
                engrav = '"'+player.ch.equipment[player.ch.equip_tags[i]].effect['engraving']+'"'
            if 'two_handed' in player.ch.equipment[player.ch.equip_tags[i]].type:
                print ' '+chr(i+97)+')  ', player.ch.equip_tags[i]+': %s (two hands), %d x %s stones %s %s' %(player.ch.equipment[player.ch.equip_tags[i]].name.capitalize(),
                                                                                          player.ch.equipment[player.ch.equip_tags[i]].qty,
                                                                                          str(player.ch.equipment[player.ch.equip_tags[i]].weight), item_effs,
                                                                                                            engrav)
            else:
                print ' '+chr(i+97)+')  ', player.ch.equip_tags[i]+': %s, %d x %s stones %s %s' %(player.ch.equipment[player.ch.equip_tags[i]].name.capitalize(),
                                                                                          player.ch.equipment[player.ch.equip_tags[i]].qty,
                                                                                          str(player.ch.equipment[player.ch.equip_tags[i]].weight),item_effs,
                                                                                             engrav)
            c.text(4,i+4,player.ch.equipment[player.ch.equip_tags[i]].tag,player.ch.equipment[player.ch.equip_tags[i]].color)
        else:
            print ' '+chr(i+97)+')  ', player.ch.equip_tags[i]+':'
    i1 = ' '
    i1 = msvcrt.getch()
    if i1 == '1':
        draw_inv()
        return 1
    if ord(i1)-97 in range(19):
        if player.ch.equipment[player.ch.equip_tags[ord(i1)-97]] == []:
            two = 0
            if player.ch.equip_tags[ord(i1)-97] == 'Right hand' and player.ch.equipment['Left hand'] != []:
                if 'two_handed' in player.ch.equipment['Left hand'].type:
                    two = 1
                    player.ch.take_off(player.ch.equip_tags.index('Left hand'))
            elif player.ch.equip_tags[ord(i1)-97] == 'Left hand' and player.ch.equipment['Right hand'] != []:
                if 'two_handed' in player.ch.equipment['Right hand'].type:
                    two = 1
                    player.ch.take_off(player.ch.equip_tags.index('Right hand'))
            if not two:
                player.ch.find_equipment(ord(i1)-97)
        else:
            if player.ch.equip_tags[ord(i1)-97] == 'Backpack':
                print ' Do you really want to drop your bag to the ground?\n You will be able to carry only one item per free hand at most! (y/n)'
                b1 = msvcrt.getch()
                if b1.lower() != 'y':
                    draw_equip()
                    return
            player.ch.take_off(ord(i1)-97)
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
    c.text(2,1,'%s' %(player.ch.name),7)
    i = 10
    if (player.ch.life < (player.ch.max_life*0.7)) and (player.ch.life > (player.ch.max_life*0.2)):
        i = 14
    elif (player.ch.life <= (player.ch.max_life*0.2)):
        i = 12
    c.text(2,3,'Life %d/%d' %(player.ch.life,player.ch.max_life),i)
    for x in atts:
        c.text(2,atts.index(x)+5,'%s  %d' %(x,player.ch.attr[x]),player.ch.attr_colors[x])
    c.text(13,3,'Armour %d' %(player.ch.armour),9)
    c.text(13,5,'Wg %.2f/%d' %(player.ch.weight, player.ch.max_weight),7)
    c.text(13,6,'Free bag %.2f' %(player.ch.backpack),7)
    c.text(13,7,'Free hands %d' %(player.ch.free_hands),9)
    c.text(13,8,'Turn %d' %(player.ch.turn),7)
    c.text(29,3,'Weapon skills',12)
    current_weapons=[]
    right_hand_weapon=''
    if player.ch.equipment['Right hand'] and 'weapon' in player.ch.equipment['Right hand'].type:
        current_weapons.append(player.ch.equipment['Right hand'].weapon_type.capitalize())
        right_hand_weapon=player.ch.equipment['Right hand'].weapon_type.capitalize()
    if player.ch.equipment['Left hand'] and 'weapon' in player.ch.equipment['Left hand'].type:
        current_weapons.append(player.ch.equipment['Left hand'].weapon_type.capitalize())
    if not current_weapons:
        current_weapons=['Unarmed']
    for s in player.ch.weapon_skills:
        if s in current_weapons:
            if s==right_hand_weapon or len(current_weapons)==1:
                c.text(29,player.ch.weapon_skills.keys().index(s)+5,'%-12s:%6.2f' %(s,player.ch.weapon_skill),10)
            else:
                c.text(29,player.ch.weapon_skills.keys().index(s)+5,'%-12s:%6.2f' %(s,player.ch.weapon_skills[s]),10)
        else:
            c.text(29,player.ch.weapon_skills.keys().index(s)+5,'%-12s:%6.2f' %(s,player.ch.weapon_skills[s]),7)
    c.text(49,1,'NATURE %17.2f' %player.ch.forces['Nature']+'%',10)
    the_line=3
    for race in races['Nature']:
        if race==player.ch.locked_race:
            col=2
        else:
            col=7
        c.text(50,the_line,'%s) %-16s:%6.2f' %(chr(all_races.index(race)+97),race.capitalize(),player.ch.races['Nature'][race])+'%',col)
        the_line+=1
    c.text(49,the_line+1,'ORDER  %17.2f' %player.ch.forces['Order']+'%',9)
    the_line+=3
    for race in races['Order']:
        if race==player.ch.locked_race:
            col=2
        else:
            col=7
        c.text(50,the_line,'%s) %-16s:%6.2f' %(chr(all_races.index(race)+97),race.capitalize(),player.ch.races['Order'][race])+'%',col)
        the_line+=1
    c.text(49,the_line+1,'CHAOS  %17.2f' %player.ch.forces['Chaos']+'%',12)
    the_line+=3
    for race in races['Chaos']:
        if race==player.ch.locked_race:
            col=2
        else:
            col=7
        c.text(50,the_line,'%s) %-16s:%6.2f' %(chr(all_races.index(race)+97),race.capitalize(),player.ch.races['Chaos'][race])+'%',col)
        the_line+=1
    c.pos(2,15)
    if player.ch.emotion == 2:
        c.text(2,20,'Tired',7)
    if player.ch.sit == True:
        c.text(2,23,'Sitting',7)
    colour = 7
    if player.ch.hunger > 60:
        sign = 'Hungry'
        if 80 < player.ch.hunger < 100:
            colour = 12
            sign = 'HUNGRY'
        if player.ch.hunger == 100:
            if player.ch.turn%2 == 1:
                colour = 14
            else:
                colour = 12
            sign = 'STARVING!'
        c.text(2,21,sign,colour)
    colour = 7
    if player.ch.thirst > 60:
        sign = 'Thirsty'
        if 80 < player.ch.thirst < 100:
            colour = 12
            sign = 'THIRSTY'
        if player.ch.thirst == 100:
            if player.ch.turn%2 == 0:
                colour = 14
            else:
                colour = 12
            sign = 'DYING OF THIRST!'
        c.text(2,22,sign,colour)
    waiting=msvcrt.getch()
    if ord(waiting) in range(97,len(all_races)+97):
        player.ch.locked_race=all_races[ord(waiting)-97]
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

    c.text(1,22,'Researching: %s -> %s' %(player.ch.research_force,player.ch.research_race.capitalize()))
    c.text(49,1,'NATURE %17.2f' %player.ch.research_forces['Nature']+'%',10)
    the_line=3
    for race in races['Nature']:
        if race==player.ch.research_race:
            col=2
        else:
            col=7
        c.text(50,the_line,'%s) %-16s:%6.2f' %(chr(all_races.index(race)+97),race.capitalize(),player.ch.research_races['Nature'][race])+'%',col)
        the_line+=1
    c.text(49,the_line+1,'ORDER  %17.2f' %player.ch.research_forces['Order']+'%',9)
    the_line+=3
    for race in races['Order']:
        if race==player.ch.research_race:
            col=2
        else:
            col=7
        c.text(50,the_line,'%s) %-16s:%6.2f' %(chr(all_races.index(race)+97),race.capitalize(),player.ch.research_races['Order'][race])+'%',col)
        the_line+=1
    c.text(49,the_line+1,'CHAOS  %17.2f' %player.ch.research_forces['Chaos']+'%',12)
    the_line+=3
    for race in races['Chaos']:
        if race==player.ch.research_race:
            col=2
        else:
            col=7
        c.text(50,the_line,'%s) %-16s:%6.2f' %(chr(all_races.index(race)+97),race.capitalize(),player.ch.research_races['Chaos'][race])+'%',col)
        the_line+=1
    waiting=msvcrt.getch()
    if ord(waiting) in range(97,len(all_races)+97):
        player.ch.research_race=all_races[ord(waiting)-97]
        for r in races:
            if all_races[ord(waiting)-97] in races[r]:
                player.ch.research_force=r
                break
        research()

def tame(animal):
    diff=animal.attr['tame'][1]
    if animal.attr['tame'][2] not in [i.id for i in player.ch.inventory]:
        message.use('taming_item',I[animal.attr['tame'][2]])
        return 0
    chance=random.randint(1,100)
    if chance+player.ch.forces['Nature']>=diff:
        message.creature('tame_success',animal)
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
                player.ch.followers.append(animal)
    else:
        message.creature('tame_fail',animal)
        animal.appearance-=10
        if animal.appearance<=0:
            animal.random=True
            for a in player.game_creatures:
                if a.id==animal.id:
                    animal.name=a.name
                    break

def command_tamed(animal):
    message.message('')
    c.text(1,0,'Choose command:   a)change mode   b)manipulate',7)
    choice=msvcrt.getch()
    if choice.lower()=='a':
        message.message('')
        c.text(1,0,'Choose mode:   a)follow   b)stay   c)guard',7)
        ch_mode=msvcrt.getch()
        if ch_mode.lower()=='a':
            message.message('')
            animal.mode='follow'
            message.creature('command_follow',animal)
        elif ch_mode.lower()=='b':
            message.message('')
            animal.mode='standing'
            animal.attr['area']=current_area
            message.creature('command_stay',animal)
        elif ch_mode.lower()=='c':
            message.message('')
            if animal.attr['tame'][0]=='guard':
                animal.mode='guarding'
                message.creature('command_guard',animal)
            else:
                message.message('cant_guard')
        else:
            message.message('')
    elif choice.lower()=='b':
        message.message('')
        c.text(1,0,'Choose action:   a)feed   b)farm   c)ride',7)
        ch_action=msvcrt.getch()
        message.message('')
        if ch_action.lower()=='a':
            chosen_food=0
            for i in player.ch.inventory:
                if i.id == animal.attr['tame'][2]:
                    chosen_food=i
                    break
            if chosen_food and animal.food<100:
                message.creature('feed',animal)
                i.lose_item(1)
                animal.food=min([animal.food+random.randint(10,20),100])
            elif chosen_food and animal.food==100:
                message.message('full_animal')
            else:
                message.use('feed_item',I[animal.attr['tame'][2]])
        elif ch_action.lower()=='b':
            message.message('')
            if animal.attr['tame'][0]=='farm':
                if animal.farm:
                    if 'container' in I[animal.attr['tame'][3]].effect:
                        needed=I[I[animal.attr['tame'][3]].effect['container']]
                        found=0
                        for cont in player.ch.inventory:
                            if cont.id==needed.id and cont.name==needed.name:
                                cont.lose_item(1)
                                found=1
                                break
                        if not found:
                            message.use('needed_container',needed)
                            return 0
                    creation=I[animal.attr['tame'][3]].duplicate(1)
                    ground_items.append([player.ch.xy[0],player.ch.xy[1],creation])
                    player.ch.pick_up(ground_items)
                    message.use('farm_harvest',creation)
                    animal.farm-=1
                else:
                    message.message('nothing_to_farm')
            else:
                message.message('cant_farm')
        elif ch_action.lower()=='c':
            message.message('')
            if animal.attr['tame'][0]=='ride' and not player.ch.ride and not player.ch.possessed:
                player.ch.followers.remove(animal)
                player.ch.ride.append(animal)
                player.ch.backpack += animal.attr['Str']*2
                hide(animal)
                animal.xy=[1,1]
                animal.mode='follow'
                message.creature('mount',animal)
                if animal.food<25:
                    message.message('hungry_mount')
                elif animal.food<75:
                    message.message('normal_mount')
                else:
                    message.message('well_fed_mount')
            else:
                if player.ch.ride:
                    message.message('cant_ride_two')
                else:
                    message.message('cant_ride')

def possess(animal,tr=''):
    message.message('')
    chance=float(player.ch.attr['Mnd'])/(player.ch.attr['Mnd']+animal.attr['Mnd'])
    tried=random.random()
    if tried<chance or tr:
        player.ch.possessed=[animal]
        for x in player.ch.attr:
            player.ch.attr[x]=animal.attr[x]
        player.ch.life+=animal.life
        player.ch.max_life+=animal.life
        if tr=='trans':
            message.creature('transform_into',animal)
        else:
            message.creature('possessed_animal',animal)
            hide(animal)
            animal.xy=[1,1]
            animal.mode='follow'
            if 'spirit of nature3' in player.ch.tool_tags:
                the_slot=''
                if player.ch.equipment['Right hand'] and player.ch.equipment['Right hand'].id==50 and \
                   (player.ch.equipment['Right hand'].effect=={} or 'totem' in player.ch.equipment['Right hand'].type):
                    the_slot='Right hand'
                elif player.ch.equipment['Left hand'] and player.ch.equipment['Left hand'].id==50 and \
                     (player.ch.equipment['Left hand'].effect=={} or 'totem' in player.ch.equipment['Left hand'].type):
                    the_slot='Left hand'
                if the_slot:
                    if 'totem' in player.ch.equipment[the_slot].type:
                        if 'temp_attr' in player.ch.equipment[the_slot].effect:
                            del(player.ch.equipment[the_slot].effect['temp_attr'])
                        if 'transform' not in player.ch.equipment[the_slot].effect and player.ch.equipment[the_slot].name[:-6]==animal.name:
                            player.ch.equipment[the_slot].effect['transform']=animal.duplicate(1,1,10000,animal.force,
                                                                                               animal.race,rand=False)
                            player.ch.equipment[the_slot].effect['transform'].mode='temp'
                    else:
                        player.ch.equipment[the_slot].type.append('totem')
                        player.ch.equipment[the_slot].type.remove('weapon')
                        player.ch.equipment[the_slot].effect[animal.name]=0.
                        player.ch.equipment[the_slot].effect['transform']=animal.duplicate(1,1,10000,animal.force,
                                                                                            animal.race,rand=False)
                        player.ch.equipment[the_slot].effect['transform'].mode='temp'
                        player.ch.equipment[the_slot].name='%s totem' %(animal.name)
    elif tried>.95:
        animal.mode='hostile'
        message.creature('anger_animal',animal)

def pickpocket(target):
    target_awareness=(target.attr['Int']+target.attr['Mnd'])/2.
    if 'stealthy' in player.ch.tool_tags:
        picking_skill=(player.ch.attr['Int']+player.ch.attr['Dex'])/1.5
    else:
        picking_skill=(player.ch.attr['Int']+player.ch.attr['Dex'])/2.
    chance=picking_skill/(target_awareness+picking_skill)
    if random.random()<chance:
        if len(target.attr['loot'])==1 and 'picked_dry' not in target.attr:
            inventory.put_item([[1000,75,1,10]],player.ch.xy)
            target.attr['picked_dry']=1
            message.creature('pilfer_last',target)
        elif len(target.attr['loot'])>1:
            inventory.put_item([target.attr['loot'][1]],player.ch.xy)
            target.attr['loot']=[target.attr['loot'][0]]+target.attr['loot'][2:]
            message.creature('pilfer',target)
        elif len(target.attr['loot'])==1 and 'picked_dry' in target.attr:
            message.creature('no_pilfer',target)
    else:
        target.mode='hostile'
        message.creature('steal_failed',target)

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
                curr_coords=[int(current_area[4:])/load.map_size,int(current_area[4:])%load.map_size]
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
                for x in player.ch.inventory:
                    if y in x.type:
                        offering.add(x)
            offering=list(offering)
            getting=[]
            if 'trade_goods' in target.attr and target.attr['trade_timer']+600>player.ch.turn:
                getting=target.attr['trade_goods'][:]
                target.attr['trade_timer']+=100
            else:
                for x in trade_goods[target.race]['buy']:
                    the_goods=inventory.put_item([x])
                    if the_goods:
                        getting.append(the_goods)
                target.attr['trade_goods']=getting[:]
                target.attr['trade_timer']=player.ch.turn
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
                            if x in player.ch.inventory:
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
                                ground_items.append([player.ch.xy[0], player.ch.xy[1], x.duplicate(chosen[x])])
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
    m=(float(merch.attr['Int']+merch.attr['Cre'])/(merch.attr['Int']+merch.attr['Cre']+player.ch.attr['Int']+player.ch.attr['Cre'])-.5)/2
    if sell:
        price-=price*m
    else:
        price+=price*m
    return price
                        

def find_place(a,b):
    good_coords=[]
    max_score=0
    for x in range(len(load.T_matrix)):
        for y in range(len(load.T_matrix)):
            if x==0 and y==0:
                continue
            else:
                if load.T_matrix[x][y][a]+load.T_matrix[x][y][b]>max_score:
                    max_score=load.T_matrix[x][y][a]+load.T_matrix[x][y][b]
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
##    c.text(35,16,'(r)estart',7)
    c.text(35,17,'(q)uit',7)
    i = ''
    while 1:
        if msvcrt.kbhit():
            i = msvcrt.getch()
            if i == 'q' or i == 'Q':
                return 0
##            elif i == 'r' or i == 'R':
##                reinitialize()
##                start_game()
##                return 1

def drink(xy):
    if T[land[xy[1]-1][xy[0]-21]].drink != {}:
        if player.ch.thirst == 0:
            message.use('over_drink',T[land[xy[1]-1][xy[0]-21]])            
            return 1
        message.use('drink',T[land[xy[1]-1][xy[0]-21]])
        if T[land[xy[1]-1][xy[0]-21]].id=='t' and 'goblin1' in player.ch.tool_tags:
            for k,v in {'energy':10,'thirst':5}.items():
                player.effect(k,v)
        else:
            for k,v in T[land[xy[1]-1][xy[0]-21]].drink.items():
                player.effect(k,v)
    elif player.ch.possessed:
        if player.ch.thirst>20 or player.ch.hunger>20:
            to_eat={'wild horse':'gb','squirrel':'T','snake':'b','poison snake':'b','camel':'Tb','giant lizard':'.,',
                    'penguin':'wW','monkey':'T','polar bear':'wW','bear':'b','cattle':'gb','chicken':'g.','fish':'wW',
                    'plant':'.g'}
            if T[land[xy[1]-1][xy[0]-21]].id in to_eat.get(player.ch.possessed[0].race,''):
                if player.ch.equipment['Right hand'] and player.ch.possessed[0].name in player.ch.equipment['Right hand'].effect:
                    player.ch.equipment['Right hand'].effect[player.ch.possessed[0].name]\
                                               =min([100,player.ch.equipment['Right hand'].effect[player.ch.possessed[0].name]+0.1])
                elif player.ch.equipment['Left hand'] and player.ch.possessed[0].name in player.ch.equipment['Left hand'].effect:
                    player.ch.equipment['Left hand'].effect[player.ch.possessed[0].name]\
                                               =min([100,player.ch.equipment['Left hand'].effect[player.ch.possessed[0].name]+0.1])
                if player.ch.xy not in player.ch.worked_places[player.ch.mode]:
                    for k,v in {'energy':10,'thirst':5,'hunger':5}.items():
                        player.effect(k,v)
                    message.message('eating_%s' %(player.ch.possessed[0].race.replace(' ','_')))
                    if player.ch.possessed[0].race!='plant':
                        player.ch.worked_places[player.ch.mode].append(xy[:])
                else:
                    message.message('no_food_%s' %(player.ch.possessed[0].race.replace(' ','_')))
            elif player.ch.possessed[0].race in ['grizzly','wolf','dog','polar wolf','hyena']:
                found_meat=0
                for x in ground_items:
                    if [x[0],x[1]]==player.ch.xy and 'meat' in x[2].name:
                        found_meat=1
                        for k,v in {'energy':10,'thirst':10,'hunger':25}.items():
                            player.effect(k,v)
                        break
                if found_meat:
                    if x[2].qty>1:
                        x[2].qty-=1
                    else:
                        ground_items.remove(x)
                    message.message('eating_carnivore')
                    if player.ch.equipment['Right hand'] and player.ch.possessed[0].name in player.ch.equipment['Right hand'].effect:
                        player.ch.equipment['Right hand'].effect[player.ch.possessed[0].name]\
                                                   =min([100,player.ch.equipment['Right hand'].effect[player.ch.possessed[0].name]+0.1])
                    elif player.ch.equipment['Left hand'] and player.ch.possessed[0].name in player.ch.equipment['Left hand'].effect:
                        player.ch.equipment['Left hand'].effect[player.ch.possessed[0].name]\
                                                   =min([100,player.ch.equipment['Left hand'].effect[player.ch.possessed[0].name]+0.1])
                else:
                    message.message('no_food_carnivore')
            else:
                message.message('no_food_%s' %(player.ch.possessed[0].race.replace(' ','_')))
        else:
            message.message('not_hungry')
    else:
        message.message('no_drink')

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
        message.message('no_open')
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
        message.message('which_open')
        i = msvcrt.getch()
        try:
            message.message('')
            try:
                i = int(i)
            except ValueError:
                message.message('direction')
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
                    message.message('no_open')
                    return 0
                else:
                    success = open_container(cont[2])
                    return success
        except KeyError:
            message.message('direction')
            return 0

def open_container(chest):
    if 'locked' in chest.type: ##Lockpicking se uchi samo kogato uspeesh!
        if 'lockpick' in player.ch.tool_tags:
            lock_atts = (player.ch.attr['Dex']+player.ch.attr['Int'])/2.0
            if 'lockpicking' not in player.ch.skills:
                player.ch.skills['lockpicking'] = float(player.ch.attr['Dex'])
            if random.random() < player.ch.skills['lockpicking']/chest.effect['lock_strength']:
                learn = random.uniform(0,100)
                if learn <= (lock_atts - player.ch.skills['lockpicking']/5)/lock_atts*100:
                    player.ch.skills['lockpicking'] += 0.1
                chest.type.remove('locked')
                message.message('success_lockpick')
                msvcrt.getch()
            else:
                if player.ch.skills['lockpicking'] < chest.effect['lock_strength']/10:
                    learn = random.uniform(0,100)
                    if learn <= (lock_atts - player.ch.skills['lockpicking']/5)/lock_atts*100:
                        player.ch.skills['lockpicking'] += 0.01
                message.message('failed_lockpick')
                msvcrt.getch()
                return 0
        else:
            message.use('no_lockpick',chest)
            msvcrt.getch()
            return 0
    c.page()
    print ' You open the %s and look inside.\n (t) take item (p) put item\n' %(chest.name)
    for i in range(len(chest.effect['contains'])):
        print ' %s)   %s %d x %s stones' %(chr(i+97),chest.effect['contains'][i].name.capitalize(),chest.effect['contains'][i].qty,
                                         str(chest.effect['contains'][i].weight))
        c.text(4,i+3,chest.effect['contains'][i].tag,chest.effect['contains'][i].color)
    print '\n You can carry %s more stones, %s more will fit in your backpack.' %(str(player.ch.max_weight-player.ch.weight),
                                                                                  str(player.ch.backpack))
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
            if item.qty > 1 and player.ch.equipment['Backpack'] != []:
                message.message('pickup')                    
                a = ''
                i = ' '
                while ord(i) != 13:
                    i = msvcrt.getch()
                    if ord(i) in range(48,58):
                        c.write(i)
                        a += i
                message.message('')
                if a =='':
                    open_container(chest)
                    return 1
                a=int(a)
            else:
                a = 1
            if a > item.qty:
                a = item.qty
            if chest in player.ch.inventory:
                player.ch.weight -= item.weight*a
                player.ch.backpack += item.weight * item.qty
            if player.ch.weight+item.weight*a <= player.ch.max_weight and item.weight*a <= player.ch.backpack and player.ch.equipment['Backpack'] != []:
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
            elif player.ch.weight+item.weight*a > player.ch.max_weight:
                message.use('cant_carry', item)
                msvcrt.getch()
            elif item.weight*a > player.ch.backpack:
                if player.ch.equipment['Backpack'] == []:
                    if 'two_handed' in item.type:
                        needed_hands = 2
                    else:
                        needed_hands = 1
                    if player.ch.free_hands >= needed_hands:
                        item.get_item()
                        chest.weight -= item.weight*a
                        player.ch.free_hands -= needed_hands
                        if 1 < item.qty:
                            item.qty -= 1
                        else:
                            chest.effect['contains'].remove(item)
                        player.ch.backpack = 0
                    else:
                        message.message('drop_first')
                        msvcrt.getch()
                else:
                    message.use('cant_fit_in_backpack', item)
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
                    message.message('ch')
                    dropped = 1
            if not dropped:
                chest.effect['contains'].append(item)
            chest.weight += item.weight * item.qty
            if chest in player.ch.inventory:
                player.ch.weight += item.weight * item.qty
                player.ch.backpack -= item.weight * item.qty
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
    message.message('open_door')
    
def creature_open_door(xy, door_id):
    land[xy[1]-1] = land[xy[1]-1][:xy[0]-21] + T[door_id].degrade_to['door'] + land[xy[1]-1][xy[0]-20:]
    c.scroll((xy[0],xy[1],xy[0]+1,xy[1]+1), 1, 1, T[land[xy[1]-1][xy[0]-21]].colour, T[land[xy[1]-1][xy[0]-21]].char)

def close_door(xy, door_id):
    blocked = 0
    for cr in player.all_beings:
        if cr.xy == xy:
            blocked = 1
    for i in ground_items:
        if i[:2] == xy:
            blocked = 1
    if blocked:
        message.message('blocked_door')
    else:
        land[xy[1]-1] = land[xy[1]-1][:xy[0]-21] + T[door_id].degrade_to['door'] + land[xy[1]-1][xy[0]-20:]
        c.scroll((xy[0],xy[1],xy[0]+1,xy[1]+1), 1, 1, T[land[xy[1]-1][xy[0]-21]].colour, T[land[xy[1]-1][xy[0]-21]].char)
        message.message('close_door')

def cook():
    mats=[]
    selected_mats=[]
    for i in player.ch.inventory:
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
            for r in inventory.CR[player.ch.attr['Cre']]:
                all_in=1
                needed_tags=inventory.cook_recipes[r][3:]
                for t in selected_tags:
                    if t in needed_tags:
                        needed_tags.remove(t)
                    else:
                        all_in=0
                        break
                for t in inventory.cook_recipes[r][1]:
                    full_tools=player.ch.tool_tags[:]
                    for gi in ground_items:
                        if gi[:2]==player.ch.xy:
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
                for x in player.ch.inventory:
                    if x.id==m.id and x.name==m.name:
                        x.lose_item(m.qty)
                        if the_meal=='get seeds':
                            veg_name=m.name
        creation=I[inventory.cook_recipes[the_meal][2]].duplicate(1)
        ## Za semena se izpolzva SAMO iztochnika (zelenchuk/cvete)
        if the_meal=='get seeds':
            creation.qty=3
            creation.name=veg_name+' seed'
            medium=creation.effect.pop('plant_vegetable')
            creation.effect['plant_specific']=[medium,veg_name]
        ground_items.append([player.ch.xy[0],player.ch.xy[1],creation])
        player.ch.pick_up(ground_items)
        c.rectangle((0,0,80,1))
        c.pos(1,0)

def choose_spell():
    c.page()
    if player.ch.spells == []:
        c.write('''
  You do not know any spells, you have to create some!''')
        i = msvcrt.getch()
    else:
        c.write('''
  Choose your spell:\n\n  ''')
        for x in player.ch.spells.keys():
            c.write('%d) %s  Ingredients:%s\n  ' %(player.ch.spells.keys().index(x)+1,x,[x.name for x in player.ch.spells[x]['ingredients']]))
        i = msvcrt.getch()
        try:
            i = int(i)-1
            if i in range(len(player.ch.spells)):
                cast_spell(player.ch.spells.keys()[i])
        except ValueError:
            pass

def cast_spell(name):
    in_stock = {}
    needed = {}
    for x in player.ch.inventory:
        in_stock[x.id] = x.qty
    for x in player.ch.spells[name]['ingredients']:
        needed[x.id] = needed.get(x.id,0) + 1
    for x in needed:
        if needed[x]>in_stock[x]:
            c.write("  You don't have the needed ingredients!")
            i = msvcrt.getch()
            return 0
    for x in player.ch.inventory:
        if x.id in needed:
            x.lose_item(needed[x.id])
    if len(player.ch.spells[name]) == 1:
        c.write('''  You cast the spell and nothing happens - you must have made a mistake in
  the incantation! Your ingredients are wasted and you throw away your useless
  writings on the spell. You will have to start over with the creation.''')
        del(player.ch.spells[name])
        i = msvcrt.getch()
    else:
        if player.ch.spells[name]['effect'] == 'Fizzle':
            c.write('''  You cast the spell and feel the energy spread around you without any purpose
  - the spell was useless! Your ingredients are wasted.''')
            del(player.ch.spells[name])
            i = msvcrt.getch()
        elif player.ch.spells[name]['effect'] == 'Damage/Healing':
            if player.ch.spells[name]['target'] == 'Self':
                act = {'-':'destructive','+':'healing'}
                c.write('''\n  The %s energy of the spell focuses on you!''' %act[player.ch.spells[name]['action']])
                player.ch.life += eval('%s%d' %(player.ch.spells[name]['action'],player.ch.spells[name]['strength']))
                if player.ch.life > player.ch.max_life:
                    player.ch.life = player.ch.max_life
                i = msvcrt.getch()
            else:
                player.ch.spell_cast = name
        elif player.ch.spells[name]['effect'] == 'Invisibility':
            if player.ch.spells[name]['target'] == 'Self':
                if player.ch.spells[name]['action'] == '+':
                    player.ch.effects['invisible']=player.ch.spells[name]['strength']+5
                    c.write('''\n  You cast the spell and feel the energy fill you up. You become invisible!''')
                    player.ch.emotion=1
                    i = msvcrt.getch()
                else:
                    c.write('''  You cast the spell and feel the energy spread around you without any purpose
 - the spell was useless! Your ingredients are wasted.''')
                    del(player.ch.spells[name])
                    i = msvcrt.getch()
            else:
                player.ch.spell_cast = name

def execute_spell(buff):
    ## Tuk se razreshavat efektite nasocheni kum drugi sushtestva i mesta. Tezi kum igracha sa v cast_spell()
    all_targets = []
    for x in player.all_creatures:
        if x.mode != 'not_appeared' and max([abs(x.xy[0]-player.ch.xy[0]),abs(x.xy[1]-player.ch.xy[1])])<=player.ch.attr['Mnd'] and clear_los(direct_path(player.ch.xy,x.xy)):
            all_targets.append(x)
    if len(all_targets):
        message.message('choose_target')
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
            message.creature('current_target',target)
            target.tag = old_tag
            target.emotion = old_emotion
            i = msvcrt.getch()
            if ord(i) == 13:
                break
        if player.ch.spells[player.ch.spell_cast]['effect'] == 'Damage/Healing':
            target.life += eval('%s%d' %(player.ch.spells[player.ch.spell_cast]['action'],player.ch.spells[player.ch.spell_cast]['strength']))
            if player.ch.spells[player.ch.spell_cast]['action'] == '-':
                target.mode = 'hostile'
                message_mode = 'spell_damage'
            else:
                message_mode = 'spell_healing'
            message.creature('%s' %message_mode,target,player.ch.spells[player.ch.spell_cast]['strength'])
        elif player.ch.spells[player.ch.spell_cast]['effect'] == 'Invisibility':
            target.attr['invisible']=player.ch.spells[player.ch.spell_cast]['strength']+5
    else:
        message.message('no_target')
            

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
        if player.ch.attr['Int']/total_diff > random.random():
            if (player.ch.attr['Mnd']/target_diff)*.95-player.ch.attr['Mnd']/total_diff < random.random():
                if target == 'Self':
                    target = 'Other'
                else:
                    target = 'Self'
            if (player.ch.attr['Mnd']/action_diff)*.95-player.ch.attr['Mnd']/total_diff < random.random():
                if action == '-':
                    action = '+'
                else:
                    action = '-'
            if (player.ch.attr['Mnd']/(strength*2))*.95-player.ch.attr['Mnd']/total_diff < random.random():
                strength = random.randint(1,max([1,strength-1]))
            if (player.ch.attr['Mnd']/effect_diffs[effect])*.95-player.ch.attr['Mnd']/total_diff < random.random():
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
    all_ings = inventory.herbs
    ings = []
    n = int(total_diff)/5
    for x in range(n):
        ings.append(random.choice(all_ings))
    if effect == 0:
        player.ch.spells[name]={'ingredients':ings}
    else:
        player.ch.spells[name]={'ingredients':ings,'effect':effect,'strength':strength,'target':target,'action':action}

def look():
    key = ' '
    c.pos(*player.ch.xy)
    xy = player.ch.xy[:]
    changed=1
    while ord(key) != 13:
        if player.ch.target and changed:
            changed=0
            redraw_screen()
            highlight_path(direct_path(player.ch.xy,player.ch.target))
            c.scroll((player.ch.target[0],player.ch.target[1],player.ch.target[0]+1,player.ch.target[1]+1),1,1,236,'X')
            c.pos(*xy)
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key=='t':
                changed=1
                player.ch.target=xy[:]
            md = {'1':[-1,1], '2':[0,1], '3':[1,1], '4':[-1,0], '5':[0,0],
              '6':[1,0], '7':[-1,-1], '8':[0,-1], '9':[1,-1], '0':[0,0]}
            a = 0
            try:
                for a in range(2):
                    xy[a] += md[key][a]
                if (xy[0] == 20) or (xy[0] == 79) or (xy[1] == 0) or (xy[1] == 24):
                    xy[0] -= md[key][0]
                    xy[1] -= md[key][1]
                message.message('')
                c.pos(*xy)
                message.look(xy, player.all_beings, T, player.ch.known_areas)
                c.pos(*xy)
            except:
                pass

def start_game(fl):
    t = 0
    i = ''
    f = ''
    while t == 0:
        load.T_matrix=[]
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
            create_character(fl)
            t = load.draw_terr(player.ch.start_force)
        if i == 'l':
            c.write('Load which character? ')
            a = ''
            i = ' '
            while ord(i) != 13:
                i = msvcrt.getch()
                if ord(i) in range(65,91) or ord(i) in range(97,123) or ord(i) == 46:
                    c.write(i)
                    a += i
            t,load.T_matrix = load.load_terr(a)
    redraw_screen()
    c.pos(*player.ch.xy)
    
def create_character(fl):
    races = {'a':'elf','b':'gnome','c':'spirit of nature','d':'dryad','e':'water elemental','f':'fairy','g':'human',
             'h':'dwarf','i':'spirit of order','j':'ork','k':'troll','l':'spirit of chaos','m':'goblin','n':'kraken',
             'o':'imp'}
    i = ''
    while i not in races.keys():
        c.page()
        c.write("""
 The form your character may take in Balance is completely controlled by his or
 her actions. If you like to go around and kill things, you are likely to end
 up with an ork, while a character that spends his time in the mine will slowly
 become a dwarf. There are various actions both on your environment and other
 beings that will form your character. They are all connected to the three
 forces in the world of Balance - Order, Chaos, and Nature. Every action will
 align you more with one of the forces, and with one or more of the forms
 governed by it. This is the only way to mold your character in the game - you
 gain and loose abilities depending on the predominant form you hold. Choosing
 a form now gives you 34% attunement to it, and 34% alignment to the
 respective force. Your total form attunement can't be higher than your
 alignment to the respective force.

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
    player.ch = player.make_player(race,force)
    player.take_force_effect()
    player.all_beings = [player.ch]
    i = 'z'
    too_heavy = 0
    heaviness = {'a':[1,['Nature']],'b':[2,['Nature','Chaos','Order']],'c':[3,['Nature']],
                 'd':[3,['Order']],'e':[2,['Order']],'f':[2,['Order']],'g':[4,['Order']],
                 'h':[3,['Chaos']],'i':[6,['Chaos']],'j':[2,['Chaos']]}
    while i not in 'abcdefghij' or too_heavy:
        c.page()
        c.write('''
  The next step to building your character is to pick the starting inventory
  set of your choise. The sets are useful to a character of the respective
  Force as they contain some of the tools needed to deliver impact on the
  world. They are also restricted by your strength (fairies are the weakest,
  while orks and trolls are the strongest).

  a) Forest healer: light clothes and a healing set.
  b) Traveler: a robe and a stick to help you on the way.
  c) Nature warrior: dryad-crafted armour and an elven bow.
  
  d) Builder of Order: a miner's pick and clothes.
  e) Farmer: clothes, a shovel and some seeds.
  f) Merchant: clothes and some money, a package of goods.
  g) Soldier: a sword and leather armour.
  
  h) Village destroyer: a big club for breaking stuff. Oh, and food...
  i) Pillager: a couple of weapons and a lot of armour.
  j) Shaman: a book of magic and a herb set.''')
        i = msvcrt.getch()
        try:
            if heaviness[i][0] > player.ch.attr['Str']:
                c.write('''\n\n  This set is too heavy for you to use!''')
                msvcrt.getch()
                too_heavy = 1
            elif force not in heaviness[i][1]:
                c.write('''\n\n  This set is only for %s characters!''' %(heaviness[i][1][0]))
                msvcrt.getch()
                too_heavy = 1
            else:
                too_heavy = 0
        except KeyError:
            pass
    player.start_inv(i)
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
        player.ch.name = a
        if player.ch.name in fl:
            print '\n  Character savefile already exists!'
            i1=msvcrt.getch()
        else:
            break
    mkdir(curdir+'//%s_dir' %(a))

def change_place(area,direction):
    if area!='areaB':
        run_away = {'Dex':0,'End':0,'Int':0,'Cre':0}
        hostiles = 0
        character_run = 0
        for thing in player.all_creatures:
            ## Broqt se samo gadinite koito sa na 7 i po malko razstoqnie ot igracha
            if thing.mode == 'hostile' and max([abs(thing.xy[0]-player.ch.xy[0]),abs(thing.xy[1]-player.ch.xy[1])])<8 and clear_los(direct_path(thing.xy,player.ch.xy)):
                hostiles += 1
                for x in run_away:
                    run_away[x] = max([run_away[x],thing.attr[x]])
                    if hostiles == 1:
                        character_run += player.ch.attr[x]
        if hostiles and 'invisible' not in player.ch.effects:
            difficulty = sum(run_away.values()+[hostiles])
            chance = 50.0*character_run/difficulty
            if random.randint(1,100) < chance:
                message.message('ran_away')
                msvcrt.getch()
            else:
                message.creature('no_escape',0)
                return 0
    if area != 'area0':
        old_temp=current_place['Temperature']
        places = open('%s//%s_dir//new_%s.dat'%(curdir,player.ch.name,current_area), 'w')
        pickle.dump(ground_items, places)
        pickle.dump(current_place, places)
        pickle.dump(terrain_type, places)
        pickle.dump(current_area, places)
        pickle.dump(directions, places)
        pickle.dump(land, places)
        pickle.dump(map_coords, places)
        creatures_left=[]
        for creature in player.all_creatures:
            if creature not in player.ch.followers+player.ch.ride+player.ch.possessed:
                creatures_left.append(creature)
        pickle.dump(creatures_left, places)
        if current_area not in player.ch.known_areas:
            player.ch.known_areas.append(current_area)
        places.close()
        load.new_terr(area,direction)
        draw_hud()
        player.ch.worked_places={'Nature':[],'Chaos':[],'Order':[]}
        player.ch.target=[]
        draw_move(player.ch, player.ch.xy[0], player.ch.xy[1])
        if old_temp<33<=current_place['Temperature']:
            for thing in player.ch.inventory:
                if thing.name=='ring of winter':
                    thing.name+=' (melted)'
                    del(thing.effect['winterwalk'])
        elif current_place['Temperature']<66<=old_temp:
            for thing in player.ch.inventory:
                if thing.name=='ring of summer':
                    thing.name+=' (withered)'
                    del(thing.effect['summerwalk'])
        for x in player.all_creatures:
            if x not in player.hidden and clear_los(direct_path(player.ch.xy,x.xy)):
                draw_move(x, x.xy[0], x.xy[1])
        c.pos(*player.ch.xy)
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
        for i in player.all_creatures:
            if not i.random:
                creatures_number += 1
        data.append(str(creatures_number)+'\n')
        for thing in player.all_creatures:
            if not thing.random:
                data.append(str(thing.id)+' '+str(thing.xy[0])+' '+str(thing.xy[1])+' '+str(thing.game_id)+' '+str(thing.appearance)+'\n')
            else:
                data.append(str(thing.id)+' '+str(thing.xy[0])+' '+str(thing.xy[1])+' '+str(thing.game_id)+' '+str(player.ch.turn)+'\n')
        if current_area not in player.ch.known_areas:
            player.ch.known_areas.append(current_area)
        places = open(current_area+'.dat', 'w')
        for i in data:
            places.write(i)
        pickle.dump(ground_items, places)

        places.close()
        t = load.world()
        current_area = 'world'
        player.ch.place_time = 100
    else:
        for x in world_places:
            if world_places[x] == player.ch.xy:
                change_place(x, 0)
                current_area = x
                player.ch.place_time = 1
                entered = 1
                break
        if entered == -1:
            entered = 0
    return current_area, entered

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

def clear_los(path):
    if len(path)>2:
        for xy in path[1:-1]:
            if not T[land[xy[1]-1][xy[0]-21]].clear_los:
                return 0
    if not T[land[path[-1][1]-1][path[-1][0]-21]].pass_through:
        return 0
    return 1
    
def highlight_path(way):
    if way != []:
        for step in way[1:]:
            x = step[0]
            y = step[1]
            if way.index(step)<=player.ch.attr['Dex']:
                c.scroll((x, y, x+1, y+1), 1, 1, 14,'*')
            else:
                c.scroll((x, y, x+1, y+1), 1, 1, 4,'*')

def good_place(thing,place):
    no_pass = 0
    for creature in player.all_creatures:
        if creature.xy == place and not (creature.mode=='hostile' and thing.mode=='guarding') and not (thing.mode=='hostile' and creature.mode=='guarding'):
            no_pass = 1
            break
    if (not T[land[place[1]-1][place[0]-21]].pass_through or no_pass or (T[land[place[1]-1][place[0]-21]].id in thing.terr_restr and thing.mode!='standing_hostile')) and not (thing.race=='spirit of order' and current_place['Order']>30 and T[land[place[1]-1][place[0]-21]].id in '#o+s') and not (thing.race=='spirit of chaos' and current_place['Chaos']>30 and T[land[place[1]-1][place[0]-21]].id in '#o+s') and not (thing.race=='gnome' and current_place['Nature']>30 and T[land[place[1]-1][place[0]-21]].id in 'nmA%') and not ('door_' in T[land[place[1]-1][place[0]-21]].world_name and thing.t=='sentient'):
        return 0
    return 1
