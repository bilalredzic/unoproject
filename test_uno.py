import unittest
from unittest.mock import patch
from card import UnoCard, Color, CardType
from player import Player
from UnoGame import UnoGame

class TestUnoCard(unittest.TestCase):
    def test_card_initialization(self):
        card = UnoCard(Color.RED, 5, CardType.NORMAL)
        self.assertEqual(card.color, Color.RED)
        self.assertEqual(card.value, 5)
        self.assertEqual(card.type, CardType.NORMAL)

    def test_card_type_change(self):
        card = UnoCard(Color.BLUE, "skip", CardType.ACTION)
        card.type = CardType.WILD
        self.assertEqual(card.type, CardType.WILD)

    def test_wild_card_color_change(self):
        card = UnoCard(Color.WILD, "wild", CardType.WILD)
        card.color = Color.RED
        self.assertEqual(card.color, Color.RED)

class TestPlayer(unittest.TestCase):
    def test_player_initialization(self):
        player = Player("Alice")
        self.assertEqual(player.name, "Alice")
        self.assertEqual(len(player.hand), 0)

    def test_player_hand(self):
        player = Player("Bob")
        card = UnoCard(Color.GREEN, 7, CardType.NORMAL)
        player.hand.append(card)
        self.assertEqual(len(player.hand), 1)
        self.assertEqual(player.hand[0].value, 7)

    def test_player_turn_switching(self):
        player1 = Player("Alice")
        player2 = Player("Bob")
        player1.is_turn = True
        player2.is_turn = False

        self.assertTrue(player1.is_turn)
        self.assertFalse(player2.is_turn)

        player1.is_turn = False
        player2.is_turn = True

        self.assertFalse(player1.is_turn)
        self.assertTrue(player2.is_turn)

class TestUnoGame(unittest.TestCase):
    def setUp(self):
        self.players = [Player("Alice"), Player("Bob")]
        self.game = UnoGame(self.players)
        self.game.create_deck()
        self.game.shuffle_deck()
        self.game.deal_cards()
        self.game.start_game()

    def test_deck_size_after_dealing(self):
        expected_deck_size = len(self.game.deck)
        self.assertGreater(expected_deck_size, 0)

    def test_turn_switching(self):
        first_player = self.game.players[self.game.current_player_index]
        self.game.next_turn()
        second_player = self.game.players[self.game.current_player_index]
        self.assertNotEqual(first_player, second_player)

    def test_shuffle_deck(self):
        original_deck = self.game.deck[:]
        self.game.shuffle_deck()
        self.assertNotEqual(original_deck, self.game.deck)

    def test_deal_cards(self):
        for player in self.game.players:
            self.assertEqual(len(player.hand), 7)

    def test_play_valid_card(self):
        player = self.game.players[self.game.current_player_index]
        valid_card = UnoCard(self.game.current_color, 5, CardType.NORMAL)
        player.hand.append(valid_card)

        initial_hand_size = len(player.hand)
        self.game.play_card(player, valid_card)

        self.assertNotIn(valid_card, player.hand)
        self.assertEqual(len(player.hand), initial_hand_size - 1)

    def test_invalid_card_play(self):
        player = self.game.players[self.game.current_player_index]
        invalid_card = UnoCard(Color.GREEN, 5, CardType.NORMAL)
        player.hand.append(invalid_card)

        initial_hand_size = len(player.hand)
        self.game.play_card(player, invalid_card)

        self.assertIn(invalid_card, player.hand)
        self.assertEqual(len(player.hand), initial_hand_size)

    def test_skip_turn_card(self):
        player = self.game.players[self.game.current_player_index]
        skip_card = UnoCard(self.game.current_color, "skip", CardType.ACTION)
        player.hand.append(skip_card)

        initial_player_index = self.game.current_player_index
        total_players = len(self.game.players)

        self.game.play_card(player, skip_card)

        expected_next_player = (initial_player_index + 2) % total_players
        self.assertEqual(self.game.current_player_index, expected_next_player)

    def test_reverse_direction(self):
        player = self.game.players[self.game.current_player_index]
        reverse_card = UnoCard(self.game.current_color, "reverse", CardType.ACTION)
        player.hand.append(reverse_card)

        original_direction = self.game.direction
        self.game.play_card(player, reverse_card)

        self.assertEqual(self.game.direction, -original_direction)

    def test_draw_two_card(self):
        player = self.game.players[self.game.current_player_index]
        next_player = self.game.players[(self.game.current_player_index + 1) % len(self.game.players)]

        draw_two_card = UnoCard(self.game.current_color, "draw_two", CardType.ACTION)
        player.hand.append(draw_two_card)

        initial_next_player_hand = len(next_player.hand)
        self.game.play_card(player, draw_two_card)

        self.assertEqual(len(next_player.hand), initial_next_player_hand + 2)

    @patch("builtins.input", return_value="blue")
    def test_draw_four_card(self, mock_input):
        player = self.game.players[self.game.current_player_index]
        next_player = self.game.players[(self.game.current_player_index + 1) % len(self.game.players)]

        draw_four_card = UnoCard(Color.WILD, "draw_four", CardType.WILD)
        player.hand.append(draw_four_card)

        initial_next_player_hand = len(next_player.hand)

        self.game.play_card(player, draw_four_card)

        self.assertEqual(len(next_player.hand), initial_next_player_hand + 4)
        self.assertEqual(self.game.current_color, Color.BLUE)

    @patch("builtins.input", return_value="blue")
    def test_choose_wild_card_color(self, mock_input):
        player = self.game.players[self.game.current_player_index]
        wild_card = UnoCard(Color.WILD, "wild", CardType.WILD)
        player.hand.append(wild_card)

        self.game.play_card(player, wild_card)
        self.game.choose_color()

        self.assertEqual(self.game.current_color, Color.BLUE)

    def test_reverse_in_two_player_game(self):
        player = self.game.players[self.game.current_player_index]
        reverse_card = UnoCard(self.game.current_color, "reverse", CardType.ACTION)
        player.hand.append(reverse_card)

        initial_player_index = self.game.current_player_index
        self.game.play_card(player, reverse_card)

        self.assertEqual(self.game.current_player_index, initial_player_index)


if __name__ == '__main__':
    unittest.main()
