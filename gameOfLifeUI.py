from random import randint
from time import sleep
import pygame
from Cell import Cell, States, RGBStates
from Grid import DataGrid, RGBDataGrid
from enum import Enum

# TODO - Before GitHub:
# 2) clearer names in UI - gridSize, gridLength, size, height, cellsize - etc - choose consistent format.

pygame.init()
size = (500, 550)

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
def drawGridLines(surface, size, cellHeight):
    for x in range(cellHeight, size, cellHeight):
        pygame.draw.line(surface, Colours.BLACK.value, (x,cellHeight), (x,size - cellHeight), 1)
    for y in range(cellHeight, size, cellHeight):
        pygame.draw.line(surface, Colours.BLACK.value, (cellHeight,y), (size - cellHeight, y), 1)
        
def drawCell(surface, x, y, colour, cellHeight):
    colour = colour.value
    cell = pygame.Rect(x + 1, y + 1, cellHeight, cellHeight)
    pygame.draw.rect(surface, colour, cell)

### Middleware methods - transform backend data to visual representation
def writeCellToUI(surface, cell, x, y, cellHeight):
    colour = statesToColours[cell.state]
    drawCell(surface, x, y, colour, cellHeight)

def fillGrid(gridSurface, grid, cellHeight):
    x = cellHeight 
    endIdx = len(grid.data) - 2
    for row in grid.data[:endIdx]:  
        y = cellHeight 
        for cell in row[:endIdx]:
            writeCellToUI(gridSurface, cell, x, y, cellHeight)
            y += cellHeight
        x += cellHeight

def updateScreen(gridSurface, grid, screen, cellHeight):
    fillGrid(gridSurface, grid, cellHeight)
    background.blit(gridSurface, (0, 50))
    screen.blit(background, (0,0))

def createRandomCoords(n):
    coords = []
    for i in range(n):
        coords.append( (randint(1,60), randint(1,60)) )
    return coords

## Script
cellSize = 5
gridLength = 250
gridSize = (gridLength // cellSize) 
grid = RGBDataGrid(gridSize)
# startingCoords1 = [(3,3), (3,4), (3,5), (4,2), (4,3), (4,4)]
startingCoords = createRandomCoords(10)
# grid.setInitialCells(startingCoords)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

background = pygame.Surface((500, 550))
background.fill(Colours.WHITE.value)
gridSurface = pygame.Surface((gridLength, gridLength))
gridSurface.fill(Colours.WHITE.value)
drawGridLines(gridSurface, gridLength, cellSize)
grid.randomInitialCells()
    
while True:  
    updateScreen(gridSurface, grid, screen, cellSize)
    pygame.display.update()
    sleep(0.2)
    grid.cycle()

