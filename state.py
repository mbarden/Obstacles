####
#
# State
# Jake Kinsman
# 11/28/2014
#
####

#file tested

class state(object):
    
    def __init__(self, position, terrain):#position = (0, 9), terrain = None):
        self.position = position
        self.terrain = terrain
        self.terrainType = str(terrain)
    
    def __repr__(self):
        return "Position: " + str(self.position) + " " + "Terrain: " + self.terrainType
    
    def __eq__(self, arg):
        return arg.getPosition() == self.getPosition() and self.getWorld() == arg.getWorld()

    def __hash__(self):
        x,y = self.getPosition()
        w = self.terrain.index
        if x == float('inf'): return 1001
        if y == float('inf'): return 1002
        return 100*w + 10*y + x

    def getWorld(self):
        return self.terrain.index

    def getState(self):
        return [self.position, self.terrain]
    
    def setPosition(self, position):
        self.position = position
    
    def getPosition(self):
        return self.position

    def getTerrainType(self):
        return self.terrainType
