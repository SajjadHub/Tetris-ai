import random
import numpy
import os
import time
import select
import sys

global stoneSet

shapes = [
        [[1, 1, 1], [0, 1, 0]],
        [[0, 2, 2], [2, 2, 0]],
        [[3, 3, 0], [0, 3, 3]],
        [[4, 0, 0], [4, 4, 4]],
        [[0, 0, 5], [5, 5, 5]],
        [[6, 6, 6, 6]],
        [[7, 7], [7, 7]]
        ]


class stone():
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape

    def rotateCW(self):
        self.shape = [[self.shape[y][x]
                      for y in range(len(self.shape))]
                      for x in range(len(self.shape[0]) - 1, -1, -1)]


def createStone():
    return stone(0, 3, random.choice(shapes))


def initBoard():
    board = numpy.zeros((24, 10))
    return board


def printBoard(board):
    for i in range(24):
        print(board[i])
    print()


def drawStone(board, stone, x, y):
    for i in range(len(stone.shape)):
        for j in range(len(stone.shape[0])):
            if board[i + x][j + y] is not 0:
                try:
                    board[i + x][j + y] = stone.shape[i][j]
                    stone.x = x
                    stone.y = y
                except IndexError:
                    break
                    print("Ive hit the bottom")
    return board


def clearStone(board, stone):
    for i in range(len(stone.shape)):
        for j in range(len(stone.shape[0])):
            board[i + stone.x][j + stone.y] = 0
    return board


def slideStone(board, stone, direction):
    if stone.y - 1 >= 0 and not direction:
        clearStone(board, stone)
        stone.y = stone.y - 1
        drawStone(board, stone, stone.x, stone.y)
    elif stone.y + 1 <= 10 and direction:
        clearStone(board, stone)
        stone.y = stone.y + 1
        drawStone(board, stone, stone.x, stone.y)
    return board


def dropStone(board, stone):
    if checkCollision(board, stone):
        clearStone(board, stone)
        stone.x = stone.x + 1
        drawStone(board, stone, stone.x, stone.y)
    return board


def clearRow(board, row):
    for j in range(len(board[row])):
        board[row][j] = 0
    return board


def checkCollision(board, stone):
    stone.x += 1
    if stone.x + len(stone.shape[0]) == len(board[0]) - 1:
        return True # collides with bottom
    for i, row in enumerate(stone.shape):
        for j, cell in enumerate(row):
            try:
                if cell and board[stone.x + i + 1][stone.y + j]:
                    return True # collides with existing piece
            except IndexError:
                return True
    stone.x -= 1
    return False


def joinMatrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1][cx+off_x] += val
    return mat1


def game():
    os.system('clear')
    board = initBoard()
    gameOver = 0

    while not gameOver:
        nextStone = createStone()
        activeStone = nextStone
        printBoard(drawStone(board, activeStone, 0, 3))

        while checkCollision(board, activeStone):
            userIn = select.select([sys.stdin], [], [], 0)[0]
            if userIn:
                value = sys.stdin.readline().rstrip()

                if value == "a":
                    os.system('clear')
                    printBoard(slideStone(board, activeStone, 0))
                elif value == "d":
                    os.system('clear')
                    printBoard(slideStone(board, activeStone, 1))
                elif value == "s":
                    os.system('clear')
                    printBoard(dropStone(board, activeStone))
                elif value == "w":
                    clearStone(board, activeStone)
                    activeStone.rotateCW()
                    printBoard(drawStone(board, activeStone, activeStone.x, activeStone.y))
                elif value == "q":
                    gameOver = 1

            time.sleep(1)
            os.system('clear')
            printBoard(dropStone(board, activeStone))
        if checkCollision(board, activeStone):
            board = joinMatrixes(board, activeStone.shape, (activeStone.y, activeStone.x))


game()
