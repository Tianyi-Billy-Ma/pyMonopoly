import sys, os
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), 'features'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'menu'))
import Dice
from Option_factory import Option_factory
from main_menu import main_menu
from normal_parameter import Parameter

def main():
    STOP = False
    pyparameter = Parameter()
    while not STOP:
         my_menu = main_menu()
         num = my_menu.print_main_menu()
         if num == pyparameter.QUIT_PARAMETER:
             STOP = True
             my_menu.exit_monopoly()
         else:
             option = Option_factory(pyparameter)
             estimator = option.factory(num)
             estimator.play()
if __name__ == '__main__':
    main()
