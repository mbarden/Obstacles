####
#
# Relay Race
# Jake Kinsman
# 11/28/2014
#
####

import terrain as Terrain
import state as State
import agent as Agent
import gameworld as Gameworld
import graphics as Graphics

import copy
import random
from collections import defaultdict

#random.seed(1)
class relayRace(object):
    
    def __init__(self):
        self.world = Gameworld.gameWorld()
        self.highScores = defaultdict(lambda: 0)
        self.tdRaceOrder = list()
        self.adpRaceOrder = list()
        self.randomRaceOrder = list()

        # Every possible (state,action,nextState) tuple
        transitions = []
        for j in range(3):
            for k in range(10):
                for l in range(10):
                    curState = self.world.states[j][k][l]
                    for action in self.world.getActions(curState):
                        for nextState in self.world.getAllPossibleSuccessors(curState, action):
                            transitions.append( (curState, action, nextState) )

        skills = { k:(random.random() + .5)  for  k   in  ['water','grass','forest','mountain'] }
        for i in range(3):
            # Each team has equal skills (apples to apples comparison)
            self.world.addAgent(Agent.adpAgent(self.world, transitions, discount=self.world.discount), skills)
            self.world.addAgent(Agent.tdAgent((9,0), gam=self.world.discount), skills)
            self.world.addAgent(Agent.randomAgent(), skills)
    
    #tested
    def trainAgents(self, numIter):
        for index, state in enumerate(self.world.states):

            for training in range(numIter):
                print training
                for tdAgent in self.world.tdAgents:
                    tdAgent.setState(self.world.getStartState(index))
                    movements = list()
                    score = 0
                    i = 0
                    while not self.world.completedRace(tdAgent.getState(), index):
                        oldState = tdAgent.getState()
                        terrainType = oldState.getTerrainType()
                        actions = self.world.getActions(tdAgent.getState())
                        action = tdAgent.chooseAction(actions, oldState, terrainType)
                        self.world.moveAgent(tdAgent, tdAgent.getState(), action)
                        newState = tdAgent.getState()
                        reward = self.world.getReward(tdAgent, oldState)
                        movements.append(tdAgent.getState())
                        nextActions = self.world.getActions(newState)
                        tdAgent.update(oldState, terrainType, action, newState, reward, nextActions)
                    for ind, state in enumerate(movements):
                        if self.world.completedRace(state, 0):
                            score += (self.world.transitionalReward * (self.world.discount ** ind))
                        elif self.world.completedRace(state, 2):
                            score += (self.world.terminalReward * (self.world.discount ** ind))
                        else:
                            score += (self.world.getReward(tdAgent, state) * (self.world.discount ** ind))
                    if score > self.highScores[(tdAgent.type, tdAgent.index, index)]:
                        self.highScores[(tdAgent.type, tdAgent.index, index)] = score

                for adpAgent in self.world.adpAgents:
                    adpAgent.setState(self.world.getStartState(index))
                    movements = list()
                    score = 0
                    while not self.world.completedRace(adpAgent.getState(), index):
                        oldState = adpAgent.getState()
                        terrainType = oldState.getTerrainType()
                        actions = self.world.getActions(adpAgent.getState())
                        action = adpAgent.chooseAction(oldState)
                        self.world.moveAgent(adpAgent, adpAgent.getState(), action)
                        newState = adpAgent.getState()
                        reward = self.world.getReward(adpAgent, oldState)
                        movements.append(adpAgent.getState())
                        adpAgent.update(oldState, terrainType, action, newState, reward)
                    for ind, state in enumerate(movements):
                        if self.world.completedRace(state, 0):
                            score += (self.world.transitionalReward * (self.world.discount ** ind))
                        elif self.world.completedRace(state, 2):
                            score += (self.world.terminalReward * (self.world.discount ** ind))
                        else:
                            score += (self.world.getReward(adpAgent, state) * (self.world.discount ** ind))
                    if score > self.highScores[(adpAgent.type, adpAgent.index, index)]:
                        self.highScores[(adpAgent.type, adpAgent.index, index)] = score

                for randomAgent in self.world.randomAgents:
                    randomAgent.setState(self.world.getStartState(index))
                    movements = list()
                    score = 0
                    while not self.world.completedRace(randomAgent.getState(), index):
                        actions = self.world.getActions(randomAgent.getState())
                        action = randomAgent.chooseAction(actions)
                        self.world.moveAgent(randomAgent, randomAgent.getState(), action)
                        movements.append(randomAgent.getState())
                        randomAgent.update()
                    for ind, state in enumerate(movements):
                        if self.world.completedRace(state, 0):
                            score += (self.world.transitionalReward * (self.world.discount ** ind))
                        elif self.world.completedRace(state, 2):
                            score += (self.world.terminalReward * (self.world.discount ** ind))
                        else:
                            score += (self.world.getReward(randomAgent, state) * (self.world.discount ** ind))
                    #print score
                    if score > self.highScores[(randomAgent.type, randomAgent.index, index)]:
                        self.highScores[(randomAgent.type, randomAgent.index, index)] = score
    #tested
    def arrangeTeam(self):
        
        adpHighScore, adpArrangement = 0, list()
        tdHighScore, tdArrangement = 0, list()
        randomHighScore, randomArrangement = 0, list()

        for i, agentI in enumerate(self.world.adpAgents):
            for j, agentJ in enumerate(self.world.adpAgents):
                for k, agentK in enumerate(self.world.adpAgents):
                    ####
                    if i != j and j != k and i != k:
                        agentIScore = self.highScores[(agentI.type, agentI.index, 0)]
                        agentJScore = self.highScores[(agentJ.type, agentJ.index, 1)]
                        agentKScore = self.highScores[(agentK.type, agentK.index, 2)]
                        score = agentIScore + agentJScore + agentKScore
                        if score > adpHighScore:
                            adpHighScore = score
                            adpArrangement = [agentI, agentJ, agentK]

        for i, agentI in enumerate(self.world.tdAgents):
            for j, agentJ in enumerate(self.world.tdAgents):
                for k, agentK in enumerate(self.world.tdAgents):
                    ####
                    if i != j and j != k and i != k:
                        agentIScore = self.highScores[(agentI.type, agentI.index, 0)]
                        agentJScore = self.highScores[(agentJ.type, agentJ.index, 1)]
                        agentKScore = self.highScores[(agentK.type, agentK.index, 2)]
                        score = agentIScore + agentJScore + agentKScore
                        if score > tdHighScore:
                            tdHighScore = score
                            tdArrangement = [agentI, agentJ, agentK]

        
        for i, agentI in enumerate(self.world.randomAgents):
            for j, agentJ in enumerate(self.world.randomAgents):
                for k, agentK in enumerate(self.world.randomAgents):
                    ####
                    if i != j and j != k and i != k:
                        agentIScore = self.highScores[(agentI.type, agentI.index, 0)]
                        agentJScore = self.highScores[(agentJ.type, agentJ.index, 1)]
                        agentKScore = self.highScores[(agentK.type, agentK.index, 2)]
                        score = agentIScore + agentJScore + agentKScore
                        if score > randomHighScore:
                            randomHighScore = score
                            randomArrangement = [agentI, agentJ, agentK]
        
        self.adpRaceOrder = adpArrangement
        self.tdRaceOrder = tdArrangement
        self.randomRaceOrder = randomArrangement
        def getIndex(agent):
            return agent.index

        print "adp: ", map(getIndex, adpArrangement), adpHighScore
        print "td: ", map(getIndex, tdArrangement), tdHighScore
        print "random: ", map(getIndex, randomArrangement), randomHighScore

    #tested
    def race(self):
        
        randomStates = list()
        adpStates = list()
        tdStates = list()
        randomScores = list()
        adpScores = list()
        tdScores = list()
        
        #Race Random Agents
        for index, racingAgent in enumerate(self.randomRaceOrder):
            racingAgentMovements = list()
            racingAgent.setState(self.world.getStartState(index))
            racingAgent.endTraining()
            while not self.world.completedRace(racingAgent.getState(), index):
                oldState = racingAgent.getState()
                terrainType = oldState.getTerrainType()
                actions = self.world.getActions(racingAgent.getState())
                action = racingAgent.chooseAction(actions)
                self.world.moveAgent(racingAgent, racingAgent.getState(), action)
                racingAgentMovements.append(racingAgent.getState())
            randomStates.append(racingAgentMovements)
            score = 0
            for ind, state in enumerate(racingAgentMovements):
                if self.world.completedRace(state, 0):
                    score += (self.world.transitionalReward * (self.world.discount ** ind))
                elif self.world.completedRace(state, 2):
                    score += (self.world.terminalReward * (self.world.discount ** ind))
                else:
                    score += (self.world.getReward(racingAgent, state) * (self.world.discount ** ind))
            randomScores.append(score)

        #Race ADP Agents
        for index, racingAgent in enumerate(self.adpRaceOrder):
            racingAgentMovements = list()
            racingAgent.setEpsilon(0.01)
            racingAgent.setState(self.world.getStartState(index))
            while not self.world.completedRace(racingAgent.getState(), index):
                oldState = racingAgent.getState()
                terrainType = oldState.getTerrainType()
                actions = self.world.getActions(racingAgent.getState())
                action = racingAgent.chooseAction(oldState)
                #print oldState, '\t', action
                self.world.moveAgent(racingAgent, racingAgent.getState(), action)
                racingAgentMovements.append(racingAgent.getState())
            adpStates.append(racingAgentMovements)
            score = 0
            for ind, state in enumerate(racingAgentMovements):
                if self.world.completedRace(state, 0):
                    score += (self.world.transitionalReward * (self.world.discount ** ind))
                elif self.world.completedRace(state, 2):
                    score += (self.world.terminalReward * (self.world.discount ** ind))
                else:
                    score += (self.world.getReward(racingAgent, state) * (self.world.discount ** ind))
            adpScores.append(score)

        #Race TD Agents
        for index, racingAgent in enumerate(self.tdRaceOrder):
            racingAgentMovements = list()
            racingAgent.endTraining()
            racingAgent.setState(self.world.getStartState(index))
            while not self.world.completedRace(racingAgent.getState(), index):
                oldState = racingAgent.getState()
                terrainType = oldState.getTerrainType()
                actions = self.world.getActions(racingAgent.getState())
                action = racingAgent.chooseAction(actions, oldState, terrainType)
                self.world.moveAgent(racingAgent, racingAgent.getState(), action)
                racingAgentMovements.append(racingAgent.getState())
            tdStates.append(racingAgentMovements)
            score = 0
            for ind, state in enumerate(racingAgentMovements):
                if self.world.completedRace(state, 0):
                    score += (self.world.transitionalReward * (self.world.discount ** ind))
                elif self.world.completedRace(state, 2):
                    score += (self.world.terminalReward * (self.world.discount ** ind))
                else:
                    score += (self.world.getReward(racingAgent, state) * (self.world.discount ** ind))
            tdScores.append(score)

        return [randomStates, adpStates, tdStates, randomScores, adpScores, tdScores], self

a = relayRace()
print ""
print "TRAINING AGENTS..."
print ""
a.trainAgents(100)
a.arrangeTeam()


'''
for i,agent in enumerate(a.adpRaceOrder):
    agent.endTraining()
    agent.epsilon = 0.0
    print agent.epsilon, agent.discount, agent.alpha
    bad = False
    for j in range(10):
        for k in range(10):
            state = a.world.states[i][k][j]
            actions = a.world.getActions(state)
            action = agent.chooseAction(state)
            if action == 'west' or action == 'south':
                bad = True

    bad = True
    if bad:
        for j in range(10):
            for k in range(10):
                state = a.world.states[i][k][j]
                actions = a.world.getActions(state)
                action = agent.chooseAction(state)
                if action == 'south' or action == 'west':
                        print '%7s' % action.upper(),
                else:
                        print '%7s' % action,
            print
        print '\n\n'
'''

'''
#print '---'


# display Policy
for i,agent in enumerate(a.tdRaceOrder):
    agent.endTraining()
    agent.epsilon = 0.0
    print agent.epsilon, agent.discount, agent.alpha
    bad = False
    for j in range(10):
        for k in range(10):
            state = a.world.states[i][k][j]
            actions = a.world.getActions(state)
            action = agent.chooseAction(actions, state,
                                        state.getTerrainType())
            if action == 'west' or action == 'south':
                bad = True

    bad = True
    if bad:
        for j in range(10):
            for k in range(10):
                state = a.world.states[i][k][j]
                actions = a.world.getActions(state)
                action = agent.chooseAction(actions, state,
                                            state.getTerrainType())
                if action == 'south' or action == 'west':
                        print '%7s' % action.upper(),
                else:
                        print '%7s' % action,
            print
        print '\n\n'

#    printVisited = True
#    if printVisited:
#        for j in range(10):
#            for k in range(10):
#                state = a.world.states[i][k][j]
#                v = agent.visited[state]
#                if 'finish' in v:
#                    print '    ' + str(v['finish']),
#                else:
#                    print ' %3d/%3d/%3d/%3d ' % (v['north'],v['east'],v['west'],v['south']),
#            print
#        print '\n\n'

    printQvals = True
    if printQvals:
        for j in range(10):
            for k in range(10):
                state = a.world.states[i][k][j]
                actions = a.world.getActions(state)
                v = {'north':0,'east':0,'west':0,'south':0}
                v.update({ a:agent.getQValue(state,a) for a in actions })
                if 'finish' in v:
                    print '    ' + str(v['finish']),
                else:
                    print ' %3f/%3f/%3f/%3f ' % (v['north'],v['east'],v['west'],v['south']),
            print
        print '\n\n'


#exit()
'''

'''
# display Terrain
for i in range(3):
    for j in range(10):
        for k in range(10):
            print '%10s' % a.world.states[i][k][j].getTerrainType(),
        print
    print '\n\n'
'''

'''
# display Skills
print 'tdAgents'
for agent in a.tdRaceOrder:
    print '\t', agent.skillLevels
    print '\t\t', agent.weights
print

print 'adpAgents'
for agent in a.adpRaceOrder:
    print '\t', agent.skillLevels
print

print 'randomAgents'
for agent in a.randomRaceOrder:
    print '\t', agents.skillLevels
print

#exit()
'''

print "\nRACING AGENTS..."
print ""
results, race = a.race()
print "First RAND AGENT: \t", results[0][0][len(results[0][0]) - 1], "\t", results[3][0]
print "Second RAND AGENT: \t", results[0][1][len(results[0][1]) - 1], "\t", results[3][1]
print "Third RAND AGENT: \t", results[0][2][len(results[0][2]) - 1], "\t", results[3][2]
print ""
print "First ADP AGENT: \t", results[1][0][len(results[1][0]) - 1], "\t", results[4][0]
print "Second ADP AGENT: \t", results[1][1][len(results[1][1]) - 1], "\t", results[4][1]
print "Third ADP AGENT: \t", results[1][2][len(results[1][2]) - 1], "\t", results[4][2]
print ""
print "First TD AGENT: \t", results[2][0][len(results[2][0]) - 1], "\t", results[5][0]
print "Second TD AGENT: \t", results[2][1][len(results[2][1]) - 1], "\t", results[5][1]
print "Third TD AGENT: \t", results[2][2][len(results[2][2]) - 1], "\t", results[5][2]
print ""
print "BEGINNING SIMULATION:"
print ""
Graphics.simulation(results, race)
