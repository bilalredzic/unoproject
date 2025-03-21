from enum import Enum


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
    def color(self, new_color):
        self.__color = new_color

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, new_type):
        self.__type = new_type
