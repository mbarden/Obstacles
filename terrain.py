####
#
# Environment Terrain Objects
# Jake Kinsman
# 11/28/2014
#
####

import random
from state import state

#file tested

class terrain(object):
    index = 0
    def __init__(self):
        self.terrainWorld = list()
        for i in range(10):
            section = list()
            for j in range(10):
                obj = random.choice([grass(), water(), mountain(), forest()])
                obj.index = terrain.index
                section.append(state((i,j), obj))
            self.terrainWorld.append(section)
        terrain.index += 1
        
    def __getitem__(self, key):
        return self.terrainWorld[key]

    def showTerrain(self):
        for i in range(10):
            print self.terrainWorld[i]

    def showScores(self):
        for i in range(10):
            print map( lambda n: n.terrain.getScore(), self.terrainWorld[i])

class terrainObject(object):
    
    def __init__(self):
        self.index = terrain.index
    
    def __repr__(self):
        return 'None'

    def __eq__(self, arg):
        return self.__repr__() == arg.__repr__()

    def getScore(self):
        return 1#self.score

class grass(terrainObject):
    
    def __init__(self):
        self.score = 5
    
    def __repr__(self):
        return 'grass'
    

class mountain(terrainObject):
    
    def __init__(self):
        self.score = 3
    
    def __repr__(self):
        return 'mountain'
    

class water(terrainObject):
    
    def __init__(self):
        self.score = 4
    
    def __repr__(self):
        return 'water'
    
class forest(terrainObject):
    
    def __init__(self):
        self.score = 4
    
    def __repr__(self):
        return 'forest'
                
