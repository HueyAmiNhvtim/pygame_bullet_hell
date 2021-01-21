import pygame


class Button:
    def __init__(self, main_game, message: str):
        self.main_game = main_game
        self.screen = self.main_game.get_rect()

        self.bar_width, self.bar_height = (300, 60)
        self.button_color = (0, 58, 7)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("font/TravelingTypewriter.ttf", 48)

        # Enclose the font with a button
        self.bar_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)
        self.bar_surface = pygame.Surface((self.bar_width, self.bar_height))
        self.bar_rect.center = self.screen.center

        self._insert_msg(message)

    def _insert_msg(self, msg):
        self.message_display = self.font.render(msg, True, self.text_color, self.button_color)
        self.message_rect = self.message_display.get_rect()
        self.message_display.center = self.bar_rect.center

    def draw_button(self):
        self.screen.blit(self.bar_surface, self.bar_rect)
        self.screen.blit(self.message_display, self.message_rect)
