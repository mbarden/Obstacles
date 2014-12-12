####
#
# Environment Terrain Objects
# Jake Kinsman
# 11/28/2014
#
####

import random

#file tested

class terrain(object):
	
	def __init__(self):
		self.terrainWorld = list()
		for _ in range(10):
			section = list()
			for __ in range(10):
				obj = random.choice([grass(), water(), mountain(), forest()])
				section.append(obj)
			self.terrainWorld.append(section)
	
	def showTerrain(self):
		for i in range(10):
			print self.terrainWorld[i]
	def showScores(self):
		for i in range(10):
			print map( lambda n: n.getScore(), self.terrainWorld[i])

class terrainObject(object):
	
	def __init__(self):
		pass
	
	def __repr__(self):
		pass

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
                
