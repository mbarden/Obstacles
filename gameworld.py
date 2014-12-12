####
#
# Gameworld
# Jake Kinsman
# 11/28/2014
#
####

import terrain as Terrain
import state as State
import copy
import random

class gameWorld(object):

    def __init__(self):
        self.states = [Terrain.terrain(), Terrain.terrain(), Terrain.terrain()]
        self.finishPos = (float('inf'), float('inf'))
        self.finalStates = []
        self.livingReward = -1.
        self.discount = 0.95
        self.noise = 0
        self.transitionalStates = [self.states[0][9][0], self.states[1][9][0]]
        self.terminalState = self.states[2][9][0]
        self.adpAgents = []
        self.adpAgentIndex = 0
        self.tdAgents = []
        self.tdAgentIndex = 0
        self.randomAgents = []
        self.randomAgentIndex = 0
        self.transitionalReward = 1000.
        self.terminalReward = 2000

        for i in range(3):
            self.finalStates.append(State.state(self.finishPos, Terrain.terrainObject()))
            self.finalStates[-1].terrain.index = i
    #tested    
    def getDiscount(self):
        return self.discount

    #tested
    def setDiscount(self, disc):
        self.discount = disc

    #tested
    def setNoise(self, noise):
        self.noise = noise
    
    #tested
    def getNoise(self):
        return self.noise

    #tested
    def setLivingReward(self, lr):
        self.livingReward = lr
    
    #tested
    def getLivingReward(self):
        return self.livingReward
    
    #tested
    def getActions(self, state):
        x, y = state.getPosition()
        actions = list()
        if self.isTransitionalState(state) or self.isTerminalState(state):
            return ['finish']
        else:
            if x != 0:
                actions.append('west')
            if x != 9:
                actions.append('east')
            if y != 0:
                actions.append('north')
            if y != 9:
                actions.append('south')
            return actions

    #tested
    def getReward(self, agent, state):
        if self.completedRace(state, 1):
            return self.transitionalReward
        elif self.completedRace(state, 2):
            return self.terminalReward
        else:        
            x, y = state.getPosition()
            manDist = (abs(y - 9) + abs(x - 0))
            terrain = state.terrain
            terrainElement = str(state.terrain)
            rew = (terrain.getScore() * agent.skillLevels[terrainElement]) + manDist #* (2000000. if agent.type == "td" else 1.)
            return self.livingReward / (rew * .1)

    #tested
    def getStartState(self, terrainNum = 0):
        return self.states[terrainNum][0][9]

    #tested
    def isTransitionalState(self, state):
        return state in self.transitionalStates

    #tested
    def isTerminalState(self, state):
        return state == self.terminalState

    #tested
    def generateNextStates(self, state, action):
        if (self.isTerminalState(state) or self.isTransitionalState(state)) and action is 'finish':
            return self.finalStates[state.terrain.index]
        x, y = state.getPosition()
        index = state.terrain.index
        if action is 'east':
            return self.states[index][x+1][y]
        if action is 'west':
            return self.states[index][x-1][y]
        if action is 'north':
            return self.states[index][x][y-1]
        if action is 'south':
            return self.states[index][x][y+1]
        else:
            raise "Error, invalid action"

    #tested
    def completedRace(self, state, worldNum = 0):
        return state.getPosition() == (float("inf"), float("inf")) and state.terrain.index <= worldNum

    #tested
    def addAgent(self, agent, skills=None):
        if skills:
            agent.skillLevels['water'] = skills['water']
            agent.skillLevels['grass'] = skills['grass']
            agent.skillLevels['forest'] = skills['forest']
            agent.skillLevels['mountain'] = skills['mountain']
        else:
            agent.skillLevels['water'] = random.random() + .5
            agent.skillLevels['grass'] = random.random() + .5
            agent.skillLevels['forest'] = random.random() + .5
            agent.skillLevels['mountain'] = random.random() + .5
        
        if agent.type is "adp":
            self.adpAgents.append(agent)
            agent.setIndex(self.adpAgentIndex)
            self.adpAgentIndex += 1
        
        elif agent.type is "td":
            self.tdAgents.append(agent)
            agent.setIndex(self.tdAgentIndex)
            self.tdAgentIndex += 1
        
        else:
            self.randomAgents.append(agent)
            agent.setIndex(self.randomAgentIndex)
            self.randomAgentIndex += 1
    
    #tested
    def moveAgent(self, agent, state, action):
        x, y = state.getPosition()
        terrainElement = str(state.terrain)
        chanceToFall = None
        chanceToSlideDown = None
        chanceToSlideLeft = None
        if state in self.transitionalStates or state == self.terminalState:
            agent.setState(self.generateNextStates(state, action))
        else:
            if terrainElement == 'mountain':
                chanceToFall = abs(agent.skillLevels[terrainElement] - 1) / 2
            else:
                chanceToFall = abs(agent.skillLevels[terrainElement] - 1) / 4
            x, y = state.getPosition()
            chanceToSlideDown = 0.1 - ((0.1 / 10) * (abs(y -  0)))
            chanceToSlideLeft = 0.1 - ((0.1 / 10) * (abs(x - 9)))
                        #agent.setState(self.generateNextStates(state, action))
                        #return
            #if random.random() <= chanceToSlideDown:
            #    agent.setState(State.state((x, min([9, y + 1])), state.getWorld()))

            #elif random.random() <= chanceToSlideLeft:
            #    agent.setState(State.state((max([x - 1, 0]), y), state.getWorld()))
            #if random.random() <= chanceToFall:
            #    agent.setState(State.state((max([x - 1, 0]), min([9, y + 1])), state.getWorld()))
            #else:
            if True:
                agent.setState(self.generateNextStates(state, action))

    #retested
    def getAllPossibleSuccessors(self, state, action):
        x, y = state.getPosition()
        index = state.terrain.index
        successors = list()
        if action is 'finish':
            return [self.finalStates[index]]
        else:
            if x >= 1:
                successors.append(self.states[index][x-1][y])
            if y < 9:
                successors.append(self.states[index][x][y+1])
            if x >= 1 and y < 9:
                successors.append(self.states[index][x-1][y+1])
            if x == 0 or y == 9:
                successors.append(self.states[index][x][y])
            successors.append(self.generateNextStates(state, action))
            return successors


# test = gameWorld()
# for world in test.terrains:
#     world.showTerrain()

# print "noise: ", test.getNoise()
# test.setNoise(1)
# print "noise is now 1: ", test.getNoise()

# print "livingReward: ", test.getLivingReward()
# test.setLivingReward(0)
# print "livingReward is now 0: ", test.getLivingReward()

# print "discount: ", test.getDiscount()
# test.setDiscount(0)
# print "discount is now 0: ", test.getDiscount()
# print "\n"
# print "startState: ", test.getStartState()
# print "\n"
# print "TransitionalState? ", test.isTransitionalState(test.getStartState())
# print "TerminalState? ", test.isTerminalState(test.getStartState())
# print "\n"

# print "Actions from start state: ", test.getActions(test.getStartState())

# for action in test.getActions(test.getStartState()):
# print "going " + action + " from " + str(test.getStartState()) + " puts us " + str(test.generateNextStates(test.getStartState(), action))
# print "\n"
# print "Terminal Actions: ", test.getActions(State.state((9,0), 2))
# print "\n"
# print "All actions: ", test.getActions(State.state((4,5), 0))
# print "\n"
# print "In the sky: ", test.generateNextStates(State.state((9,0), 0), "finish")
# print "\n"
# print "Completed? ", test.completedRace(test.generateNextStates(State.state((9,0), 0), "finish"))
# print "Not Completed?", test.completedRace(test.getStartState())
# print "\n"
# print "grass==grass? ", Terrain.grass() == Terrain.grass()
# print "grass==mountain? ", Terrain.grass() == Terrain.mountain() 
# print "\n"
# print "No ADP Agents!"
# print "Adding ADP Agent!"
# test.addAgent(Agent.adpAgent(test))
# print test.adpAgentIndex, " ADP Agents!"
# print "adpAgent.waterScore:", test.adpAgents[0].getWaterSkill()
# print "adpAgent.grassScore:", test.adpAgents[0].getGrassSkill()
# print "adpAgent.forestScore:", test.adpAgents[0].getForestSkill()
# print "adpAgent.mountainScore:", test.adpAgents[0].getMountainSkill()
# print "adpAgent State: ", test.getAgentState(test.adpAgents[0])
# print "\n"
# print "No TD Agents!"
# print "Adding TD Agent!"
# test.addAgent(Agent.tdAgent())
# print test.tdAgentIndex, " TD Agents!"
# print "tdAgent.waterScore:", test.tdAgents[0].getWaterSkill()
# print "tdAgent.grassScore:", test.tdAgents[0].getGrassSkill()
# print "tdAgent.forestScore:", test.tdAgents[0].getForestSkill()
# print "tdAgent.mountainScore:", test.tdAgents[0].getMountainSkill()
# print "tdAgent State: ", test.getAgentState(test.tdAgents[0])
# print "\n"
# print "Testing getReward():"
# print "transitionalReward: ", test.getReward(test.adpAgents[0], State.state((float("inf"), float("inf")), 0))
# print "terminalReward: ", test.getReward(test.adpAgents[0], State.state((float("inf"), float("inf")), 2))
# print "not fallen", test.getReward(test.adpAgents[0], test.getAgentState(test.adpAgents[0]))
# print "terrain was: ", test.terrains[0].terrainWorld[0][9]
# print "\n"
# print "Create testAgent"
# testAgent = Agent.tdAgent()
# test.addAgent(testAgent)
# print "getting testAgent State: ", test.getAgentState(testAgent)
# print "Settings testAgent State to (5,4), terrain #1: ", 
# test.setAgentState(testAgent, State.state((5,4), 1))
# print "testAgent State: ", test.getAgentState(testAgent)
# print "moving testAgent: "
# test.moveAgent(testAgent, test.getAgentState(testAgent), 'east')
# print test.getAgentState(testAgent)
# print ""
# print "Test get terrain type: ", test.getTerrainType(State.state((0, 9), 0))
# print "TESTING GET POSSIBLE SUCCESSORS:"
# print "TEST START: "
# test = gameWorld()
# start = test.getStartState()
# print test.getAllPossibleSuccessors(start, 'north')
# print "TEST END: "
# end = State.state((9,0), 0)
# print end.getPosition()
# print test.getAllPossibleSuccessors(end, 'finish')
# print "Testing random state on map 2: "
# inter = State.state((5,5), 2)
# print test.getAllPossibleSuccessors(inter, 'north')
# test = gameWorld()
# print test.getAllPossibleSuccessors(State.state((0,9), 1), 'east')
# print test.getAllPossibleSuccessors(State.state((9,0), 1), 'finish')
# print test.getAllPossibleSuccessors(State.state((5, 9), 1), 'north')
# print test.getAllPossibleSuccessors(State.state((0, 4), 1), 'east')
# print test.getAllPossibleSuccessors(State.state((4,4), 1), 'east')
# test = gameWorld()
# agent = Agent.tdAgent((9,0))
# test.addAgent(agent)
# state = State.state((0,9), 2)
# print test.getReward(agent, state), test.getTerrainType(state)
# print test.tdAgents[0].skillLevels[test.getTerrainType(state)]
