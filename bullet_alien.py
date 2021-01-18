from pygame.sprite import Sprite
from pygame import Vector2


class BulletAlienUno(Sprite):
    """Bullet for the alien. First time using spritesheet"""
    """I'm guessing that each class is for different patterns"""
    def __init__(self, main_game):
        """Initialize attributes for the alien's boolets"""
        super().__init__()
        self.screen = main_game.screen
        self.settings = main_game.settings
        self.image = main_game.al_bullet_one

        # Start each bullet out of the alien. This is where the alien will shoot the pattern
        self.rect = self.image.get_rect()

        # Vector movement for the bullet
        self.vector = Vector2()
        self.normalized_vector = Vector2()
        # print(self.vector)
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def draw_bullet(self):
        """Draw the boolet"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Generic bullet update in 2D"""
        self.x += self.normalized_vector[0] * self.settings.ali_bullet_speed
        self.y += self.normalized_vector[1] * self.settings.ali_bullet_speed
        self.rect.x = self.x
        self.rect.y = self.y
        # print(self.normalized_vector)


class BulletAlienDos(BulletAlienUno):
    """Exactly same class, just with different image"""
    def __init__(self, main_game):
        super().__init__(main_game)
        self.image = main_game.al_bullet_two


class BulletAlienTres(BulletAlienUno):
    """Exactly same class, just with different image"""
    def __init__(self, main_game):
        super().__init__(main_game)
        self.image = main_game.al_bullet_three

