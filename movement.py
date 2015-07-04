from terrain import T
import player
import init_screen
import random
import message
import msvcrt
from inventory import put_item
from time import sleep

def attack(attacker,defender):
    for pc,other in [(defender,attacker),(attacker,defender)]:
        ## Uchi se orujieto ako umenieto e pod 100. Pri Atribut = 20 shansa da se vdigne poveche ot 100 e 0.
        ## Pri Atribut = 1 max-skill=5 => po 5 tochki na tochka Atribut
        ## Ako se bie s dve orujiq tova v lqvata ruka se uchi dva puti po-bavno
        if pc.tag=='@':
            learn = random.uniform(0,100)
            if learn <= (pc.battle_att - pc.weapon_skill/5)/pc.battle_att*100:
                pc.weapon_skill += 0.1*max([float(other.weapon_skill)/pc.weapon_skill,0.1])
            if pc.equiped_weaps == 2:
                learn = random.uniform(1,100)
                if learn <= (pc.battle_att - pc.weapon_skill/5)/pc.battle_att*50:
                    if pc.equipment['Left hand'].weapon_type==pc.equipment['Right hand'].weapon_type:
                        pc.weapon_skill += 0.1*max([float(other.weapon_skill)/pc.weapon_skill,0.1])
                    else:
                        pc.weapon_skills[pc.equipment['Left hand'].weapon_type.capitalize()] += 0.1*max([float(other.weapon_skill)/pc.weapon_skill,0.1])
    if attacker.tag == '@':
        if (attacker.equipment['Right hand'] and 'ranged' in attacker.equipment['Right hand'].type) or (attacker.equipment['Left hand'] and 'ranged' in attacker.equipment['Left hand'].type):
            message.message('cant_hit_with_bow')
            return 0
        attacker.force_attack(defender)
        if attacker.equiped_weaps == 2:
        ##  Ako se bie s dve orujiq e po vajna Dex, obshtiq sbor e maksimum 90
            att = attacker.attr[attacker.att_att]/2.0 + (attacker.attr[attacker.att_att]/25.0)*attacker.weapon_skill*attacker.armour_mod + random.randint(-5,5)
        else:
        ##  Ako se bie s edno orujie obshtiq sbor e maksimum 120
            att = float(attacker.attr[attacker.att_att]) + attacker.weapon_skill*attacker.armour_mod + random.randint(-5,5)
    else:
        att = float(max(attacker.attr['Dex'],attacker.attr['Str'])) + attacker.weapon_skill + random.randint(-5,5)
    if defender.tag == '@':
        defence = float(defender.attr[defender.def_att]) + defender.weapon_skill*defender.armour_mod + random.randint(-5,5)
    else:
        defence = float(max(defender.attr['Dex'],defender.attr['Str'])) + defender.weapon_skill + random.randint(-5,5)
    if att < 0:
        defence -= att
        att = 1
    if defence < 0:
        att -= defence
        defence = 1
    return att/(att+defence)*100 > random.uniform(0,100)

## NPCS only shoot at the player for now!!!
def shoot(attacker):
    if attacker.energy > 50:
        attacker.energy-=10
        if attacker.tag=='@':
            if 'invisible' in attacker.effects:
                del(attacker.effects['invisible'])
            bullet=attacker.equipment['Ammunition'].duplicate(1)
            found=0
            for item in attacker.inventory:
                if item.id==bullet.id and item.name==bullet.name:
                    found=1
                    item.lose_item(1)
            if not found:
                attacker.equipment['Ammunition']=[]
                attacker.weight-=bullet.weight
            shot_length=len(init_screen.direct_path(attacker.xy,attacker.target))-1
            learn = random.uniform(0,100)
            if learn <= (attacker.attr['Dex'] - attacker.weapon_skill/5)/attacker.attr['Dex']*100 and shot_length>=attacker.attr['Dex']*3/4:
                attacker.weapon_skill += 0.1*min([0.5,max([(shot_length*5)/attacker.weapon_skill,0.1])])
        else:
            attacker.target=player.ch.xy[:]
            bullet=attacker.attr['shoot'].duplicate(1)
            shot_length=len(init_screen.direct_path(attacker.xy,player.ch.xy))-1
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
        attack_path=init_screen.direct_path(attacker.xy,fall_spot)[1:]
        for spot in attack_path:
            if T[init_screen.land[spot[1]-1][spot[0]-21]].pass_through: #id in "i:wWtL`S.gBaTdDFblOop,~'":
                for creature in player.all_beings:
                    if creature not in player.hidden and creature.xy==spot:
                        dodge_chance=creature.attr['Dex']*attack_path.index(spot)/2
                        if attacker.tag=='@' and creature.mode!='hostile':
                            dodge_chance-=20
                        if not init_screen.clear_los(init_screen.direct_path(attacker.xy,creature.xy)):
                            dodge_chance-=100
                            if (creature.tag=='@' and 'elf3' in creature.tool_tags) or (creature.tag!='@' and creature.race=='elf' and init_screen.current_place['Nature']>90):
                                dodge_chance+=80
                        if random.randint(1,100)>dodge_chance:
                            add_dmg = 0
                            crit = random.randint(1,100)
                            if crit <= attacker.attr['Dex']:
                                add_dmg = attacker.attr['Dex']/10 + 1
                            if attacker.tag=='@':
                                attacker.force_attack(creature)
                                if creature.tag!='@':
                                    creature.mode='hostile'
                                if 'elf3' in attacker.tool_tags and spot==attack_path[-1]:
                                    kill_chance=init_screen.current_place['Chaos']/4
                                    if init_screen.current_place['Nature']>=33 and init_screen.current_place['Temperature']>=33:
                                        kill_chance+=25
                                    if random.randint(1,100)<=kill_chance:
                                        add_dmg+=creature.life+5
                                        if kill_chance>12 and init_screen.current_place['Chaos']>0:
                                            player.effect('force',{'Nature':{'terrain':1}})
                                if add_dmg<creature.life+5:
                                    for each_other in player.all_creatures:
                                        if each_other.force==creature.force and (creature.t=='sentient' and each_other.t=='sentient') and not (creature.force=='Chaos' and attacker.mode=='Chaos'):
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
                            if ((creature.tag=='@' and 'troll2' in creature.tool_tags) or (creature.tag!='@' and creature.race=='troll' and init_screen.current_place['Chaos']>=60)) and (player.ch.turn%2400>=1200):
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

## Player.turn dependence need to be removed
def combat(attacker,defender,second_swing=0):
    for combatant in [attacker,defender]:
        if combatant.tag=='@':
            if 'invisible' in combatant.effects:
                del(combatant.effects['invisible'])
            if combatant.possessed and 'spirit of nature3' in combatant.tool_tags:
                if combatant.equipment['Right hand'] and combatant.possessed[0].name in combatant.equipment['Right hand'].effect:
                    combatant.equipment['Right hand'].effect[combatant.possessed[0].name]\
                                               =min([66,combatant.equipment['Right hand'].effect[combatant.possessed[0].name]+0.1])
                elif combatant.equipment['Left hand'] and combatant.possessed[0].name in combatant.equipment['Left hand'].effect:
                    combatant.equipment['Left hand'].effect[combatant.possessed[0].name]\
                                               =min([66,combatant.equipment['Left hand'].effect[combatant.possessed[0].name]+0.1])
    if attacker.energy > 50:
        if attack(attacker, defender):
            add_dmg = 0
            crit = random.randint(1,100)
            if crit <= attacker.attr['Dex']:
                add_dmg = attacker.attr['Dex']/10 + 1
                
            chance = random.uniform(1,500)
            ## Resisted damage categories based on armour. If armour >=500 there's always a resisted amount
            cats = {5:[1,11],4:[11,26],3:[26,46],2:[46,71],1:[71,101]}
            resisted = 0
            if chance < defender.armour: 
                cat = int(100*chance/defender.armour)
                cat = max([cat, 1])
                for x in cats:
                    if cat in range(*cats[x]):
                        resisted = x
                        break
	    if ((defender.tag=='@' and 'troll2' in defender.tool_tags) or (defender.tag!='@' and defender.race=='troll' and init_screen.current_place['Chaos']>=60)) and player.ch.turn%2400>=1200:
                resisted+=2
            damage = random.randint(1,attacker.dmg) + attacker.weapon_dmg + add_dmg - resisted
            if damage < 1:
                damage = 0
            if attacker.tag == '@':
                if 'kraken2' in attacker.tool_tags and \
                       T[init_screen.land[attacker.xy[1]-1][attacker.xy[0]-21]].id in "wWt" and \
                       T[init_screen.land[defender.xy[1]-1][defender.xy[0]-21]].id in "wWt" and \
                       attacker.turn%2400>1200:
                    damage += defender.life+5
                    message.creature('kraken_death',defender)
                elif add_dmg:
                    message.creature('crit',defender,damage)
                else:
                    message.creature('hit',defender,damage)
            elif defender.tag == '@':
                message.creature('creature_hit',attacker,damage)
                if 'fairyland' in defender.effects:
                    fairy_magick=set(['fairyland','summerwalk','winterwalk','midnight fears','sun armour','invisible'])
                    fairy_dmg=1+len(fairy_magick&set(defender.effects.keys()))
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
