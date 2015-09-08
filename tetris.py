import pygame

class Block(pygame.sprite.Sprite):
    """ Represents a single block of a tetromino. """
    def __init__(self, x, y, img):
        super().__init__()

        self.image = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

pygame.display.set_caption("Tetris")

background_image = pygame.image.load("tetris_screen.png").convert()

clock = pygame.time.Clock()
done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.blit(background_image, [0, 0])

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
