class Station():

    def __init__(self, node, num_bikes, available_bikes, available_spots):
        self.node = node
        self.num_bikes = num_bikes
        self.available_bikes = available_bikes
        self.available_spots = available_spots

    def return_bike(self):
        if self.available_spots <= 0:
            return False
        self.available_bikes += 1
        self.available_spots -= 1
        return True
    
    def rent_bike(self):
        if self.available_bikes <= 0:
            return False
        self.available_bikes -= 1
        self.available_spots += 1
        return True