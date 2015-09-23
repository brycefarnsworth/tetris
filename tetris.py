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

# In order: Z, L, O, S, I, J, T
BLOCK_SPRITES = ["block_red.png", "block_orange.png", "block_yellow.png",
                 "block_green.png", "block_cyan.png", "block_blue.png",
                 "block_purple.png"]

class Grid:
    """ The Tetris grid containing all the blocks. """
    def __init__(self, screen):
        """ Grid consists of 20 rows, but we'll keep 4 extra for blocks to go
        offscreen when the player loses. """
        self.x = GRID_X
        self.y = GRID_Y
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.grid = [[(0, None) for i in range(10)] for j in range(24)]
        self.screen = screen
        self.falling_block = None

    def gen_block(self):
        """ Generates a new block on the grid. """
        new_block = random.randrange(7)
        self.falling_block = [4, 4, BLOCK_SPRITES[new_block]]
        self.grid[4][4] = (-1, BLOCK_SPRITES[new_block])

    def update(self):
        """ Moves the block down, if possible, otherwise generates a new
        block. """
        y = self.falling_block[0]
        x = self.falling_block[1]
        block_image = self.falling_block[2]
        if y == 23 or self.grid[y+1][x][0]:
            self.grid[y][x] = (1, block_image)
            self.gen_block()
        else:
            self.grid[y][x] = (0, None)
            self.grid[y+1][x] = (-1, block_image)
            self.falling_block[0] = y + 1

    def move_left(self):
        """ Move block left, if possible. """
        y = self.falling_block[0]
        x = self.falling_block[1]
        block_image = self.falling_block[2]
        if x > 0 and not self.grid[y][x-1][0]:
            self.grid[y][x] = (0, None)
            self.grid[y][x-1] = (-1, block_image)
            self.falling_block[1] = x - 1

    def move_right(self):
        """ Move block left, if possible. """
        y = self.falling_block[0]
        x = self.falling_block[1]
        block_image = self.falling_block[2]
        if x < 9 and not self.grid[y][x+1][0]:
            self.grid[y][x] = (0, None)
            self.grid[y][x+1] = (-1, block_image)
            self.falling_block[1] = x + 1

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

    def draw(self):
        """ Draws every block currently on the screen. """
        for row in range(4, 24):
            for col in range(0, 10):
                if self.grid[row][col][0]:
                    x, y = self.grid2pix(col, row)
                    block_image = pygame.image.load(self.grid[row][col][1]) \
                                  .convert()
                    self.screen.blit(block_image,
                                     [x, y, BLOCK_WIDTH, BLOCK_HEIGHT])
    
  
pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

pygame.display.set_caption("Tetris")

grid = Grid(screen)
grid.gen_block()

clock = pygame.time.Clock()
done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        grid.move_left()
    if keys[pygame.K_RIGHT]:
        grid.move_right()

    
    grid.update()

    # Draw the screen
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLACK, [GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT])
    

    # Draw the blocks
    grid.draw()

    pygame.display.flip()
    

    clock.tick(10)

pygame.quit()
