 # The loop is to make sure that the position chosen is not screwed up.
        for alien in self.aliens:
            if alien.rect.y < 0 or alien.rect.y > self.settings.screen_height or alien.rect.x < 0 or alien.rect.x > self.settings.screen_width:
                sys.exit()