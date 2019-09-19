# object representing all neighbour states of a cell in a grid.
# DataGrid passes neighbour states to the cell
# Cell sets it's own state according to its update rules and its received neighbourStates

class NeighbourStates:
    def __init__(self, cell, grid):
        self.row = cell.row
        self.col = cell.col
        self.grid = grid

        self.neighbourCoords = [
            (self.col-1, self.row-1),  (self.col, self.row-1),  (self.col+1, self.row-1),
            (self.col-1, self.row),                             (self.col+1, self.row),
            (self.col-1, self.row+1),  (self.col, self.row+1),  (self.col+1, self.row+1)  
        ] 

        self.neighbourStates = self.getNeighbourStates()
        
    def getNeighbourStates(self):
        states = []
        for x,y in self.neighbourCoords:
            # only get neighbours within grid boundaries
            if x > 0 and y > 0 and x < self.grid.length -1 and y < self.grid.length -1:  
                neighbour = self.grid.data[y][x]
                states.append(neighbour.state)
        return states