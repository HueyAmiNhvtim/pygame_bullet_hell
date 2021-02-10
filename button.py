import pygame


class Button:
    def __init__(self, main_game, message: str, index, font_size=48):
        self.main_game = main_game
        self.screen = main_game.screen
        self.screen_rect = self.main_game.screen_rect
        self.message = message
        self.bar_width, self.bar_height = (300, 60)
        self.button_color = (0, 58, 7)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("font/TravelingTypewriter.ttf", font_size)

        # Enclose the font with a RECT
        self.bar_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)
        self.bar_surface = pygame.Surface((self.bar_width, self.bar_height))
        self.bar_rect.centerx = self.screen_rect.centerx
        self.bar_rect.y = self.screen_rect.centery + self.bar_width // 4 * index

        self.insert_msg()

    def insert_msg(self):
        self.update_msg()
        self.message_rect = self.message_display.get_rect()
        self.message_rect.center = self.bar_rect.center

    def update_msg(self):
        self.message_display = self.font.render(self.message, True, self.text_color, self.button_color)

    def draw_button(self):
        self.screen.blit(self.bar_surface, self.bar_rect)
        self.screen.blit(self.message_display, self.message_rect)
