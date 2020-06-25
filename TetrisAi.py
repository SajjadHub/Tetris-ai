import Tetris
import random
import copy
import pygame
import numpy

populationSize = 16
chromosomeSize = 4


class TetrisAi(Tetris.Tetris):
    """Modified Tetris for the computer to run
    - Note computer doesn't make moves, it 'teleports' the piece to
    the calculated spot"""

    def createBoard(self):
        """Using numpy array instead of list **"""
        self.board = numpy.zeros((Tetris.row, Tetris.col), dtype=int)

    def run(self, chromosomes):
        lines = 0
        self.createBoard()
        self.score = 0
        self.gameover = False
        self.paused = False
        self.createStone()

        pygame.time.set_timer(pygame.USEREVENT+1, 750)
        # clock = pygame.time.Clock()

        while not self.gameover:
            getMoves(self.board, self.stone, chromosomes)
            self.drawGame(self.board, (0, 0))
            # self.drawGame(self.stone.shape,
            #              (self.stone.x, self.stone.y))
            lines = 0
            for i, row in enumerate(self.board):
                if 0 not in row:
                    self.board = numpy.delete(self.board, i, 0)
                    self.board = numpy.insert(self.board, 0, numpy.zeros(
                        Tetris.col, dtype=int), 0)
                    self.drawGame(self.board, (0, 0))
                    lines += 1

            self.score += Tetris.scores[lines]
            pygame.display.update()
            # self.drop()
            # clock.tick(1)
            pygame.time.wait(40)
            self.createStone()
        return self.score

    def getChromosomeScores(self, population):
        chromosomeScore = []
        for chrom in population:
            temp = self.run(chrom)
            self.gameover = False
            chromosomeScore.append(temp)
        return chromosomeScore

    def selectPopulation(self):
        population = initalPopulation()
        for i in range(10):
            print("Generation: " + str(i))
            chromosomeScore = self.getChromosomeScores(population)
            print(chromosomeScore)

            bestChromIndex = chromosomeScore.index(max(chromosomeScore))
            parentA = population[bestChromIndex]
            population.pop(bestChromIndex)
            chromosomeScore.pop(bestChromIndex)
            print(parentA, bestChromIndex)

            goodChromIndex = chromosomeScore.index(max(chromosomeScore))
            parentB = population[goodChromIndex]
            print(parentB, goodChromIndex)
            print()

            population = crossover(parentA, parentB)


rotations = (4, 2, 2, 4, 4, 2, 1)


def returnRotation(stone):
    for u in stone.shape:
        for v in u:
            if v:
                return rotations[v - 1]


def hitBottom(board, stone):
    if stone.y + len(stone.shape) >= Tetris.row:
        return True
    for j, row in enumerate(stone.shape):
        for i, cell in enumerate(row):
            if board[stone.y + j + 1][i + stone.x] and cell:
                return True
    return False


def isValidPosition(board, stone):
    for j, row in enumerate(stone.shape):
        for i, cell in enumerate(row):
            if board[j + stone.y - 1][i + stone.x - 1] and cell:
                return False
    return True


def rotateClockwise(shape):
    return numpy.rot90(shape)


def getMoves(board, stone, chrom):
    """Get best possible move set based on heuristics"""
    aiScore = 0
    bestScore = -10000000000000
    tempStone = Tetris.Stone(stone.x, stone.y, stone.shape)
    tempBoard = copy.deepcopy(board)

    for i in range(returnRotation(stone)):
        tempStone.shape = rotateClockwise(tempStone.shape)
        for j in range(Tetris.col - len(tempStone.shape[0]) + 1):
            tempStone.x = j
            tempStone.y = 0
            tempBoard = copy.deepcopy(board)
            while not Tetris.checkCollision(tempBoard, tempStone):
                tempStone.y += 1
            if tempStone.y != 0:
                aiScore = getScore(tempBoard, tempStone, chrom)
                if aiScore > bestScore:
                    bestScore = aiScore
                    stone.shape = copy.deepcopy(tempStone.shape)
                    stone.x = j
                    stone.y = tempStone.y
    board = Tetris.joinMatrixes(board, stone.shape, (stone.x, stone.y))


def getScore(board, stone, chrom):
    aggHeight, completeLines, holes, bump = 0, 0, 0, 0
    tempBoard = copy.deepcopy(board)

    tempBoard = Tetris.joinMatrixes(tempBoard, stone.shape, (stone.x, stone.y))
    a, b, c, d = chrom

    aggHeight = getAggregateHeight(tempBoard)
    completeLines = getCompleteLines(tempBoard)
    holes = getHoles(tempBoard)
    bump = getBumpiness(tempBoard)

    """
    file = open("boards/boards.txt", "a")
    for item in tempBoard:
        file.write("%s\n" % item)
    file.write("%s\n" % stone.x)
    file.write("%s\n" % stone.y)
    file.write("%s\n" % stone.shape)
    file.write("\n")
    file.close
    print(aggHeight, completeLines, holes, bump)
    """

    return a*aggHeight + b*completeLines + c*holes + d*bump


def getAggregateHeight(board):
    height = []
    for j in range(Tetris.col):
        i = 0
        for i in range(Tetris.row):
            if board[i][j] != 0:
                height.append(Tetris.row - i)
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
    for j in range(Tetris.col):
        i = 0
        possibleHoles = False
        while i < Tetris.row:
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
    for j in range(Tetris.col):
        for i in range(Tetris.row):
            if board[i][j] != 0 or i == Tetris.row:
                height.append(Tetris.row - i)
    for j in range(len(height) - 1):
        diff += height[j] - height[j + 1]
    return diff


def initalPopulation():
    population = []
    tempChromosome = []

    for i in range(populationSize):
        tempChromosome = []
        for j in range(chromosomeSize):
            tempChromosome.append(random.uniform(-10, 10))
        population.append(tempChromosome)
    return population


def crossover(parentA, parentB):
    mutation = 19
    population = []
    for i in range(populationSize):
        tempChromosome = []
        for j in range(chromosomeSize):
            if j <= chromosomeSize/2:
                tempChromosome.append(parentA[j])
            else:
                tempChromosome.append(parentB[j])
            if random.randrange(mutation) == 1:
                index = tempChromosome.index(random.choice(tempChromosome))
                tempChromosome[index] = random.uniform(-10, 10)
        population.append(tempChromosome)
    return population


aiGame = TetrisAi()
aiGame.selectPopulation()
'''
aiGame.run([-2.268910153676363, -0.4314094583476784, -
            4.4774033698388145, 4.817498457835743])
[-4.979091611231792, -3.874580968703741, 3.6813670576263906, 0.2492662938148813]
'''
