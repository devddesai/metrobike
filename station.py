class Station():
    def __init__(self, capacity, available_bikes):
        """
        Initializes a station with a given capacity and number of available bikes.

        Args
        ---
        capacity: int
            The total number of bikes that the station can hold.
        available_bikes: int
            The number of bikes that are currently at the station.
        """
        self.capacity = capacity
        self.available_bikes = available_bikes
        self.available_spots = capacity - available_bikes
        self.popularity = 0
        assert self.available_spots >= 0, "Station init: available_bikes > capacity"
        assert self.capacity > 0, "Station init: capacity <= 0"

    def return_bike(self):
        """
        Returns a bike to the station. If the station is full, the bike cannot be returned.

        Args
        ---
        None

        Returns
        ---
        bool
            True if the bike was successfully returned, False otherwise.
        """
        if self.available_spots <= 0:
            return False
        self.available_bikes += 1
        self.available_spots -= 1
        assert self.available_spots+self.available_bikes == self.capacity and self.available_spots >= 0, "Station return_bike: available_spots + available_bikes != capacity, available spots>capacity"
        return True
    
    def rent_bike(self):
        """
        Rents a bike from the station. If there are no bikes available, the bike cannot be rented.

        Args
        ---
        None

        Returns
        ---
        bool
            True if the bike was successfully rented, False otherwise.
        """
        if self.available_bikes <= 0:
            return False
        self.available_bikes -= 1
        self.available_spots += 1
        assert self.available_spots+self.available_bikes == self.capacity and self.available_spots >= 0, "Station return_bike: available_spots + available_bikes != capacity, available spots>capacity"
        return True

    def get_bike_availability(self):
        """
        Returns whether there are bikes available at the station.

        Args
        ---
        None

        Returns
        ---
        bool
            True if there are bikes available, False otherwise.
        """
        return self.available_bikes > 0
    
    def get_spot_availability(self):
        """
        Returns whether there are spots available at the station.

        Args
        ---
        None

        Returns
        ---
        bool
            True if there are spots available, False otherwise.
        """
        return self.available_spots > 0

    def assign_bikes(self, num_bikes):
        """
        Assigns a number of bikes to the station. The number of bikes must be non-negative.

        Args
        ---
        num_bikes: int
            The number of bikes to assign to the station.

        Returns
        ---
        None
        """
        self.available_bikes = num_bikes
        self.available_spots = self.capacity - num_bikes
        assert self.available_spots >= 0, "Station assign_bikes: available_spots < 0"
        assert num_bikes >= 0, "Station assign_bikes: num_bikes assigned to station must be non-negative"

    def set_station_info(self, capacity, available_bikes):
        """
        Set the capacity and available bikes for each station

        Parameters
        ----------
        capacity : dict
            A dictionary where the keys are station indices and the values are the capacity of the station
        available_bikes : dict
            A dictionary where the keys are station indices and the values are the number of available bikes at the station

        Returns
        -------
        None
        """
        self.capacity = capacity
        self.available_bikes = available_bikes
        self.available_spots = capacity - available_bikes
        assert self.available_spots >= 0, "Station set_station_info: available_spots < 0"
        assert self.capacity > 0, "Station set_station_info: capacity <= 0"
    
    def __str__(self):
        return "Station: capacity {}, available bikes {}, available spots {}".format(self.capacity, self.available_bikes, self.available_spots)
    
