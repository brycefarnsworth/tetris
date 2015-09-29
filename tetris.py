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
BLOCK_TYPES = ['Z', 'L', 'O', 'S', 'I', 'J', 'T']
BLOCK_SPRITES = ["block_red.png", "block_orange.png", "block_yellow.png",
                 "block_green.png", "block_cyan.png", "block_blue.png",
                 "block_purple.png"]


class Grid:
    """ The Tetris grid containing all the blocks. """
    def __init__(self, screen):
        """ Grid consists of 20 rows, but we'll keep 4 extra for blocks to go
        offscreen when the player loses. """
        self.done = False
        self.x = GRID_X
        self.y = GRID_Y
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.grid = [[(0, None) for i in range(10)] for j in range(24)]
        self.screen = screen
        self.center_block = None
        self.falling_blocks = [None, None, None, None]

    def get_center_block(self):
        return self.grid[self.center_block[0]][self.center_block[1]]

    def gen_block(self):
        """ Generates a new block on the grid. """
        new_block = random.randrange(7)
        self.center_block = [4, 4]
        if new_block == 0:
            # Z Block
            self.falling_blocks = [[4, 4], [4, 5], [3, 4], [3, 3]]
        elif new_block == 1:
            # L Block
            self.falling_blocks = [[4, 4], [4, 3], [4, 5], [3, 5]]
        elif new_block == 2:
            # O Block
            self.falling_blocks = [[4, 4], [4, 5], [3, 4], [3, 5]]
        elif new_block == 3:
            # S Block
            self.falling_blocks = [[4, 4], [4, 3], [3, 4], [3, 5]]
        elif new_block == 4:
            # I Block
            self.falling_blocks = [[4, 4], [4, 3], [4, 5], [4, 6]]
        elif new_block == 5:
            # J Block
            self.falling_blocks = [[4, 4], [4, 5], [4, 3], [3, 3]]
        elif new_block == 6:
            # T Block
            self.falling_blocks = [[4, 4], [4, 3], [4, 5], [3, 4]]
        stop = False
        for block in self.falling_blocks:
            if self.grid[block[0]][block[1]][0] == 1:
                stop = True
        if stop:
            self.done = True
        else:
            for block in self.falling_blocks:
                self.grid[block[0]][block[1]] = [-1, BLOCK_SPRITES[new_block]]

    def update(self):
        """ Moves the block down, if possible, otherwise generates a new
        block. """
        stop = False
        for block in self.falling_blocks:
            # Check to see if block can go down
            if block[0] == 23 or self.grid[block[0]+1][block[1]][0] == 1:
                stop = True
        if stop:
            for block in self.falling_blocks:
                self.grid[block[0]][block[1]][0] = 1
            # Check for completed rows
            for i in range(23, 3, -1):
                complete = True
                while complete:
                    for j in range(0, 10):
                        if not self.grid[i][j][0]:
                            complete = False
                    if complete:
                        self.clear_line(i)
            self.gen_block()
        else:
            center = self.get_center_block()
            block_image = center[1]
            for block in self.falling_blocks:
                # Remove blocks from grid
                self.grid[block[0]][block[1]] = [0, None]
            for block in self.falling_blocks:
                # Replace them one space lower on the grid
                block[0] += 1
                self.grid[block[0]][block[1]] = [-1, block_image]
            # Move center
            self.center_block = self.falling_blocks[0]

    def move_left(self):
        """ Move block left, if possible. """
        stop = False
        for block in self.falling_blocks:
            # Check to see if block can go left
            if block[1] == 0 or self.grid[block[0]][block[1]-1][0] == 1:
                stop = True
        if not stop:
            center = self.get_center_block()
            block_image = center[1]
            for block in self.falling_blocks:
                # Remove blocks from grid
                self.grid[block[0]][block[1]] = [0, None]
            for block in self.falling_blocks:
                # Replace blocks one space to the left on the grid
                block[1] -= 1
                self.grid[block[0]][block[1]] = [-1, block_image]
            self.center_block = self.falling_blocks[0]

    def move_right(self):
        """ Move block left, if possible. """
        stop = False
        for block in self.falling_blocks:
            # Check to see if block can go right
            if block[1] == 9 or self.grid[block[0]][block[1]+1][0] == 1:
                stop = True
        if not stop:
            center = self.get_center_block()
            block_image = center[1]
            for block in self.falling_blocks:
                # Remove blocks from grid
                self.grid[block[0]][block[1]] = [0, None]
            for block in self.falling_blocks:
                # Replace blocks one space to the right on the grid
                block[1] += 1
                self.grid[block[0]][block[1]] = [-1, block_image]
            self.center_block = self.falling_blocks[0]

    def rotate_cw(self):
        """ Rotate clockwise, if possible. """
        center = self.get_center_block()
        block_image = center[1]
        if block_image == "block_yellow.png":
            # O Block does not need to rotate
            return
        from_center = []
        for block in self.falling_blocks:
            # Find where each block is relative to the center block
            from_center_y = block[0] - self.center_block[0]
            from_center_x = block[1] - self.center_block[1]
            from_center.append([from_center_y, from_center_x])
        for i in range(len(from_center)):
            # Rotate positions around center block
            new_pos_y = 0
            new_pos_x = 0
            if from_center[i][0] > 0:
                # Block is below center - rotate to the left
                new_pos_x = -from_center[i][0]
            elif from_center[i][0] < 0:
                # Block is above center - rotate to the right
                new_pos_x = -from_center[i][0]
            else:
                # Block is in same row - rotate to same column
                new_pos_x = 0
            if from_center[i][1] > 0:
                # Block is right of center - rotate below
                new_pos_y = from_center[i][1]
            elif from_center[i][1] < 0:
                # Block is left of center - rotate above
                new_pos_y = from_center[i][1]
            else:
                # Block is in same column - rotate to same row
                new_pos_y = 0
            from_center[i] = [new_pos_y, new_pos_x]
        if block_image == "block_cyan.png":
            # Make I Block follow SRS
            count_x = 0
            count_y = 0
            for pos in from_center:
                if pos[0] > 0:
                    count_y += 1
                elif pos[0] < 0:
                    count_y -= 1
                if pos[1] > 0:
                    count_x += 1
                elif pos[1] < 0:
                    count_x -= 1
            current_center = self.center_block
            if count_x > 0:
                self.center_block = [current_center[0] - 1,
                                     current_center[1]]
            elif count_x < 0:
                self.center_block = [current_center[0] + 1,
                                     current_center[1]]
            elif count_y > 0:
                self.center_block = [current_center[0],
                                     current_center[1] + 1]
            elif count_y < 0:
                self.center_block = [current_center[0],
                                     current_center[1] - 1]
        stop = False
        for new_pos in from_center:
            # Check each of the new block positions on the grid
            new_pos_y = self.center_block[0] + new_pos[0]
            new_pos_x = self.center_block[1] + new_pos[1]
            if (new_pos_y < 0 or new_pos_y > 23 or new_pos_x < 0 or
                new_pos_x > 9 or self.grid[new_pos_y][new_pos_x][0] == 1):
                stop = True
        if not stop:
            for block in self.falling_blocks:
                # Remove blocks from grid
                self.grid[block[0]][block[1]] = [0, None]
            for i in range(len(self.falling_blocks)):
                # Replace blocks
                block = self.falling_blocks[i]
                block[0] = self.center_block[0] + from_center[i][0]
                block[1] = self.center_block[1] + from_center[i][1]
                self.grid[block[0]][block[1]] = [-1, block_image]
        else:
            if block_image == "block_cyan.png":
                self.center_block = current_center

    def rotate_ccw(self):
        """ Rotate counter-clockwise, if possible. """
        center = self.get_center_block()
        block_image = center[1]
        if block_image == "block_yellow.png":
            # O Block does not need to rotate
            return
        from_center = []
        for block in self.falling_blocks:
            # Find where each block is relative to the center block
            from_center_y = block[0] - self.center_block[0]
            from_center_x = block[1] - self.center_block[1]
            from_center.append([from_center_y, from_center_x])
        for i in range(len(from_center)):
            # Rotate positions around center block
            new_pos_y = 0
            new_pos_x = 0
            if from_center[i][0] > 0:
                # Block is below center - rotate to the right
                new_pos_x = from_center[i][0]
            elif from_center[i][0] < 0:
                # Block is above center - rotate to the left
                new_pos_x = from_center[i][0]
            else:
                # Block is in same row - rotate to same column
                new_pos_x = 0
            if from_center[i][1] > 0:
                # Block is right of center - rotate above
                new_pos_y = -from_center[i][1]
            elif from_center[i][1] < 0:
                # Block is left of center - rotate below
                new_pos_y = -from_center[i][1]
            else:
                # Block is in same column - rotate to same row
                new_pos_y = 0
            from_center[i] = [new_pos_y, new_pos_x]
        if block_image == "block_cyan.png":
            # Make I Block follow SRS
            count_x = 0
            count_y = 0
            for pos in from_center:
                if pos[0] > 0:
                    count_y += 1
                elif pos[0] < 0:
                    count_y -= 1
                if pos[1] > 0:
                    count_x += 1
                elif pos[1] < 0:
                    count_x -= 1
            current_center = self.center_block
            if count_x > 0:
                self.center_block = [current_center[0],
                                     current_center[1] - 1]
            elif count_x < 0:
                self.center_block = [current_center[0],
                                     current_center[1] + 1]
            elif count_y > 0:
                self.center_block = [current_center[0] - 1,
                                     current_center[1]]
            elif count_y < 0:
                self.center_block = [current_center[0] + 1,
                                     current_center[1]]
        stop = False
        for new_pos in from_center:
            # Check each of the new block positions on the grid
            new_pos_y = self.center_block[0] + new_pos[0]
            new_pos_x = self.center_block[1] + new_pos[1]
            if (new_pos_y < 0 or new_pos_y > 23 or new_pos_x < 0 or
                new_pos_x > 9 or self.grid[new_pos_y][new_pos_x][0] == 1):
                stop = True
        if not stop:
            for block in self.falling_blocks:
                # Remove blocks from grid
                self.grid[block[0]][block[1]] = [0, None]
            for i in range(len(self.falling_blocks)):
                # Replace blocks
                block = self.falling_blocks[i]
                block[0] = self.center_block[0] + from_center[i][0]
                block[1] = self.center_block[1] + from_center[i][1]
                self.grid[block[0]][block[1]] = [-1, block_image]
        else:
            if block_image == "block_cyan.png":
                self.center_block = current_center

    def drop(self):
        i = 0
        stop = False
        while not stop:
            i += 1
            for block in self.falling_blocks:
                if (block[0] + i == 24 or
                    self.grid[block[0]+i][block[1]][0] == 1):
                    stop = True
        center = self.get_center_block()
        block_image = center[1]
        for block in self.falling_blocks:
            # Remove blocks from grid
            self.grid[block[0]][block[1]] = [0, None]
        for block in self.falling_blocks:
            # Replace them to the drop position
            block[0] += i-1
            self.grid[block[0]][block[1]] = [-1, block_image]
        # Move center
        self.center_block = self.falling_blocks[0]
        self.update()

    def clear_line(self, line):
        """ Clear the numbered line and move all blocks above it down. """
        for i in range(line, 3, -1):
            for j in range(0, 10):
                self.grid[i][j] = self.grid[i - 1][j]
        
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

while not grid.done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            grid.done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                grid.rotate_cw()
            if event.key == pygame.K_z:
                grid.rotate_ccw()
            if event.key == pygame.K_SPACE:
                grid.drop()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        grid.move_left()
    if keys[pygame.K_RIGHT]:
        grid.move_right()
    if keys[pygame.K_DOWN]:
        grid.update()

    
    grid.update()

    # Draw the screen
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLACK, [GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT])
    

    # Draw the blocks
    grid.draw()

    pygame.display.flip()
    
    clock.tick(10)

pygame.quit()
