import math
import numpy as np
import random
import globfile as g
import parent_selection as ps
import two_opt
import optimise
from time import process_time

def generate_random_selection(xxx, lenght):
    n_sublists = len(xxx)
    num_sublists_to_select = int(lenght)

    # Create a list of indices for all sublists
    indices = list(range(n_sublists))

    # Shuffle the indices to get a random order
    random.shuffle(indices)

    # Take the first 'num_sublists_to_select' indices as the randomly selected ones
    selected_indices = indices[:num_sublists_to_select]

    return selected_indices


def convert_route(route,pois):
   # converts a route into a list of poi elements - pois from initital set - each poi is a list
   route_list=[]
   for r in route:
       for p in pois:
           if p[3]==r:
               route_list.append(p)
        
   return route_list

# mutation function
def mutate(offspring,pois):
    tempDist = 0
    optScore = offspring[0]
    optRoute = [x[3] for x in offspring[1]]
    newDist = distance_check(optRoute)
    tempScore=0
 
    tempDist=newDist
    tempScore=optScore
    
    # mutation steps
    optRoute,newDist = two_opt.two_opt(optRoute,newDist,g.e) # 2-opt    
     
    optRoute,newDist,optScore = optimise.insert(pois,optRoute,calcScore(optRoute,pois),g.tmax,newDist,g.e) #insert step
    optRoute,newDist = optimise.swap(optRoute,newDist,g.e) # replace step
    optRoute,newDist,optScore = optimise.swap_insert_updated(pois,optRoute,calcScore(optRoute,pois),g.tmax,newDist,g.e) # swap step

    return [calcScore(optRoute,pois), optRoute, distance_check(optRoute)]

# function to calculate cost of route
def distance_check(p):
    dist=0
    for i in range(len(p)-1):
        dist+=g.e[p[i]][p[i+1]]
        
    ##print ('correct distance should be', dist)
    return dist

# function to calculate score of route
def calcScore(route,pois):
    score=0
    for i in route:
        score+=pois[i][2]
    return score

# crossover function
def order_crossover(a, b):
    dist=g.tmax+1
    
    counter=0
    while dist>g.tmax and counter<10000:
        #while dist>tmax:
        if len(a)<len(b):
            parent1=a.copy()
            parent2=b.copy()
        else:
            parent1=b.copy()
            parent2=a.copy() # Exclude first and last indices
             
        valid_indices = list(range(1, len(parent1) - 1))
        # if a route contains 3 or less pois then crossover will lead in no changes
        # parent a is selected as offspring
        if valid_indices==[0] or valid_indices==[1]:
            offspring=a
            break
        
        # Generate two random indices
        crossover_points = random.sample(valid_indices, 2)
        crossover_points.sort()
        
        # generae parents
        split1=parent2[0:crossover_points[0]]
        split2=parent2[crossover_points[1]+1:len(parent2)]
        order=parent1[crossover_points[0]:crossover_points[1]+1]
          
        u = [x for x in split1 if x[3] not in [y[3] for y in order] ]
        w = [x for x in split2 if x[3] not in [y[3] for y in order] ]
        
        # generate offspring
        offspring = u + order + w
    
        dist = distance_check([x[3] for x in offspring])
        # if dist<=g.tmax:
        #     offspring = offspring
        counter+=1
    if counter==10000 and dist>g.tmax:
        offspring=a
            
    selected_offspring = offspring

    return selected_offspring
        
# function to calculate distance between two pois
def distance( p1, p2 ):

   return math.sqrt( ( p1[0] - p2[0] ) ** 2 + ( p1[1] - p2[1] ) ** 2 )

# returns a list of L paths with the best path in the first position
# by weight rather than length
# NOT USED IN 1_2 ορ 2_2
def init_replacement( s1 ):
    # function adapted from mc-ride
    s = list( s1 )
    L = len( s ) if len( s ) <= 10 else 10
    if( L == 0 ):
      
        return [ [ g.start_point, g.end_point ] ]

    #decorate and sort by weight
    dsub = sorted( [ ( x[4], x ) for x in s ] )[::-1] 
    ls = dsub[ :L ] 
    rest = dsub[ L: ]
    paths = []
    for i in range( L ):
        path = [ g.start_point, ls[ i ][1] , g.end_point ] 
        length = distance( path[0], path[1] ) + distance( path[1], path[2] )
        assert( length < g.tmax )
        arest = ls[ :i ] + ls[ i + 1: ] + rest
        arest = [ x[1] for x in arest ] #undecorate
        assert( len( arest ) + len( path ) == len( s ) + 2 )
        found = True
        while( found == True and len( arest ) > 0 ):
            min_added_length = -1
            max_weight = 0
            for j in range( len( arest ) ):
                for k in range( len( path ) - 1 ):
                    added_length = ( distance( path[ k ], arest[ j ] ) + 
                                     distance( path[ k + 1 ], arest[ j ] ) - 
                                     distance( path[ k ], path[ k + 1 ] ) ) 
                    if( length + added_length < g.tmax and arest[ j ][4] < max_weight ):
                        min_added_length = added_length
                        max_weight = arest[ j ][4]
                        minpoint = j
                        pathpoint = k + 1
            if( min_added_length > 0 ):
                #add to path
                path.insert( pathpoint, arest.pop( minpoint ) )
                length = length + min_added_length
            else:
                found = False
        if( length < g.tmax ):
            paths.append( path )
       
    assert( len( paths ) > 0 )

    # return best route out of the set randomly generated
    best = sorted(
        [
            [
                sum(sublist_elem[2] for sublist_elem in sublist),
                sublist,
                distance_check([sublist_elem[3] for sublist_elem in sublist])
            ]
            for sublist in paths
        ],
        key=lambda x: (-x[0], x[2]),
    )[0]

    return best

    
# NOT USED IN 1_2 ορ 2_2
def ell_sub(aug):
    result = []
    for item in aug:
        if( g.e[item[3]][g.start] + g.e[item[3]][g.end] <= g.tmax ):
            result.append( item )
    return result

# NOT USED IN 1_2 ορ 2_2
def fitness(chrom, s):
    
    aug = [] 
    for i in range(len( s )):
        aug.append(( s[ i ][0],
                       s[ i ][1],
                       s[ i ][2],
                       s[ i ][3],  + chrom[ i ] ))
    g.augs=aug
    # set of available pois based on tmax
    ellset = ell_sub(aug)
    
    return init_replacement(ellset)


def random_initial_elipsis(L,pois):
    distance_list=[]
    initial_set=[]
                  
    # generate list of pois within tmax
    poi_list=[x[3] for x in pois if (g.e[g.start][x[3]] + g.e[x[3]][g.end])<=g.tmax]
    poi_list.remove(g.start)
    if g.start!=g.end:
        poi_list.remove(g.end)

    # generate set of L routes
    while len(initial_set) < L:
        
        # put pois in random order
        random.shuffle(poi_list)
        
        #assign random 0, 1 
        binary_list= [random.choice([0, 1]) for _ in range(len(poi_list))]
        
        #select the pois with value 1 for the route
        route = [num for num, value in zip(poi_list, binary_list) if value == 1]
        route.insert(0, g.start)
        route.append(g.end)

        dist=distance_check(route)
        temp= [calcScore(route,pois),convert_route(route,pois), dist, route]
        distance_list.append(temp)
        if dist<=g.tmax:
            initial_set.append(temp)

    return initial_set


def run_alg(pois, initialPopulation, parentSelection): 
   
    #random.seed()
  
    popsize = 100
    crossover_prob=0.7
    generations = 0
    kt = 3 #3
    mutation_prob=0.4
    isigma = 10 # NOT USED IN 1_2 ορ 2_2
    solution_is_same=0
    previous_best=[0]
    
    g.start_time=process_time()
    g.end_time=[]
    
    g.parent_s_time=[]
    g.parent_e_time=[]
    #------------------------------------
    # generate initial population of popsize
    if initialPopulation == 1:
        # option 1
        #generate initial population based on fitness and heuristic
        #print('in initial population method 1')
        init_pop = []
        for i in range( popsize ):
            chrom = []
            for j in range( len( g.cpoints ) ):
                
                chrom.append( random.normalvariate( 0, isigma ) )
    
            chrom = (fitness(chrom, g.cpoints))     
            g.chrom = chrom
            init_pop.append(chrom)
    
    if initialPopulation == 2:
        # option 2
        # generate random population
        #print('in initial population method 2')
        init_pop=random_initial_elipsis(popsize,pois)
        
    nextgen=init_pop
    g.allroutes=[]
    g.testtest=[]
    stopping_number= stopping_number = max(11, int(len(pois) / 3)) # 1/3 of pois or at least 10
    
    while solution_is_same<stopping_number and generations<300: # comment 'generations<300' after test
        # k = stopping_number -1 extra generations need to pass where the solution has not changed for the routine to end

        parents=[]
        if parentSelection == 1:
            #select parents in k tournaments
            #print('in parent selection method a')
            parents = sorted( random.sample( nextgen, kt ) )[ kt - 2: ] #
        
        if parentSelection == 2:
            # new selection process
            #print('in parent selection method b')
    
            g.parent_s_time.append(process_time())
            parents= ps.parent_selection(nextgen, generations, g.tmax)
            g.parent_e_time.append(process_time())


        # crossover and generate offsprings
        #print('in crossover')
        for k in range(round(popsize*crossover_prob)): #optimise
            offspring = order_crossover( parents[0][1], parents[1][1] )

            nextgen.append([calcScore([x[3] for x in offspring],pois),offspring, distance_check([x[3] for x in offspring]) ])
        
        # mutate
        selected_for_mutation = generate_random_selection(nextgen, len(nextgen)*mutation_prob)
        
        #print('in mutation')
        for s in selected_for_mutation:
            temp=mutate(nextgen[s],pois)
            p=temp[1]
            
            if len(set(p))!=len(p):
                print('FALSE')

            converted=convert_route(temp[1],pois)
            nextgen[s]= [calcScore(temp[1],pois), converted, distance_check(temp[1])]
        
        #find so far best solution
        nextgen.sort(key=lambda z: (-z[0], z[2]))
        best=nextgen[0]
        
        if best==previous_best:
            solution_is_same+=1
            #print('best solution not changed in this gen')
        else:
            solution_is_same=1 
            #print('start over')

        previous_best=best       
     
        #update population for next gen
        g.all_routes.append([generations, nextgen])
        g.testtest.append([generations, nextgen])
        temp_population=nextgen.copy()
        nextgen=[]
        # out of the pop select l for the next gen
        for n in generate_random_selection(temp_population, popsize):
            nextgen.append(temp_population[n])
        
        generations+=1
        g.end_time.append(process_time())    
        
    # select based on sorted list
    # output best solution 
    glob_best=best
    best.append(generations-(stopping_number))

    return glob_best

#----------------------------------------------------------------------------
# basic function for GA
def genetic_alg(pois,numOfPois, tmax, start , end, initialPopulation, parentSelection):
    g.cpoints=pois.copy()
    g.start=start
    g.end=end
    g.tmax=tmax
    
    #slpit data to single lists
    x=[]
    y=[]
    score=[]
    num=[]
       
    for p in pois:
        x.append(p[0])
        y.append(p[1])
        score.append(p[2])
        num.append(p[3])
        
    # Eucl dist matrix
    e=np.zeros((len(pois), len(pois)))
    for i, poi in enumerate(pois):
        for j, p in enumerate(pois):
            e[i][j]=math.sqrt(( poi[0] - p[0] ) ** 2 + ( poi[1] - p[1] ) ** 2)
            
    
    g.e=e
    #proposed route using ga - ----- -
    assert( e[start][end] < tmax)
    
    random.seed()
    
    g.start_point = g.cpoints.pop(start)
    
    if start==end:
        g.end_point= g.start_point
    elif start!=end:
        for i in range(len(g.cpoints)):
            if end==g.cpoints[i][3]: 
                g.end_point = g.cpoints.pop(i)
                break
    
    
    routes=[]
    i=0
    best_fit = 0
    test_runs=1
    for j in range( test_runs ):
        proposed_route = run_alg(pois, initialPopulation, parentSelection)
        routes.append(proposed_route)         
        
    #out of all routes select the best (based on best fit calculated)  
    routes.sort(key=lambda x: (-x[0], x[2]))
    best=routes[0]
    
    return best
