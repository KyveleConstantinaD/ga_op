import matplotlib.pyplot as plt

def plot_pois(pois, route, tmax, files):
    plt.clf()  # Clear the current figure

    # Extract x and y coordinates of points of interest (POIs)
    poisx = [x[0] for x in pois]
    poisy = [y[1] for y in pois]

    # Plot all points of interest as green dots
    plt.subplot(1, 1, 1)
    plt.plot(poisx, poisy, 'go')

    # Set the title of the plot to indicate the time maximum (tmax)
    plt.title("Proposed Route for tmax = " + str(tmax))

    # Annotate each point with its index for better identification
    for i in range(len(poisx)):
        plt.annotate(i, (poisx[i], poisy[i]), fontsize=11)

    # Prepare lists to hold the route coordinates
    routex = []
    routey = []

    # Loop through the route to get the coordinates of the points in the route
    for i in route:
        for j in range(len(poisx)):
            if pois[j][3] == i:  # Check if the index matches the route
                routex.append(pois[j][0])  # Append x coordinate
                routey.append(pois[j][1])  # Append y coordinate

    # Plot the route as a red line
    plt.plot(routex, routey, 'r-')

    # Prepare the filename for saving the plot
    filename = 'Plots/' + str(files) + ' Best out of 30 reps - for Tmax ' + str(tmax) + '.png'

    # Save the plot to the specified filename
    plt.savefig(filename)

    plt.clf()  # Clear the figure again to free up memory


