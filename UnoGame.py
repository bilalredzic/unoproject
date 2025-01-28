from player import Player

class UnoModel:
    def __init__(self, player):
        #self.board
        self.__player = Player.ONE
        self.__message_code = None

    #def valid_move(self, ):


    #def move(self, ):

    @property
    def current_player(self):
        return self.__player

    @current_player.setter
    def current_player(self, new):
        self.__player = new

    @property
    def messageCode(self):
        return self.__message_code

    @messageCode.setter
    def messageCode(self, mes):
        self.__message_code = mes
    def set_next_player(self):
        if self.current_player == Player.ONE:
            self.__player = Player.TWO
        elif self.current_player == Player.TWO:
            self.__player = Player.ONE

