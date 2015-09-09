import pygame
import random

BLACK = (0, 0, 0)
GRAY = (140, 140, 140)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLOCK_WIDTH = 25
BLOCK_HEIGHT = 25
MARGIN = 5

GRID_X = 270
GRID_Y = 45
GRID_WIDTH = 260
GRID_HEIGHT = 510

BLOCK_SPRITES = ["block_red.png", "block_orange.png", "block_yellow.png",
                 "block_green.png", "block_cyan.png", "block_blue.png",
                 "block_purple.png"]

class Block(pygame.sprite.Sprite):
    """ Represents a single block of a tetromino. """
    def __init__(self, x, y, img):
        super().__init__()

        self.falling = True

        self.image = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.falling:
            self.rect.y += BLOCK_HEIGHT
            if self.rect.y > GRID_Y + GRID_HEIGHT - MARGIN - BLOCK_HEIGHT:
                self.rect.y = GRID_Y + GRID_HEIGHT - MARGIN - BLOCK_HEIGHT
                self.falling = False


class Tetromino:
    """ Parent class of the tetromino - a group of 4 blocks. """
    def __init__(self):
        self.blocks = []
        

pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

pygame.display.set_caption("Tetris")

# Grid consists of 20 rows, but we'll keep 4 extra for blocks to go
# offscreen when the player loses
grid = [[0] * 10] * 24

block_list = pygame.sprite.Group()

clock = pygame.time.Clock()
done = False

falling_block = Block(375, 50, BLOCK_SPRITES[random.randrange(7)])
block_list.add(falling_block)

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and falling_block.rect.x > GRID_X + MARGIN:
        falling_block.rect.x -= BLOCK_WIDTH
    elif keys[pygame.K_RIGHT] and falling_block.rect.x < GRID_X + GRID_WIDTH - MARGIN - BLOCK_WIDTH:
        falling_block.rect.x += BLOCK_WIDTH

    if not falling_block.falling:
        falling_block = Block(375, 50, BLOCK_SPRITES[random.randrange(7)])
        block_list.add(falling_block)
        
    block_list.update()
    

    # Draw the screen
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLACK, [GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT])

    # Draw the blocks
    block_list.draw(screen)
    

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
