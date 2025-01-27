from player import Player

class UnoModel:
    def __init__(self):
            #self.board
            self.__player = Player.ONE
            self.__message_code = None

    #def valid_move(self, ):


    #def move(self, ):

    def set_next_player(self):
        if self.current_player == Player.ONE:
            self.__player = Player.TWO
        elif self.current_player == Player.TWO:
            self.__player = Player.ONE