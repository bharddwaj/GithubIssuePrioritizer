# Python meta chess game

class Direction:
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"
    UP_RIGHT = "upper-right"
    UP_LEFT = "upper-left"
    DOWN_RIGHT = "down-right"
    DOWN_LEFT = "down-left"

class Movement:

    def __init__(self, movement, can_jump=False, can_capture=True):
        assert isinstance(movement, tuple), "Movement needs to be a tuple!"
        assert len(movement) == 2, "Movement needs to be a pair of values!"

        self.movement = movement
        self.jumping = can_jump
        self.capturing = can_capture
        pass

    def __str__(self):
        if self.jumping:
            if self.capturing:
                return f"<Movement {self.movement} that can capture and jump>"
            else:
                return f"<Movement {self.movement} that can jump>"
        else:
            if self.capturing:
                return f"<Movement {self.movement} that can capture>"
            else:
                return f"<Movement {self.movement}>"


m = Movement((2, Direction.UP))
print(m)
