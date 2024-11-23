class Station():

    def __init__(self, capacity, available_bikes):
        self.capacity = capacity
        self.available_bikes = available_bikes
        self.available_spots = capacity - available_bikes
        assert self.available_spots >= 0, "Station init: available_bikes > capacity"

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
    
