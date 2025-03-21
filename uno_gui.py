import pygame as pg
import pygame_gui as gui
from UnoGame import UnoGame
from card import Color
from player import Player

# Constants
CARD_WIDTH, CARD_HEIGHT = 120, 180
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
player_icon_height, player_icon_width = 30, 60
MARGIN = 10


class UnoGUI:
    def __init__(self):
        pg.init()
        self._screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("UNO")

        self.ui_manager = gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'theme.json')

        self._create_ui_elements()
        self.start_new_game()

    def _create_ui_elements(self):
        draw_card_image_path = "./images/uno_back.png"  # Draw Pile Creation
        draw_card_surface = pg.image.load(draw_card_image_path)
        draw_card_surface = pg.transform.scale(draw_card_surface, (CARD_WIDTH, CARD_HEIGHT))

        # Create an image button
        self.draw_button = gui.elements.UIImage(
            relative_rect=pg.Rect((180, 200), (CARD_WIDTH, CARD_HEIGHT)),  # Position and size
            image_surface=draw_card_surface,
            manager=self.ui_manager
        )

        self.color_dropdown = gui.elements.UIDropDownMenu(
           options_list=['Red', 'Blue', 'Green', 'Yellow'],
           starting_option='Red',
           relative_rect=pg.Rect((650, 400), (120, 40)),
           manager=self.ui_manager
        )
        self.color_dropdown.hide()

        self.message_display = gui.elements.UITextBox(
            html_text="Welcome to Uno!<br>",
            relative_rect=pg.Rect((600, 10), (190, 380)),
            manager=self.ui_manager
        )

        self.play_again_button = gui.elements.UIButton(
            relative_rect=pg.Rect((300, 350), (200, 50)),
            text="Play Again",
            manager=self.ui_manager
        )
        self.play_again_button.hide()

    def start_new_game(self):
        self.game = UnoGame([Player("1"), Player("2"), Player("3")])
        self.game.create_deck()
        self.game.start_game()
        self.game_over = False
        self.winner = None
        self.play_again_button.hide()
        self.message_display.set_text("Welcome to Uno!\n")
        self.card_images = {}
        self.load_Player_Icons()
        self.load_card_images()
        self.message_display.show()
        self.draw_button.show()

    def load_card_images(self):
        color_options = ['red', 'blue', 'green', 'yellow', 'wild']
        number_values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        action_values = ['skip', 'reverse', 'draw_two', 'wild', 'draw_four']

        for color in color_options:
            for number in number_values:
                image_path = f"./images/{color}_{number}.png"
                image = pg.image.load(image_path)
                scaled_image = pg.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
                self.card_images[(color, number)] = scaled_image

            for action in action_values:
                image_path = f"./images/{color}_{action}.png"
                image = pg.image.load(image_path)
                scaled_image = pg.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
                self.card_images[(color, action)] = scaled_image

    def load_Player_Icons(self):
        direction_image_path = f"images/Player_Icons/Direction Right.png"  # PlayerIcon
        direction_surface = pg.image.load(direction_image_path)
        direction_surface = pg.transform.scale(direction_surface, (50, 30))
        self.direction_right_icon = gui.elements.UIImage(
            relative_rect=pg.Rect((5, 15), (50, 30)),  # Position and size
            image_surface=direction_surface,
            manager=self.ui_manager
        )
        direction_image_path = f"images/Player_Icons/Direction Left.png"
        direction_surface = pg.image.load(direction_image_path)
        direction_surface = pg.transform.scale(direction_surface, (50, 30))
        self.direction_left_icon = gui.elements.UIImage(
            relative_rect=pg.Rect((5, 15), (50, 30)),  # Position and size
            image_surface=direction_surface,
            manager=self.ui_manager
        )
        if self.game.direction == 1:
            self.direction_right_icon.show()
            self.direction_left_icon.hide()
        if self.game.direction == -1:
            self.direction_left_icon.show()
            self.direction_right_icon.hide()
        x = 60
        for i in range(1, len(self.game.players)+1):
            if self.game.current_player_index + 1 == i:
                player_i_image_path = f"images/Player_Icons/Active Player Icon({i}).png"
                player_i_surface = pg.image.load(player_i_image_path)
                player_i_surface = pg.transform.scale(player_i_surface, (player_icon_height, player_icon_width))
                self.player_A_icon = gui.elements.UIImage(
                    relative_rect=pg.Rect((x, 0), (player_icon_height, player_icon_width)),  # Position and size
                    image_surface=player_i_surface,
                    manager=self.ui_manager
                )
            else:
                player_i_image_path = f"images/Player_Icons/Player Icon({i}).png"  # PlayerIcon
                player_i_surface = pg.image.load(player_i_image_path)
                player_i_surface = pg.transform.scale(player_i_surface, (player_icon_height, player_icon_width))
                self.player_B_icon = gui.elements.UIImage(
                    relative_rect=pg.Rect((x, 0), (player_icon_height, player_icon_width)),  # Position and size
                    image_surface=player_i_surface,
                    manager=self.ui_manager
            )
            x += 40


    def run_game(self):
        clock = pg.time.Clock()
        running = True

        while running:
            time_delta = clock.tick(30) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                self._handle_event(event)
                self.player_A_icon.hide()
                self.player_B_icon.hide()
                self.load_Player_Icons()

            if self.game_over:
                self._show_win_screen()
            else:
                self._update_display(time_delta)

        pg.quit()

    def _handle_event(self, event):
        if self.game_over:
            if event.type == gui.UI_BUTTON_PRESSED and event.ui_element == self.play_again_button:
                self.start_new_game()
            self.ui_manager.process_events(event)
            return

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_position = pg.mouse.get_pos()
            if self.draw_button.rect.collidepoint(mouse_position):
                self._handle_draw_action()

            self._handle_mouse_click(mouse_position)

        if event.type == gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.draw_button:
                self._handle_draw_action()

        if event.type == gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.color_dropdown:
            chosen_color = event.text.lower()
            self.game.current_color = Color(chosen_color)
            self.color_dropdown.hide()

            if self.game.pending_wild_card.value == "draw_four":
                self.game.draw_four()
            else:
                self.game.next_turn()

            self._update_game_display(f"Color changed to {chosen_color.upper()}")
            self._check_for_win()

        self.ui_manager.process_events(event)

    def _handle_mouse_click(self, position):
        if self.game_over:
            return

        x, y = position
        current_player = self.game.players[self.game.current_player_index]

        if y >= 500 and y <= 500 + CARD_HEIGHT:
            card_index = (x - MARGIN) // (CARD_WIDTH // 2)

            if card_index < len(current_player.hand):
                selected_card = current_player.hand[card_index]
                play_result = self.game.play_card(current_player, selected_card)

                if play_result == "choose_color":
                    self.color_dropdown.show()
                    self.selected_card = selected_card  # Save the wild card for post-color-selection logic
                    self._update_game_display(
                        f"{current_player.name} played {selected_card.value.upper()} - choose a color")
                    return
                elif play_result is not False:
                    self._update_game_display(
                        f"{current_player.name} played {selected_card.color.value} {selected_card.value}")
                else:
                    self._update_game_display(f"{current_player.name} played an invalid move")

        self._check_for_win()

    def _handle_draw_action(self):
        if self.game_over:
            return

        current_player = self.game.players[self.game.current_player_index]

        if len(self.game.deck) > 0:
            drawn_card = self.game.deck.pop()
            current_player.hand.append(drawn_card)
            self._update_game_display(f"{current_player.name} drew a card")
            self.game.next_turn()

        self._check_for_win()

    def _check_for_win(self):
        for player in self.game.players:
            if not player.hand:
                self.game_over = True
                self.winner = player.name

    def _show_win_screen(self):
        """Displays a separate win screen."""
        self._screen.fill((0, 0, 0))

        font = pg.font.Font(None, 64)
        text_surface = font.render(f"{self.winner} WINS!", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self._screen.blit(text_surface, text_rect)
        self.message_display.hide()
        self.draw_button.hide()
        self.direction_right_icon.hide()
        self.direction_left_icon.hide()
        self.player_A_icon.hide()
        self.player_B_icon.hide()
        self.play_again_button.show()
        self.ui_manager.update(0)
        self.ui_manager.draw_ui(self._screen)
        pg.display.update()

    def _update_game_display(self, message):
        current_text = self.message_display.html_text
        new_text = f"{current_text}{message}<br>"
        self.message_display.set_text(new_text)
        pg.display.set_caption(f"UNO - {message}")

    def _update_display(self, time_delta):
        self._screen.fill((40, 40, 40))

        if len(self.game.deck) > 0:
            top_card = self.game.discard_pile[-1]
            self._draw_card(top_card, (350, 200))

        current_player = self.game.players[self.game.current_player_index]

        x_position = MARGIN
        for card in current_player.hand:
            self._draw_card(card, (x_position, 500))
            x_position += CARD_WIDTH // 2

        self.ui_manager.update(time_delta)
        self.ui_manager.draw_ui(self._screen)
        pg.display.update()

    def _draw_card(self, card, position):
        key = (card.color.value if card.color != Color.WILD else 'wild', str(card.value))
        if key in self.card_images:
            self._screen.blit(self.card_images[key], position)


def main():
    game = UnoGUI()
    game.run_game()


if __name__ == "__main__":
    main()
