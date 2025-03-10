from card import Color, UnoCard, CardType
import random


class UnoGame:
    def __init__(self, players):
        self.__players = players
        self.__deck = []
        self.__discard_pile = []
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
    def discard_pile(self):
        return self.__discard_pile

    @discard_pile.setter
    def discard_pile(self, dis):
        self.__discard_pile = dis

    @property
    def deck(self):
        return self.__deck

    @deck.setter
    def deck(self, new_deck):
        self.__deck = new_deck

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
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        action_cards = ["skip", "reverse", "draw_two"]
        wild_cards = ["wild", "draw_four"]
        deck = []
        for color in colors:
            deck.append(UnoCard(color, 0, CardType.NORMAL))
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

    def shuffle_deck(self):
        random.shuffle(self.deck)
        # print("Shuffled Deck: ", self.deck)  # delete when testing is finished

    def reshuffle(self):
        random.shuffle(self.discard_pile)
        self.deck = self.discard_pile
        self.discard_pile = []
        # print("Reshuffled Deck: ", self.deck)  # delete when testing is finished
        # print(self.discard_pile)  # delete when testing is finished

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
            print(first_card)
            if first_card.type == CardType.NORMAL:
                self.current_color = first_card.color
                self.discard_pile.append(first_card)
                break
            else:
                self.deck.append(first_card)
                print("Retry")

    def next_turn(self):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
        for player in self.players:
            player.is_turn = False
        self.players[self.current_player_index].is_turn = True
        print(f"It Is Now: {self.players[self.current_player_index]} Turn")

    def play_card(self, player, card):
        last_played_card = self.discard_pile[-1]

        is_valid = (card.color == self.current_color or
                    card.value == last_played_card.value or
                    card.color == Color.WILD)

        if is_valid:
            player.hand.remove(card)
            self.discard_pile.append(card)

            if card.color == Color.WILD:
                self.choose_color()
                if card.value == "draw_four":
                    self.draw_four()
                else:
                    self.next_turn()
                return

            self.current_color = card.color

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
            print(f"Invalid move! You can't play {card.color.value} {card.value}")
            return False

    def choose_color(self):
        valid_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
        while True:
            chosen_color = input("Choose a color (red, blue, green, yellow): ").strip().lower()
            color_values = []
            for color in valid_colors:
                color_values.append(color.value)

            if chosen_color in color_values:
                selected_color = None
                for color in valid_colors:
                    if color.value == chosen_color:
                        selected_color = color
                        break

                self.current_color = selected_color
                print(f"Color changed to {self.current_color.value.upper()}")
                return
            else:
                print("Invalid color, try again. Please enter: red, blue, green, or yellow.")

    def skip_player(self):
        skipped_player_index = (self.current_player_index + self.direction) % len(self.players)
        print(f"Skipped {self.players[skipped_player_index].name}")
        self.current_player_index = (skipped_player_index + self.direction) % len(self.players)

    def reverse_direction(self):
        self.direction *= -1
        print("Direction Reversed")

        if len(self.players) == 2:
            self.skip_player()
        else:
            self.next_turn()

    def draw_two(self):
        next_player_index = (self.current_player_index + self.direction) % len(self.players)
        for i in range(2):
            if len(self.__deck) == 0:
                self.reshuffle()
            self.players[next_player_index].hand.append(self.__deck.pop())
        print(f"{self.players[next_player_index].name} Drew 2")
        self.current_player_index = next_player_index
        self.next_turn()

    def draw_four(self):
        next_player_index = (self.current_player_index + self.direction) % len(self.players)
        for i in range(4):
            if len(self.__deck) == 0:
                self.reshuffle()
            self.players[next_player_index].hand.append(self.__deck.pop())
        print(f"{self.players[next_player_index].name} Drew 4")

        self.current_player_index = next_player_index
        self.next_turn()

    # def uno_end(self):
