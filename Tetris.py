import sys
import pygame
import random
import copy

row = 24
col = 10
cell = 30

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
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1][cx+off_x] += val
    return mat1


def rotateClockwise(shape):
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


def removeRow(board, row):
    del board[row]
    return [[0 for i in range(col)]] + board


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
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.createBoard()

    def createBoard(self):
        # self.board = np.zeros((row, col), dtype=int)
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
        offx, offy = offset
        for y, row in enumerate(mat):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, colours[val], pygame.Rect(
                        (offx+x) * cell, (offy+y) * cell, cell, cell))

    def clearGame(self, mat, offset):
        offx, offy = offset
        for y, row in enumerate(mat):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, colours[0], pygame.Rect(
                        (offx+x) * cell, (offy+y) * cell, cell, cell))

    def drop(self):
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
        print(getMoves(self.board, self.stone, 'NONE'))
        for item in self.board:
            print(item)
        print()
        # print(getMoves(self.board, self.stone, 'None'))
        sys.exit()

    def playerDrop(self):
        self.drop()
        self.score += 1

    def run(self):
        self.score = 0
        keys = {
            'ESCAPE':	self.quit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': self.playerDrop,
            'UP': self.rotateStone,
        }
        self.gameover = False
        self.paused = False
        self.createStone()

        pygame.time.set_timer(pygame.USEREVENT+1, 750)
        clock = pygame.time.Clock()

        while not self.gameover:

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


def getMoves(board, stone, move):
    """Get best possible move set based on heuristics"""
    aiScore = 0
    bestScore = -10000000000000
    tempStone = Stone(stone.x, stone.y, stone.shape)
    tempBoard = copy.deepcopy(board)
    moves = []
    temp = 0

    for i in range(4):
        tempStone.shape = rotateClockwise(tempStone.shape)
        for j in range(col - len(tempStone.shape[0]) + 1):
            tempStone.x = j
            for k in range(row - len(tempStone.shape) + 2):
                tempBoard = copy.deepcopy(board)
                tempStone.y = k
                temp += 1
                if checkCollision(tempBoard, tempStone):
                    aiScore = getScore(tempBoard, tempStone)
                    if aiScore > bestScore:
                        moves = []
                        bestScore = aiScore
                        distance = i - stone.x
                        if distance > 0:
                            moves.append(distance * 'RIGHT')
                        elif distance < 0:
                            moves.append(distance * 'LEFT')
                        else:
                            pass
                        for _ in range(j):
                            moves.append('UP')
                        for _ in range(k):
                            moves.append('DOWN')

    return moves


def getScore(board, stone):
    tempBoard = joinMatrixes(board, stone.shape, (stone.x, stone.y))
    """
    for item in tempBoard:
        print(item)
    print()
    print(aggHeight, completeLines, holes, bump)
    """

    a = -0.5
    b = 0.76
    c = -0.35
    d = -0.18

    aggHeight = getAggregateHeight(tempBoard)
    completeLines = getCompleteLines(tempBoard)
    holes = getHoles(tempBoard)
    bump = getBumpiness(tempBoard)

    return a*aggHeight + b*completeLines + c*holes + d*bump


def getAggregateHeight(board):
    height = []
    for j in range(col):
        i = 0
        for i in range(row):
            if board[i][j] != 0:
                height.append(row - i)
                break
    return sum(height)


def getCompleteLines(board):
    lines = 0
    for row in board:
        if 0 not in row:
            lines += 1
    return lines


def getHoles(board):
    holes = 0
    possibleHoles = False
    for j in range(col):
        i = 0
        possibleHoles = False
        while i < row:
            if possibleHoles:
                if board[i][j] == 0:
                    holes += 1
            elif board[i][j] != 0:
                possibleHoles = True
            i += 1
    return holes


def getBumpiness(board):
    diff = 0
    height = []
    for j in range(col):
        for i in range(row):
            if board[i][j] != 0 or i == row:
                height.append(row - i)
    for j in range(len(height) - 1):
        diff += height[j] - height[j + 1]
    return diff


def checkCollision(board, stone):
    for j, row in enumerate(stone.shape):
        for i, cell in enumerate(row):
            try:
                if cell and board[j + stone.y][i + stone.x]:
                    return True
            except IndexError:
                return True
    return False


game = Tetris()
game.run()

"""    moves.append(move)

    tempStone.shape = rotateClockwise(tempStone.shape)
    moves.append(getMoves(tempBoard, tempStone, 'UP'))
    tempStone.shape = stone.shape

    tempStone.x -= 1
    moves.append(getMoves(tempBoard, tempStone, 'LEFT'))
    tempStone.x += 2

    moves.append(getMoves(tempBoard, tempStone, 'RIGHT'))
"""
"""<                moves = []
                bestScore = aiScore
                distance = i - stone.x
                if distance > 0:
                    moves.append(distance * 'RIGHT')
                elif distance < 0:
                    moves.append(distance * 'LEFT')
                else:
                    pass
                for _ in range(j):
                    moves.append('UP')
                for _ in range(k):
                    moves.append('DOWN')
"""
