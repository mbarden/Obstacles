####
#
# Agents
# Jake Kinsman
# 11/28/2014
#
####

###
# README:
#
# 1.  If you want a dictionary with a default value (util.counters from UC Berkeley Problem Sets), 
#       use a defaultdict as shown:  a = defaultdict(lambda: <DEFAULT-VALUE> )
#
# 2.  Choose action should use your current model of the world (however you choose to store it), 
#       and compute the optimal action to be taken.  If you are in a terminal state, the only action is "finish"
#
# 3.  Update needs to perform whatever learning is needed to your model after each action is performed.
#
# 4.  the gameworld variable passed to your agents methods should contain all information required to perform your computations.
#
# 5.  Feel free to add more methods as needed!  training the agents only calls the methods provided, 
#       and racing only calls chooseAction()
###

###
# GAMEWORLD FUNCTIONALITY:
# def getDiscount(self):
#   returns discount factor [0,1)
# def getLivingReward(self):
#    returns reward for staying alive
# 
###


import random
from collections import defaultdict
from empiricalMDP import EmpiricalMDP
from  valueIterationAgent import ValueIterationAgent
from policyIterationAgent import PolicyIterationAgent



def flipCoin( p ):
    r = random.random()
    return r < p


class agent(object):

    def __init__(self):
        self.rewardValues = { 'mountain':3, 'forest':4, 'water':4, 'grass':5 }
        self.skillLevels  = { 'mountain':1, 'forest':1, 'water':1, 'grass':1 }
        self.index = None
        self.state = None

    def getSkill(self, skill):
        return self.skillLevels[skill]

    def getWaterSkill(self):
        return self.getSkill('water')

    def getGrassSkill(self):
        return self.getSkill('grass')

    def getForestSkill(self):
        return self.getSkill('forest')

    def getMountainSkill(self):
        return self.getSkill('mountain')

    def setSkill(self, skill, val):
        self.skillLevels[skill] = val

    def setWaterSkill(self, val):
        self.setSkill('water', val)

    def setGrassSkill(self, val):
        self.setSkill('grass', val)

    def setForestSkill(self, val):
        self.setSkill('forest', val)

    def setMountainSkill(self, val):
        self.setSkill('mountain', val)

    def __eq__(self, arg):
        return arg.type == self.type and arg.index == self.index

    def getIndex(self):
        return self.index

    def setIndex(self, value):
        self.index = value

    def getState(self):
        return self.state
    
    def setState(self, state):
        self.state = state

    def endTraining(self):
        self.epsilon = 0.02
        self.alpha = 1.
        self.discount = 1.

    
class randomAgent(agent):
    
    def __init__(self):
        super(randomAgent, self).__init__()
        self.type = "random"

    def chooseAction(self, actions):
        if flipCoin(0.08):
            filteredActions = filter(lambda n: n == 'south' or n == 'west' or n == 'finish', actions)
            if filteredActions == []: filteredActions = actions
        else:
            filteredActions = filter(lambda n: n == 'north' or n == 'east' or n == 'finish', actions)
        return random.choice(filteredActions)
    
    def update(self):
        pass


class adpAgent(agent):
    
    def __init__(self, gameworld, all_qstate_results, discount=0.5):
        super(adpAgent, self).__init__()
        self.type = "adp"

        # Parameters
        self.epsilon = 0.4
        self.discount = discount

        # Estimate of model
        self.inferredSkills = { k:1 for k  in ['water','grass','forest','mountain'] }
        self.empirical_mdp = EmpiricalMDP(all_qstate_results, self.rewardValues, self.inferredSkills)
        #print 'solving MDP'
        self.solver = PolicyIterationAgent(self.empirical_mdp, discount=discount, iterations=10)
        #print 'solved MDP'

        #exit()

        # Keep track of number of completed episodes
        self.converged = False
        self.completed = 0
        self.nextUpdate = 1


    def setEpsilon(self, epsilon):
        self.epsilon = epsilon


    def update(self, state, terrain, action, nextState, reward):

        # If already converged, then skip update
        if self.converged:
            return

        # update empirical MDP
        self.empirical_mdp.update(state, action, nextState, reward, terrain)

        # If converged AFTER most recent update, then solve MDP for final time
        if self.empirical_mdp.converged():
            #print str(self.completed) + ': final solving'
            self.solver = self.solver = PolicyIterationAgent(self.empirical_mdp, discount=self.discount, iterations=50)
            #print 'solved MDP'
            self.converged = True
            return

        # If finished epsiode
        if action == 'finish':
            #print 'finished\n\n\n'
            # Backoff how often you re-solve (speeds up training)
            if self.completed == self.nextUpdate:
                #print str(self.completed) + ': solving again'
                self.solver = self.solver = PolicyIterationAgent(self.empirical_mdp, discount=self.discount, iterations=50)
                #print 'solved MDP'
                self.nextUpdate *= 2
            self.completed += 1

    def chooseAction(self, state):
        ###Your Code Here :)###
        #return random.choice(filter(lambda a: (a=='north') or (a=='east') or (a=='finish'), self.empirical_mdp.getPossibleActions(state)))

        if flipCoin(self.epsilon):
            #print 'random'
            return random.choice(self.empirical_mdp.getPossibleActions(state))
        else:
            #print 'policy'
            return self.solver.getAction(state)


class tdAgent(agent):
    
    def __init__(self, goalPosition, eps = 0.5, alp = 0.9, gam = 0.9):
        super(tdAgent, self).__init__()
        self.type = "td"
        self.x, self.y = goalPosition
        self.weights = dict()
        self.qvalues = dict()
        self.epsilon = eps
        self.alpha = alp
        self.discount = gam
        self.its = 0
        self.oldAct = None
        ###Your Code Here :)###

    def __dirToVect(self, action):
        if action == 'north':
            return (0,-1)
        elif action == 'south':
            return (0,1)
        elif action == 'east':
            return (1,0)
        elif action == 'west':
            return (-1,0)
        else:
            return (0,0)

    def __getFeatures(self, state, action):

        x,y = state.getPosition()
        dx, dy = self.__dirToVect(action)
        next_x, next_y = x + dx, y + dy
        dy = next_y - self.y + 1
        dx = self.x - next_x + 1
        norm = 1. / (dx + dy)

#        print (x,y)
#        if (x,y) == (8,0) or (x,y) == (9,1):
#            print ((x,y), action), (dx, dy)
        return dict({(state, action) : 1.})
        if (x,y) != (float('inf'), float('inf')):
#            feat = dict({state.getTerrainType() : .01})
#            feat = dict({state : 1.})
            feat = dict({'dy %d' %(dy) : 1.,
                         'dx %d' %(dx) : 1.,
                         'action %s' %(action) : 1.,
                         'world %d' %(state.getWorld()) : 1.,
                         state.getTerrainType() : 1.})
#            feat = dict({'dy %d' %(dx) : norm,
#                         'dx %d' %(dx): norm,
#                         state.getTerrainType() : .01})
#            feat = dict({'dy %d' %(dy) : .1 / dy,
#                         'dx %d' %(dx) : .1 / dx,
#                         'action %s' %(action) : 1.,
#                         state.getTerrainType() : .01})
#            feat = dict({'dy' : .1 / dy,
#                         'dx' : .1 / dx,
#                         state.getTerrainType() : .01})
#            feat = dict({'dy %d' %(dx) : .1**dy,
#                         'dx %d' %(dx): .1**dx,
#                         state.getTerrainType() : .01})

            #feat = dict({'dy %d' %(dy) : .1 / (dy * dy),
            #'dx %d' %(dx): .1 / (dx * dx),
            #state.getTerrainType() : .01})
        else:
            feat = dict({'finish' : 1000})

        return feat
    def computeValueFromQValues(self, state):
        actions = self.getLegalActions(state)

        if not actions:
            return 0.0

        return max(self.getQValue(state, action) for action in actions)

    def getLegalActions(self, state):
        return self.actions

    def computeActionFromQValues(self, state):
        actions = self.getLegalActions(state)

        if not actions:
            return None

#        actvals = map(lambda action: self.getQValue(state, action) + random.uniform(0, .00001), actions)
        actvals = map(lambda action: self.getQValue(state, action), actions)
#        if len(frozenset(actvals)) == 1:
#            print "all the same"
#        elif not self.its % 1:
#            print zip(actions, actvals)
        return max(actions, key = lambda action: self.getQValue(state, action) + random.uniform(0,.00001))

    def getAction(self, state):
        return random.choice(self.getLegalActions(state)) if flipCoin(self.epsilon) else self.computeActionFromQValues(state)
#        return random.choice(
#            filter(
#                lambda action: action not in ('west', 'south'),
#                self.getLegalActions(state))
#        ) if flipCoin(self.epsilon) else self.computeActionFromQValues(state)

    def getQValue(self, state, action):
        features = self.__getFeatures(state, action)
#        print features
        return sum(self.weights.get(feature,0.) * features[feature] for feature in features.keys())

    def __printWeights(self):
        for key, val in self.weights.items():
            print key, val
        print

    def update(self, state, terrainType, action, nextState, reward, nextActions):
        ###Your Code Here :)###
        DEBUG = 0
        p = False if not DEBUG else not (self.its % 50000)
#        p = True
        self.its += 1
        features = self.__getFeatures(state, action)
#        self.actions = filter(lambda action : action not in ['west', 'south'], nextActions)
        self.actions = nextActions
        pos = state.getPosition()
        qv = self.computeValueFromQValues(nextState)
        difference = reward + \
                     self.discount * qv - \
                     self.getQValue(state, action)
        #print features
        #print reward
#        print reward, difference, [(feature,
#                                    self.weights.get(feature, 0.) + \
#                                    self.alpha * difference * features[feature])
#                                   for feature in features.keys()]
        if p:
            print
#            print features
            self.__printWeights()
 #           print reward, difference
        self.weights.update((feature, self.weights.get(feature,0.) + \
                             self.alpha * difference * features[feature])
                            for feature in features.keys())
        if p:
            self.__printWeights()
            print

    def chooseAction(self, actions, state, terrainType):
        ###Your Code Here :)###
#        self.actions = filter(lambda action : action not in ['west', 'south'], actions)
        self.actions = actions
        act = self.getAction(state)
        self.oldAct = act
        pos = state.getPosition()
        #if pos == (8, 0) or pos == (9,1):# or not self.its % 1000:
        #    print state, act
        return act

