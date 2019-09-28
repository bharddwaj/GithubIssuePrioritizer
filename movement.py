class Movement():
    def __init__(self,coordinate,jumping = False, capturing = True,jumping_coordinate = None):
        self.jumping = jumping
        self.capturing = capturing
        self.coordinate = coordinate
        self.jumping_coordinate = coordinate
    
