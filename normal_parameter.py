#This is some normal parameter that may be changeable
class Parameter:
    def __init__(self):
        self.START_GAME = 1
        self.OPTIONS = 2
        self.LOADMAP= 3
        self.QUIT_PARAMETER = 4
    def get_QUIT_PARAMETER(self): return self.QUIT_PARAMETER
    def get_START_GAME(self): return self.START_GAME
    def get_OPTIONS(self): return self.OPTIONS
    def get_LOADMAP(self): return self.LOADMAP
