import random

class Die:
    def __init__(self, number, saved):
        self.number = number
        self.saved = saved

    def roll_dice(self):
        self.number = random.randint(1, 6)
        return self.number