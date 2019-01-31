import msvcrt

class Message_system:
    def __init__(self,game):
        self.game=game

    def message(self,x):
        md = {'wall':'You hit a wall!', '?':'What?', 'wait':'You wait.', 'tree':'You walk under a tree.',
              'rock':'You can\'t go through rocks!', 'break_rock':'You smash the rock to pieces!', 'q':'Save the game? (y/n)',
              'ch':'  CHECK!', 'break_wall':'You break down the wall!', 'cut_tree':'You cut the tree down.',
              'log':'A tree log lays here.', 'what_to_drop':' Which item do you want to drop?',
              'water':'You splash into the water.', 'magic_water':'You step into the sparkling water.',
              'no_drink':'There\'s nothing here to drink!','no_pickup':'There\'s nothing here to pick up!',
              'work':'What do you want to interact with?(direction)','direction':'That is not a direction!',
              'how_much':' How much do you want to drop?','pickup':' How much do you want to take?',
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
        self.game.c.pos(0,0)
        try:
            if x not in ['work','no_fill','which_open','how_much','q','pickup','look','ran_away','need_human1&dwarf1','need_dryad3',
                         'no_riding_fighting','save_failed','break_rock','found_gem','found_metal','failed_smelt','clear_build_site',
                         'cant_fit_container','?','dryad_song','need_human3','not_when_possessed','no_gather','failed_gather',
                         'what_to_drop']:
                self.game.combat_buffer+=' '+md[x]
            else:
                self.game.c.write(md[x])
        except:
            self.game.c.rectangle((0,0,80,1))

    def tool_msg(self,x,t):
        md={'no_tool':'You don\'t have the appropriate tool! (%s)',}
        self.game.c.pos(0,0)
        try:
            self.game.c.write(md[x] %(', '.join(t)))
        except:
            self.game.c.rectangle((0,0,80,1))

    def emotion(self,x,t=0):
        md = {'tired':'You are too tired!', 'not_tired':'You are no longer tired.',
              'exhausted':'You are too exhausted to work, you need sustenance!',
              'not_tough':'You are not tough enough to work effectively, increase your endurance!',
              'hostiles':"You can't focus on this, you are under attack!",
              'gain_waterform':'You drain in the ground! You have %d turns to find magic water to reform!'}
        self.game.c.pos(0,0)
        try:
            if x=='gain_waterform':
                print(md[x] %(t))
            else:
                print(md[x])
        except:
            self.game.c.rectangle((0,0,80,1))

    def creature(self,x, a, dmg=0,d=''):
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
        self.game.c.pos(0,0)
        try:
            if x == 'hit' or x == 'crit' or x == 'creature_hit' or x == 'spell_damage' or x=='fairyland_hit':
                mess = md[x] %(a.race,dmg)
                self.game.combat_buffer += mess+' '
            elif  x == 'kill' or x == 'elf_kill' or x == 'crit_kill' or x == 'miss' or x == 'creature_miss':
                mess = md[x] %(a.race)
                self.game.combat_buffer += mess+' '
            elif x == 'no_escape':
                self.game.combat_buffer += md[x]
            elif x == 'creature_hits_creature':
                self.game.combat_buffer += md[x] %(a.race,d.name,dmg)
            elif x in ['talk','attack','tame','tamed_use','command_follow','command_stay','command_guard','steal','possess']:
                print(md[x] %(a.race))
            elif x == 'sapphired':
                if a.life<1:
                    self.game.combat_buffer += 'The %s falls frozen to the ground!' %(a.race)+' '
                elif a.life/5>2:
                    self.game.combat_buffer += 'The %s shrugs off the cold wave.' %(a.race)+' '
                else:
                    self.game.combat_buffer += md[x][int(a.life/5)] %(a.race)+' '
            elif x == 'rubied':
                if a.life<1:
                    self.game.combat_buffer += 'The %s falls to the ground charred!' %(a.race)+' '
                elif a.life/5>2:
                    self.game.combat_buffer += 'The %s grunts as the heat washes over it.' %(a.race)+' '
                else:
                    self.game.combat_buffer += md[x][int(a.life/5)] %(a.race)+' '
            else:
                self.game.combat_buffer += md[x] %a.name
        except:
            self.game.c.rectangle((0,0,80,1))

    def creatures(self,x, a, b, dmg=0):
        md = {'miss_attack':'The %s jumps at the %s and misses!','good_attack':'The %s hits the %s for %d!',
              'kill':'The %s finishes the %s off!'}
        self.game.c.pos(0,0)
        try:
            if x=='miss_attack' or x=='kill':
                self.game.combat_buffer += md[x] %(a.race, b.race)
            else:
                self.game.combat_buffer += md[x] %(a.race, b.race, dmg)
        except:
            self.game.c.rectangle((0,0,80,1))

    def use(self,x, a, qty=1, xy=[]):
        md = {'drink':'You drink from the %s.','over_drink':'You can\'t drink the %s, you are full!',
              'over_eat':'You can\'t eat the %s, you are full!','cant_carry':'You can\'t carry the %s, it\'s too heavy!',
              'gr_item':'There is %s here.','pickup':'You take the %s.','create_drop':'You can\'t carry the %s and drop it.',
              'cant_fit_in_backpack':'There is no place in your backpack for the %s!','no_lockpick':"The %s is locked and you don't have a lockpick.",
              'taming_item':'You need some %ss to try and tame that animal.','feed_item':'You need some %ss to feed that animal.',
              'farm_harvest':'You get some %s.','needed_container':'You need a %s to do that!','craft_item':'You craft a %s.',
              'pickup_melt':'The %s melts as you pick it up!','pickup_dry':'The %s withers as you pick it up!'}
        self.game.c.pos(0,0)
        try:
            if x == 'gr_item':
                items = []
                for item in self.game.ground_items:
                    if item[:2] == xy:
                        items.append(item[2:])
                if len(items) > 1:
                    print('You see several items on the ground.')
                else:
                    self.message('')
                    if qty == 1 and a.name[0].lower() in 'aieo':
                        print(md[x] %('an ' + a.name))
                    elif qty == 1 and a.name[0].lower() not in 'aieo':
                        print(md[x] %('a ' + a.name))
                    else:
                        print(md[x] %(a.name+'('+str(qty)+')'))
            elif x == 'craft_item':
                self.game.combat_buffer += md[x] %(a.name)
            else:
                print(md[x] %a.name)
        except:
            self.game.c.rectangle((0,0,80,1))

    def look(self,xy,T):
        try:
            added_thing=''
            if self.game.current_area == 'world':
                things = 'You see: ' + T[self.game.land[xy[1]-1][xy[0]-21]].world_name + '.'
                for place in self.game.world_places:
                    if self.game.world_places[place] == xy and place in self.game.player.known_areas:
                        things = 'You see: ' + self.game.top_world_places[str(xy)]
            else:
                things = 'You see: ' + T[self.game.land[xy[1]-1][xy[0]-21]].name + '.'
                for one in self.game.all_beings:
                    if one.xy == xy:
                        if one in self.game.player.followers:
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
                                things += ' An %s stands here.%s' %(one.race,added_thing)
                                break
                            else:
                                things += ' A %s stands here.%s' %(one.race,added_thing)
                                break
                for piece in self.game.ground_items:
                    if piece[:2] == xy:
                        things += ' There are items here.'
                        break

            self.game.c.text(0,0,things,7)
        except:
            self.game.c.rectangle((0,0,80,1))

    def choice(self,x):
        md = {'leave_area':'Do you wish to leave this area? (y/n)'}
        self.game.c.pos(0,0)
        try:
            print(md[x])
            answer = msvcrt.getch()
            if answer == 'y' or answer == 'Y':
                return 1
            else:
                self.game.c.rectangle((0,0,80,1))
                return 0
        except:
            self.game.c.rectangle((0,0,80,1))
            return 0

    def combat_buffer(self):
        if self.game.combat_buffer:
            self.game.c.rectangle((0,0,80,1))
            self.game.combat_buffer = self.game.combat_buffer.strip()
            while self.game.combat_buffer:
                pause = 0
                if len(self.game.combat_buffer) > 79:
                    pause = 1
                self.game.c.text(0,0,self.game.combat_buffer[:79],7)
                self.game.combat_buffer = self.game.combat_buffer[79:]
                if pause:
                    msvcrt.getch()
                    self.game.c.rectangle((0,0,80,1))
