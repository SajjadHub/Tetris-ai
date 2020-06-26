import Tetris
import random
import copy
import pygame
import numpy

populationSize = 20
chromosomeSize = 4


class TetrisAi(Tetris.Tetris):
    """Modified Tetris for the computer to run
    - Note computer doesn't make moves, it 'teleports' the piece to
    the calculated spot"""

    def createBoard(self):
        """Using numpy array instead of list **"""
        self.board = numpy.zeros((Tetris.row, Tetris.col), dtype=int)

    def createStone(self):
        """Creates stone and places it at the top of the board if it can"""
        self.nextStone = Tetris.Stone(
            int(Tetris.col/2 - 1), 0, random.choice(Tetris.shapes))
        self.stone = Tetris.Stone(
            self.nextStone.x, self.nextStone.y, self.nextStone.shape)

        if Tetris.checkCollision(self.board, self.stone):
            self.gameover = True

    def run(self, chromosomes):
        random.seed()
        lines = 0
        self.createBoard()
        self.score = 0
        self.gameover = False
        self.paused = False
        self.createStone()

        pygame.time.set_timer(pygame.USEREVENT+1, 750)
        # clock = pygame.time.Clock()

        while not self.gameover:
            getMoves(self.board, self.stone, chromosomes, self.nextStone)
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
        for i in range(25):
            print("Generation: " + str(i))
            chromosomeScore = self.getChromosomeScores(population)
            print(chromosomeScore)
            pool = []
            for i in range(populationSize):
                indexA = random.randint(0, populationSize - 1)
                parentA = population[indexA]
                indexB = random.randint(0, populationSize - 1)
                parentB = population[indexB]
                print(indexA, indexB)
                if chromosomeScore[indexA] == chromosomeScore[indexB] and chromosomeScore[indexA] == 0:
                    tempChromosome = []
                    for j in range(chromosomeSize):
                        tempChromosome.append(random.uniform(-10, 10))
                    pool.append(tempChromosome)
                elif chromosomeScore[indexA] > chromosomeScore[indexB]:
                    pool.append(parentA)
                else:
                    pool.append(parentB)

            for j in pool:
                print(j)
            population = []
            for i in range(populationSize):
                population.append(
                    crossover(random.choice(pool), random.choice(pool)))


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


def getMoves(board, stone, chrom, nextStone=None):
    """Get best possible move set based on heuristics"""
    aiScore = 0
    bestScore = -10000000000000
    nextAiScore = 0
    nextBestScore = -1000000000000
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
                if nextStone:
                    nextTempBoard = copy.deepcopy(tempBoard)
                    nextTempBoard = Tetris.joinMatrixes(
                        nextTempBoard, tempStone.shape, (tempStone.x, tempStone.y))
                    getMoves(nextTempBoard, nextStone, chrom)
                    nextAiScore = getScore(nextTempBoard, nextStone, chrom)
                    if nextAiScore > nextBestScore:
                        nextBestScore = nextAiScore
                        stone.shape = copy.deepcopy(tempStone.shape)
                        stone.x = j
                        stone.y = tempStone.y
                else:
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
    chrom = []
    for j in range(0, chromosomeSize):
        if j <= chromosomeSize/2:
            chrom.append(parentA[j])
        else:
            chrom.append(parentB[j])
    if random.randint(0, mutation) == 1:
        chrom[random.randint(0, chromosomeSize - 1)
              ] = random.uniform(-10, 10)
    return chrom


aiGame = TetrisAi()
aiGame.selectPopulation()
'''
aiGame.run(
    [-6.375925963691524, 2.1971346793421525, -5.146724194390657, 6.237154216524964]
)
print(aiGame.score)
[-4.979091611231792, -3.874580968703741, 3.6813670576263906, 0.2492662938148813]
'''
