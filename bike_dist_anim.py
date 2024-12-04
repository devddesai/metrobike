from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt


def animate(agent_data):
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
    ani.save('bike_distribution.gif', writer='imagemagick', fps=30)