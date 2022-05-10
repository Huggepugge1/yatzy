import random

class Die:
    # Initializes Die object
    def __init__(self):
        self.number = 0
        self.saved = False

    def roll_dice(self):
        self.number = random.randint(1, 6)
        return self.number