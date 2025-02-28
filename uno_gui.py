import pygame as pg
import pygame_gui as gui
from UnoGame import UnoGame
from card import Color
from player import Player

# Constants
CARD_WIDTH, CARD_HEIGHT = 120, 180
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MARGIN = 10


class UnoGUI:
    def __init__(self):
        pg.init()
        self._screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("UNO")

        self.game = UnoGame([Player("Player 1"), Player("Player 2")])
        self.game.create_deck()
        self.game.start_game()

        self.ui_manager = gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

        self._create_ui_elements()

        self.selected_card = None
        self.card_images = {}
        self.load_card_images()

    def _create_ui_elements(self):
        # Creates the draw button
        self.draw_button = gui.elements.UIButton(
            relative_rect=pg.Rect((635, 400), (120, 40)),
            text='Draw',
            manager=self.ui_manager
        )

        # self.color_dropdown = gui.elements.UIDropDownMenu(
        #    options_list=['Red', 'Blue', 'Green', 'Yellow'],
        #    starting_option='Red',
        #    relative_rect=pg.Rect((650, 400), (120, 40)),
        #    manager=self.ui_manager
        # )
        # self.color_dropdown.hide()

        # Creates the message box
        self.message_display = gui.elements.UITextBox(
            html_text="Welcome to Uno!<br>",
            relative_rect=pg.Rect((600, 10), (190, 380)),
            manager=self.ui_manager
        )

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

            # Load action and wild card images.
            for action in action_values:
                image_path = f"./images/{color}_{action}.png"
                image = pg.image.load(image_path)
                scaled_image = pg.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
                self.card_images[(color, action)] = scaled_image

    def run_game(self):
        clock = pg.time.Clock()
        running = True

        while running:
            time_delta = clock.tick(30) / 1000.0

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                self._handle_event(event)

            self._update_display(time_delta)

        pg.quit()

    def _handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_position = pg.mouse.get_pos()
            self._handle_mouse_click(mouse_position)

        if event.type == gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.draw_button:
                self._handle_draw_action()

        # if event.type == gui.UI_DROP_DOWN_MENU_CHANGED:
            # if event.ui_element == self.color_dropdown:
                # selected_color = event.text.lower()
                # self.game.current_color = Color(selected_color)
                # self.color_dropdown.hide()
                # self.game.next_turn()

        self.ui_manager.process_events(event)

    def _handle_mouse_click(self, position):
        x, y = position
        current_player = self.game.players[self.game.current_player_index]

        if y >= 500 and y <= 500 + CARD_HEIGHT:
            card_index = (x - MARGIN) // (CARD_WIDTH // 2)

            if card_index < len(current_player.hand):
                selected_card = current_player.hand[card_index]
                if self.game.play_card(current_player, selected_card) is not False:
                    if selected_card.value == "wild":
                        self._update_game_display(f"{current_player.name} played a {selected_card.value}")
                    else:
                        self._update_game_display(f"{current_player.name} played a {selected_card.color.value} {selected_card.value}")
                else:
                    self._update_game_display(f"{current_player.name} played an invalid move")

                # if selected_card.type == "WILD":
                    # self.color_dropdown.show()

    def _handle_draw_action(self):
        current_player = self.game.players[self.game.current_player_index]

        if len(self.game.deck) > 0:
            drawn_card = self.game.deck.pop()
            current_player.hand.append(drawn_card)
            self._update_game_display(f"{current_player.name} drew a card")
            self.game.next_turn()
            self._update_display(0)

    def _update_game_display(self, message):
        current_text = self.message_display.html_text
        new_text = f"{current_text}{message}<br>"
        self.message_display.set_text(new_text)
        pg.display.set_caption(f"UNO - {message}")

    def _update_display(self, time_delta):
        self._screen.fill((40, 40, 40))

        if len(self.game.deck) > 0:
            top_card = self.game.discard_pile[-1]
            self._draw_card(top_card, (350, 250))

        current_player = self.game.players[self.game.current_player_index]

        x_position = MARGIN
        for card in current_player.hand:
            self._draw_card(card, (x_position, 500))
            x_position += CARD_WIDTH // 2

        self.ui_manager.update(time_delta)
        self.ui_manager.draw_ui(self._screen)
        pg.display.update()

    def _draw_card(self, card, position):
        if card.color != Color.WILD:
            color_name = card.color.value
        else:
            color_name = 'wild'
        if isinstance(card.value, int):
            card_value = str(card.value)
        else:
            card_value = card.value
        key = (color_name, card_value)
        card_image = self.card_images.get(key)

        if card_image is not None:
            self._screen.blit(card_image, position)


def main():
    game = UnoGUI()
    game.run_game()


if __name__ == "__main__":
    main()
