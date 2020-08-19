from graphics import *
import sys
import enum
from time import sleep

# DRAW
class PlaceState(enum.Enum):
    Nothing = 1
    Queen = 2
    Visited = 3

class PlaceRectangle():
    def __init__(self, rectangle):
        self.rectangle = rectangle # rectangle drawed on window
        self.state = PlaceState.Nothing

    def changeState(self, state):
        if self.state == state:
            return

        self.state = state

class DrawController():
    def __init__(self, n, width, height):
        self.n = n # nxn
        self.width = width # of screen
        self.height = height # of screen
        self.win = GraphWin(str(n)+ "-Queens", width, height)
        self.createRectangles()

    def createRectangles(self):
        num = self.n
        rectW = self.width // num
        rectH = self.height // num

        self.rectMatrix = [[None for x in range(num)] for y in range(num)]

        pX = 0
        pY = 0

        for i in range(num):
            for j in range(num):
                rect = Rectangle(Point(pY, pX),Point(pY + rectW, pX + rectH))
                rect.draw(self.win)
                self.rectMatrix[i][j] = PlaceRectangle(rect)
                pX += rectH

            pX = 0
            pY += rectW

    def changeState(self, i, j, state):
        if i >= self.n or i < 0 or j < 0 or j >= self.n:
            print("Warning: outside")
            return

        rect = self.rectMatrix[i][j]
        if  isinstance(rect, PlaceRectangle):
            rect.changeState(state)
            self.draw(rect)

    def draw(self, rect):
        if isinstance(rect, PlaceRectangle):
            if rect.state == PlaceState.Queen:
                rect.rectangle.setFill('green')
            elif rect.state == PlaceState.Visited:
                rect.rectangle.setFill('red')
            else:
                rect.rectangle.setFill('white')

# Program
class MyProgram():
    def __init__(self, nQueens, screenW, screenH, timeSleep):
        self.drawController = DrawController(nQueens, screenW, screenH)
        self.nQueens = nQueens
        self.tSleep = timeSleep # time to sleep, to see better the draw
        self.board = [[0 for x in range(nQueens)] for y in range(nQueens)]
        self.nsol = 0

    def printSolution(self):
        for i in range(self.nQueens): 
            for j in range(self.nQueens): 
                print(str(self.board[i][j]) + ",", end = " ") 
            print()

    def solveNQueens(self):
        if self.solveBT(0):
            print("Solutions exists!")
            self.printSolution()
            self.drawController.win
        else:
            print("Solution does not exists")

    def solveBT(self, row):
        sleep(self.tSleep)

        N = self.nQueens
        if row >= N:
            return True
        else:
            # try put row-th queen on all columns
            for j in range(N):
                if self.prune(row, j):
                    self.drawController.changeState(j, row, PlaceState.Visited)
                    continue
                else:
                    self.board[row][j] = 1
                    self.drawController.changeState(j, row, PlaceState.Queen)
                    if self.solveBT(row + 1):
                        return True
                    self.board[row][j] = 0
                    self.drawController.changeState(j, row, PlaceState.Visited)
                    
            for j in range(N): # clear squares
                self.drawController.changeState(j, row, PlaceState.Nothing)
            return False
    
    def prune(self, row, col):
        N = self.nQueens
        
        # search on the same column
        for i in range(N):
            if self.board[i][col] == 1: 
                return True

        # Check left upper diagonal
        for i,j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return True

        # Check right upper diagonal
        for i,j in zip(range(row, -1, -1), range(col, N, 1)):
            if self.board[i][j] == 1:
                return True

        # Check left lower diagonal
        for i, j in zip(range(row, N, 1), range(col, -1, -1)): 
            if self.board[i][j] == 1: 
                return True

        # Check right lower diagonal
        for i, j in zip(range(row, N, 1), range(col, N, 1)): 
            if self.board[i][j] == 1: 
                return True

        return False

# init program
def main():
    if len(sys.argv) != 5:
        print("execute: python ./main.py <nQueens> <window_width> <window_height> <time_sleep(seconds)>")
        return
    
    nQueens = int(sys.argv[1])
    wW= int(sys.argv[2])
    wH = int(sys.argv[3])
    tSleep = float(sys.argv[4])

    print("Resolve to " + str(nQueens) + " Queens")

    prog = MyProgram(nQueens, wW, wH, tSleep)
    prog.solveNQueens()

    # finished
    exit = input("Anything to exit: ")

# Start
main()