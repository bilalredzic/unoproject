from player import Player
from card import Color, UnoCard, CardType
import random


class UnoGame:
    def __init__(self, players):
        # self.board
        self.__players = players
        self.__deck = []
        self.__spent_deck = []
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
    def deck(self, new_deck):
        self.__deck = new_deck

    @property
    def spent_deck(self):
        return self.__spent_deck

    @spent_deck.setter
    def spent_deck(self, new_spent_deck):
        self.__spent_deck = new_spent_deck

    @property
    def current_color(self):
        return self.__current_color

    @current_color.setter
    def current_color(self, new_current_color):
        self.__current_color = new_current_color

    @property
    def current_player_index(self):
        return self.__current_player_index

    @current_player_index.setter
    def current_player_index(self, new_current_player_index):
        self.__current_player_index = new_current_player_index

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, new_direction):
        self.__direction = new_direction

    # Creates the deck that the players will be drawing from
    def create_deck(self):
        colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
        values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        action_cards = ["skip", "reverse", "draw_two"]
        wild_cards = ["wild", "draw_four"]
        deck = []
        for color in colors:
            deck.append(UnoCard(color, 0, CardType.NORMAL))  # Are we adding an extra 4 zeros when we should be having 4 less zeros? 0 is included in our values list.
            for value in values:
                deck.append(UnoCard(color, value, CardType.NORMAL))
                deck.append(UnoCard(color, value, CardType.NORMAL))

        for color in colors:
            for action in action_cards:
                deck.append(UnoCard(color, action, CardType.ACTION))
                deck.append(UnoCard(color, action, CardType.ACTION))

        for wild in wild_cards:
            for i in range(4):
                deck.append(UnoCard(Color.WILD, wild, CardType.WILD))

        self.deck = deck
        print("Deck Created!")  # delete when testing is finished
        print(deck)  # delete when testing is finished

    def shuffle_deck(self):
        random.shuffle(self.__deck)
        print("Shuffled Deck: ", self.deck)  # delete when testing is finished

    def shuffle_spent_deck(self):
        random.shuffle(self.__spent_deck)
        print("Reshuffled The Deck: ", self.spent_deck)
        self.deck = self.spent_deck
        self.spent_deck = []


    # Deals each player 7 random cards
    def deal_cards(self):
        self.shuffle_deck()
        for player in self.players:
            player.hand = []
            for i in range(7):
                player.hand.append(self.deck.pop())

    # Puts the first card on the table
    def start_game(self):
        self.deal_cards()
        while True:
            first_card = self.deck.pop(random.randrange(len(self.deck)))
            print(first_card)  # delete when testing is finished
            if first_card.type == CardType.NORMAL:
                self.current_color = first_card.color
                print("Success: ", first_card)  # delete when testing is finished
                break
            else:
                self.deck.append(first_card)
                print("Retry")  # delete when testing is finished

    def next_turn(self):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
        for player in self.players:
            player.is_turn = False
        self.players[self.current_player_index].is_turn = True
        print(f"It Is Now: {self.players[self.current_player_index]} Turn")

    # Checks if played card is valid and reacts if it's an action or wild card
    def play_card(self, player, card):
        if card.color == self.__current_color or card.value == self.__deck[-1].value or card.color == Color.WILD:
            player.hand.remove(card)
            self.__deck.append(card)

            if card.color == Color.WILD:
                self.choose_color()
            else:
                self.__current_color = card.color

            if card.value == "skip":
                self.skip_player()
            elif card.value == "reverse":
                self.reverse_direction()
            elif card.value == "draw_two":
                self.draw_two()
            elif card.value == "draw_four":
                self.draw_four()
            else:
                self.next_turn()
        else:
            return False

    # Asks player to choose a color when a WILD is played
    def choose_color(self):
        valid_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
        chosen_color = input("Choose a color (red, blue, green, yellow): ").strip().lower()
        if chosen_color in [color.value for color in valid_colors]:
            self.__current_color = Color(chosen_color)
            print(f"Color changed to {self.__current_color.value.upper()}")
        else:
            print("Invalid color, try again")
            self.choose_color()

# skips the next player
    def skip_player(self):
        next_player_index = (self.current_player_index + self.direction) % len(self.players)
        print(f"Skipped {self.players[next_player_index].name}")
        self.next_turn()

    def reverse_direction(self):
        self.direction *= -1
        print("Direction Reversed")

        if len(self.players) == 2:
            self.next_turn()

    # Makes the next player draw 2 cards
    def draw_two(self):
        next_player_index = (self.current_player_index + self.direction) % len(self.players)
        for i in range(2):
            if self.deck:
                self.players[next_player_index].hand.append(self.deck.pop())
        print(f"{self.players[next_player_index].name} Drew 2")
        self.next_turn()

    # Makes the next player draw 4 cards and the current player choose a color
    def draw_four(self):
        next_player_index = (self.current_player_index + self.direction) % len(self.players)
        for i in range(4):
            if self.deck:
                self.players[next_player_index].hand.append(self.deck.pop())
        print(f"{self.players[next_player_index].name} Drew 4")
        self.choose_color()
        self.next_turn()

    # def uno_end(self):
