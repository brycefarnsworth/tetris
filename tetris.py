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

class Grid:
    """ The Tetris grid containing all the blocks. """
    def __init__(self):
        """ Grid consists of 20 rows, but we'll keep 4 extra for blocks to go
        offscreen when the player loses. """
        self.x = GRID_X
        self.y = GRID_Y
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.grid = [[None for i in range(10)] for j in range(24)] 

    def grid2pix(self, x, y):
        """ Converts (x, y) grid coordinates to (x, y) pixel coordinates. """
        if (x < 0 or x > 9 or y < 0 or y > 23):
            try:
                raise IndexError
            except IndexError as inst:
                print("""x index must be between 0 and 9, y index must be
                      between 4 and 23. (%d, %d) not valid.""" % (x, y))
        pix_x = self.x + MARGIN + (x * BLOCK_WIDTH)
        pix_y = self.y + MARGIN + ((y - 4) * BLOCK_HEIGHT)
        return pix_x, pix_y
                      
    def pix2grid(self, x, y):
        """ Converts (x, y) pixel coordinates to (x, y) coordinates on the
        grid. """
        if (x < self.x + MARGIN or x > self.x + self.width - MARGIN or
            y < self.y + MARGIN or y > self.y + self.height - MARGIN):
            try:
                raise Exception("Pixels out of bounds:", x, y)
            except Exception as inst:
                print(inst)
        grid_x = (x - (self.x + MARGIN)) // BLOCK_WIDTH
        grid_y = ((y - (self.y + MARGIN)) // BLOCK_HEIGHT) + 4
        return grid_x, grid_y
    

class Block(pygame.sprite.Sprite):
    """ Represents a single block of a tetromino. """
    def __init__(self, grid, x, y, img):
        super().__init__()

        self.falling = True

        self.grid = grid
        self.x = x
        self.y = y
        self.grid.grid[y][x] = 1
        self.image = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.grid.grid2pix(x, y)

    def update(self):
        if self.falling:
            if self.y >= 23 or self.grid.grid[self.y + 1][self.x]:
                self.falling = False
                self.rect.x, self.rect.y = self.grid.grid2pix(self.x, self.y)
            else:
                self.grid.grid[self.y][self.x] = None
                self.y += 1
                self.grid.grid[self.y][self.x] = self
                self.rect.x, self.rect.y = self.grid.grid2pix(self.x, self.y)
            

class Tetromino:
    """ Parent class of the tetromino - a group of 4 Blocks. """
    def __init__(self):
        self.blocks = []
        self.rotations = []

    def rotate_cw(self):
        pass

    def rotate_ccw(self):
        pass


class S_Block(Tetromino):

    def __init__(self, grid, x, y):
        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[0]),
                       Block(grid, x+1, y, BLOCK_SPRITES[0]),
                       Block(grid, x, y+1, BLOCK_SPRITES[0]),
                       Block(grid, x-1, y+1, BLOCK_SPRITES[0])]


class J_Block(Tetromino):

    def __init__(self, grid, x, y):
        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[1]),
                       Block(grid, x-1, y, BLOCK_SPRITES[1]),
                       Block(grid, x-2, y, BLOCK_SPRITES[1]),
                       Block(grid, x, y+1, BLOCK_SPRITES[1])]


class O_Block(Tetromino):

    def __init__(self, grid, x, y):
        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[2]),
                       Block(grid, x+1, y, BLOCK_SPRITES[2]),
                       Block(grid, x, y+1, BLOCK_SPRITES[2]),
                       Block(grid, x+1, y+1, BLOCK_SPRITES[2])]


class Z_Block(Tetromino):

    def __init__(self, grid, x, y):
        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[3]),
                       Block(grid, x-1, y, BLOCK_SPRITES[3]),
                       Block(grid, x, y+1, BLOCK_SPRITES[3]),
                       Block(grid, x+1, y+1, BLOCK_SPRITES[3])]


class I_Block(Tetromino):

    def __init__(self, grid, x, y):
        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[4]),
                       Block(grid, x, y+1, BLOCK_SPRITES[4]),
                       Block(grid, x, y+2, BLOCK_SPRITES[4]),
                       Block(grid, x, y+3, BLOCK_SPRITES[4])]


class L_Block(Tetromino):

    def __init__(self, grid, x, y):
        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[5]),
                       Block(grid, x, y+1, BLOCK_SPRITES[5]),
                       Block(grid, x+1, y, BLOCK_SPRITES[5]),
                       Block(grid, x+2, y, BLOCK_SPRITES[5])]


class T_Block(Tetromino):

    def __init__(self, grid, x, y):
        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[6]),
                       Block(grid, x+1, y, BLOCK_SPRITES[6]),
                       Block(grid, x-1, y, BLOCK_SPRITES[6]),
                       Block(grid, x, y+1, BLOCK_SPRITES[6])]
                       
    
pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

pygame.display.set_caption("Tetris")

grid = Grid()

block_list = pygame.sprite.Group()

clock = pygame.time.Clock()
done = False

falling_block = Block(grid, 4, 4, BLOCK_SPRITES[random.randrange(7)])
block_list.add(falling_block)

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] and falling_block.x > 0 and
        grid.grid[falling_block.y][falling_block.x-1] == None):
        grid.grid[falling_block.y][falling_block.x] = None
        falling_block.x -= 1
        grid.grid[falling_block.y][falling_block.x] = falling_block
    elif (keys[pygame.K_RIGHT] and falling_block.x < 9 and
          grid.grid[falling_block.y][falling_block.x+1] == None):
        grid.grid[falling_block.y][falling_block.x] = None
        falling_block.x += 1
        grid.grid[falling_block.y][falling_block.x] = falling_block
        
    block_list.update()

    if not falling_block.falling:
        falling_block = Block(grid, 4, 4, BLOCK_SPRITES[random.randrange(7)])
        block_list.add(falling_block)
    

    # Draw the screen
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLACK, [GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT])

    # Draw the blocks
    block_list.draw(screen)
    

    pygame.display.flip()

    clock.tick(10)

pygame.quit()
