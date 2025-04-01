import globfile as g
import matplotlib.pyplot as plt

def opt_swap_two_opt(route, i, j):
    # This function performs a 2-opt swap on the given route. It reverses the segment of the route between
    # indices i and j to potentially improve the route
    new_route = route[:i+1] + route[i+1:j+1][::-1] + route[j+1:]
    return new_route

def get_distance(route, e):
    # This function calculates the total distance of a given route by summing the distances between consecutive cities.
    distance = 0
    for i in range(len(route) - 1):
        distance += e[route[i]][route[i+1]]
    return distance

def checkTwoOpt(route,max):
    # This function applies the 2-opt algorithm to optimize the given route
    improved = True
    best_distance = get_distance(route, g.e)
    counter = 0

    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                new_route = opt_swap_two_opt(route, i, j)
                new_distance = get_distance(new_route, g.e)
                if new_distance < best_distance and new_distance <= max:
                    counter += 1
                    route = new_route
                    best_distance = new_distance
                    improved = True

    # print('two_opt counter:', counter)
    g.counter.append(counter)

    return counter

def parent_selection(nextgen,gen,tmax): #(popPois,pop,gen,j):
    # new parent selection method
    info=[]
    nextgenfeas=[n for n in nextgen if n[2]<=tmax]
       
    g.feas=nextgenfeas
    #generate new data structure with quality scores
    # info = [index, route, route distance,score, quality score (number of 3-opt itter needed), weighted Score]
    # weighted score = 0,5*quality score + a * route score
    for i in range(len(nextgenfeas)):
    #for i in range(len(nextgen)):
        route=[x[3] for x in nextgenfeas[i][1]]
        routex= [x[0] for x in nextgenfeas[i][1]]
        routey= [x[1] for x in nextgenfeas[i][1]]
        routeDistance= nextgenfeas[i][2]
        # route=[x[3] for x in nextgen[i][1]]
        # routex= [x[0] for x in nextgen[i][1]]
        # routey= [x[1] for x in nextgen[i][1]]
        # routeDistance= nextgen[i][2]
        qualityScore=checkTwoOpt(route, routeDistance)
        score=nextgen[i][0]
        info.append([i,nextgen[i],qualityScore,score,routex,routey])
            
    sortedInfo = sorted(info, key=lambda x: (-x[3], x[2]))
    
    parent1=sortedInfo[0][1] #index of first solution based on ordered info list
    if len(sortedInfo)==1:
        parent2=parent1
    else:
        parent2=sortedInfo[1][1] #index of second solution based on ordered info list
    
   
    return [parent1, parent2]
