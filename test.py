import _pickle as Pickle
import os
CURRENT_LOCATION = os.path.dirname(os.path.abspath(__file__))+"/"
GAME_LOCATION = os.path.dirname(os.path.abspath(__file__)) + "/Data/Games/"
import numpy as np
import os
import _pickle as cPickle
import traceback
CURRENT_LOCATION = os.path.dirname(os.path.abspath(__file__))
DATA_LOCATION = os.path.dirname(os.path.abspath(__file__)) + "/Data"
PLAYER_LOCATION  = os.path.dirname(os.path.abspath(__file__)) + "/Data/Players/"
MAP_LOCATION = os.path.dirname(os.path.abspath(__file__)) + "/Data/Maps/"
GAME_LOCATION = os.path.dirname(os.path.abspath(__file__)) + "/Data/Games/"
Menu_in_Game = [
" The next player is ",
" What do you want to do?",
" 1.Roll Dices",
" 2.Trade property",
" 3.Finish turn",
" 4.Save and Quit"
]
tmp_property ={
 "name": "prop",
 "sell_price": 100,
 "upgrade_price": 50,
 "Special": 0
}
Card_property ={
"name": np.random.choice(["Chance","Welfare"]),
"sell_price": -1,
"upgrade_price": -1,
"Special": 2
}
start_property ={
"name": "Start!",
"sell_price": -1,
"upgrade_price": -1,
"Special": 1
}

def empty_screen():
    print("\n"*100)
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
        self.dimx = 150
        self.dimy = 61
    def get_QUIT_PARAMETER(self): return self.QUIT_PARAMETER
    def get_START_GAME(self): return self.START_GAME
    def get_OPTIONS(self): return self.OPTIONS
    def get_LOADMAP(self): return self.LOADMAP
    def get_optionfile(self):return self.optionfile
    def save_settings(self,settings): self.settings = settings
    def get_settings(self): return self.settings
PYPARAMETER = Parameter()
class Dice:
    def __init__(self):
        self.num_rolls = 0
    def roll_two(self):
        return np.random.randint(1,7,size = 2)
    def roll_one(self):
        return np.random.randint(1,7,size = 1)
class Player:
    def __init__(self,player_file = '',name = '', mark = ''):
        if player_file != '':
            self.dict = read_dictionary(PLAYER_LOCATION +player_file,":")
            self.name = self.dict['name'].strip('\n').strip(" ")
            self.mark = self.dict['mark'].strip('\n').strip(" ")
            self.games_palyed = int(self.dict['games_played'].strip('\n').strip(" "))
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
class Loading():
    def __init__(self):
        self.setting_address = DATA_LOCATION+'/Settings.txt'
        self.normal_map = MAP_LOCATION+'normal.txt'
    def loads(self,str):
        if str == "settings":
            address = self.setting_address
        elif str == "default map":
            address = self.normal_map
        file = open(address,'rb')
        pyclass = cPickle.load(file)
        file.close()
        return pyclass
    def load_map(self,str):
        file = open(MAP_LOCATION+str,'rb')
        pyclass = cPickle.load(file)
        file.close()
        return pyclass
pyLoad = Loading()
class Property:
    def __init__(self,dict):
        self.name = dict['name']
        self.sell_price = int(dict['sell_price'])
        self.owner = None
        self.upgrade_price = int(dict["upgrade_price"])
        self._status = 0 #1 = 1 building 2 = 2 building 5 = hotel
        self.price = (self._status+1) * self.upgrade_price
        self.idx = None
    def get_name(self): return self.name
    def get_sell_price(self): return self.sell_price
    def get_owner(self): return self.owner
    def get_upgrade_price(self): return self.upgrade_price
    def get_price(self):
        self.price = (self._status+1) * self.upgrade_price
        return self.price
    def sale_to(self,player,idx):
        check = False
        if player.money - self.sell_price > 0:
            check = True
            player.money -= self.sell_price
            self.owner = player
            self.idx = idx
        return player,check
    def collect_price(self,owner,player):
        self.owner = owner
        if player.money < self.price:
            self.owner.money += player.money
            player.money = 0
            return self.owner,None
        else:
            player.money -= self.price
            self.owner += self.price
            return self.onwer,player
    def upgrade_building(self,player):
        self.owner = player
        if self.onwer.money < self.upgrade_price:
            return self.owner, -1
        if self._status == 5:
            return self.owner,-2
        else:
            self.onwer.money -= self.upgrade_price
            self._status += 1
            self.price = (self._status+1) * self.upgrade_price
            return self.owner,True
    def Mortgaging(self,player):
        self.owner = player
        self.owner.money += int(self.sale_price/2)
        self._status = -1
        return self.owner
    def clear_mortgage(self,player):
        self.owner = player
        if self.owner.money < int(self.sale_price* 1.1/2):
            return self.owner,False
        else:
            self.owner.moneu -= int(self.sale_price* 1.1/2)
            self._status = 1
class cards:
    def __init__(self,chance = [3000,2000,1000,2400,1500,-1250,-50,-150,-200],welfare = [1000,2000,1500,-100,-50,-150,-200]):
        self.chance = chance
        self.welfare = welfare
    def draw_chance(self,player):
        return np.random.choice(self.chance)
    def draw_welfare(self):
        return np.random.choice(self.welfare)
class pyMap:
    def __init__(self,map_name):
        self.mapname = map_name
        self.properties_list = []
    def get_name(self): return self.mapname
    def get_info(self):
        return self.properties_list.copy()
    def save(self):
        file = open(MAP_LOCATION+str(self.mapname)+'.txt','wb+')
        cPickle.dump(self,file,0)
        file.close()
class Game:
    def __init__(self,gameName,state_setting):
        self.players = state_setting.get_play_players()
        self.cplayer_idx = np.random.randint(len(self.players))
        self.cplayer = self.players[self.cplayer_idx]
        self.cplayer_location = [0 for _ in range(len(self.players))]
        self.cmoved = False
        self.map = state_setting.get_play_map()
        self.properties = self.map.get_info()
        self.players_own_properties = [ []* len(self.players)]
        self.map_size = len(self.properties)
        self.name = gameName
        self.dice = Dice()
        self.cards = cards()
        self.start_money = state_setting.money
        self.player_names = []
        self.player_money = []
        self.termnial_controller = - 1
        for player in self.players:
            player.money = self.start_money
            self.player_names.append(player.get_name())
            self.player_money.append(self.start_money)
        self.loop_reward = self.start_money* 0.2
        self.map_list = np.zeros((PYPARAMETER.dimy, PYPARAMETER.dimx),dtype = "str")
        self.MAP_XY_TO_IDX = []
        for i in range(10):
            self.MAP_XY_TO_IDX.append([55,136-i*15])
        for i in range(1,10):
            self.MAP_XY_TO_IDX.append([55-i*6,1])
        for i in range(1,10):
            self.MAP_XY_TO_IDX.append([1,1+i*15])
        for i in range(1,9):
            self.MAP_XY_TO_IDX.append([1+ i*6,136])
    def play(self):
        while self.termnial_controller != 4 :
            empty_screen()
            self.termnial_controller = self.display_map(0)
            if self.termnial_controller == 1:  #roll dice
                if self.cmoved == False:
                    dice = self.roll_dice()
                    self.cmoved = True
                    tmp = self.display_map(1,dice)
                    finish_around = self.move(dice)
                    if finish_around:
                        self.display_map(2)
                    tmp = self.display_map(1,dice)
                    self.triger_loc()
                    self.cmoved = not (dice[0] == dice[1])
                else:
                    self.display_map(-1)  # -1 for double move
            elif self.termnial_controller == 2 : #trade
                self.trade()
            elif self.termnial_controller == 3 :
                self.switch_player()
            self.update()
        self.update()
        self.save()
    def update(self):
        self.player_money =  [player.money for player in self.players]
        self.players_own_properties = [ []* len(self.players)]
        for property in self.properties:
            owner = property.get_owner()
            if owner == None:
                pass
            else:
                owner_name = owner.get_name()
                try:
                    owner_name_idx = self.player_names.index(owner_name)
                    self.players_own_properties[owner_name_idx].append(property)
                except:
                    print("no owner name")
    def triger_loc(self):
        property = self.properties[self.cplayer_location[self.cplayer_idx]]
        try:
            owner,owner_idx = property.get_owner()
            loc_player = self.players[self.cplayer_idx]
            if owner.get_name()!= loc_player.get_name():
                money_to_pay = property.get_price()
                owner,loc_player = property.collect_price(owner,loc_player)
                self.players[owner_idx] = owner
                self.players[self.cplayer_idx] = loc_player
        except:
            pass
        if property.get_name() not in ["Chance","Welfare"]:
            answer = self.display_map(3)
            if answer == 1:
                self.players[self.cplayer_idx],check = property.sale_to(self.players[self.cplayer_idx],self.cplayer_idx)
                if not check:
                    print("Not enough money to purchase")
                else:
                    print("successfully buy the property")
            else:
                pass
            input("Press any key to continues\n")
        elif property.get_name() in ["Chance","Welfare"]:
            money = self.cards.draw_chance() if property.get_name() == "Chance" else self.cards.draw_welfare()
            print("You draw a card, and get {}!".format(money))
            self.players[self.cplayer_idx].money += money
            input("Press any key to continues\n")
    def roll_dice(self):
        return self.dice.roll_two()
    def game_main_menu(self,idx):
        my_line = "     "
        menu_idx = 6 - len(self.map_list) + idx
        if menu_idx == 0:
            my_line += Menu_in_Game[ menu_idx] + self.cplayer.get_name()
        else:
            my_line += Menu_in_Game[ menu_idx]
        return my_line
    def move(self,dice):
        step = sum(dice)
        self.cplayer_location[self.cplayer_idx] += step
        if self.cplayer_location[self.cplayer_idx] >= self.map_size:
            self.cplayer_location[self.cplayer_idx] -= self.map_size
            return True
        return False
    def display_map(self,spares_type,dice = None):
        self.update_map_list()
        my_line = ''
        for idx,line in enumerate(self.map_list):
            for c in line:
                my_line += ' ' if c == '' else c
            if idx == 0:
                my_line+= "      Map name:  {0:<15}".format(self.map.get_name())
            elif idx-1 < len(self.player_names):
                player_name = self.player_names[idx - 1]
                player_money = self.player_money[idx - 1]
                player_mark = self.players[idx-1]
                my_line += "      {0}{1:<15} : {2:<15}".format(player_mark.get_mark(),player_name,player_money)
            elif spares_type == 0:
                if idx >= len(self.map_list) - 6:
                   my_line +=self.game_main_menu(idx)
            elif spares_type == 1 and dice is not None:
                if idx == len(self.map_list) - 6:
                    my_line += "  You roll a {} and a {}".format(dice[0],dice[1])
                elif idx == len(self.map_list) - 5:
                    my_line += "  Moving forward {}".format(sum(dice))
            elif spares_type == -1:
                if idx == len(self.map_list) - 6:
                    my_line += "  You have moved already!"
            elif spares_type == 2:
                if idx == len(self.map_list) - 6:
                    my_line += "  Congradulation, You have went a round!"
                if idx == len(self.map_list) - 5:
                    my_line += "  You earn {}!".format(self.loop_reward)
            elif spares_type == 3:
                if idx == len(self.map_list) - 6:
                    my_line += "  Do you want to buy this property?"
                if idx == len(self.map_list) - 5:
                    my_line += "  0 for no and 1 for yes"
            my_line += "\n"
        print(my_line)
        answer = input("Press  correct number or other key to continues\n")
        try:
            answer = int(answer)
        except:
            answer = None
        return answer
    def switch_player(self):
        try:
            self.cplayer_idx += 1
            self.cplayer = self.players[self.cplayer_idx]
        except:
            self.cplayer_idx = 0
            self.cplayer = self.players[self.cplayer_idx]
        self.cmoved = False
    def update_map_list(self):
        self.map_list = np.zeros((PYPARAMETER.dimy, PYPARAMETER.dimx),dtype = "str")
        for y in range(PYPARAMETER.dimy):
            if y == 0 or y == (PYPARAMETER.dimy - 1):
                 self.map_list[y,:] = "*"
                 #["*" * PYPARAMETER.dimx]
            elif y%6 == 0 and (y//6 == 1 or y//6 == 9):
                self.map_list[y,:] = "*"
                #["*" * PYPARAMETER.dimx]
            elif y%6 == 0:
                self.map_list[y,0:15] = "*"
                self.map_list[y,-15:-1] = "*"
                self.map_list[y,-1] = "*"
            else:
                self.map_list[y,0] = "*"
                self.map_list[y,-1] = "*"
        for x in range(PYPARAMETER.dimx):
            if x%15 == 0 and (x//15 == 1 or x//15 == 9):
                self.map_list[:,x] = "*"
            elif x%15 == 0:
                self.map_list[0:6,x] = "*"
                self.map_list[-6:-1,x] = "*"
        for idx,YX in enumerate(self.MAP_XY_TO_IDX):
            y,x= YX
            property_name = self.properties[idx].get_name()
            property_price = self.properties[idx].get_sell_price()
            property_price = str(property_price) if property_price >= 0 else ""
            property_marker = self.properties[idx].get_owner().get_mark() if self.properties[idx].get_owner()!=None else None
            for str_idx in range(8):
                if property_marker != None and str_idx == 0:
                    self.map_list[y,x+str_idx] = property_marker
                elif str_idx > 0 :
                    try:
                        self.map_list[y,x+str_idx] = property_name[str_idx-1]
                    except:
                        break

            for str_idx in range(7):
                try:
                    self.map_list[y,x+8+str_idx] = property_price[str_idx]
                except:
                    break
        for idx,loc in enumerate(self.cplayer_location):
            marker = self.players[idx].get_mark()
            y,x = self.MAP_XY_TO_IDX[loc]
            self.map_list[y+1,x+idx] = marker
    def save(self):
        file = open(GAME_LOCATION+str(self.name)+'.txt','wb+')
        cPickle.dump(self,file,0)
        file.close()
    def load(self):
        file = open(GAME_LOCATION+self.name+'.txt','rb')
        dataPickle = file.read()
        file.close()
        self.__dict__ = cPickle.loads(dataPickle)

class LoadGame:
    def __init__(self):
        self.games_address = os.listdir(GAME_LOCATION)
        self.games_list = []
        self.games_address.sort()
        self.num_games = len(self.games_list)
        self.game_file  = None
    def get_num_games(self):return self.num_games
    def play(self,ask = "\nPlease make selection\n"):
        print("\n"*100)
        no_files = False
        idx = 0
        print("Load Games: \n")
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
            game = self.load(self.game_file)
        except:
            self.play("\nPlease select the correct number\n")
    def load(self,file_name):
        file = open(GAME_LOCATION+file_name,'rb')
        game = cPickle.load(file)
        file.close()
        empty_screen()
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
    def __init__(self):
        self.maps = []
        self.players = []
        self.dict = dict
        self.num_players = 0
        self.money = 0
        self.playmap = None
        self.play_players = []
        self.maps_address = os.listdir(MAP_LOCATION)
        self.players_address= os.listdir(PLAYER_LOCATION)
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
            try:
                if tmp[index-1] not in self.play_players:
                    self.play_players.append(tmp[index-1])
                tmp.remove(self.play_players[-1])
            except:
                print("Please select true index\n")
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
        if tmp:
            for idx,map in enumerate(tmp):
                print("{}. {}".format(idx+1,map.get_name()))
            index = int(input(ask))
        else:
            print("There is no data of maps")
            return None
        try:
            self.playmap = pyLoad.load_map(tmp[index - 1].get_name())
        except:
            self.playmap = self.selectmap("Please input correct the number\n")
        input("\n"*100 + "Map select successful\n" + "Press anything to continue\n")
        print("\n"*100)
        return self.playmap
    def create_player(self):
        player_name = input("\n"*100 + "What's your player's name?\n\n")
        player_mark = input("\n"*100 + "What's your player's mark?\n\n")
        new_player = Player('',player_name,player_mark)
        new_player.save()
        print("\n"*100 +"Create player {} successfully".format(new_player.get_name()))
        return new_player
    def get_player(self,name):
        for player in self.players:
            if player.get_name() == name: return player
        return None
    def save(self):
        file = open(DATA_LOCATION+'/Settings.txt','wb+')
        cPickle.dump(self,file,0)
        file.close()
    def load(self):
        try:
            file = open(DATA_LOCATION+'/Settings.txt','rb')
            self = cPickle.load(file)
            file.close()
            return True
        except:
            return False
    def play(self):
        print("\n"*100)
        STOP = False
        for file in self.maps_address:
            if file.endswith(".txt"):
                new_map = pyMap(file)
                if new_map.get_name() not in self.get_maps_names():
                    self.maps.append(new_map)
        for player_file in self.players_address:
            if player_file.endswith(".txt"):
                new_player = Player(player_file,'','')
                if new_player.get_name() not in self.get_players_names():
                    self.players.append(new_player)
        while not STOP:
            print("Settings\n")
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
                self.money = int(input("\n"*100 + "Please enter the money\n"))
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
            return self.settings_menu("Please enter the selection from 1 to 6")
class Option_factory:
    def __init__(self):
        self.parameter = PYPARAMETER
    def factory(self,num):
        state = None
        try:
            #Initie the SetOption()
            #state_setting = SetOption()
            #state_setting.save()
            state_setting = pyLoad.loads("settings")
        except:
            state_setting = SetOption()
            print("No setting file found\n")
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
                state =  Game(gameName,state_setting)
        elif num == self.parameter.OPTIONS:
            state =  state_setting
        elif num == self.parameter.LOADGAME:
            state =  LoadGame()
        return state
def main():
    STOP = False
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
    file = open(GAME_LOCATION+"1.txt",'rb')
    game = Pickle.load(file)
    file.close()
    game.play()
