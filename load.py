import msvcrt
import init_screen
import terrain
import player
import pickle
import inventory
import random
from os import curdir

map_size=10
T_matrix = []
force_terrains={'Nature':[["'","'",'.','g','l'],['g','g','b','g','T','n'],[',','b','g','g','g','T','J']],
                 'Chaos':[['i','.','I','F','%'],['.','d','d','D','%','B'],[',',',','.','L','B','%']],
                 'Order':[["'","'",'.','g','%'],['.','g',':','g','%','g'],[',',',',':','g','%']]}

## Load-va savenat fail
def load_terr(f):
    try:
        terr = open(f, 'r')
    except:
        print 'No such file!'
        terr = msvcrt.getch()
        return 0,0
    init_screen.c.page()
    init_screen.land = []
    for i in range(23):
        init_screen.land.append(terr.read(58))
        terr.read(1)
    for x in range(1,24):
        init_screen.c.pos(21, x)
        for y in range(21,79):
            init_screen.c.scroll((y,x,y+1,x+1), 1, 1, terrain.T[init_screen.land[x-1][y-21]].colour, terrain.T[init_screen.land[x-1][y-21]].char)
    player.ch = pickle.load(terr)
    player.ch.inventory = pickle.load(terr)
    player.ch.equipment = pickle.load(terr)
    player.ch.skills = pickle.load(terr)
    player.ch.spells = pickle.load(terr)
    player.ch.forces = pickle.load(terr)
    player.ch.races = pickle.load(terr)
    player.ch.effects = pickle.load(terr)
    player.ch.land_effects = pickle.load(terr)
    player.ch.known_areas = pickle.load(terr)
    player.ch.weapon_skills = pickle.load(terr)
    player.ch.attr_colors = pickle.load(terr)
    player.all_creatures = pickle.load(terr)
    max_id=0
    creature_coords=[]
    for c in player.all_creatures:
        max_id=max([max_id,c.game_id])
        creature_coords.append(c.xy)
    for fol in player.ch.followers+player.ch.ride+player.ch.possessed:
        if fol.mode!='standing':
            player.all_beings.append(fol)
            player.all_creatures.append(fol)
            fol.game_id=max_id+1
            max_id+=1
        if fol.mode=='standing' and fol.attr['area']==area:
            player.all_beings.append(fol)
            player.all_creatures.append(fol)
            fol.game_id=max_id+1
            max_id+=1
    player.hidden = pickle.load(terr)
    for one in player.hidden:
        for two in player.all_creatures:
            if one.game_id == two.game_id:
                player.all_creatures.remove(two)
                player.all_creatures.append(one)
                break
    player.all_beings = player.all_creatures + [player.ch]
    init_screen.ground_items = pickle.load(terr)
    init_screen.directions = pickle.load(terr)
    init_screen.world_places = pickle.load(terr)
    init_screen.top_world_places = pickle.load(terr)
    init_screen.place_descriptions = pickle.load(terr)
    init_screen.map_coords = pickle.load(terr)
    init_screen.current_area = pickle.load(terr)
    init_screen.current_place = pickle.load(terr)
    init_screen.treasure_modifier = pickle.load(terr)
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
    init_screen.current_place=T_matrix[starting_point[0]][starting_point[1]]
    unknown_terrain(starting_point,direction)

    init_screen.place_descriptions = {'world':'Your country.'}
    area_number=starting_point[0]*map_size+starting_point[1]
    init_screen.place_descriptions['area%s' %(area_number)] = 'A place of %s.' %(start_force)
    init_screen.world_places = {'world':[0,0]}
    init_screen.top_world_places = {}
    return 1

def unknown_terrain(coords,direction):
    init_screen.c.page()
    init_screen.land = []
    init_screen.directions = []
    area_number=coords[0]*map_size+coords[1]
    init_screen.current_area = 'area%s' %(area_number)
    init_screen.treasure_modifier = T_matrix[coords[0]][coords[1]]['Treasure']
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
    init_screen.directions = [max([0,area_number-map_size]),down_dir,left_dir,right_dir,0,0]
    for x in range(len(init_screen.directions)):
        init_screen.directions[x]=str(init_screen.directions[x])
    init_screen.land=generate_terr(coords)
    for x in range(1,24):
        for y in range(21,79):
            init_screen.c.scroll((y,x,y+1,x+1), 1, 1, terrain.T[init_screen.land[x-1][y-21]].colour, terrain.T[init_screen.land[x-1][y-21]].char)
    init_screen.map_coords = '47 22;47 2;77 12;22 12;0 0;0 0'
    new_coords = init_screen.map_coords.split(';')
    for i in range(6):
        new_coords[i] = new_coords[i].split(' ')
    spot=[int(new_coords[direction][0]),int(new_coords[direction][1])]
    while not terrain.T[init_screen.land[spot[1]-1][spot[0]-21]].pass_through:
        if direction==0:
            spot[1]-=1
        elif direction==1:
            spot[1]+=1
        elif direction==2:
            spot[0]-=1
        elif direction==3:
            spot[1]+=1
    for i in range(2):
        player.ch.xy[i] = spot[i]
        
def unknown_Bterrain(coords,direction):
    ## The direction sets the spot in which the character appears, according to his race
    init_screen.current_place={'Nature':33,'Chaos':33,'Order':33,'Population':0,'Treasure':50,'Temperature':0,'Water':10,
                               'Nspirit':0,'Ospirit':0,'Cspirit':0,'Npop':0,'Opop':0,'Cpop':0}
    for x in range(map_size):
        for y in range(map_size):
            init_screen.current_place['Nature']=max([T_matrix[x][y]['Nature'],init_screen.current_place['Nature']])
            init_screen.current_place['Order']=max([T_matrix[x][y]['Order'],init_screen.current_place['Order']])
            init_screen.current_place['Chaos']=max([T_matrix[x][y]['Chaos'],init_screen.current_place['Chaos']])
            if not T_matrix[x][y]['Nature']==T_matrix[x][y]['Order']==T_matrix[x][y]['Chaos']:
                predominant_f={T_matrix[x][y]['Nature']:'Nature',T_matrix[x][y]['Order']:'Order',
                               T_matrix[x][y]['Chaos']:'Chaos'}
                if predominant_f.keys().count(max(predominant_f.keys()))==1:
                    the_force=predominant_f[max(predominant_f.keys())]
                    the_power=T_matrix[x][y][the_force]-(100-T_matrix[x][y][the_force])/2
                    if T_matrix[x][y]['Population']>20:
                        init_screen.current_place['%spop' %(the_force[0])]+=the_power
                    else:
                        init_screen.current_place['%sspirit' %(the_force[0])]+=the_power
##                    else:
    init_screen.c.page()
    init_screen.land = []
    init_screen.directions = []
    area_number=coords[0]*map_size+coords[1]
    init_screen.current_area = 'area%s' %(area_number)
    init_screen.treasure_modifier = T_matrix[coords[0]][coords[1]]['Treasure']
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
    init_screen.directions = [max([0,area_number-map_size]),down_dir,left_dir,right_dir,0,0]
    for x in range(len(init_screen.directions)):
        init_screen.directions[x]=str(init_screen.directions[x])
    init_screen.land=generate_terr(coords)
    for x in range(1,24):
        for y in range(21,79):
            init_screen.c.scroll((y,x,y+1,x+1), 1, 1, terrain.T[init_screen.land[x-1][y-21]].colour, terrain.T[init_screen.land[x-1][y-21]].char)
    init_screen.map_coords = '47 22;47 2;77 12;22 12;0 0;0 0'
    new_coords = init_screen.map_coords.split(';')
    for i in range(6):
        new_coords[i] = new_coords[i].split(' ')
    spot=[int(new_coords[direction][0]),int(new_coords[direction][1])]
    while not terrain.T[init_screen.land[spot[1]-1][spot[0]-21]].pass_through:
        if direction==0:
            spot[1]-=1
        elif direction==1:
            spot[1]+=1
        elif direction==2:
            spot[0]-=1
        elif direction==3:
            spot[1]+=1
    for i in range(2):
        player.ch.xy[i] = spot[i]

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
            if not terrain.T[terrain_selection[f][add_terr]].pass_through and random.random()>0.25:
                other_terr=terrain_selection[f][:]
                other_terr.remove(terrain_selection[f][add_terr])
                add_terr=random.choice(other_terr)
                all_land+=add_terr
                done_lands+=1
            elif terrain.T[terrain_selection[f][add_terr]].pass_through:
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
    creature_coords=[player.ch.xy[:]]
    if random.random()<tp['Water']/100.:
        init_screen.terrain_type='w'
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
                ID = random.choice(player.water_creatures)
                for thing in player.game_creatures:
                    if ID == thing.id:
                        break
                game_id = i+1
                x = random.randint(21,78)
                y = random.randint(1,23)
                while [x,y] in creature_coords or not terrain.T[lands[y-1][x-21]].pass_through or terrain.T[lands[y-1][x-21]].id in thing.terr_restr:
                    x = random.randint(21,78)
                    y = random.randint(1,23)
                creation = thing.duplicate(x,y,game_id,thing.force,thing.race,True)
                creature_coords.append(creation.xy[:])
                player.all_creatures.append(creation)
                game_ids.append(game_id)
    else:
        init_screen.terrain_type=''
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
                c_race=random.choice(player.ch.races[c_force].keys())
                ID = 1
                game_id = i+add_id+1
                game_ids.append(game_id)
                x = random.randint(21,78)
                y = random.randint(1,23)
                while [x,y] in creature_coords or not terrain.T[lands[y-1][x-21]].pass_through or terrain.T[lands[y-1][x-21]].id in player.wood.terr_restr:
                    x = random.randint(21,78)
                    y = random.randint(1,23)
                creation = player.wood.duplicate(x,y,game_id,c_force,c_race,True)
                creature_coords.append(creation.xy[:])
                player.all_creatures.append(creation)
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
                ID = random.choice(player.random_by_force[c_force][c_temp])
                for thing in player.game_creatures:
                    if ID == thing.id:
                        break
                game_id = i+add_id+1
                game_ids.append(game_id)
                x = random.randint(21,78)
                y = random.randint(1,23)
                while [x,y] in creature_coords or not terrain.T[lands[y-1][x-21]].pass_through or \
                      (terrain.T[lands[y-1][x-21]].id in thing.terr_restr and thing.race!='plant') or \
                      terrain.T[lands[y-1][x-21]].id in ['pa']:
                    x = random.randint(21,78)
                    y = random.randint(1,23)
                creation = thing.duplicate(x,y,game_id,thing.force,thing.race,True)
                creature_coords.append(creation.xy[:])
                player.all_creatures.append(creation)
                
    if tp['Population']>35:
        village_type=[]
        if  tp['Order']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
            village_type.append('Order')
        if  tp['Nature']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
            village_type.append('Nature')
        if  tp['Chaos']==max([tp['Nature'],tp['Order'],tp['Chaos']]):
            village_type.append('Chaos')
        houses=random.randint(1,(tp['Population']-25)/5)
        add_ons=list(inventory.house_generated[:])
        for x in range(houses):
            house_type=random.choice(village_type)
            if house_type=='Nature' or house_type=='Chaos':
                add_on=inventory.cauldron
            else:
                if add_ons:
                    add_on=random.choice(add_ons)
                    add_ons.remove(add_on)
                else:
                    add_on=inventory.cauldron
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
                    c_race=random.choice(player.ch.races[c_force].keys())
                    ID = 2
                    game_id = 1+add_id
                    game_ids.append(game_id)
                    x = random.randint(21,78)
                    y = random.randint(1,23)
                    while [x,y] in creature_coords or not terrain.T[lands[y-1][x-21]].pass_through or terrain.T[lands[y-1][x-21]].id in player.wood.terr_restr:
                        x = random.randint(21,78)
                        y = random.randint(1,23)
                    creation = player.wood_perm.duplicate(x,y,game_id,c_force,c_race,False)
                    creature_coords.append(creation.xy[:])
                    player.all_creatures.append(creation)
                init_screen.ground_items.append([center[1]+21,center[0]+1,add_on.duplicate(1)])
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

    player.all_beings += player.all_creatures
    return lands

## Loads terrain when traveling
def new_terr(area,direction,f=''):
    if area in player.ch.known_areas:
        try:
            f = curdir+'//%s_dir//new_%s.dat' %(player.ch.name,area)
            terr = open(f, 'r')
        except IOError:
            f = curdir+'//%s_dir//%s.dat' %(player.ch.name,area)
            try:
                terr = open(f, 'r')
            except IOError:
                player.ch.known_areas.remove(area)
                new_terr(area,direction)
                return 0
        init_screen.ground_items = pickle.load(terr)
        init_screen.current_place = pickle.load(terr)
        tp=init_screen.current_place
        init_screen.c.page()

        init_screen.terrain_type = pickle.load(terr)
        init_screen.current_area = pickle.load(terr)
        init_screen.directions = pickle.load(terr)
        if init_screen.terrain_type=='w':
            waters=36
        else:
            waters=0
        init_screen.land = pickle.load(terr)
        init_screen.map_coords = pickle.load(terr)
        player.all_creatures = pickle.load(terr)
        for x in range(1,24):
            for y in range(21,79):
                init_screen.c.scroll((y,x,y+1,x+1), 1, 1, terrain.T[init_screen.land[x-1][y-21]].colour, terrain.T[init_screen.land[x-1][y-21]].char)
##        init_screen.map_coords = terr.readline()
##        new_coords = init_screen.map_coords[:len(init_screen.map_coords)-1].split(';')
                
        new_coords = init_screen.map_coords.split(';')
        
        for i in range(6):
            new_coords[i] = new_coords[i].split(' ')
        spot=[int(new_coords[direction][0]),int(new_coords[direction][1])]
        while not terrain.T[init_screen.land[spot[1]-1][spot[0]-21]].pass_through:
            if direction==0:
                spot[1]-=1
            elif direction==1:
                spot[1]+=1
            elif direction==2:
                spot[0]-=1
            elif direction==3:
                spot[1]+=1
        player.ch.xy = spot[:]
        init_screen.treasure_modifier = init_screen.current_place['Treasure']
        player.hidden = []
        player.all_beings = [player.ch]
        creature_coords=[player.ch.xy[:]]
        game_ids = []

        randoms=0
        if len(player.all_creatures):
            to_remove=[]
            for each_creature in player.all_creatures:
                if each_creature.random:
                    appear = 100-min([99,player.ch.turn-each_creature.appearance])
                    if random.randint(1,100)<=appear:
                        randoms=1
                        player.all_beings.append(each_creature)
                        creature_coords.append(each_creature.xy[:])
                        game_ids.append(each_creature.game_id)
                    else:
                        to_remove.append(each_creature)
                else:
                    if each_creature.appearance == 0:
                        player.all_beings.append(each_creature)
                        creature_coords.append(each_creature.xy[:])
                        game_ids.append(each_creature.game_id)
                    else: #if each_creature.id not in player.random_creatures:
                        if random.randint(1,1000)>each_creature.appearance:
                            each_creature.mode = 'not_appeared'
                            player.hidden.append(each_creature)
                        else:
                            player.all_beings.append(each_creature)
                            creature_coords.append(each_creature.xy[:])
                            game_ids.append(each_creature.game_id)
            for rem in to_remove:
                player.all_creatures.remove(rem)
        if not randoms:
            if init_screen.current_place['Population']<20:
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
                        ID = random.choice(player.random_by_force[c_force][c_temp])
                        for thing in player.game_creatures:
                            if ID == thing.id:
                                break
                        game_id = i+add_id+1
                        game_ids.append(game_id)
                        x = random.randint(21,78)
                        y = random.randint(1,23)
                        while [x,y] in creature_coords or not terrain.T[init_screen.land[y-1][x-21]].pass_through or \
                              (terrain.T[init_screen.land[y-1][x-21]].id in thing.terr_restr and thing.race!='plant') or \
                              terrain.T[init_screen.land[y-1][x-21]].id in ['pa']:
                            x = random.randint(21,78)
                            y = random.randint(1,23)
                        creation = thing.duplicate(x,y,game_id,thing.force,thing.race,True)
                        creature_coords.append(creation.xy[:])
                        player.all_creatures.append(creation)
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
                        c_race=random.choice(player.ch.races[c_force].keys())
                        ID = 1
                        game_id = i+add_id+1
                        game_ids.append(game_id)
                        x = random.randint(21,78)
                        y = random.randint(1,23)
                        while [x,y] in creature_coords or not terrain.T[init_screen.land[y-1][x-21]].pass_through or terrain.T[init_screen.land[y-1][x-21]].id in player.wood.terr_restr:
                            x = random.randint(21,78)
                            y = random.randint(1,23)
                        creation = player.wood.duplicate(x,y,game_id,c_force,c_race,True)
                        creature_coords.append(creation.xy[:])
                        player.all_creatures.append(creation)
            if waters>35:
                creatures = random.randint(0,2)
                if creatures:
                    if game_ids:
                        add_id=max(game_ids)
                    else:
                        add_id=1
                    for i in range(creatures):
                        ID = random.choice(player.water_creatures)
                        for thing in player.game_creatures:
                            if ID == thing.id:
                                break
                        game_id = i+add_id+1
                        game_ids.append(game_id)
                        x = random.randint(21,78)
                        y = random.randint(1,23)
                        while [x,y] in creature_coords or not terrain.T[init_screen.land[y-1][x-21]].pass_through or terrain.T[init_screen.land[y-1][x-21]].id in thing.terr_restr:
                            x = random.randint(21,78)
                            y = random.randint(1,23)
                        creation = thing.duplicate(x,y,game_id,thing.force,thing.race,True)
                        creature_coords.append(creation.xy[:])
                        player.all_creatures.append(creation)
                            
        player.all_beings += player.all_creatures
        init_screen.draw_items()
        terr.close()
    else:
        an=area[4:]
        if an=='B':
            coords=[0,0]
            player.all_creatures = []
            player.hidden = []
            init_screen.ground_items = []
            player.all_beings = [player.ch]
            unknown_Bterrain(coords,direction)
            predominant_f={init_screen.current_place['Nature']:'Nature',init_screen.current_place['Order']:'Order',
                           init_screen.current_place['Chaos']:'Chaos'}
            init_screen.place_descriptions['area%s' %(an)] = 'A place of %s.' %(predominant_f[max(predominant_f.keys())])
        else:
            an=int(an)
            coords=[an/map_size,an%map_size]
            init_screen.current_place=T_matrix[coords[0]][coords[1]]
            player.all_creatures = []
            player.hidden = []
            init_screen.ground_items = []
            player.all_beings = [player.ch]
            unknown_terrain(coords,direction)
            predominant_f={T_matrix[coords[0]][coords[1]]['Nature']:'Nature',T_matrix[coords[0]][coords[1]]['Order']:'Order',
                           T_matrix[coords[0]][coords[1]]['Chaos']:'Chaos'}
            init_screen.place_descriptions['area%s' %(an)] = 'A place of %s.' %(predominant_f[max(predominant_f.keys())])
    max_id=0
    creature_coords=[]
    for c in player.all_creatures:
        max_id=max([max_id,c.game_id])
        creature_coords.append(c.xy)
    for fol in player.ch.followers+player.ch.ride+player.ch.possessed:
        if fol.mode!='standing':
            player.all_beings.append(fol)
            player.all_creatures.append(fol)
            fol.game_id=max_id+1
            max_id+=1
            if fol in player.ch.ride or fol in player.ch.possessed:
                x = 1
                y = 1
            else:
                x = random.randint(max([player.ch.xy[0]-3,21]),min([78,player.ch.xy[0]+3]))
                y = random.randint(max([player.ch.xy[1]-3,1]),min([23,player.ch.xy[1]+3]))
                while [x,y] in creature_coords or not terrain.T[init_screen.land[y-1][x-21]].pass_through or terrain.T[init_screen.land[y-1][x-21]].id in fol.terr_restr:
                    x = random.randint(max([player.ch.xy[0]-3,21]),min([78,player.ch.xy[0]+3]))
                    y = random.randint(max([player.ch.xy[1]-3,1]),min([23,player.ch.xy[1]+3]))
            fol.xy=[x,y]
        if fol.mode=='standing' and fol.attr['area']==area:
            player.all_beings.append(fol)
            player.all_creatures.append(fol)
            fol.game_id=max_id+1
            max_id+=1
    return 1

def world():
    f = 'terrain.dat'
    terr = open(f, 'r')
    init_screen.c.page()
    init_screen.land = []
    places = {}
    place_descriptions = {}
    line = ''
    while 'world' not in line:
        line = terr.readline()
    init_screen.directions = line[:len(line)-1].split(' ')[1:]
    for i in range(23):
        init_screen.land.append(terr.read(58))
        terr.read(1)

    areas = terr.readline()
    if int(areas):
        for i in range(int(areas)):
            line = terr.readline()
            chop = line[:len(line)-1].split(':')
            xy = [int(chop[1]),int(chop[2])]
            if init_screen.current_area == 'area'+chop[0]:
                player.ch.xy[0] = xy[0]
                player.ch.xy[1] = xy[1]
            init_screen.world_places['area'+chop[0]] = xy
            if not chop[4]:
                init_screen.top_world_places[str(xy)] = chop[3]
            init_screen.place_descriptions['area'+chop[0]] = chop[3]

    init_screen.ground_items = []
    player.all_beings = [player.ch]
    player.all_creatures = []
    player.hidden = []

    terr.close()
    return 1
