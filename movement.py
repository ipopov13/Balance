from terrain import T
import player
import init_screen
import random
import message
import msvcrt
from inventory import put_item
from time import sleep

def attack(attacker,defender):
    if attacker.tag == '@' or defender.tag == '@':
        if attacker.tag == '@' and (player.ch.equipment['Right hand'] and 'ranged' in player.ch.equipment['Right hand'].type) or (player.ch.equipment['Left hand'] and 'ranged' in player.ch.equipment['Left hand'].type):
            message.message('cant_hit_with_bow')
            return 0
        if player.ch.weapon_weight < 6:
            att_att = 'Dex'
            def_att = 'Dex'
            battle_att = player.ch.attr['Dex']
        elif player.ch.weapon_weight < 10:
    ## Ako orujieto e sredno maksimalnata stoinost na umenieto stava 100 pri balans na Dex i Str
            the_max=max([player.ch.attr['Dex'],player.ch.attr['Str']])
            the_min=min([player.ch.attr['Dex'],player.ch.attr['Str']])
            battle_att = min([the_max+(the_min-the_max*2/3),20])
            att_att = 'Str'
            def_att = 'Dex'
        elif player.ch.weapon_weight >= 10:
            battle_att = player.ch.attr['Str']
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
        if learn <= (battle_att - player.ch.weapon_skill/5)/battle_att*100:
            player.ch.weapon_skill += 0.1*max([against/player.ch.weapon_skill,0.1])
        if player.ch.equiped_weaps == 2:
            learn = random.uniform(1,100)
            if learn <= (battle_att - player.ch.weapon_skill/5)/battle_att*50:
                if player.ch.equipment['Left hand'].weapon_type==player.ch.equipment['Right hand'].weapon_type:
                    player.ch.weapon_skill += 0.1*max([against/player.ch.weapon_skill,0.1])
                else:
                    player.ch.weapon_skills[player.ch.equipment['Left hand'].weapon_type.capitalize()] += 0.1*max([against/player.ch.weapon_skill,0.1])
    if attacker.tag == '@':
        player.ch.force_attack(defender)
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
            if 'invisible' in player.ch.effects:
                del(player.ch.effects['invisible'])
            bullet=player.ch.equipment['Ammunition'].duplicate(1)
            found=0
            for item in player.ch.inventory:
                if item.id==bullet.id and item.name==bullet.name:
                    found=1
                    item.lose_item(1)
            if not found:
                player.ch.equipment['Ammunition']=[]
                player.ch.weight-=bullet.weight
            shot_length=len(direct_path(player.ch.xy,player.ch.target))-1
            learn = random.uniform(0,100)
            if learn <= (player.ch.attr['Dex'] - player.ch.weapon_skill/5)/player.ch.attr['Dex']*100 and shot_length>=player.ch.attr['Dex']*3/4:
                player.ch.weapon_skill += 0.1*min([0.5,max([(shot_length*5)/player.ch.weapon_skill,0.1])])
        else:
            attacker.target=player.ch.xy[:]
            bullet=attacker.attr['shoot'].duplicate(1)
            shot_length=len(direct_path(attacker.xy,player.ch.xy))-1
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
            if T[init_screen.land[spot[1]-1][spot[0]-21]].id in "i:wWtL`S.gBaTdDFblOop,~'":
                for creature in player.all_beings:
                    if creature not in player.hidden and creature.xy==spot:
                        dodge_chance=creature.attr['Dex']*attack_path.index(spot)/2
                        if attacker.tag=='@' and creature.mode!='hostile':
                            dodge_chance-=20
                        if not clear_los(direct_path(attacker.xy,creature.xy)):
                            dodge_chance-=100
                            if (attacker.tag!='@' and 'elf3' in player.ch.tool_tags) or (attacker.tag=='@' and init_screen.current_place['Nature']>90):
                                dodge_chance+=80
                        if random.randint(1,100)>dodge_chance:
                            if attacker.tag=='@':
                                player.ch.force_attack(creature)
                                creature.mode='hostile'
                            add_dmg = 0
                            crit = random.randint(1,100)
                            if crit <= attacker.attr['Dex']:
                                add_dmg = attacker.attr['Dex']/10 + 1
                            if attacker.tag=='@':
                                if 'elf3' in player.ch.tool_tags and spot==attack_path[-1]:
                                    kill_chance=init_screen.current_place['Chaos']/4
                                    if init_screen.current_place['Nature']>=33 and init_screen.current_place['Temperature']>=33:
                                        kill_chance+=25
                                    if random.randint(1,100)<=kill_chance:
                                        add_dmg+=creature.life+5
                                        if kill_chance>12 and init_screen.current_place['Chaos']>0:
                                            init_screen.current_place['Chaos']-=1
                                            if init_screen.current_place['Nature']<100:
                                                init_screen.current_place['Nature']+=1
                                if add_dmg<creature.life+5:
                                    for each_other in player.all_creatures:
                                        if each_other.force==creature.force and (creature.t=='sentient' and each_other.t=='sentient') and not (creature.force=='Chaos' and player.ch.mode=='Chaos'):
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
                            if ((creature.tag=='@' and 'troll2' in player.ch.tool_tags) or (creature.tag!='@' and creature.race=='troll' and init_screen.current_place['Chaos']>=60)) and (player.ch.turn%2400>=1200):
                                resisted+=2
                            damage = random.randint(0,max([1,attacker.attr['Dex']/5]))+attacker.weapon_dmg+add_dmg+bullet.dmg-resisted
                            if damage < 1:
                                damage = 0
                            if attacker.tag=='@':
                                if add_dmg>=creature.life+5:
                                    message.creature('elf_kill',creature)
                                elif add_dmg:
                                    message.creature('crit',creature,damage)
                                else:
                                    message.creature('hit',creature,damage)
                            else:
                                if creature.tag=='@':
                                    message.creature('creature_hit',attacker,damage)
                                else:
                                    message.creature('creature_hits_creature',attacker,damage,creature)
                            creature.life -= damage
                            if attacker.tag=='@':
                                creature.attr['loot'].append([bullet.id,75,1,1])
                                if creature.life<=0:
                                    defender_dead(creature,add_dmg,attacker)
                            return 1
                        else:
                            if attacker.tag=='@':
                                message.creature('dodged',creature)
                            elif creature.tag=='@':
                                message.creature('creature_dodged',attacker)
                x=spot[0]
                y=spot[1]
                init_screen.c.scroll((x, y, x+1, y+1), 1, 1, bullet.color,bullet.tag)
                sleep(.04)
                if spot==attack_path[-1]:
                    init_screen.ground_items.append([attack_path[attack_path.index(spot)][0],attack_path[attack_path.index(spot)][1],bullet])
                    return 0
                else:
                    init_screen.c.scroll((x, y, x+1, y+1), 1, 1, T[init_screen.land[spot[1]-1][spot[0]-21]].colour,T[init_screen.land[spot[1]-1][spot[0]-21]].char)
                    for be in player.all_beings:
                        if be.xy==spot:
                            init_screen.draw_move(be,be.xy[0],be.xy[1])
                            break
                if T[init_screen.land[spot[1]-1][spot[0]-21]].id in 'TDFboO':
                    chance=random.randint(0,100)-(attacker.attr['Dex']-attack_path.index(spot))*10
                    if chance>shot_chance:
                        init_screen.ground_items.append([spot[0],spot[1],bullet])
                        return 0
            else:
                init_screen.ground_items.append([attack_path[attack_path.index(spot)-1][0],attack_path[attack_path.index(spot)-1][1],bullet])
                return 0

def defender_dead(defender,add_dmg,attacker):
    if attacker.tag=='@':
        if defender.race=='dwarf':
            player.effect('force',{'Chaos':{'troll':0.02}})
        elif defender.race=='troll':
            player.effect('force',{'Order':{'dwarf':0.02}})
        elif defender.race=='spirit of order':
            player.effect('force',{'Chaos':{'spirit of chaos':0.02}})
        elif defender.race=='spirit of chaos':
            player.effect('force',{'Order':{'spirit of order':0.02}})
        elif defender.race=='spirit of nature':
            player.effect('force',{'Chaos':{'goblin':0.02}})
        elif defender.race=='dryad':
            player.effect('force',{'Chaos':{'goblin':0.02}})
        elif defender.race=='fairy':
            player.effect('force',{'Chaos':{'goblin':0.02}})
        elif defender.race=='kraken':
            player.effect('force',{'Nature':{'water elemental':0.02}})
        elif defender.race=='water elemental':
            player.effect('force',{'Chaos':{'kraken':0.02}})
        init_screen.c.scroll((defender.xy[0], defender.xy[1], defender.xy[0]+1, defender.xy[1]+1), 1, 1,
                             T[init_screen.land[defender.xy[1]-1][defender.xy[0]-21]].colour,
                             T[init_screen.land[defender.xy[1]-1][defender.xy[0]-21]].char)
        if add_dmg:
            message.creature('crit_kill',defender)
        else:
            message.creature('kill',defender)
    else:
        message.creatures('kill',attacker,defender)
    found_item=put_item(defender.attr['loot'],defender.xy)
    if found_item:
        init_screen.draw_items()
    player.all_creatures.remove(defender)
    player.all_beings.remove(defender)
    if defender in player.ch.followers:
        player.ch.followers.remove(defender)
    del(defender)


def combat(attacker,defender,second_swing=0):
    if attacker.tag=='@' or defender.tag=='@':
        if 'invisible' in player.ch.effects:
            del(player.ch.effects['invisible'])
        if player.ch.possessed and 'spirit of nature3' in player.ch.tool_tags:
            if player.ch.equipment['Right hand'] and player.ch.possessed[0].name in player.ch.equipment['Right hand'].effect:
                player.ch.equipment['Right hand'].effect[player.ch.possessed[0].name]\
                                           =min([66,player.ch.equipment['Right hand'].effect[player.ch.possessed[0].name]+0.1])
            elif player.ch.equipment['Left hand'] and player.ch.possessed[0].name in player.ch.equipment['Left hand'].effect:
                player.ch.equipment['Left hand'].effect[player.ch.possessed[0].name]\
                                           =min([66,player.ch.equipment['Left hand'].effect[player.ch.possessed[0].name]+0.1])
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
	    if ((defender.tag=='@' and 'troll2' in player.ch.tool_tags) or (defender.tag!='@' and defender.race=='troll' and init_screen.current_place['Chaos']>=60)) and (player.ch.turn%2400>=1200):
                resisted+=2
            damage = random.randint(1,attacker.dmg) + attacker.weapon_dmg + add_dmg - resisted
            if damage < 1:
                damage = 0
            if attacker.tag == '@':
                if 'kraken2' in attacker.tool_tags and \
                       T[init_screen.land[attacker.xy[1]-1][attacker.xy[0]-21]].id in "wWt" and \
                       T[init_screen.land[defender.xy[1]-1][defender.xy[0]-21]].id in "wWt" and \
                       player.ch.turn%2400>1200:
                    damage += defender.life+5
                    message.creature('kraken_death',defender)
                elif add_dmg:
                    message.creature('crit',defender,damage)
                else:
                    message.creature('hit',defender,damage)
            elif defender.tag == '@':
                message.creature('creature_hit',attacker,damage)
                if 'fairyland' in player.ch.effects:
                    fairy_magick=set(['fairyland','summerwalk','winterwalk','midnight fears','sun armour','invisible'])
                    fairy_dmg=1+len(fairy_magick&set(player.ch.effects.keys()))
                    attacker.life-=fairy_dmg
                    message.creature('fairyland_hit',attacker,fairy_dmg)
                    if attacker.life<1:
                        defender_dead(attacker,0,defender)
            else:
                message.creatures('good_attack',attacker,defender,damage)
            defender.life -= damage
        else:
            if attacker.tag == '@':
                message.creature('miss',defender)
            elif defender.tag == '@':
                message.creature('creature_miss',attacker)
            else:
                message.creatures('miss_attack',attacker,defender)
        attacker.energy -= 20
        if defender.life <= 0:
            if defender.tag =='@':
                pass
            else:
                defender_dead(defender,add_dmg,attacker)
        if attacker.tag == '@' and not second_swing and defender.life > 0:
            if attacker.equiped_weaps == 2:
                combat(attacker,defender,1)

def creature_passage(ch, x, y):
    ## Check if creature is in its allowed area
    if (ch.area != []):
        if (ch.xy[0] < ch.area[0]) or (ch.xy[0] > ch.area[2]) or (ch.xy[1] < ch.area[1]) or (ch.xy[1] > ch.area[3]):
            ch.xy[0] = x
            ch.xy[1] = y
            return 1
    ## Check if creature has moved beyond the screen boundaries
    if (ch.xy[0] == 20) or (ch.xy[0] == 79) or (ch.xy[1] == 0) or (ch.xy[1] == 24):
        ch.xy[0] = x
        ch.xy[1] = y
        return 1
    elif T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id in ch.terr_restr and not ch.mode=='standing_hostile':
        ch.xy[0] = x
        ch.xy[1] = y
        return 1
    elif T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].pass_through or (ch.race=='spirit of order' and init_screen.current_place['Order']>30 and T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id in '#o+`sS') or (ch.race=='spirit of chaos' and init_screen.current_place['Chaos']>30 and T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id in '#o+`sS') or (ch.race=='gnome' and init_screen.current_place['Nature']>30 and T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id in 'nmA%'):
        for a in player.all_beings:
            if a.xy == ch.xy and a.game_id != ch.game_id:
                ch.xy[0] = x
                ch.xy[1] = y
                if (ch.mode=='guarding' and a.mode=='hostile') or (a.mode=='guarding' and ch.mode=='hostile') or (a.xy == player.ch.xy and ch.mode in ['hostile','standing_hostile'] and 'waterform' not in player.ch.effects):
                    combat(ch,a)
		return 1
        if T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].tire_move>ch.energy:
            if T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].drowning and ch.race!='fish':
                ch.life -= 1
            ch.xy[0] = x
            ch.xy[1] = y
        elif not (ch.race=='kraken' and init_screen.current_place['Chaos']>30 and T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id in 'wWt~')\
             and not (ch.race=='fairy' and init_screen.current_place['Nature']>60 and T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id in "'i,")\
             and not (ch.race=='fish' and T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id in "Wwt~"):
            ch.energy-=T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].tire_move
        if ch.mode=='standing_hostile':
            ch.xy[0] = x
            ch.xy[1] = y
    elif 'door_' in T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].world_name:
        init_screen.creature_open_door(ch.xy, init_screen.land[ch.xy[1]-1][ch.xy[0]-21])
        ch.xy[0] = x
        ch.xy[1] = y
    else:
          ch.xy[0] = x
          ch.xy[1] = y
##  elif T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].degradable:
##        d = init_screen.degrade_terr(init_screen.land[ch.xy[1]-1][ch.xy[0]-21], ch.xy)
##        if d == 1:
##            ch.xy[0] = x
##            ch.xy[1] = y
##        elif d == -1:
##            message.emotion('tired')
##            ch.xy[0] = x
##            ch.xy[1] = y
##        else:
##            message.message('no_tool')
##            ch.xy[0] = x
##            ch.xy[1] = y
##            

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
    creature_sight=direct_path(ch.xy, player.ch.xy)
    creature_los = clear_los(creature_sight)
    player_los = clear_los(direct_path(player.ch.xy,ch.xy))
    if ch.t=='sentient':
        if float(ch.fear)/(ch.fear+(ch.attr['Int']+ch.attr['Mnd'])*10)>random.random():
            mode='fearfull'
    if ch.race=='troll' and init_screen.current_place['Chaos']>=60 and player.ch.turn%2 and player.ch.turn%2400<1200:
        ch.path=[]
        mode='wander'
    if mode in ['follow','hostile','fearfull_hide','fearfull'] and ('invisible' in player.ch.effects or not creature_los):
        mode = 'wander'
    if mode in ['hostile','fearfull_hide','fearfull'] and 'elf1' in player.ch.tool_tags and ch.t=='animal':
        mode = 'wander'
    if mode in ['hostile','standing_hostile','fearfull_hide','fearfull'] and 'stealthy' in player.ch.tool_tags and creature_los:
        hide_chance=player.ch.attr['Dex']*3+player.ch.attr['Int']-ch.attr['Int']+len(creature_sight)
        if random.randint(1,100)<hide_chance:
            if mode=='standing_hostile':
                mode='standing'
            else:
                mode='wander'
    if 'ork1' in player.ch.tool_tags and ch.mode=='hostile' and creature_los:
        if 'human3' in player.ch.tool_tags:
            if random.random()<player.ch.research_races['Chaos']['ork']/(2*(max([init_screen.current_place['Order'],init_screen.current_place['Nature']])+player.ch.research_races['Chaos']['ork'])):
                mode='fearfull'
        else:
            if random.random()<player.ch.races['Chaos']['ork']/(2*(max([init_screen.current_place['Order'],init_screen.current_place['Nature']])+player.ch.races['Chaos']['ork'])):
                mode='fearfull'
    ## wander, follow, hostile, fearfull_hide, standing_hostile, standing, guarding, fearfull
    if mode == 'guarding':
        fighting=0
        if 'target' in ch.attr and ch.attr['target']!=[] and ch.attr['target'] in player.all_creatures:
            if len(direct_path(ch.attr['target'].xy,player.ch.xy))<5:
                fighting=1
                ch.path=direct_path(ch.xy,ch.attr['target'].xy)
            else:
                ch.attr['target']=[]
        if not fighting:
            for enemy in player.all_creatures:
                if enemy.mode=='hostile' and len(direct_path(enemy.xy,player.ch.xy))<3 and clear_los(direct_path(ch.xy,enemy.xy)):
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
            if ch.race=='troll' and init_screen.current_place['Chaos']>=60 and player.ch.turn%2 and player.ch.turn%2400<1200: 
                key='5'
            else:
                key = str(random.randint(1,9))
    if mode == 'follow' or mode == 'hostile' or mode=='standing_hostile' or mode=='guarding':
        if mode != 'guarding':
            ch.path = direct_path(ch.xy, player.ch.xy)
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
        ch.xy[0] -= cmp(player.ch.xy[0],x)
        ch.xy[1] -= cmp(player.ch.xy[1],y)
        key='0'
    if mode == 'fearfull_hide':
        if (abs(player.ch.xy[0]-x) + abs(player.ch.xy[1]-y)) < 7:
            ch.xy[0] += cmp(ch.area[4],x)
            ch.xy[1] += cmp(ch.area[5],y)
            if ((cmp(ch.area[4],x) == 0) and (cmp(ch.area[5],y) == 0)) and (ch not in player.hidden):
                player.hidden.append(ch)
            key = '0'
        else:
            key = str(random.randint(1,9))
        if (ch in player.hidden) and ([x,y] != ch.area[4:]):
            player.hidden.remove(ch)
    if mode == 'standing':
        key='5'
    for a in range(2):            
        ch.xy[a] = ch.xy[a] + md[key][a]
    creature_passage(ch, x, y)
    if (ch in player.hidden):
        if (player.ch.xy != ch.xy):
            init_screen.hide(ch)
    else:
        if player_los or (init_screen.current_place['Nature']>=33 and init_screen.current_place['Temperature']>=33 and 'elf2' in player.ch.tool_tags):
            init_screen.draw_move(ch, x, y)
        if ch.race=='water elemental' and T[init_screen.land[ch.xy[1]-1][ch.xy[0]-21]].id in 'wWt':
            ch.attr['invisible']=2
        if 'invisible' in ch.attr:
            init_screen.hide(ch)
            ch.attr['invisible']-=1
            if ch.attr['invisible']==0:
                del(ch.attr['invisible'])

def clear_path(thing,a,b):
    xy = a[:]
    no_pass = 0
    for creature in player.all_beings:
        if creature.xy == xy and creature.game_id != thing.game_id:
            no_pass = 1
            break
    if not T[init_screen.land[xy[1]-1][xy[0]-21]].pass_through or no_pass or T[init_screen.land[xy[1]-1][xy[0]-21]].id in thing.terr_restr:
        return 0
    while xy != b:
        xy[0] += cmp(b[0],xy[0])
        xy[1] += cmp(b[1],xy[1])
        no_pass = 0
        for creature in player.all_beings:
            if creature.xy == xy and creature.game_id != thing.game_id:
                no_pass = 1
                break
        if not T[init_screen.land[xy[1]-1][xy[0]-21]].pass_through or no_pass or T[init_screen.land[xy[1]-1][xy[0]-21]].id in thing.terr_restr:
            return 0
    return 1

def good_path(thing,path):
##    broken = 0
##    for step_index in range(len(path)-1):
##        if abs(path[step_index][0] - path[step_index+1][0]) > 1 or abs(path[step_index][1] - path[step_index+1][1]) > 1:
##            broken = 1
    for xy in path[:len(path)-1]:
        no_pass = 0
        for creature in player.all_beings:
            if creature.xy == xy and creature.game_id != thing.game_id:
                no_pass = 1
                break
        if (not T[init_screen.land[xy[1]-1][xy[0]-21]].pass_through or no_pass or T[init_screen.land[xy[1]-1][xy[0]-21]].id in thing.terr_restr) and not (thing.race=='spirit of order' and init_screen.current_place['Order']>30 and T[init_screen.land[xy[1]-1][xy[0]-21]].id in '#o+`sS') and not (thing.race=='spirit of chaos' and init_screen.current_place['Chaos']>30 and T[init_screen.land[xy[1]-1][xy[0]-21]].id in '#o+`sS') and not (thing.race=='gnome' and init_screen.current_place['Nature']>30 and T[init_screen.land[xy[1]-1][xy[0]-21]].id in 'nmA%'):
            return 0
    return 1

def clear_los(path):
    if len(path)>2:
        for xy in path[1:-1]:
            if not T[init_screen.land[xy[1]-1][xy[0]-21]].clear_los:
                return 0
    if not T[init_screen.land[path[-1][1]-1][path[-1][0]-21]].pass_through:
        return 0
    return 1

def good_place(thing,place):
    no_pass = 0
    for creature in player.all_creatures:
        if creature.xy == place and not (creature.mode=='hostile' and thing.mode=='guarding') and not (thing.mode=='hostile' and creature.mode=='guarding'):
            no_pass = 1
            break
    if (not T[init_screen.land[place[1]-1][place[0]-21]].pass_through or no_pass or (T[init_screen.land[place[1]-1][place[0]-21]].id in thing.terr_restr and thing.mode!='standing_hostile')) and not (thing.race=='spirit of order' and init_screen.current_place['Order']>30 and T[init_screen.land[place[1]-1][place[0]-21]].id in '#o+s') and not (thing.race=='spirit of chaos' and init_screen.current_place['Chaos']>30 and T[init_screen.land[place[1]-1][place[0]-21]].id in '#o+s') and not (thing.race=='gnome' and init_screen.current_place['Nature']>30 and T[init_screen.land[place[1]-1][place[0]-21]].id in 'nmA%') and not ('door_' in T[init_screen.land[place[1]-1][place[0]-21]].world_name and thing.t=='sentient'):
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
    
def highlight_path(way):
    if way != []:
        for step in way[1:]:
            x = step[0]
            y = step[1]
            if way.index(step)<=player.ch.attr['Dex']:
                init_screen.c.scroll((x, y, x+1, y+1), 1, 1, 14,'*')
            else:
                init_screen.c.scroll((x, y, x+1, y+1), 1, 1, 4,'*')
