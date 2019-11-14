import numpy as np
import os
import _pickle as cPickle
import traceback
CURRENT_LOCATION = os.path.dirname(os.path.abspath(__file__))
DATA_LOCATION = os.path.dirname(os.path.abspath(__file__)) + "/Data"
PLAYER_LOCATION  = os.path.dirname(os.path.abspath(__file__)) + "/Data/Players"
MAP_LOCATION = os.path.dirname(os.path.abspath(__file__)) + "/Data/Maps/"
GAME_LOCATION = os.path.dirname(os.path.abspath(__file__)) + "/Data/Games/"
ERROR = ""
class Parameter:
    def __init__(self):
        self.START_GAME = 1
        self.OPTIONS = 2
        self.LOADGAME= 3
        self.QUIT_PARAMETER = 4
        #Please set
        self.optionfile = DATA_LOCATION + "/Setting.txt"
        self.ERROR1 = "There is no game to load"
        self.ERRORS = [self.ERROR1]
    def get_QUIT_PARAMETER(self): return self.QUIT_PARAMETER
    def get_START_GAME(self): return self.START_GAME
    def get_OPTIONS(self): return self.OPTIONS
    def get_LOADMAP(self): return self.LOADMAP
    def get_optionfile(self):return self.optionfile
    def save_settings(self,dict): self.settings = SetOption(dict)
    def get_settings(self): return self.settings
PYPARAMETER = Parameter()
class player:
    def __init__(self,player_file = '',name = '', mark = ''):
        if player_file != '':
            self.dict = read_dictionary(PLAYER_LOCATION + '/'+player_file+ '.txt',":")
            self.name = self.dict['name'].strip('\n').strip(" ")
            self.mark = self.dict['mark']
            self.games_palyed = self.dict['games_played']
        else:
            self.name = name
            self.mark = mark
            self.games_played = 0
        self.money = 0
    def get_name(self): return self.name
    def get_mark(self): return self.mark
    def get_money(self):return self.money
    def save(self):
        f = open(PLAYER_LOCATION + '/{}.txt'.format(self.name), "w+")
        f.write("name:" + self.name + "\n")
        f.write("mark:" + self.mark + "\n")
        f.write("games_played:" + str(self.games_played))
        f.close()
def read_dictionary(file_address,operation):
    d = {}
    with open(file_address) as f:
        for line in f:
            (key, val) = line.split(operation)
            d[key] = val
    d['setting address'] = file_address
    return d
class pyMap:
    def __init__(self,mapaddress):
        self.address = MAP_LOCATION  + "{}.txt".format(mapaddress)
        self.dict = read_dictionary(self.address,":")
        self.mapname = self.dict['name'].strip("\n")
    def get_name(self): return self.mapname
class Game:
    def __init__(self,gameName,players,map):
        self.players = players
        self.map = map
        self.name = gameName
    def play(self):
        self.save()
    def save(self):
        file = open(GAME_LOCATION+str(self.name)+'.txt','wb+')
        cPickle.dump(self,file,0)
        file.close()
    def load(self):
        file = open(GAME_LOCATION+self.name+'.txt','rb')
        dataPickle = file.read()
        file.close()
        self.__dict__ = cPickle.loads(dataPickle)
class Dice:
    def __init__(self):
        self.num_rolls = 0
    def roll_two(self):
        return np.random.randint(1,7,size = 2)
    def roll_one(self):
        return np.random.randint(1,7,size = 1)
class LoadGame:
    def __init__(self):
        self.games_address = os.listdir(GAME_LOCATION)
        self.games_list = []
        self.games_address.sort()
        self.num_games = len(self.games_list)
        self.game_file  = None
    def get_num_games(self):return self.num_games
    def play(self,ask = "\nPlese make selection\n"):
        print("\n"*100)
        no_files = False
        idx = 0
        for file in self.games_address:
            if file.endswith(".txt"):
                print("{}. {}".format(idx+1,file))
                no_files = True
                idx += 1
                self.games_list.append(file)
        if not no_files: return PYPARAMETER.ERROR1
        num = int(input(ask))
        try:
            self.game_file = self.games_list[num-1]
            self.load(self.game_file)
        except:
            self.play("\nPlease select the correct number\n")
    def load(self,file_name):
        file = open(GAME_LOCATION+file_name,'rb')
        game = cPickle.load(file)
        file.close()
        print("\n"*100)
        print("Welcome back!\n")
        input("Press any key to continue\n")
        game.play()
class main_menu:
    def __init__(self):
        self.num_mainmenu = 0
    def print_main_menu(self,ask = "Please enter your selection"):
        print("\n"*100)
        print("Welcome to the Monopoly world!\n")

        print("main menu")
        print("1.Start Game")
        print("2.Option")
        print("3.load game")
        print("4.Exit\n")
        selection = input(ask + "\n")
        self.num_mainmenu += 1
        try:
            return int(selection)
        except:
            return self.print_main_menu("Please enter the selection from 1 to 4")
    def exit_monopoly(self):
        print("See you next time!")
PYMENU = main_menu()
class SetOption:
    def __init__(self,dict = None):
        self.maps = []
        self.players = []
        self.dict = dict
        self.num_players = 0
        self.money = 0
        self.playmap = None
        self.play_players = []
        if self.dict:
            try:
                maps_list = self.dict['maps'].split(",")
                for map in maps_list:
                    map = map.strip('\n')
                    map = pyMap(map)
                    self.maps.append(map)
                    if map.get_name() == self.dict["selected_map"].strip("\n"):
                        self.playmap = map
            except:
                print("Fail to load maps from setting.txt")
            try:
                players_list = self.dict['players'].split(",")
                for player_file in players_list:
                    self.players.append(player(player_file.strip('\n')))
            except:
                print("Fail to load players from setting.txt")
            try:
                self.money = int(self.dict['money'].strip("\n"))
                self.num_players = int(self.dict['num_players'].strip("\n"))
            except:
                print("Fail to load money and num of players")
            try:
                selected_player_list = self.dict['select_players'].split(",")
                selected_player_list[-1] = selected_player_list[-1].strip("\n")
                for selected_player in selected_player_list:
                    for search_player in self.players:
                        if selected_player == search_player.get_name():
                                self.play_players.append(search_player)
            except:
                print("Fail to load selected player")

        else:
            print("Error exist in loading settings or there are no default settings")
    def get_players(self): return self.players
    def get_players_names(self): return [player.get_name() for player in self.players]
    def get_maps_names(self): return [map.get_name().strip('\n') for map in self.maps]
    def get_play_map(self):return self.playmap
    def get_play_players_name(self): return [player.get_name() for player in self.play_players]
    def get_play_players(self): return self.play_players
    def selectplayers(self):
        tmp = [player for player in self.players if player not in self.play_players ]
        while self.num_players != len(self.play_players):
            print("\n"*100)
            print("The num of player needed {}".format(self.num_players -len(self.play_players)))
            for idx,player in enumerate(tmp):
                print("{}. {}".format(idx+1,player.get_name()))
            index = int(input("Please input the number\n"))
            if tmp[index-1] not in self.play_players:
                self.play_players.append(tmp[index-1])
            tmp.remove(self.play_players[-1])
        input("\n"*100 + "Players select successful\n" + "Press anything to continue\n")
        return self.play_players
    def removeplayers(self):
        print("\n"*100 + "Please input the player number that you want to remove from selected\n")
        for idx,player in enumerate(self.play_players):
            print("{}. {}".format(idx+1,player.get_name()))
        index = int(input("Please input the number\n"))
        self.play_players.pop(index-1)
    def selectmap(self,ask = "Please input the number\n"):
        tmp = self.maps.copy()
        print("\n"*100 + "Maps")
        for idx,map in enumerate(tmp):
            print("{}. {}".format(idx+1,map.get_name()))
        index = int(input(ask))
        try:
            self.playmap = tmp[index - 1]
        except:
            self.playmap = self.selectmap("Please input correct the number\n")
        input("\n"*100 + "Map select successful\n" + "Press anything to continue\n")
        print("\n"*100)
        return self.playmap
    def create_player(self):
        player_name = input("\n"*100 + "What's your player's name?\n\n")
        player_mark = input("\n"*100 + "What's your player's mark?\n\n")
        new_player = player('',player_name,player_mark)
        new_player.save()
        print("\n"*100 +
        "Create player {} successfully".format(new_player.get_name()))
        return new_player
    def get_player(self,name):
        for player in self.players:
            if player.get_name() == name: return player
        return None
    def save(self):
        map_list = ""
        name_list = ""
        selected_player_list = ""
        f = open(PYPARAMETER.get_optionfile(), "w+")
        for map_name in self.get_maps_names():
            map_list += map_name + ","
        map_list = map_list[:-1]
        f.write("maps:" + map_list + "\n")
        for selected_player in self.play_players:
            selected_player_list += selected_player.get_name() + ","
        selected_player_list = selected_player_list[:-1]
        f.write("select_players:" +selected_player_list + "\n" )
        for player_name in self.get_players_names():
            name_list += player_name + ","
        name_list = name_list[:-1]
        f.write("selected_map:" + self.playmap.get_name() + "\n")
        f.write("players:" + name_list + "\n")
        f.write("money:" + str(self.money) + "\n")
        f.write("num_players:" + str(self.num_players))
        f.close()
        file = open(DATA_LOCATION+'/Settings.txt','wb+')
        cPickle.dump(self,file,0)
        file.close()
    def load(self):
        file = open(DATA_LOCATION+'/Settings.txt','rb')
        self = cPickle.load(file)
        file.close()
        return True
    def play(self):
        print("\n"*100)
        STOP = False
        while not STOP:
            if self.load():
                print("Players: {}".format(self.get_players_names()))
                print("Selected player: {}".format(self.get_play_players_name()))
                print("Maps: {}".format(self.get_maps_names()))
                try:
                    print("Selected Map: {}".format(self.playmap.get_name()))
                except:
                    print("Selected Map: Not selected")
                print("Startup money: {}".format(self.money))
                print("Number of players: {}".format(self.num_players))

            num = self.settings_menu()
            if num == 1:
                player = self.create_player()
                self.players.append(player)
            elif num == 2:
                self.playmap = self.selectmap()
            elif num == 3:
                self.money = int(input("\n"*100 + "Please enter the money"))
            elif num == 4:
                self.num_players = int(input("\n"*100 + "Please enter the number of players\n"))
                self.play_players = self.selectplayers()
            elif num == 5:
                self.removeplayers()
            else:
                STOP = True
                print("Saving settings")
                self.save()
    def settings_menu(self,ask = "Please choose "):
        print("Settings")
        print("1.Create player")
        print("2.Load Map")
        print("3.Set startup money")
        print("4.Set number of player")
        print("5.Remove selected player")
        print("6.Goes Back\n")
        selection = input(ask + "\n")
        try:
            return int(selection)
        except:
            return self.settings_menu("Please enter the selection from 1 to 4")
#state_setting = SetOption(read_dictionary(PYPARAMETER.get_optionfile(),":"))
state_setting = SetOption()
state_setting.load()
class Option_factory:
    def __init__(self,):
        self.parameter = PYPARAMETER
    def factory(self,num):
        state = None
        if num == self.parameter.START_GAME:
            players = state_setting.get_players()
            play_players = state_setting.get_play_players()
            play_map = state_setting.get_play_map()
            num_players = state_setting.num_players
            if not players or len(play_players) != num_players or not play_map:
                print("Please make setting first")
                state = state_setting
            else:
                gameName = input("\n"*100 + "Please name the GAME\n")
                state =  Game(gameName,play_players,play_map)
        elif num == self.parameter.OPTIONS:
            state =  state_setting
        elif num == self.parameter.LOADGAME:
            state =  LoadGame()
        return state
def main():
    STOP = False

    try:
        option_dict = read_dictionary(pyparameter.get_optionfile(),":")
    except:
        print("Fail to read the settings, please set the settings latter")
    while not STOP:
         num = PYMENU.print_main_menu()

         if num == PYPARAMETER.QUIT_PARAMETER:
             STOP = True
             PYMENU.exit_monopoly()
         else:
             option = Option_factory()
             estimator = option.factory(num)
             global Error
             ERROR = estimator.play()
             if ERROR in PYPARAMETER.ERRORS:
                 print("\n"*100)
                 print(ERROR)
                 ERROR = ""
                 input("Press any key to main menu\n")







if __name__ == '__main__':
    main()
