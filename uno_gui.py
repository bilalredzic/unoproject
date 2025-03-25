import pygame as pg
import pygame_gui as gui
from UnoGame import UnoGame
from card import Color
from player import Player
import random  # for confetti

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

        self.state = "login"
        self.player_inputs = []
        self.player_count_dropdown = None
        self.name_input_panels = []
        self.submit_button = None
        self.player_icons = []
        self.card_images = {}
        self.scroll_to_bottom_pending = False
        self.card_scroll_offset = 0

        self._create_login_ui()

    def _create_login_ui(self):
        self.player_count_dropdown = gui.elements.UIDropDownMenu(
            options_list=[str(i) for i in range(2, 11)],
            starting_option='2',
            relative_rect=pg.Rect((300, 50), (200, 40)),
            manager=self.ui_manager
        )

        self.submit_button = gui.elements.UIButton(
            relative_rect=pg.Rect((300, 500), (200, 40)),
            text="Start Game",
            manager=self.ui_manager
        )

        self.login_message_display = gui.elements.UITextBox(
            html_text="Enter number of players and names:<br>",
            relative_rect=pg.Rect((250, 10), (300, 30)),
            manager=self.ui_manager,
            object_id="#login_message"
        )

        self.generate_name_inputs(2)

    def generate_name_inputs(self, count):
        for panel in self.name_input_panels:
            panel.kill()
        self.name_input_panels.clear()
        self.player_inputs.clear()

        for i in range(count):
            input_box = gui.elements.UITextEntryLine(
                relative_rect=pg.Rect((300, 120 + i * 40), (200, 30)),
                manager=self.ui_manager
            )
            input_box.set_text(f"Player {i + 1}")
            self.name_input_panels.append(input_box)
            self.player_inputs.append(input_box)

    def start_new_game(self, names):
        self.state = "game"
        self.game = UnoGame([Player(name) for name in names])
        self.game.create_deck()
        self.game.start_game()
        self.game_over = False
        self.winner = None

        self._create_ui_elements()
        self.message_display.set_text("Welcome to Uno!<br>")
        self.load_card_images()
        self.load_Player_Icons()

    def _create_ui_elements(self):
        draw_card_image_path = "./images/uno_back.png"
        draw_card_surface = pg.image.load(draw_card_image_path)
        draw_card_surface = pg.transform.scale(draw_card_surface, (CARD_WIDTH, CARD_HEIGHT))

        self.draw_button = gui.elements.UIImage(
            relative_rect=pg.Rect((180, 200), (CARD_WIDTH, CARD_HEIGHT)),
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

        self.message_panel = gui.elements.UIPanel(
            relative_rect=pg.Rect((580, 10), (210, 380)),
            manager=self.ui_manager
        )

        self.message_display = gui.elements.UITextBox(
            html_text="Welcome to Uno!<br>",
            relative_rect=pg.Rect((10, 10), (190, 360)),
            container=self.message_panel,
            manager=self.ui_manager,
            object_id="#game_log"
        )

        self.play_again_button = gui.elements.UIButton(
            relative_rect=pg.Rect((300, 350), (200, 50)),
            text="Play Again",
            manager=self.ui_manager,
            object_id="#play_again_button"
        )
        self.play_again_button.hide()

        # Direction arrows
        self.direction_right_surface = pg.image.load("images/Player_Icons/Direction Right.png")
        self.direction_right_surface = pg.transform.scale(self.direction_right_surface, (50, 30))
        self.direction_right_icon = gui.elements.UIImage(
            relative_rect=pg.Rect((5, 15), (50, 30)),
            image_surface=self.direction_right_surface,
            manager=self.ui_manager
        )

        self.direction_left_surface = pg.image.load("images/Player_Icons/Direction Left.png")
        self.direction_left_surface = pg.transform.scale(self.direction_left_surface, (50, 30))
        self.direction_left_icon = gui.elements.UIImage(
            relative_rect=pg.Rect((5, 15), (50, 30)),
            image_surface=self.direction_left_surface,
            manager=self.ui_manager
        )

        # Scroll buttons
        self.left_scroll_btn = gui.elements.UIButton(
            relative_rect=pg.Rect((10, 550), (30, 30)),
            text="<",
            manager=self.ui_manager
        )
        self.right_scroll_btn = gui.elements.UIButton(
            relative_rect=pg.Rect((760, 550), (30, 30)),
            text=">",
            manager=self.ui_manager
        )



    def show_blank_screen(self):
        self._screen.fill((40, 40, 40))
        pg.display.flip()
        pg.time.delay(600)

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
        for icon in self.player_icons:
            icon.kill()
        self.player_icons.clear()

        if self.game.direction == 1:
            self.direction_right_icon.show()
            self.direction_left_icon.hide()
        else:
            self.direction_left_icon.show()
            self.direction_right_icon.hide()

        x = 60
        for i, player in enumerate(self.game.players):
            is_active = (i == self.game.current_player_index)
            icon_path = f"images/Player_Icons/Active Player Icon({i + 1}).png" if is_active \
                else f"images/Player_Icons/Player Icon({i + 1}).png"

            surface = pg.image.load(icon_path)
            surface = pg.transform.scale(surface, (player_icon_height, player_icon_width))

            icon = gui.elements.UIImage(
                relative_rect=pg.Rect((x, 0), (player_icon_height, player_icon_width)),
                image_surface=surface,
                manager=self.ui_manager
            )
            self.player_icons.append(icon)
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

            if self.state == "login":
                self._screen.fill((40, 40, 40))
                self.ui_manager.update(time_delta)
                self.ui_manager.draw_ui(self._screen)
                pg.display.update()
                continue

            if self.game_over:
                self._show_win_screen()
            else:
                self.load_Player_Icons()
                self._update_display(time_delta)

        pg.quit()

    def _handle_event(self, event):
        self.ui_manager.process_events(event)

        if self.state == "login":
            if event.type == gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.player_count_dropdown:
                self.generate_name_inputs(int(event.text))
            elif event.type == gui.UI_BUTTON_PRESSED and event.ui_element == self.submit_button:
                names = [box.get_text().strip() for box in self.player_inputs]
                if all(names):
                    for el in [self.player_count_dropdown, self.submit_button,
                               self.login_message_display] + self.name_input_panels:
                        el.hide()
                    self.start_new_game(names)
                else:
                    self.login_message_display.set_text("Please enter a name for each player.")
            return

        if self.game_over:
            if event.type == gui.UI_BUTTON_PRESSED and event.ui_element == self.play_again_button:
                self.play_again_button.hide()
                self._create_login_ui()
                self.state = "login"
            return

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_position = pg.mouse.get_pos()

            # prevent card clicks from registering under buttons
            if self.left_scroll_btn.rect.collidepoint(mouse_position) or self.right_scroll_btn.rect.collidepoint(
                    mouse_position):
                return

            if self.draw_button.rect.collidepoint(mouse_position):
                self._handle_draw_action()
            self._handle_mouse_click(mouse_position)

        if event.type == gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.draw_button:
                self._handle_draw_action()

            # scroll handling
            elif event.ui_element == self.left_scroll_btn:
                self.card_scroll_offset = max(0, self.card_scroll_offset - 60)
                print(f"Scrolled left: {self.card_scroll_offset}")
            elif event.ui_element == self.right_scroll_btn:
                hand = self.game.players[self.game.current_player_index].hand
                max_scroll = max(0, len(hand) * (CARD_WIDTH // 2) - SCREEN_WIDTH + 80)
                self.card_scroll_offset = min(max_scroll, self.card_scroll_offset + 60)
                print(f"Scrolled right: {self.card_scroll_offset}")

        if event.type == gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.color_dropdown:
            chosen_color = event.text.lower()
            self.game.current_color = Color(chosen_color)
            self.color_dropdown.hide()

            if self.game.pending_wild_card.value == "draw_four":
                self.game.draw_four()
            else:
                self.game.next_turn()

            self._update_game_display(f"Color shifted to {chosen_color.upper()}!")
            self.show_blank_screen()
            self._check_for_win()

    def _handle_mouse_click(self, position):
        if self.game_over:
            return
        if self.left_scroll_btn.rect.collidepoint(position) or self.right_scroll_btn.rect.collidepoint(position):
            return  # Don't process this as a card click

        x, y = position
        current_player = self.game.players[self.game.current_player_index]

        if 500 <= y <= 500 + CARD_HEIGHT:
            card_index = (x - MARGIN) // (CARD_WIDTH // 2)
            if card_index < len(current_player.hand):
                selected_card = current_player.hand[card_index]
                play_result = self.game.play_card(current_player, selected_card)

                if play_result == "choose_color":
                    self.color_dropdown.show()
                    self.selected_card = selected_card
                    self._update_game_display(
                        f"{current_player.name} played a Wild card – choose a color!")
                    return
                elif play_result is not False:
                    color = selected_card.color.value.capitalize()
                    value = str(selected_card.value).replace("_", " ").title()

                    msg = (f"🔥 {current_player.name} unleashed a WILD Draw Four!"
                           if value.lower() == "draw four" else
                           f"{current_player.name} played a {color} {value}")
                    self._update_game_display(msg)

                    image_key = (selected_card.color.value if selected_card.color != Color.WILD else 'wild', str(selected_card.value))
                    card_image = self.card_images.get(image_key)
                    start_pos = (x, 500)
                    end_pos = (350, 200)

                    self.show_blank_screen()
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
            self.show_blank_screen()
            self.game.next_turn()

        self._check_for_win()

    def _check_for_win(self):
        for player in self.game.players:
            if not player.hand:
                self.game_over = True
                self.winner = player.name

    def _show_win_screen(self):
        # 🎉 Confetti animation
        confetti = []
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(-400, 0)
            color = [random.randint(100, 255) for _ in range(3)]
            speed = random.uniform(1, 4)
            confetti.append({"pos": [x, y], "color": color, "speed": speed})

        start = pg.time.get_ticks()
        while pg.time.get_ticks() - start < 1500:
            self._screen.fill((0, 0, 0))
            for c in confetti:
                pg.draw.circle(self._screen, c["color"], (int(c["pos"][0]), int(c["pos"][1])), 4)
                c["pos"][1] += c["speed"]

            self.ui_manager.update(0)
            self.ui_manager.draw_ui(self._screen)
            pg.display.flip()
            pg.time.delay(16)

        # Win text
        font = pg.font.Font(None, 64)
        text_surface = font.render(f"{self.winner} WINS!", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self._screen.blit(text_surface, text_rect)
        self.message_display.hide()
        self.draw_button.hide()
        self.direction_right_icon.hide()
        self.direction_left_icon.hide()
        for icon in self.player_icons:
            icon.hide()
        self.play_again_button.show()
        self.ui_manager.update(0)
        self.ui_manager.draw_ui(self._screen)
        pg.display.update()


    def _draw_static_ui(self):
        if len(self.game.deck) > 0:
            top_card = self.game.discard_pile[-1]
            self._draw_card(top_card, (350, 200))

        current_player = self.game.players[self.game.current_player_index]
        x_position = MARGIN - self.card_scroll_offset
        for card in current_player.hand:
            self._draw_card(card, (x_position, 500))
            x_position += CARD_WIDTH // 2

    def _update_game_display(self, message):
        current_text = self.message_display.html_text

        # Highlight important messages
        if "draw four" in message.lower():
            message = f"<font color='#FF4444'><b>{message}</b></font>"
        elif "wild" in message.lower():
            message = f"<font color='#FF66CC'><b>{message}</b></font>"
        elif "wins" in message.lower():
            message = f"<font color='#FFD700'><b>🏆 {message} 🏆</b></font>"

        # Limit to last 10 messages
        lines = current_text.split("<br>")
        if len(lines) > 10:
            lines = lines[-10:]
        new_text = "<br>".join(lines + [message])

        self.message_display.set_text(new_text)
        pg.display.set_caption(f"UNO - {message}")

    def _update_display(self, time_delta):
        self._screen.fill((40, 40, 40))
        self._draw_static_ui()
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

