def get_distance(route, e):
    # Computes the total distance of a route based on the distance matrix.

    distance = 0
    for i in range(len(route) - 1):
        distance += e[route[i]][route[i+1]]
    return distance