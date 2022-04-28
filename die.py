import random

class Die:
    def __init__(self):
        self.number = 0
        self.saved = False

    def roll_dice(self):
        self.number = random.randint(1, 6)
        return self.number