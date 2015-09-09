import pygame

BLACK = (0, 0, 0)
GRAY = (140, 140, 140)

BLOCK_WIDTH = 25
BLOCK_HEIGHT = 25
MARGIN = 5

class Block(pygame.sprite.Sprite):
    """ Represents a single block of a tetromino. """
    def __init__(self, x, y, img):
        super().__init__()

        self.image = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Tetromino:
    """ Parent class of the tetromino - a group of 4 blocks. """
    def __init__(self):
        self.blocks = []
        

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

pygame.display.set_caption("Tetris")

# Grid consists of 20 rows, but we'll keep 4 extra for blocks to go
# offscreen when the player loses
grid = [[0] * 10] * 24
GRID_X = 270
GRID_Y = 45
GRID_HEIGHT = 510
GRID_WIDTH = 260

block_list = pygame.sprite.Group()

block = Block(275, 525, "block_red.png")
block_list.add(block)
block = Block(300, 525, "block_orange.png")
block_list.add(block)
block = Block(325, 525, "block_yellow.png")
block_list.add(block)
block = Block(350, 525, "block_green.png")
block_list.add(block)
block = Block(375, 525, "block_cyan.png")
block_list.add(block)
block = Block(400, 525, "block_blue.png")
block_list.add(block)
block = Block(425, 525, "block_purple.png")
block_list.add(block)

clock = pygame.time.Clock()
done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    # Draw the screen
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLACK, [GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT])

    # Draw the blocks
    block_list.draw(screen)
    

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
