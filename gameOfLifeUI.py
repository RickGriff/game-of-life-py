from random import randint
from time import sleep
import pygame
from Cell import Cell, States, RGBStates
from Grid import DataGrid, RGBDataGrid
from enum import Enum

# TODO - Before GitHub:
# 2) clearer names in UI - gridSize, gridLength, size, height, cellsize - etc - choose consistent format.

class Colours(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
statesToColours = {
    States.DEAD: Colours.WHITE,
    States.ALIVE: Colours.BLACK,
    RGBStates.DEAD: Colours.WHITE,
    RGBStates.RED: Colours.RED,
    RGBStates.GREEN: Colours.GREEN,
    RGBStates.BLUE: Colours.BLUE,
}

### UI Drawing methods
def drawGridLines(surface, size, cellLengthPx):
    for x in range(cellLengthPx, size, cellLengthPx):
        pygame.draw.line(surface, Colours.BLACK.value, (x,cellLengthPx), (x,size - cellLengthPx), 1)
    for y in range(cellLengthPx, size, cellLengthPx):
        pygame.draw.line(surface, Colours.BLACK.value, (cellLengthPx, y), (size - cellLengthPx, y), 1)
        
def drawCell(surface, x, y, colour, cellLengthPx):
    colour = colour.value
    cell = pygame.Rect(x + 1, y + 1, cellLengthPx, cellLengthPx)
    pygame.draw.rect(surface, colour, cell)

### Middleware methods - transform backend data to visual representation
def writeCellToUI(surface, cell, x, y, cellLengthPx):
    colour = statesToColours[cell.state]
    drawCell(surface, x, y, colour, cellLengthPx)

def fillGrid(gridSurface, grid, cellLengthPx):
    x = cellLengthPx 
    endIdx = len(grid.data) - 2
    for row in grid.data[:endIdx]:  
        y = cellLengthPx 
        for cell in row[:endIdx]:
            writeCellToUI(gridSurface, cell, x, y, cellLengthPx)
            y += cellLengthPx
        x += cellLengthPx

def updateScreen(gridSurface, grid, screen, cellLengthPx):
    fillGrid(gridSurface, grid, cellLengthPx)
    background.blit(gridSurface, (0, 50))
    screen.blit(background, (0,0))

# Helper function
def createRandomCoords(n):
    coords = []
    for i in range(n):
        coords.append( (randint(1,60), randint(1,60)) )
    return coords

### Game script
if __name__ == "__main__":
    pygame.init()
    cellLengthPx = 5
    gridLengthPx = 400
    gridSize = (gridLengthPx // cellLengthPx) 

    dataGrid = DataGrid(gridSize)

    screen = pygame.display.set_mode((500, 500))

    background = pygame.Surface((500, 550))
    background.fill(Colours.WHITE.value)
    gridSurface = pygame.Surface((gridLengthPx, gridLengthPx))
    gridSurface.fill(Colours.WHITE.value)
    drawGridLines(gridSurface, gridLengthPx, cellLengthPx)

    dataGrid.randomInitialCells()
        
    while True:  
        updateScreen(gridSurface, dataGrid, screen, cellLengthPx)
        pygame.display.update()
        sleep(0.2)
        dataGrid.cycle()

