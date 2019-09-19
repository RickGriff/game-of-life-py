from Cell import Cell, RGBCell, CyclicRGBCell, States, RGBStates
from NeighbourStates import NeighbourStates
from random import randint

# object representing all neighbours of a cell
class DataGrid:
    def __init__(self, size):
        self.length = size
        self.data = [[Cell(row,col) for col in range(size)] for row in range(size)]
        self.cycles = 0

    def calcNextStates(self):
        for row in self.data:
            for cell in row:
                neighbourStates = NeighbourStates(cell, self).neighbourStates
                cell.setNextState(neighbourStates)
        
    def updateStates(self):
        for row in self.data:
            for cell in row:
                cell.updateState()

    def cycle(self):
        self.cycles += 1
        print("perform cycle " + str(self.cycles))
        self.calcNextStates()
        # self.randomlySpawn()
        self.updateStates()
        # self.display()
    
    def setInitialCells(self, coordsList):
        for coords in coordsList:
            cell = self.data[coords[0]][coords[1]]
            cell.state = States.ALIVE
    
    def randomInitialCells(self):
        for row in self.data:
            for cell in row:
                cell.state = States(randint(1,2))

    # display command-line grid of letters representing data
    def display(self):
        rowNum = 1
        for row in self.data:
            states = [cell.state for cell in row]
            charsFromStatesMap = map(self.stateToChar, states)
            chars = list(charsFromStatesMap)
            # chars = ["H" if (state == States.ALIVE) else "o" if (state == States.DEAD) else None for state in states] 
            print (chars[0])
            print("{}. [ {} ]".format(rowNum, " ".join(chars)))
            rowNum += 1

    def stateToChar(self, state):
        states = {
            States.DEAD: "o", 
            States.ALIVE: "A"
            }
        return states[state]
         
class RGBDataGrid(DataGrid):
    def __init__(self, size, isCyclic=False):
        self.isCyclic = isCyclic
        self.length = size
        self.data = [[self.cellInstance(row,col) for col in range(size)] for row in range(size)]
        self.cycles = 0
          
    def cellInstance(self, row, col):
        if self.isCyclic == True:
            return CyclicRGBCell(row,col)
        elif self.isCyclic == False:
             return RGBCell(row,col)

    def setInitialCells(self, coordsList):
        for coords in coordsList:
            cell = self.data[coords[0]][coords[1]]
            cell.state = RGBStates(randint(2,4))
    
    def randomInitialCells(self):
        for row in self.data:
            for cell in row:
                cell.state = RGBStates(randint(1,4))

    def randomlySpawn(self):
        if randint(1,8) > 1:
            return None
        height = randint(5,30)
        width = randint(5,30)

        x = randint(1, self.length - width - 1)
        y = randint(1, self.length - height - 1)
        spawnState = RGBStates(randint(2,4))

        for row in self.data[x : x + width]:
            for cell in row[y : y + height]:
                cell.nextState = spawnState
    
    def stateToChar(self, state):
        states = {
            RGBStates.DEAD: "o", 
            RGBStates.RED: "R",
            RGBStates.GREEN: "G",
            RGBStates.BLUE: "B" 
            }
        return states[state]
