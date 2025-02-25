import pygame
from pygame import mixer


# Creates overworld environment and displays background
class Shop:
    # Constructor
    def __init__(self, shop_image, brown_pot_image, pink_pot_image, shop_song) -> None:
        self.shop_image = pygame.image.load(shop_image).convert_alpha()

        self.brown_pot_image = pygame.image.load(brown_pot_image).convert_alpha()
        self.pink_pot_image = pygame.image.load(pink_pot_image).convert_alpha()

        self.items = [[self.brown_pot_image, 120, 240], [self.pink_pot_image, 415, 325], [self.brown_pot_image, 265, 200]]

        mixer.init()
        mixer.music.load(shop_song)
        mixer.music.play()

    # Resizes the shop to be correct
    def resize_image(self) -> None:
        self.shop_image = pygame.transform.scale(self.shop_image, (550, 550))
        self.brown_pot_image = pygame.transform.scale(self.brown_pot_image, (100, 100))

    # Displays the shop to the screen (royalShopLayout.png)
    def display_background(self, screen) -> None:
        screen.blit(self.shop_image, (0, 0))

    def display_items(self, screen) -> None:
        for item in self.items:
            screen.blit(item[0], (item[1], item[2]))


