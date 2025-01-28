from enum import Enum
from player import Player


class CardType(Enum):
    NORMAL = 0
    ACTION = 1
    WILD = 2

class Color(Enum):
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    YELLOW = 'yellow'
    WILD = 'wild'


class UnoCard:
    def __init__(self, color, value, card_type):
        self.__color = color
        self.__value = value
        self.__type = card_type

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, newcolor):
        self.__color = newcolor

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newvalue):
        self.__value = newvalue

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, newtype):
        self.__type = newtype
