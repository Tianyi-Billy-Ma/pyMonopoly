import numpy as np

class main_menu:
    def __init__(self):
        self.num_mainmenu = 0
    def print_main_menu(self,ask = "Please enter your selection"):
        print("\n"*100)
        print(" Welcome to the Monopoly world!\n")
        print("main menu")
        print("1.Start Game")
        print("2.Option")
        print("3.load Map")
        print("4.Exit\n")
        selection = input(ask + "\n")
        self.num_mainmenu += 1
        try:
            return int(selection)
        except:
            return self.print_main_menu("Please enter the selection from 1 to 4")
    def exit_monopoly(self):
        print("See you next time!")
