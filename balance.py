import terrain
import player
import msvcrt
import init_screen
import os
import pickle
import message
from movement import shoot
from movement import move
from glob import glob

def save():
##    init_screen.c.write('Save to which file?')
##    a = ''
##    i = ' '
##    while ord(i) != 13:
##        i = msvcrt.getch()
##        if ord(i) in range(65,91) or ord(i) in range(97,123) or ord(i) == 46:
##            init_screen.c.write(i)
##            a += i
    try:
        f = open(player.ch.name, 'w')
    except:
        return 0
    for x in range(23):
        f.write(init_screen.land[x]+'\n')
    pickle.dump(player.ch, f)
    pickle.dump(player.ch.inventory, f)
    pickle.dump(player.ch.equipment, f)
    pickle.dump(player.ch.skills, f)
    pickle.dump(player.ch.spells, f)
    pickle.dump(player.ch.forces, f)
    pickle.dump(player.ch.races, f)
    pickle.dump(player.ch.effects, f)
    pickle.dump(player.ch.land_effects, f)
    pickle.dump(player.ch.known_areas, f)
    pickle.dump(player.ch.weapon_skills, f)
    pickle.dump(player.ch.attr_colors, f)
    creatures_left=[]
    for creature in player.all_creatures:
        if creature not in player.ch.followers+player.ch.ride+player.ch.possessed:
            creatures_left.append(creature)
    pickle.dump(creatures_left, f)
    pickle.dump(player.hidden, f)
    pickle.dump(init_screen.ground_items, f)
    pickle.dump(init_screen.directions, f)
    pickle.dump(init_screen.world_places, f)
    pickle.dump(init_screen.top_world_places, f)
    pickle.dump(init_screen.place_descriptions, f)
    pickle.dump(init_screen.map_coords, f)
    pickle.dump(init_screen.current_area, f)
    pickle.dump(init_screen.current_place, f)
    pickle.dump(init_screen.treasure_modifier, f)
    from load import T_matrix
    pickle.dump(T_matrix, f)
    f.close()
    ## area files update
    os.chdir(os.curdir+r'\%s_dir' %(player.ch.name))
    new_files=glob('new_area*.dat')
    for f in [every.split('_')[-1] for every in new_files]:
        os.system('del %s' %(f))
    for f in new_files:
        os.system('ren %s %s' %(f,f.split('_')[-1]))
    os.chdir('..')

    return 1

local_files=glob('*')
init_screen.start_game(local_files)
i = ' '
clock = 1
riding=0
while i:
    if msvcrt.kbhit():
        message.message('')
        i = msvcrt.getch()
        if player.ch.ride and player.ch.ride[0].food>24 and i in ['1','2','3','4','5','6','7','8','9']:
            if riding:
                move(i,player.ch,riding)
                player.ch.ride[0].food-=1
                riding=0
                continue
            else:
                riding=1
        if i == '0':
            i = '-1'
        if i == 'S':
            message.message('q')
            i = msvcrt.getch()
            if i == 'y' or i == 'Y':
                if save():
                    init_screen.redraw_screen()
                    i = '0'
                else:
                    message.message('')
                    message.message('save_failed')
            else:
                message.message('')
            continue
        if i == 'Q':
            break
        if i == 'c':
            init_screen.character()
            init_screen.redraw_screen()
            continue
        if i == 'l':
            message.message('look')
            init_screen.look()
            init_screen.redraw_screen()
##            message.message('')
            continue
            i = '0'
        ## Form-dependent actions
        if 'waterform' not in player.ch.effects:
            if i == 's' and init_screen.current_area != 'world':
                if player.ch.ride:
                    message.message('dismount')
                    player.ch.ride[0].mode='follow'
                    player.ch.ride[0].xy=player.ch.xy[:]
                    player.ch.backpack-=player.ch.ride[0].attr['Str']*2
                    while player.ch.backpack<0:
                        drop = player.ch.inventory[-1].drop_item('yes',10000)
                        dropped = 0
                        for item in init_screen.ground_items:
                            if item[:2] == player.ch.xy and item[2].id == drop.id and item[2].stackable and item[2].name == drop.name:
                                item[2].qty += drop.qty
                                dropped = 1
                        if not dropped:
                            init_screen.ground_items.append([player.ch.xy[0], player.ch.xy[1],drop])
                        message.use('create_drop',drop)
                        msvcrt.getch()
                    player.ch.followers.append(player.ch.ride[0])
                    player.ch.ride=[]
                    i='0'
                elif player.ch.possessed:
                    if player.ch.possessed[0].mode=='temp':
                        message.creature('transform_outof',player.ch.possessed[0])
                    else:
                        message.creature('unpossess',player.ch.possessed[0])
                        player.ch.possessed[0].xy=player.ch.xy[:]
                        player.ch.possessed[0].mode='wander'
                    player.ch.life-=player.ch.possessed[0].life
                    player.ch.max_life-=player.ch.possessed[0].life
                    if player.ch.life<=0:
                        player.ch.possessed[0].life+=player.ch.life
                        player.ch.life=1
                    for at in player.ch.attr:
                        player.ch.attr[at]=player.ch.max_attr[at]
                    player.ch.possessed=[]
                    for cr in player.all_creatures:
                        if cr not in player.ch.followers+player.ch.ride+player.ch.possessed:
                            if cr.force=='Nature':
                                if player.ch.forces['Chaos']:
                                    if player.ch.forces['Nature']-player.ch.forces['Chaos']<\
                                       init_screen.current_place['Nature']-init_screen.current_place['Chaos']:
                                        cr.mode='hostile'
                            elif cr.force=='Order':
                                if player.ch.forces['Chaos']:
                                    if player.ch.forces['Order']-player.ch.forces['Chaos']<\
                                       init_screen.current_place['Order']-init_screen.current_place['Chaos']:
                                        cr.mode='hostile'
                            elif cr.force=='Chaos':
                                if player.ch.forces['Order']:
                                    if player.ch.forces['Chaos']-player.ch.forces['Order']<\
                                       init_screen.current_place['Chaos']-init_screen.current_place['Order']:
                                        cr.mode='hostile'
                                if player.ch.forces['Nature']:
                                    if player.ch.forces['Chaos']-player.ch.forces['Nature']<\
                                       init_screen.current_place['Chaos']-init_screen.current_place['Nature']:
                                        cr.mode='hostile'
                                if 'spirit of order3' in player.ch.tool_tags and random.randint(1,30)>cr.attr['Mnd']:
                                    cr.mode='fearfull'
                    i='0'
                else:
                    if terrain.T[init_screen.land[player.ch.xy[1]-1][player.ch.xy[0]-21]].id in terrain.unsittable:
                        message.message('no_sit')
                        i = '0'
                    else:
                        player.ch.sit = True
                        player.ch.rest = 25
                        message.message('sit')
                        i = '0'
            if i == 'm':
                if player.ch.mode == 'Nature':
                    player.ch.mode = 'Order'
                elif player.ch.mode == 'Order':
                    player.ch.mode = 'Chaos'
                elif player.ch.mode == 'Chaos':
                    player.ch.mode = 'Nature'
                init_screen.draw_mode()
                init_screen.c.pos(*player.ch.xy)
                continue
                i = '0'
            if i == 'q' and init_screen.current_area != 'world':
                init_screen.drink(player.ch.xy)
                i = '0'
            if not player.ch.possessed:
                if i=='h':
                    if player.ch.target:
                        if (player.ch.equipment['Right hand'] and 'ranged' in player.ch.equipment['Right hand'].type) or (player.ch.equipment['Left hand'] and 'ranged' in player.ch.equipment['Left hand'].type):
                            if player.ch.equipment['Right hand']:
                                handed='Right hand'
                            else:
                                handed='Left hand'
                            if player.ch.equipment['Ammunition']:
                                if player.ch.equipment['Ammunition'].effect['shoot']==player.ch.equipment[handed].effect['shoot']:
                                    shoot(player.ch)
                                else:
                                    message.message('wrong_ammo')
                            else:
                                message.message('need_ammo')
                        else:
                            message.message('need_ranged_weapon')
                    else:
                        message.message('target_first')
                    i='0'
                if i == 'i':
                    init_screen.draw_inv()
                    init_screen.redraw_screen()
                    if init_screen.current_area == 'world':
                        i = '-1'
                    else:
                        i = '0'
                if i == 'e':
                    init_screen.draw_equip()
                    init_screen.redraw_screen()
                    if init_screen.current_area == 'world':
                        i = '-1'
                    else:
                        i = '0'
                if i == 'k' and init_screen.current_area != 'world':
                    init_screen.cook()
                    init_screen.redraw_screen()
                    i = '0'
                if i == 'b' and not player.ch.ride:
                    if 'human1' in player.ch.tool_tags or 'dwarf1' in player.ch.tool_tags:
                        init_screen.ground_items=init_screen.build(init_screen.ground_items)
                    else:
                        message.message('need_human1&dwarf1')
                    continue
                    i = '0'
                if i == 't':
                    if 'dryad3' in player.ch.tool_tags:
                        init_screen.dryad_grow()
                    else:
                        message.message('need_dryad3')
                    continue
                    i = '0'
                if i == 'C' and not player.ch.ride:
                    init_screen.ground_items=init_screen.create(init_screen.ground_items)
                    i = '0'
                if i == '+' and init_screen.current_area != 'world':
                    opened = init_screen.find_to_open(player.ch.xy)
                    if opened:
                        init_screen.redraw_screen()
                    i = '0'
                if i == 'p' and init_screen.current_area != 'world':
                    player.ch.pick_up(init_screen.ground_items)
                    i = '0'
                if i == 'w' and init_screen.current_area != 'world' and not player.ch.ride:
                    player.ch.sit = False
                    player.ch.rest = 1
                    message.message('work')
                    i = ''
                    while not i:        
                        if msvcrt.kbhit():
                            i = msvcrt.getch()
                    init_screen.work(i)
                    continue
                    i = '0'
                if i == 'r':
                    if 'human3' in player.ch.tool_tags:
                        init_screen.research()
                        init_screen.redraw_screen()
                    else:
                        message.message('need_human3')
                    continue
            elif i in 'rwp+bkeiCt':
                message.message('not_when_possessed')
                msvcrt.getch()
                i='0'
        elif i in 'rwmp+bkqseiCt':
            message.message('not_in_waterform')
            msvcrt.getch()
            i='0'
##        if i == '<':
##            player.ch.sit = False
##            if terrain.T[init_screen.land[player.ch.xy[1]-1][player.ch.xy[0]-21]].id == '<':
##                init_screen.change_place('area'+init_screen.directions[5],5)
##                message.message('going_down')
##                i = '0'
##            elif terrain.T[init_screen.land[player.ch.xy[1]-1][player.ch.xy[0]-21]].id == '>':
##                message.message('nowhere_togo')
##                i = '0'
##            else:
##                message.message('no_stairs')
##                i = '0'
##        if i == '>':
##            player.ch.sit = False
##            if terrain.T[init_screen.land[player.ch.xy[1]-1][player.ch.xy[0]-21]].id == '>':
##                init_screen.change_place('area'+init_screen.directions[4],4)
##                message.message('going_up')
##                i = '0'
##            elif terrain.T[init_screen.land[player.ch.xy[1]-1][player.ch.xy[0]-21]].id == '<':
##                message.message('nowhere_togo')
##                i = '0'
##            else:
##                message.message('no_stairs')
##                i = '0'
##        if i == 'W':
##            if init_screen.world_places[init_screen.current_area] == [1,1]:
##                message.message('no_exit')
##            else:
##                init_screen.current_area, entered = init_screen.world(init_screen.current_area)
##                init_screen.redraw_screen()
##                if entered == 0:
##                    message.message('nowhere_togo')
##            i = '-1'
        if (i != '0') and (i != '5') and (i != '-1'):
            player.ch.sit = False
            player.ch.rest = 1
        clock = player.game_time(i)
        if clock == 0:
            break
        init_screen.c.pos(*player.ch.xy)

## area files clean-up
new_files=glob(r'%s_dir\new_area*.dat' %(player.ch.name))
all_files=glob(r'%s_dir\*' %(player.ch.name))
local_files=glob('*')
for f in new_files:
    os.system('del %s' %(f))
if '%s' %(player.ch.name) not in local_files:
    for f in all_files:
        os.system('del %s' %(f))
    os.system('rd %s_dir' %(player.ch.name))
raw_input("If you got an error, please send it to the creator!\nOtherwise press ENTER to exit (no pun intended).")
os._exit(0)
