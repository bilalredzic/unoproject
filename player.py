from enum import Enum

#class Player(Enum):
    #ONE = 0
    #TWO = 1

class Player:
    def __init__(self, name):
        self.__name = name
        self.__hand = []
        self.__is_turn = False

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, newname):
        self.__name = newname

    @property
    def hand(self):
        return self.__hand

    @hand.setter
    def hand(self, new_hand):
        self.__hand = new_hand

    @property
    def is_turn(self):
        return self.__is_turn

    @is_turn.setter
    def is_turn(self, new_is_turn):
        self.__is_turn = new_is_turn
