from enum import Enum
from random import randint, choice

class States(Enum):
    ALIVE = 1
    DEAD = 2

class RGBStates(Enum):
    DEAD = 1
    RED = 2
    GREEN = 3
    BLUE = 4

# Cell implements classic Conway Game of Life rules
class Cell:
    def __init__(self, row, col):
        self.state = States.DEAD
        self.nextState = States.DEAD
        self.row = row
        self.col = col
  
    # define the rules for life/death of cell based on adjacent population
    def getState(self, pop):
         # Classic Conway rules:
        def conway(pop):
            if pop < 2:
                return States.DEAD
            elif pop == 2:
                return self.state   
            elif pop == 3:
                return States.ALIVE
            elif pop > 3:
                return States.DEAD
       
        # viral spread rule:
        def viralSpread(pop):
            if pop > 0:
                return States.ALIVE
            else:
                return self.state

        return conway(pop)
    
    def setNextState(self, neighbourStates):
        adjacentPop = 0
        for state in neighbourStates:
            if state == States.ALIVE:
                adjacentPop += 1

        self.nextState = self.getState(adjacentPop)

    def updateState(self):
        self.state = self.nextState

# RGBCell implements 'largest neighbour' rules: 
# -Cell takes the colour of the most frequent neighbouring colour. 
# -If two neighbouring colours have equal count, randomly choose between them.
class RGBCell(Cell):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = RGBStates.DEAD
        self.nextState = RGBStates.DEAD

    # overrides parent method
    def getState(self, statesCount):  
        # grab all states that share the max count
        highest = max(statesCount.values()) 
        maxStates = [state for state, count in statesCount.items() if count == highest and count > 0]
        
        if len(maxStates) == 0:
            return RGBStates.DEAD

        return choice(list(maxStates))
        
    # overrides parent method
    def setNextState(self, neighbourStates):
        statesCount = { RGBStates.RED: 0, RGBStates.GREEN: 0, RGBStates.BLUE: 0}

        for state in neighbourStates:
            if state in statesCount.keys():
                statesCount[state] += 1

        self.nextState = self.getState(statesCount)

    #optional random mutator for introducing noise 
    def checkRandomMutate(self, state):
        if randint(1,20) > 1:
            return state
        else:
            return RGBStates(randint(2,4))


# CyclicRGB implements RGB largest neighbour rules for dead cells, and 'cyclical eating' for live cells:
# Red eats Green, Green eats Blue, Blue eats Red.
class CyclicRGBCell(RGBCell):

    # dead cells are subject to 'largest neighbour' eating
    def getBirthState(self, statesCount):
        highest = max(statesCount.values()) 
        maxStates = [state for state, count in statesCount.items() if count == highest and count > 0]

        if len(maxStates) == 0:
            return self.state  # stay dead if surrounded by dead neighbours
        else:
            return choice(list(maxStates))

    def getState(self, statesCount):  
        preyToPredator = {
            RGBStates.GREEN: RGBStates.RED,
            RGBStates.RED: RGBStates.BLUE,
            RGBStates.BLUE:  RGBStates.GREEN 
        }

        if self.state == RGBStates.DEAD:
            return self.getBirthState(statesCount)
        
        predator = preyToPredator[self.state] 
        if statesCount[predator] >=3:
            self.state = predator
        return self.state     
        