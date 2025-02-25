import pygame


# Creates a player object for user control
class Player:
    # Basic Constructor
    # player_image is a link to an image
    def __init__(self, player_image) -> None:
        self.player_image = pygame.image.load(player_image).convert_alpha()
        self.x = 250
        self.y = 250
        self.velocity = .1

    # Resizes image in order to fit background
    def resize_image(self) -> None:
        self.player_image = pygame.transform.scale(self.player_image, (100, 100))

    # Takes all active keys and moves the player based on key presses
    def movement(self, keys) -> None:
        if keys[pygame.K_w]:
            self.y -= self.velocity
        if keys[pygame.K_s]:
            self.y += self.velocity
        if keys[pygame.K_a]:
            self.x -= self.velocity
        if keys[pygame.K_d]:
            self.x += self.velocity

    # Displays player to argument screen
    def display_player(self, screen) -> None:
        screen.blit(self.player_image, (self.x, self.y))

    # This will display the collision rectangle
    def display_collision_rect(self, screen) -> None:
        pygame.draw.rect(screen, (255, 255, 0), self.collision_rect)


