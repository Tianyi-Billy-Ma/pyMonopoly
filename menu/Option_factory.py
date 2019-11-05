import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..','features'))
from normal_parameter import Parameter
from Game import Game
from Options import SetOption
class Option_factory:
    def __init__(self,parameter):
        self.parameter = parameter
    def factory(self,num):
        if num == self.parameter.START_GAME: return Game()
        elif num == self.parameter.OPTIONS: return SetOption()
    elif num == self.parameter.LOADMAP: return LoadMap()
