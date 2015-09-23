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
        self.grid.grid[y][x] = self
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
    def __init__(self, grid, x, y):
        self.grid = grid
        self.x = x
        self.y = y
        self.blocks = []
        self.rotation = 0
        self.rotations = []
        self.bottoms = []
        self.rights = []
        self.lefts = []
        self.falling = True

    def update(self):
        for i in self.bottoms:
            if self.grid.grid[self.blocks[i].x][self.blocks[i].y + 1]:
                self.falling = False
        if self.falling:
            for block in self.blocks:
                # Move blocks down if nothing is in the way
                self.grid.grid[block.y][block.x] = None
                block.y += 1
                block.rect.x, block.rect.y = \
                    self.grid.grid2pix(block.x, block.y)
                self.grid.grid[block.y][block.x] = block
            self.y += 1

    def move_right(self):
        success = True
        for i in self.rights:
            if self.grid.grid[self.blocks[i].x + 1][self.blocks[i].y]:
                success = False
        if success:
            for block in self.blocks:
                # Move blocks right if nothing is in the way
                self.grid.grid[block.y][block.x] = None
                block.x += 1
                block.rect.x, block.rect.y = \
                    self.grid.grid2pix(block.x, block.y)
                self.grid.grid[block.y][block.x] = block
            self.x += 1

    def move_left(self):
        success = True
        for i in self.lefts:
            if self.grid.grid[self.blocks[i].x - 1][self.blocks[i].y]:
                success = False
        if success:
            for block in self.blocks:
                # Move blocks right if nothing is in the way
                self.grid.grid[block.y][block.x] = None
                block.x -= 1
                block.rect.x, block.rect.y = \
                    self.grid.grid2pix(block.x, block.y)
                self.grid.grid[block.y][block.x] = block
            self.x -= 1

    def rotate_cw(self):
        new_rotation = (self.rotation + 1) % len(self.rotations)
        success = True
        for i in range(4):
            # Check where the blocks are rotating on the grid
            new_x = self.x + self.rotations[new_rotation][i][0]
            new_y = self.y + self.rotations[new_rotation][i][1]
            if self.grid.grid[new_y][new_x]:
                # If there is no room, don't rotate
                success = False
        if success:
            # If there is room, rotate:
            self.rotation = new_rotation
            for i in range(4):
                # Remove all blocks from the grid
                self.grid.grid[self.blocks[i].y][self.blocks[i].x] = None
            for i in range(4):
                # Put the blocks back at their new coordinates and change
                # the block accordingly
                self.blocks[i].x = self.rotations[self.rotation][i][0]
                self.blocks[i].y = self.rotations[self.rotation][i][1]
                self.grid.grid[self.blocks[i].y][self.blocks[i].x] = \
                               self.blocks[i]
                self.blocks[i].rect.x, self.blocks[i].rect.y = \
                    self.grid.grid2pix(self.blocks[i].x, self.blocks[i].y)
            self.bottoms = self.rotations[self.rotation][4]
            self.rights = self.rotations[self.rotation][5]
            self.lefts = self.rotations[self.rotation][6]
            
    def rotate_ccw(self):
        new_rotation = (self.rotation - 1) % len(self.rotations)
        success = True
        for i in range(4):
            # Check where the blocks are rotating on the grid
            new_x = self.x + self.rotations[new_rotation][i][0]
            new_y = self.y + self.rotations[new_rotation][i][1]
            if self.grid.grid[new_y][new_x]:
                # If there is no room, don't rotate
                success = False
        if success:
            # If there is room, rotate:
            self.rotation = new_rotation
            for i in range(4):
                # Remove all blocks from the grid
                self.grid.grid[self.blocks[i].y][self.blocks[i].x] = None
            for i in range(4):
                # Put the blocks back at their new coordinates and change
                # the block accordingly
                self.blocks[i].x = self.rotations[self.rotation][i][0]
                self.blocks[i].y = self.rotations[self.rotation][i][1]
                self.grid.grid[self.blocks[i].y][self.blocks[i].x] = \
                               self.blocks[i]
                self.blocks[i].rect.x, self.blocks[i].rect.y = \
                    self.grid.grid2pix(self.blocks[i].x, self.blocks[i].y)
            self.bottoms = self.rotations[self.rotation][4]
            self.rights = self.rotations[self.rotation][5]
            self.lefts = self.rotations[self.rotation][6]
            

class Z_Block(Tetromino):

    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)
        
        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[0]),
                       Block(grid, x+1, y, BLOCK_SPRITES[0]),
                       Block(grid, x, y-1, BLOCK_SPRITES[0]),
                       Block(grid, x-1, y-1, BLOCK_SPRITES[0])]

        """ List of rotations that describe where the other blocks go relative
            to the 'center' block (0, 0). The last element is the list of
            'bottom' blocks, to be checked while the block is falling. """
        self.rotations = [((0, 0), (1, 0), (0, -1), (-1, -1), 
                           [0, 1, 3], [1, 2], [0, 3]), 
                          ((0, 0), (0, 1), (1, 0), (1, -1), 
                           [1, 2], [1, 2, 3], [0, 1, 3]), 
                          ((0, 0), (-1, 0), (0, 1), (1, 1), 
                           [1, 2, 3], [0, 3], [1, 2]), 
                          ((0, 0), (0, -1), (-1, 0), (-1, 1), 
                           [0, 3], [0, 1, 3], [1, 2, 3])]

        self.bottoms = self.rotations[self.rotation][4]
        self.rights = self.rotations[self.rotation][5]
        self.lefts = self.rotations[self.rotation][6]


class L_Block(Tetromino):

    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)
        
        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[1]),
                       Block(grid, x-1, y, BLOCK_SPRITES[1]),
                       Block(grid, x+1, y, BLOCK_SPRITES[1]),
                       Block(grid, x+1, y-1, BLOCK_SPRITES[1])]

        """ List of rotations that describe where the other blocks go relative
            to the 'center' block (0, 0). The last element is the list of
            'bottom' blocks, to be checked while the block is falling. """
        self.rotations = [((0, 0), (-1, 0), (1, 0), (1, -1), 
                           [0, 1, 2], [2, 3], [1, 3]), 
                          ((0, 0), (0, -1), (0, 1), (1, 1), 
                           [2, 3], [0, 1, 3], [0, 1, 2]), 
                          ((0, 0), (1, 0), (-1, 0), (-1, 1), 
                           [0, 1, 3], [1, 3], [2, 3]), 
                          ((0, 0), (0, 1), (0, -1), (-1, -1), 
                           [1, 3], [0, 1, 2], [0, 1, 3])]

        self.bottoms = self.rotations[self.rotation][4]
        self.rights = self.rotations[self.rotation][5]
        self.lefts = self.rotations[self.rotation][6]


class O_Block(Tetromino):

    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)
        
        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[2]),
                       Block(grid, x+1, y, BLOCK_SPRITES[2]),
                       Block(grid, x, y-1, BLOCK_SPRITES[2]),
                       Block(grid, x+1, y-1, BLOCK_SPRITES[2])]

        """ The O-Block only has one possible orientation. """
        self.rotations = [((0, 0) (1, 0), (0, -1), (1, -1), 
                           [0, 1], [1, 3], [0, 2])]

        self.bottoms = self.rotations[self.rotation][4]
        self.rights = self.rotations[self.rotation][5]
        self.lefts = self.rotations[self.rotation][6]


class S_Block(Tetromino):

    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)

        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[3]),
                       Block(grid, x-1, y, BLOCK_SPRITES[3]),
                       Block(grid, x, y-1, BLOCK_SPRITES[3]),
                       Block(grid, x+1, y-1, BLOCK_SPRITES[3])]

        """ List of rotations that describe where the other blocks go relative
            to the 'center' block (0, 0). The last element is the list of
            'bottom' blocks, to be checked while the block is falling. """
        self.rotations = [((0, 0), (-1, 0), (0, -1), (1, -1), 
                           [0, 1, 3], [0, 3], [1, 2]), 
                          ((0, 0), (0, -1), (0, 1), (1, 1), 
                           [0, 3], [1, 2, 3], [0, 1, 3]), 
                          ((0, 0), (1, 0), (0, 1), (-1, 1), 
                           [1, 2, 3], [1, 2], [0, 3]), 
                          ((0, 0), (0, 1), (-1, 0), (-1, -1), 
                           [1, 2], [0, 1, 3], [1, 2, 3])]

        self.bottoms = self.rotations[self.rotation][4]
        self.rights = self.rotations[self.rotation][5]
        self.lefts = self.rotations[self.rotation][6]


class I_Block(Tetromino):

    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)

        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[4]),
                       Block(grid, x-1, y, BLOCK_SPRITES[4]),
                       Block(grid, x+1, y, BLOCK_SPRITES[4]),
                       Block(grid, x+2, y, BLOCK_SPRITES[4])]

        """ The I-Block is a little tricky; its 'center' is not positioned on
            a block. We will just keep track of the 'block' to the top left of
            its 'center' and move every block in relation to that one. """
        self.rotations = [((0, 0), (-1, 0), (1, 0), (2, 0), 
                           [0, 1, 2, 3], [3], [1]), 
                          ((1, 0), (1, -1), (1, 1), (1, 2), 
                           [3], [0, 1, 2, 3], [0, 1, 2, 3]), 
                          ((1, 1), (2, 1), (0, 1), (-1, 1), 
                           [0, 1, 2, 3], [1], [3]), 
                          ((0, 1), (0, 2), (0, 0), (0, -1), 
                           [1], [0, 1, 2, 3], [0, 1, 2, 3])]

        self.bottoms = self.rotations[self.rotation][4]
        self.rights = self.rotations[self.rotation][5]
        self.lefts = self.rotations[self.rotation][6]


class J_Block(Tetromino):

    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)

        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[5]),
                       Block(grid, x+1, y, BLOCK_SPRITES[5]),
                       Block(grid, x-1, y, BLOCK_SPRITES[5]),
                       Block(grid, x-1, y-1, BLOCK_SPRITES[5])]

        """ List of rotations that describe where the other blocks go relative
            to the 'center' block (0, 0). The last element is the list of
            'bottom' blocks, to be checked while the block is falling. """
        self.rotations = [((0, 0), (1, 0), (-1, 0), (-1, -1), 
                           [0, 1, 2], [1, 3], [2, 3]), 
                          ((0, 0), (0, 1), (0, -1), (1, -1), 
                           [1, 3], [0, 1, 3], [0, 1, 2]), 
                          ((0, 0), (-1, 0), (1, 0), (1, 1), 
                           [0, 1, 3], [2, 3], [1, 3]), 
                          ((0, 0), (0, -1), (0, 1), (-1, 1), 
                           [2, 3], [0, 1, 2], [0, 1, 3])]

        self.bottoms = self.rotations[self.rotation][4]
        self.rights = self.rotations[self.rotation][5]
        self.lefts = self.rotations[self.rotation][6]


class T_Block(Tetromino):

    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)

        self.blocks = [Block(grid, x, y, BLOCK_SPRITES[6]),
                       Block(grid, x+1, y, BLOCK_SPRITES[6]),
                       Block(grid, x-1, y, BLOCK_SPRITES[6]),
                       Block(grid, x, y-1, BLOCK_SPRITES[6])]

        """ List of rotations that describe where the other blocks go relative
            to the 'center' block (0, 0). The last element is the list of
            'bottom' blocks, to be checked while the block is falling. """
        self.rotations = [((0, 0), (1, 0), (-1, 0), (0, -1), 
                           [0, 1, 2], [1, 3], [2, 3]), 
                          ((0, 0), (0, 1), (0, -1), (1, 0), 
                           [1, 3], [1, 2, 3], [0, 1, 2]), 
                          ((0, 0), (-1, 0), (1, 0), (0, 1), 
                           [1, 2, 3], [2, 3], [1, 3]), 
                          ((0, 0), (0, -1), (0, 1), (-1, 0), 
                           [2, 3], [0, 1, 2], [1, 2, 3])]

        self.bottoms = self.rotations[self.rotation][4]
        self.rights = self.rotations[self.rotation][5]
        self.lefts = self.rotations[self.rotation][6]


TETROMINOES = [Z_Block, L_Block, O_Block, S_Block, I_Block, J_Block, T_Block]
                       
    
pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

pygame.display.set_caption("Tetris")

grid = Grid()

block_list = pygame.sprite.Group()

clock = pygame.time.Clock()
done = False

falling_block = TETROMINOES[random.randrange(7)](grid, 4, 4)
for block in falling_block.blocks:
    block_list.add(block)

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        falling_block.move_left()
    elif keys[pygame.K_RIGHT]:
        falling_block.move_right()
    elif keys[pygame.K_UP]:
        falling_block.rotate_ccw()
        
    falling_block.update()

    if not falling_block.falling:
        falling_block = TETROMINOES[random.randrange(7)](grid, 4, 4)
        for block in falling_block.blocks:
            block_list.add(block)
    

    # Draw the screen
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLACK, [GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT])

    # Draw the blocks
    block_list.draw(screen)
    

    pygame.display.flip()

    clock.tick(10)

pygame.quit()
