import pygame
from shop import Shop
from player import Player


# Main Function. Instantiates all classes, and has the main game loop
def main():
    pygame.init()
    size = (550, 550)
    screen = pygame.display.set_mode(size)

    # Initializes world and player class and resizes their images
    world = Shop(r"image/Tiles/Layout_Examples/royalShopLayout.png",
                 r"image/Props/PNG/sprBrownPot.png",
                 r"image/Props/PNG/sprBluePot.png",
                 r"music/subway-surfers-theme.mp3")

    world.resize_image()
    player = Player(r"image/Zink/PNG/Zink_Only/sprZinkJumpN.png")
    player.resize_image()

    while True:
        pressed_keys = pygame.key.get_pressed()
        # Quits out of game and raises exception
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise Exception("Process Closed")
            
        # World updates
        world.display_background(screen)
        world.display_items(screen)

        # Player Updates
        player.display_player(screen)
        player.movement(pressed_keys)

        pygame.display.flip()

# A class if Statement
if __name__ == "__main__":
    main()
