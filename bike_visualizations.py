from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate_bike_distribution(agent_data):
    '''
    Animates the bike distribution at each station over time

    Parameters
    ----------
    agent_data : DataFrame
        The DataFrame containing the agent data

    Returns
    -------
    None
    '''

    df = agent_data

    # Prepare the animation
    fig, ax = plt.subplots()

    # Function to update the bar plot for each frame
    def update(frame):
        ax.clear()
        capacities = df.loc[frame,1]['All Station Capacity']
        stations = [f"Station {key}" for key in capacities.keys()]
        bikes = [value for value in capacities.values()]
        ax.bar(stations, bikes, color='blue')
        ax.set_title(f"Bike Distribution at Frame {frame}")
        ax.set_xlabel("Stations")
        ax.set_ylabel("Number of Bikes")
        ax.set_ylim(0, 10) # Adjust Y-axis dynamically

    # Create animation with one frame per row in the DataFrame
    ani = FuncAnimation(fig, update, frames=len(df)//100-1, repeat=False)
    writer = animation.PillowWriter(fps=30)
    ani.save('bike_distribution.gif', writer=writer)


def station_bike_hist(agent_data):
    '''
    Plots a histogram of the bike distribution at each station over time

    Parameters
    ----------
    agent_data : DataFrame
        The DataFrame containing the agent data

    Returns
    -------
    None
    '''

    df=agent_data
    station_histogram = {station: {} for station in range(len(df.iloc[0]['All Station Capacity']))}

    # Populate the histogram
    for _, row in df.iterrows():
        capacities = row['All Station Capacity']
        for station, capacity in capacities.items():
            if capacity not in station_histogram[station]:
                station_histogram[station][capacity] = 0
            station_histogram[station][capacity] += 1/100

    # Plot histograms for each station
    for station, capacity_counts in station_histogram.items():
        plt.figure()
        plt.bar(capacity_counts.keys(), capacity_counts.values(), color='blue')
        plt.title(f"Station {station} Capacity Distribution")
        plt.xlabel("Capacity")
        plt.ylabel("Counts")
        plt.xlim(-1,11)
        plt.show()