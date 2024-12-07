from matplotlib import pyplot as plt

def hist(agent_data):
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