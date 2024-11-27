class Station():
    def __init__(self, capacity, available_bikes):
        self.capacity = capacity
        self.available_bikes = available_bikes
        self.available_spots = capacity - available_bikes
        assert self.available_spots >= 0, "Station init: available_bikes > capacity"
        assert self.capacity > 0, "Station init: capacity <= 0"

    def return_bike(self):
        if self.available_spots <= 0:
            return False
        self.available_bikes += 1
        self.available_spots -= 1
        assert self.available_spots+self.available_bikes == self.capacity and self.available_spots >= 0, "Station return_bike: available_spots + available_bikes != capacity, available spots>capacity"
        return True
    
    def rent_bike(self):
        if self.available_bikes <= 0:
            return False
        self.available_bikes -= 1
        self.available_spots += 1
        assert self.available_spots+self.available_bikes == self.capacity and self.available_spots >= 0, "Station return_bike: available_spots + available_bikes != capacity, available spots>capacity"
        return True

    def get_bike_availability(self):
        return self.available_bikes > 0
    
    def get_spot_availability(self):
        return self.available_spots > 0

    def assign_bikes(self, num_bikes):
        self.available_bikes = num_bikes
        self.available_spots = self.capacity - num_bikes
        assert self.available_spots >= 0, "Station assign_bikes: available_spots < 0"
        assert num_bikes >= 0, "Station assign_bikes: num_bikes assigned to station must be non-negative"
    
    def __str__(self):
        return "Station: capacity {}, available bikes {}, available spots {}".format(self.capacity, self.available_bikes, self.available_spots)
    
