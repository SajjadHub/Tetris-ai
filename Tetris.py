import sys
import pygame
import random

# Global variables
row = 24
col = 10
cell = 30

# Colours for pygame display
colours = [
    (0,   0,   0),
    (255, 0,   0),
    (0,   150, 0),
    (0,   0,   255),
    (255, 120, 0),
    (255, 255, 0),
    (180, 0,   255),
    (0,   220, 220)
]

# scores according to original nintendo scoring (pre line clear)
scores = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}

# Define the shapes of the single parts
shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]


def joinMatrixes(mat1, mat2, mat2_off):
    """Adds a piece (mat2) to the board"""
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1][cx+off_x] += val
    return mat1


def rotateClockwise(shape):
    """Rotates a piece"""
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


def removeRow(board, row):
    """Deletes a row and adds new one to the top"""
    del board[row]
    return [[0 for i in range(col)]] + board


def checkCollision(board, stone):
    """Checks if there is a collision"""
    if stone.y + len(stone.shape) - 1 >= row:
        return True
    for j, rows in enumerate(stone.shape):
        for i, cell in enumerate(rows):
            if cell and board[j + stone.y][i + stone.x]:
                return True
    return False


class Stone():
    """Stone class holds shape and position (offset)"""

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape


class Tetris():
    """Tetris app"""

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(6, 3)
        self.width = col*cell
        self.height = row*cell
        self.bagIndex = 0
        self.bagShapes = []
        for i in range(len(shapes)):
            self.bagShapes.append(random.choice(shapes))
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.createBoard()

    def createBoard(self):
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

    def createStone(self):
        """Creates stone and places it at the top of the board if it can"""
        self.stone = Stone(int(col/2 - 1), 0, random.choice(shapes))

        if checkCollision(self.board, self.stone):
            self.gameover = True

    def rotateStone(self):
        temp = self.stone.shape
        newShape = rotateClockwise(self.stone.shape)
        newShape = rotateClockwise(newShape)
        newShape = rotateClockwise(newShape)
        self.stone.shape = newShape
        if checkCollision(self.board, self.stone):
            self.stone.shape = temp

    def drawGame(self, mat, offset):
        """Renders the matrix on the display"""
        offx, offy = offset
        for y, row in enumerate(mat):
            for x, val in enumerate(row):
                pygame.draw.rect(self.screen, colours[val], pygame.Rect(
                    (offx+x) * cell, (offy+y) * cell, cell, cell))

    def clearGame(self, mat, offset):
        """Clears the matrix from the display"""
        offx, offy = offset
        for y, row in enumerate(mat):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, colours[0], pygame.Rect(
                        (offx+x) * cell, (offy+y) * cell, cell, cell))

    def drop(self):
        """Drops piece and updates score"""
        lines = 0
        self.clearGame(self.stone.shape, (self.stone.x, self.stone.y))
        self.stone.y += 1
        if checkCollision(self.board, self.stone):
            self.board = joinMatrixes(
                self.board, self.stone.shape, (self.stone.x, self.stone.y))
            for i, row in enumerate(self.board):
                if 0 not in row:
                    lines += 1
                    self.clearGame(self.board, (0, 0))
                    del self.board[i]
                    self.board.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                    self.drawGame(self.board, (0, 0))

            self.score += scores[lines]
            print(self.score)
            self.createStone()

    def move(self, dir):
        """Slides stone left and right"""
        temp = self.stone.x
        newX = self.stone.x + dir
        if newX < 0:
            newX = 0
        if newX > col - len(self.stone.shape[0]):
            newX = col - len(self.stone.shape[0])
        self.stone.x = newX
        if checkCollision(self.board, self.stone):
            self.stone.x = temp

    def quit(self):
        sys.exit()

    def playerDrop(self):
        self.drop()
        self.score += 1

    def togglePaused(self):
        self.paused = not self.paused

    def run(self):
        """Actually runs the game"""
        self.score = 0
        keys = {
            'ESCAPE':	self.quit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': self.playerDrop,
            'UP': self.rotateStone,
            'p': self.togglePaused,
        }
        self.gameover = False
        self.paused = False
        self.createStone()

        pygame.time.set_timer(pygame.USEREVENT+1, 750)
        clock = pygame.time.Clock()

        while not self.gameover and not self.paused:

            self.drawGame(self.board, (0, 0))
            self.drawGame(self.stone.shape, (self.stone.x, self.stone.y))

            pygame.display.update()
            self.drop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    for key in keys:
                        if event.key == eval("pygame.K_"+key):
                            keys[key]()
            clock.tick(12)
        # pygame.time.wait(110)


# game = Tetris()
# game.run()
