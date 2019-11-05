import numpy as np

class Dice:
    def __init__(self):
        self.num_rolls = 0
    def roll_two(self):
        return np.random.randint(1,7,size = 2)
    def roll_one(self):
        return np.random.randint(1,7,size = 1)
