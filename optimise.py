import numpy as np
import math
import get_distance as gd

def notVisited(cpoints, route):
# based on a list with points return a list with points not included in a route
    notVis=[]
    for c in cpoints:
        if c[3] not in route:
            notVis.append(int(c[3]))
    
    return notVis

def nextPPoi (p,a,e=0):
# From an array of n points of interest, 
# find the closest one to a point p based on the Euclidean distance e.

    # find max value of e and use this to search for the minimum one
    max_value = max([max(row) for row in e])
    min=max_value
    point=p
    for i in a:
        if e[p][i]<min:
            min=e[p][i]
            point=i
                
    return point    

def insert(cpoints, route, score, tmax, troute, edist):
    # This function tries to insert a poi into an existing route
    # while ensuring that the total cost of the route time does not exceed the maximum time limit (tmax)

    # Convert the list of candidate points into a numpy array for easier handling
    cpoints_=np.asarray(cpoints)  
    # Identify the points that have not been visited yet using the 'notVisited' function
    toVisit=notVisited(cpoints_, route) 
    
    newT=troute
    prevScore=score
    newScore=score
    performInsert=0
    best_augmentation = float('inf')

    # Loop over the candidate pois for insertion
    for poi in toVisit:
        for i in range(1, len(route)-1):
            augmentation = edist[route[i - 1]][poi] + edist[poi][route[i]] - edist[route[i - 1]][route[i]]
            if augmentation < best_augmentation and augmentation>0 and augmentation+troute<=tmax:
                best_augmentation = augmentation
                best_position = i
                best_poi=poi
                performInsert=1

    # If a valid insertion has been found, update the route, score, and other relevant variables
    if performInsert != 0:
        route.insert(best_position,best_poi)
        newScore=score+cpoints[best_poi][2]
        #toVisit.remove(nextP)
        
    return route, gd.get_distance(route, edist), newScore

def swap_insert_updated(cpoints, route, score, tmax, troute, edist):
    # This function performs replace operation to optimize the given route 
    # while ensuring that the total cost of the route time does not exceed the maximum time limit (tmax)
    
    # Initialize the visited route and create a list of unvisited points
    visited=route
    unvisited= [p for p in range(len(cpoints)) if p not in visited]

    # Iterate through all positions in the route (except the first and last positions)
    for j in range(1, len(route)-1):
        # Try inserting each unvisited point into the current position 'j' in the route
        for i in unvisited:
            if not unvisited:
                break

            # Calculate the added and removed distances when inserting point 'i' at position 'j'
            added_dist = edist[route[j-1]][i] + edist[i][route[j+1]]
            removed_dist = edist[route[j-1]][j] + edist[j][route[j+1]]
            temp_distance = troute + added_dist - removed_dist
            
            if added_dist > edist[route[j-1]][j+1]:
                triang = True
            else:
                triang = False
                
            if temp_distance <= tmax and triang:
                new_route = route.copy() # Create a copy of the current route to apply the changes
                new_score = score + cpoints[i][2] - cpoints[route[j]][2]
                new_route.insert(j, i)
                new_route.remove(route[j])
                new_troute = gd.get_distance(new_route, edist) # troute + edist[route[j - 1], i] + edist[i, route[j]] - edist[route[j - 1], route[j]]
                
                # If the new score is greater or if the cost is smaller (while ensuring it is within tmax)
                # update the route, score, and cost and remove the inserted point 'i' from the unvisited list

                if (new_score > score or new_troute < troute) and new_troute <= tmax:
                    route, score, troute = new_route, new_score, new_troute
                    unvisited.remove(i)
                    break

    
    return route, troute, score
       

def swap(p,routeDistance, e):
    # This function attempts to improve a given route swapping pois
    
    # Initialize the new route distance with the provided current route distance
    newDist=routeDistance
    improved = True
    w=0
    counter=0
    while improved and counter <20000: #remove 'counter <20000' after testing:
        counter+=1
        best2opt = p # start with an initial tour
        size = len(p)
        w+=1

        for i in range(0,size-3):
            #  j=i+2 because i+1 will be the tail of the edge
            j=i+2          
            improved = False

            # Calculate the "gain" from performing the swap: old edges - new edges
            gain=e[p[i]][p[i+1]]+e[p[j]][p[j+1]]-e[p[i]][p[j]]-e[p[i+1]][p[j+1]]
            
            if gain > 0:
                newDist-=gain # Decrease the route distance by the gain 
                temp=p[i+1]
                p[i+1]=p[j]
                p[j]=temp                                                   
                improved = True

    return p, newDist

