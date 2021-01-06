import pygame


class Boolet:
    def __init__(self, background, ship):
        self.background = background
        self.ship = ship
        self.shiprect = self.ship.coin_rect
        self.width = 20
        self.height = 20
        self.dy = 1
        self.x = self.ship.x + self.shiprect.width / 2 - self.width / 2
        self.y = self.ship.y - self.height
        self.boolet_shape = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.background, (0, 0, 0), self.boolet_shape)

    def _boolet_out(self):
        pygame.draw.rect(self.background, (0, 0, 0), self.boolet_shape)
        pygame.display.update(self.boolet_shape)

    def boolet_move(self):
        while self.y >= 0:
            self.y -= self.dy
            self.boolet_shape.y = self.y
            self._boolet_out()

