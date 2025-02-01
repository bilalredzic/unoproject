from player import Player


class UnoGame:
    def __init__(self, players):
        # self.board
        self.__players = players
        self.__deck = []
        self.__current_color = None
        self.__current_player_index = 0
        self.__direction = 1
        self.__message_code = None

    @property
    def players(self):
        return self.__players

    @players.setter
    def players(self, new):
        self.__players = new

    @property
    def messageCode(self):
        return self.__message_code

    @messageCode.setter
    def messageCode(self, mes):
        self.__message_code = mes

    @property
    def deck(self):
        return self.__deck

    @deck.setter
    def deck(self, newdeck):
        self.__deck = newdeck

    @property
    def current_color(self):
        return self.__current_color

    @current_color.setter
    def current_color(self, newcurrent_color):
        self.__current_color = newcurrent_color

    @property
    def current_player_index(self):
        return self.__current_player_index

    @current_player_index.setter
    def current_player_index(self, newcurrent_player_index):
        self.__current_player_index = newcurrent_player_index

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, newdirection):
        self.__direction = newdirection


    #def create_deck(self):
        colors = ["red", "blue", "green", "yellow"]
        deck = []



