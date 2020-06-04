import sys
import time
import os
import select
import tty
import termios
import random
import array
from termcolor import cprint


class NonBlockingConsole(object):

    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_data(self):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return False


class stone():
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape

    def rotateCW(self):
        self.shape = [[self.shape[y][x]
                      for y in range(len(self.shape))]
                      for x in range(len(self.shape[0]) - 1, -1, -1)]


cols = 10
rows = 24

shapes = [
        [[1, 1, 1], [0, 1, 0]],
        [[0, 2, 2], [2, 2, 0]],
        [[3, 3, 0], [0, 3, 3]],
        [[4, 0, 0], [4, 4, 4]],
        [[0, 0, 5], [5, 5, 5]],
        [[6, 6, 6, 6]],
        [[7, 7], [7, 7]]
        ]


scores = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}

colours = {0: "white", 1: "yellow", 2: "green", 3: "cyan", 4: "grey", 5: "magenta", 6: "red", 7: "blue"}


def initBoard():
    board = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    ]
    return board


def printBoard(board):
    for row in board:
        for item in row:
            cprint(item, colours[item], end=" ")
        print()


def createStone(board):
    return stone(0, len(board[0])/2 - 1, random.choice(shapes))


def drawStone(board, stone):
    for i in range(len(stone.shape)):
        for j in range(len(stone.shape[i])):
            if board[int(i + stone.x)][int(j + stone.y)] == 0 and stone.shape[i][j] != 0:
                board[int(i + stone.x)][int(j + stone.y)] = stone.shape[i][j]
    return board


def checkCollision(board, stone):
    for i, row in enumerate(stone.shape):
        for j, cell in enumerate(row):
            try:
                tempBoard = clearStone(board, stone)
                if cell != 0 and tempBoard[int(stone.x + i)][int(stone.y + j)] != 0:
                    return True # collides with existing piece
            except IndexError:
                return True
    return False



def hitStone(board, stone):
    for i, row in enumerate(stone.shape):
        for j, cell in enumerate(row):
            try:
                tempBoard = board
                if cell != 0 and tempBoard[int(stone.x + i)][int(stone.y + j)] != 0:
                    return True # collides with existing piece
            except IndexError:
                return True
    return False



def clearRows(board):
    linesCleared = 0
    for i, row in enumerate(board):
        if 0 not in row:
            del board[i]
            linesCleared += 1
            board.insert(0, [0,0,0,0,0,0,0,0,0,0])
    return scores[linesCleared]


def slideStone(board, stone, direction):
    if stone.y - 1 >= 0 and not direction:
        clearStone(board, stone)
        stone.y = stone.y - 1
        if hitStone(board, stone):
            stone.y += 1
            return board
        return drawStone(board, stone)
    elif stone.y + 1 + len(stone.shape[0]) <= len(board[0]) and direction:
        clearStone(board, stone)
        stone.y = stone.y + 1
        if hitStone(board, stone):
            stone.y -= 1
            return board
        return drawStone(board, stone)
    else:
        return board


def clearStone(board, stone):
    for i in range(len(stone.shape)):
        for j in range(len(stone.shape[0])):
            if board[int(i + stone.x)][int(j + stone.y)] != 0 and stone.shape[i][j] != 0:
                board[int(i + stone.x)][int(j + stone.y)] = 0
    return board


def game():
    os.system('clear')
    board = initBoard()
    gameOver = False
    gamePause = False
    score = 0
    
    with NonBlockingConsole() as nbc:

        while not gameOver and not gamePause:
            nextStone = createStone(board)
            try:
                printBoard(drawStone(board, activeStone))
            except NameError:
                pass
            finally:
                activeStone = nextStone

            if not hitStone(board, activeStone):
                printBoard(drawStone(board, activeStone))
            else:
                gameOver = True
                print("Game Over")
                break

            while not checkCollision(board, activeStone) and activeStone.x + len(activeStone.shape) != len(board):

                data = nbc.get_data()
                print(data)
                if data == "q":
                    gameOver = True
                    break
                if data == "s" and not hitStone(board, activeStone): # Down
                    print("entered down key")
                    clearStone(board, activeStone)
                    activeStone.x += 1
                    os.system('clear')
                    printBoard(drawStone(board, activeStone))
                elif data == "a": # Left
                    os.system('clear')
                    printBoard(slideStone(board, activeStone, 0))
                elif data == "d": # Right
                    os.system('clear')
                    printBoard(slideStone(board, activeStone, 1))
                elif data == "w": # Up
                    clearStone(board, activeStone)
                    activeStone.rotateCW()
                    printBoard(drawStone(board, activeStone))

                os.system('clear')
                print()
                print(score, data)
                print()
                printBoard(drawStone(board, activeStone))
                time.sleep(0.2)
                clearStone(board, activeStone)
                activeStone.x += 1
                if hitStone(board, activeStone):
                    activeStone.x -= 1
                    break
                score += clearRows(board)
                data = 0
        

game()
