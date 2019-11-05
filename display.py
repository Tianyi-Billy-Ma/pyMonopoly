def main_menu():
    print(" Welcome to the Monopoly world!\n")
    print("\n\n\n")
    print("\n\n\n")
    print("main menu")
    print("1.Start Game")
    print("2.Option")
    print("3.load Map")
    print("4.Exit")
    print("\n\n\n")
    print("\n\n\n")
def exit_monopoly():
    print("See you next time!")
def Start_Game():
    print("Please input number of player")
def show_maps():
    print()
def main():
    show_example_map()
def show_example_map():
    display_screen = ""
    normal_line = "*" + " "*118+"*"
    display_screen += "*"*131 + "\n"
    for idx in range(0,60):
        if idx < 6 or idx > 54 :
            for i in range(10):
                display_screen += "*" + " "*12
            display_screen += "*\n"
        elif idx == 6 or idx == 54:
            display_screen += "*"*131 + "\n"
        elif (idx + 1)%7 == 0:
            display_screen += "*"*14 + " "*103 + "*"*14 + "\n"
        else:
            display_screen += "*"+" "*12+"*"+" "*103+"*"+" "*12+"*" + "\n"
    display_screen += "*"*131 + "\n"
    print(display_screen)
if __name__ == '__main__':
    main()
