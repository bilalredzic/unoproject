from player import Player
from card import Color, UnoCard, CardType
import random

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


    def create_deck(self):
        colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
        values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        action_cards = ["skip", "reverse", "draw_two"]
        wild_cards = ["wild", "draw_four"]
        deck = []
        for color in colors:
            deck.append(UnoCard(color, 0, CardType))
            for value in values:
                deck.append(UnoCard(color, value, CardType.NORMAL))
                deck.append(UnoCard(color, value, CardType.NORMAL))

        for color in colors:
            for action in action_cards:
                deck.append(UnoCard(color, action, CardType.ACTION))
                deck.append(UnoCard(color, action, CardType.ACTION))

        for wild in wild_cards:
            for i in range (4):
                deck.append(UnoCard(Color.WILD, wild, CardType.WILD))

        self.deck = deck

    def shuffle_deck(self):
        random.shuffle(self.__deck)

    def deal_cards(self):
        self.shuffle_deck()
        for player in self.players:
            player.hand = []
            for i in range(7):
                player.hand.append(self.deck.pop())

    def start_game(self):
        self.deal_cards()
        while True:
            first_card = self.deck.pop()
            if first_card.type == CardType.NORMAL:
                self.current_color = first_card.color
                break
            else:
                self.deck.append(first_card)

    def next_turn(self):


    def uno_end(self):







