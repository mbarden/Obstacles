#
#  Empirical MDP
#
#  Purpose: Estimate MDP based on empirical observations of transitions and rewards
#
#  Author: Willie Boag
#


from collections import defaultdict
import state as State


class EmpiricalMDP:

    def __init__(self, all_qstate_results, rewardValues, skills):

        # Parameters
        self.alpha = 0.5

        # Constant rewards for each terrain type
        self.rewardValues = rewardValues


        # Empirical estimate of transition model
        # Initially, assume every q-state result is equally likely
        counts = defaultdict(lambda:defaultdict(lambda:{}))
        for state,action,nextState in all_qstate_results:
            counts[state][action][nextState] = 1
        self.frequencies = counts


        # Inferred skills
        self.skills = skills


        # Convergence streaks
        self.streaks = { k:0 for k in self.skills }
        self.completed = []



    def getPossibleActions(self, state):
        return self.frequencies[state].keys()



    def getSuccessors(self, state):
        retVal = []
        for action in self.frequencies[state]:
            retVal += self.frequencies[state][action].keys()
        return list(retVal)



    def getStates(self):
        return self.frequencies.keys()



    def getReward(self, state, action, nextState):
        if action == 'finish':
            return 1000

        x, y = state.getPosition()
        manDist = (abs(y - 9) + abs(x - 0))

        terrain = state.getTerrainType()
        skillScore = self.skills[terrain] * self.rewardValues[terrain]

        return skillScore + manDist



    def isTerminal(self, state):
        return (self.frequencies[state].keys() == ['finish'])



    def getTransitionStatesAndProbs(self, state, action):
        if action not in self.getPossibleActions(state):
            raise "Illegal action!"

        x, y = state.getPosition()
        t = state.terrain

        if action == 'finish':
            return [(state, 1)]

        # Store mapping from state to likelihood
        possibles = defaultdict(lambda:0)

        chanceToSlideLeft = 0.1 - (0.01 * (abs(x - 9)))
        if x != 9:
            possibles[State.state((x+1,y),t)]   += chanceToSlideLeft
        else:
            possibles[state]                    += chanceToSlideLeft


        chanceToSlideDown = 0.1 - (0.01 * (abs(y - 0)))
        if y != 0:
            possibles[State.state((x,y-1),t)]   += chanceToSlideDown
        else:
            possibles[state]                    += chanceToSlideDown


        terrainElement = state.getTerrainType()
        if terrainElement == 'mountain':
            chanceToFall = abs(self.skills[terrainElement] - 1) / 2
        else:
            chanceToFall = abs(self.skills[terrainElement] - 1) / 2

        if x != 9 and y != 0:
            possibles[State.state((x+1,y-1),t)] += chanceToFall
        elif x != 9:
            possibles[State.state((x+1,y  ),t)] += chanceToFall
        elif y != 0:
            possibles[State.state((x  ,y-1),t)] += chanceToFall
        elif x == 9 and y == 0:
            possibles[State.state((x  ,y  ),t)] += chanceToFall
        else:
            raise 'didnt account for this'


        if action == 'north':
            newState = State.state((x  ,y-1),t)
        if action == 'east':
            newState = State.state((x+1,y  ),t)
        if action == 'west':
            newState = State.state((x-1,y  ),t)
        if action == 'south':
            newState = State.state((x  ,y+1),t)
        possibles[newState] += 1 - (chanceToFall + chanceToSlideLeft + chanceToSlideDown)

        # Probabilities must sum to 1
        assert abs(sum(possibles.values()) - 1) < .001

        return possibles.items()


    def converged(self):
        return len(self.completed) == 4


    def update(self, state, action, nextState, reward, terrain):

        # If skill for terrain has already convereged
        if terrain in self.completed:
            return

        # Get empirical skill estimate
        x,y = state.getPosition()
        skillScore = reward - (abs(y - 9) + abs(x - 0))
        skillSample = skillScore/self.rewardValues[terrain]

        difference = skillSample - self.skills[terrain]
        if difference < .01:
            self.streaks[terrain] += 1
            if self.streaks[terrain] >= 25:
                self.completed.append(terrain)
        else:
            self.streaks[terrain] = 0
            self.skills[terrain] = (1 - self.alpha) * self.skills[terrain]   +     \
                                        self.alpha  * skillSample
        #print self.skills
