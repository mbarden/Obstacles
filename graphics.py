####
#
# Graphics
# Jake Kinsman
# 11/28/2014
#
####

import pygame, sys
from pygame.locals import *
import state as State
victors = list()
victorPositions = list()
winnerHistory = list()
headStart = [[0,0,0]]

def simulation(results, race):
	randomAgentMovements = results[0]
	adpAgentMovements = results[1]
	tdAgentMovements = results[2]
	randomAgentScores = results[3]
	adpAgentScores = results[4]
	tdAgentScores = results[5]

	pygame.init()
	pygame.time.set_timer(USEREVENT + 1, 500)
	completedRace = False
	surface = pygame.display.set_mode((1440, 850), 0, 32)
	for i in range(3):
		drawSplashScreen(surface, i)
		drawEnvironment(surface, race, i, results)

def drawSplashScreen(windowSurface, raceNum):
	sky = pygame.image.load("background.jpg")
	sky = pygame.transform.scale(sky, (1440, 850))
	font = pygame.font.SysFont("arial", 25, True, False)
	if raceNum is 0:
		text = font.render("Beginning the Relay Race!", 1, (0,0,0), (255, 255, 255))
	else:
		text = font.render("Displaying Leg #" + str(raceNum + 1) + ":", 1, (0,0,0), (255, 255, 255))
	numSeconds = 0
	while numSeconds < 8:
		windowSurface.blit(sky, (0,0))
		windowSurface.blit(text, (600,400))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == USEREVENT + 1:
				numSeconds += 1
		pygame.display.flip()

def drawClosingScreen(windowSurface, race, results):
	randomAgents = list()
	adpAgents = list()
	tdAgents = list()
	for i in range(3):
		randomAgents.append(getAgentImage('random', race.randomRaceOrder[i], 200))
		adpAgents.append(getAgentImage('adp', race.adpRaceOrder[i], 200))
		tdAgents.append(getAgentImage('td', race.tdRaceOrder[i], 200))
	sky = pygame.image.load("background.jpg")
	sky = pygame.transform.scale(sky, (1440, 850)) 
	font = pygame.font.SysFont("arial", 25, True, False)
	scoreText = font.render("Score: ", 1, (0, 0, 0), (255, 255, 255))
	randomScore = sum(results[3])
	adpScore = sum(results[4])
	tdScore = sum(results[5])
	teamImages = [float('inf'), float('inf'), float('inf')]
	teamOneResultsText, teamTwoResultsText, teamThreeResultsText = None, None, None
	scoreList = [adpScore, tdScore, randomScore]
	scoreList.sort()
	if randomScore == scoreList[2]:
		teamOneResultsText = font.render("Random Agents: ", 1, (0, 0, 0), (255, 255, 255))
		teamImages[0] = randomAgents
	elif adpScore == scoreList[2]:
		teamOneResultsText = font.render("ADP Agents: ", 1, (0, 0, 0), (255, 255, 255))
		teamImages[0] = adpAgents
	else:
		teamOneResultsText = font.render("Approx. Q-Learning Agents: ", 1, (0, 0, 0), (255, 255, 255))
		teamImages[0] = tdAgents
	
	if randomScore == scoreList[0]:
		teamThreeResultsText = font.render("Random Agents: ", 1, (0, 0, 0), (255, 255, 255))
		teamImages[2] = randomAgents
	elif adpScore == scoreList[0]:
		teamThreeResultsText = font.render("ADP Agents: ", 1, (0, 0, 0), (255, 255, 255))
		teamImages[2] = adpAgents
	elif tdScore == scoreList[0]:
		teamThreeResultsText = font.render("Approx. Q-Learning Agents: ", 1, (0, 0, 0,), (255, 255, 255))
		teamImages[2] = tdAgents

	if randomScore == scoreList[1]:
		teamTwoResultsText = font.render("Random Agents: ", 1, (0, 0, 0), (255, 255, 255))
		teamImages[1] = randomAgents
	elif adpScore == scoreList[1]:
		teamTwoResultsText = font.render("ADP Agents: ", 1, (0, 0, 0), (255, 255, 255))
		teamImages[1] = adpAgents
	elif tdScore == scoreList[1]:
		teamTwoResultsText = font.render("Approx. Q-Learning Agents: ", 1, (0, 0, 0,), (255, 255, 255))
		teamImages[1] = tdAgents
	randomScoreText = font.render(str(randomScore), 0, (0, 0, 0), (255, 255, 255))
	adpScoreText = font.render(str(adpScore), 0, (0, 0, 0), (255, 255, 255))
	tdScoreText = font.render(str(tdScore), 0, (0, 0, 0), (255, 255, 255))
	scoreText = font.render("Score: ", 1, (0, 0, 0), (255, 255, 255))
	displayResultsText = font.render("Displaying Results: ", 1, (0,0,0), (255, 255, 255))
	displayResultsPos = (600, 0)	
	teamOneResultsPos = (420, 100)
	teamTwoResultsPos = (420, 350)
	teamThreeResultsPos = (420, 600)
	firstPlaceText = font.render("First Place: ", 1, (0, 0, 0), (255, 255, 255))
	secondPlaceText = font.render("Second Place: ", 1, (0, 0, 0), (255, 255, 255))
	thirdPlaceText = font.render("Third Place: ", 1, (0, 0, 0), (255, 255, 255))
	firstPlacePos = (0, 100)
	secondPlacePos = (0, 350)
	thirdPlacePos = (0, 600)
	numSeconds = 0
	while numSeconds < 30:
		windowSurface.blit(sky, (0,0))
		windowSurface.blit(firstPlaceText, firstPlacePos)
		windowSurface.blit(secondPlaceText, secondPlacePos)
		windowSurface.blit(thirdPlaceText, thirdPlacePos)

		windowSurface.blit(displayResultsText, displayResultsPos)
		windowSurface.blit(teamOneResultsText, teamOneResultsPos)
		windowSurface.blit(teamTwoResultsText, teamTwoResultsPos)
		windowSurface.blit(teamThreeResultsText, teamThreeResultsPos)
		
		windowSurface.blit(scoreText, (1325, 0))
		for i, score in enumerate(reversed(scoreList)):
			tScore = font.render("%.2f" % score, 1, (0, 0, 0), (255, 255, 255))
			windowSurface.blit(tScore, (1325, (100 + 250 * i)))
		for i, team in enumerate(teamImages):
			for j, member in enumerate(team):
				member = pygame.transform.scale(member, (200, 200))
				windowSurface.blit(member, (( 420 + 200 * j), (250 * i + 130)))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == USEREVENT + 1:
				numSeconds += 1
		pygame.display.flip()


def drawEnvironment(windowSurface, race, worldNum, results):
	tdAgent = getAgentImage('td', race.tdRaceOrder[worldNum])
	randomAgent = getAgentImage('random', race.randomRaceOrder[worldNum])
	adpAgent = getAgentImage('adp', race.adpRaceOrder[worldNum])
	tdHeadStart = headStart[worldNum][2]
	randomHeadStart = headStart[worldNum][0]
	adpHeadStart = headStart[worldNum][1]
	tdNewHeadStart, randomNewHeadStart, adpNewHeadStart = 0, 0, 0
	tdAgentScore = results[5][worldNum]
	randomAgentScore = results[3][worldNum]
	adpAgentScore = results[4][worldNum]
	grass = pygame.image.load("grass.png")
	grass = pygame.transform.scale(grass, (144, 70))
	water = pygame.image.load("water.png")
	water = pygame.transform.scale(water, (144, 70))
	mountain = pygame.image.load("mountain.jpg")
	mountain = pygame.transform.scale(mountain, (144, 70))
	forest = pygame.image.load("forest.png")
	forest = pygame.transform.scale(forest, (144, 70))
	sky = pygame.image.load("background.jpg")
	sky = pygame.transform.scale(sky, (1440, 850))
	platform = pygame.image.load("platform.tiff")
	platform = pygame.transform.scale(platform, (100, 50))
	font = pygame.font.SysFont("monospace", 25, True, False)
	start = font.render("START", 1, (0,0,0), (255, 255, 255))
	finish = font.render("FINISH", 1, (0,0,0), (255, 255, 255))
	pygame.display.set_caption("Relay Race: Leg " + str(worldNum + 1))
	move = 0
	numWinners = -1
	tdWinner, adpWinner, randomWinner = -1, -1, -1
	if tdAgentScore == max([randomAgentScore, tdAgentScore, adpAgentScore]):
		tdWinner = 0
	elif adpAgentScore == max([randomAgentScore, tdAgentScore, adpAgentScore]):
		adpWinner = 0
	else:
		randomWinner = 0

	if tdAgentScore == min([randomAgentScore, tdAgentScore, adpAgentScore]):
		tdWinner = 2
	elif adpAgentScore == min([randomAgentScore, tdAgentScore, adpAgentScore]):
		adpWinner = 2
	else:
		randomWinner = 2

	if tdWinner == -1:
		tdWinner = 1
	elif adpWinner == -1:
		adpWinner = 1
	else:
		randomWinner = 1
	while not(move + randomHeadStart > len(results[0][worldNum]) and move + adpHeadStart > len(results[1][worldNum]) and move + tdHeadStart > len(results[2][worldNum])):
	    randomAgentState = results[0][worldNum][min([move + randomHeadStart, len(results[0][worldNum]) - 1])]
	    adpAgentState = results[1][worldNum][min([move + adpHeadStart, len(results[1][worldNum]) - 1])]
	    tdAgentState = results[2][worldNum][min([move + tdHeadStart, len(results[2][worldNum]) - 1])]
	    for event in pygame.event.get():
	        if event.type == QUIT:
	            pygame.quit()
	            sys.exit()
	        windowSurface.blit(sky, (0,0))
	    	if event.type == USEREVENT + 1:
	    		for i in range(len(race.world.terrains[worldNum].terrainWorld)):
	        		for j in range(len(race.world.terrains[worldNum].terrainWorld)):
	        			position = ((144 * i), ((70 * j) + 150))
	        			if repr(race.world.terrains[worldNum].terrainWorld[i][j]) == 'grass':
	        				windowSurface.blit(grass, position)
	        			elif repr(race.world.terrains[worldNum].terrainWorld[i][j]) == 'water':
	        				windowSurface.blit(water, position)
	        			elif repr(race.world.terrains[worldNum].terrainWorld[i][j]) == 'forest':
	        				windowSurface.blit(forest, position)
	        			else:
	        				windowSurface.blit(mountain, position)        
	    		windowSurface.blit(platform, (0, 60))
	    		windowSurface.blit(platform, (100, 60))
	    		windowSurface.blit(platform, (200, 60))
	    		windowSurface.blit(platform, (570, 60))
	    		windowSurface.blit(platform, (670, 60))
	    		windowSurface.blit(platform, (770, 60))
	    		windowSurface.blit(platform, (1140, 60))
	    		windowSurface.blit(platform, (1240, 60))
	    		windowSurface.blit(platform, (1340, 60))
	    		windowSurface.blit(tdAgent, stateToCoordinates(tdAgentState ,'td', worldNum, tdWinner))
	    		if tdAgentState.getPosition() == (float("inf"), float("inf")):
	    			drawAgentScore(results[5][worldNum], tdWinner, worldNum, windowSurface)
	    		windowSurface.blit(adpAgent, stateToCoordinates(adpAgentState ,'adp', worldNum, adpWinner))
	    		if adpAgentState.getPosition() == (float("inf"), float("inf")):
	    			drawAgentScore(results[4][worldNum], adpWinner, worldNum, windowSurface)
	    		windowSurface.blit(randomAgent, stateToCoordinates(randomAgentState ,'random', worldNum, randomWinner))
	    		if randomAgentState.getPosition() == (float("inf"), float("inf")):
	    			drawAgentScore(results[3][worldNum], randomWinner, worldNum, windowSurface)
	    		windowSurface.blit(start, stateToCoordinates(State.state((0,9), worldNum), None, worldNum))
	    		windowSurface.blit(finish, stateToCoordinates(State.state((9,0), worldNum), None, worldNum))
	    		if worldNum > 0:
	    			for i, winner in enumerate(victors[0]):
	    				windowSurface.blit(winner, victorPositions[0][i])
	    			for j in range(3):
	    				drawAgentScore(winnerHistory[0][2-j], j, 0, windowSurface)

	    			if worldNum is 2:
	    				for i, winner in enumerate(victors[1]):
	    					windowSurface.blit(winner, victorPositions[1][i])
	    				for j in range(3):
	    					drawAgentScore(winnerHistory[1][2 - j], j, 1, windowSurface)

	    		pygame.display.flip()
	    		if len(results[0][worldNum]) <= move + randomHeadStart:
	    			randomNewHeadStart += 1
	    		if len(results[1][worldNum]) <= move + adpHeadStart:
	    			adpNewHeadStart += 1
	    		if len(results[2][worldNum]) <= move + tdHeadStart:
	    			tdNewHeadStart += 1
	    		move += 1
	headStart.append([randomNewHeadStart, adpNewHeadStart, tdNewHeadStart])
	scoreList = [tdAgentScore, randomAgentScore, adpAgentScore]
	scoreList.sort()
	winnerHistory.append(scoreList)
	victors.append([tdAgent, adpAgent, randomAgent])
	victorPositions.append([stateToCoordinates(State.state((float("inf"), float("inf")), worldNum), 'td', worldNum, tdWinner), 
		stateToCoordinates(State.state((float("inf"), float("inf")), worldNum), 'adp', worldNum, adpWinner), 
		stateToCoordinates(State.state((float("inf"), float("inf")), worldNum), 'random', worldNum, randomWinner)])
	if worldNum is 2:
		drawClosingScreen(windowSurface, race, results)

def getAgentImage(agentType, index, defSize = 60):
	image = None
	if agentType == 'random':
		if index == 0:
			image = pygame.image.load("mario.png")
		elif index == 1:
			image = pygame.image.load("luigi.png")
		else:
			image = pygame.image.load("bowser.png")
	elif agentType == 'td':
		if index == 0:
			image = pygame.image.load("jake.jpg")
		elif index == 1:
			image = pygame.image.load("willie.jpg")
		else:
			image = pygame.image.load("matt.jpg")
	else:
		if index == 0:
			image = pygame.image.load("fred.jpg")
		elif index == 1:
			image = pygame.image.load("karen.jpg")
		else:
			image = pygame.image.load("jim.jpg")
	image = pygame.transform.scale(image, (defSize, defSize))
	return image

def stateToCoordinates(state, typeAgent, worldNum, numWinners = 0):
	offset = 0
	if state.getPosition() == (float("inf"), float("inf")):
		if worldNum is 0:
			if numWinners is 0:
				offset = 20
			elif numWinners is 1:
				offset = 120
			else:
				offset = 220
		elif worldNum is 1:
			offset += 570
			if numWinners is 0:
				offset += 20
			elif numWinners is 1:
				offset += 120
			else:
				offset += 220
		else:
			offset += 1140
			if numWinners is 0:
				offset += 20
			elif numWinners is 1:
				offset += 120
			else:
				offset += 220
		return(offset, 0)
	else:
		if typeAgent is "adp":
			offset = 44
		if typeAgent is "random":
			offset = 84
		x, y = state.getPosition()
		return (((144 * x) + offset), ((70 * y) + 150))
def drawAgentScore(score, position, worldNum, windowSurface):
	x, y = 0, 100
	font = pygame.font.SysFont("arial", 12, False, False)
	text = text = font.render("Score: %.2f" % score, 1, (0,0,0), (255, 255, 255))
	location = tuple()
	if position is 0 and worldNum is 0:
		location = (x, y)
	if position is 1 and worldNum is 0:
		location = (x + 100, y)
	if position is 2 and worldNum is 0:
		location = (x + 200, y)
	if position is 0 and worldNum is 1:
		location = (x + 570, y)
	if position is 1 and worldNum is 1:
		location = (x + 670, y)
	if position is 2 and worldNum is 1:
		location = (x + 770, y)
	if position is 0 and worldNum is 2:
		location = (x + 1140, y)
	if position is 1 and worldNum is 2:
		location = (x + 1240, y)
	if position is 2 and worldNum is 2:
		location = (x + 1340, y)
	windowSurface.blit(text, location)








