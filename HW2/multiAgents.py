# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        foodPositions=currentGameState.getFood().asList()
        if action=='Stop':
		return -float('inf')
        for ghostLocation in newGhostStates:
		if(ghostLocation.getPosition()==newPos and ghostState.scaredTimer is 0):
			return -float('inf')
	max=-float('inf')
	for foodLocation in foodPositions:
		xDistance=-1*abs(foodLocation[0]-newPos[0])
		yDistance=-1*abs(foodLocation[1]-newPos[1])
		if max<xDistance+yDistance:
			max=xDistance+yDistance
        "*** YOUR CODE HERE ***"
        return max
def scoreEvaluationFunction(currentGameState):
        return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """
    def __init__(self,evalFn='scoreEvaluationFunction',depth = 2):
        self.depth = int(depth)
        self.evaluationFunction=util.lookup(evalFn,globals())

class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        possiblePacmanMoves = gameState.getLegalActions(0) # Get Possible Moves for root of the min max tree
        maxMove = (-float('inf'),None) # Best Move
        for move in possiblePacmanMoves:
            possibleBestMove = max(maxMove[0], self.minValue(gameState.generateSuccessor(0, move), 1,self.depth))
            if possibleBestMove!= maxMove[0]:
                maxMove=(possibleBestMove,move)
        return maxMove[1]

    def value(self,gameState,agentIndex,depth):
        if agentIndex==gameState.getNumAgents():
            depth-=1
            agentIndex=0
        if agentIndex==0:
            return self.maxValue(gameState, depth)
        else:
            return self.minValue(gameState, agentIndex,depth)

    def minValue(self, gameState,ghostIndex,depth):
        if (gameState.isLose()):
            return self.evaluationFunction(gameState)
        if(gameState.isWin()):
             return self.evaluationFunction(gameState)
        if(depth==0):
             return self.evaluationFunction(gameState)
        possibleMovesForGhosts= gameState.getLegalActions(ghostIndex)
        minScore = float('inf')
        for move in possibleMovesForGhosts:
            minScore = min(minScore, self.value(gameState.generateSuccessor(ghostIndex, move),ghostIndex+1,depth))
        return minScore

    def maxValue(self, gameState,depth):
        if (gameState.isLose()):
            return self.evaluationFunction(gameState)
        if(gameState.isWin()):
             return self.evaluationFunction(gameState)
        if(depth==0):
             return self.evaluationFunction(gameState)
        possiblePacmanMoves = gameState.getLegalActions(0)
        maxScore = -float('inf')
        for move in possiblePacmanMoves:
            maxScore = max(maxScore, self.value(gameState.generateSuccessor(0, move),1,depth))
        return maxScore



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        possiblePacmanMoves = gameState.getLegalActions(0) # Get Possible Moves for root of the min max tree
        maxMove = (-float('inf'),None) # Best Move
        alpha=-float('inf')
        beta=float('inf')
        for move in possiblePacmanMoves:
            possibleBestMove = max(maxMove[0], self.minValue(gameState.generateSuccessor(0, move), 1,self.depth,alpha,beta))
            if possibleBestMove!= maxMove[0]:
                maxMove=(possibleBestMove,move)
            if maxMove[0]>beta:
                return maxMove[0]
            alpha=max(alpha,maxMove[0])
        return maxMove[1]

    def value(self,gameState,agentIndex,depth,alpha,beta):
        if agentIndex==gameState.getNumAgents():
            depth-=1
            agentIndex=0
        if agentIndex==0:
            return self.maxValue(gameState,depth,alpha,beta)
        else:
            return self.minValue(gameState,agentIndex,depth,alpha,beta)

    def minValue(self, gameState,ghostIndex,depth,alpha,beta):
        if (gameState.isLose()):
            return self.evaluationFunction(gameState)
        if(gameState.isWin()):
             return self.evaluationFunction(gameState)
        if(depth==0):
             return self.evaluationFunction(gameState)
        possibleMovesForGhosts= gameState.getLegalActions(ghostIndex)
        minScore = float('inf')
        for move in possibleMovesForGhosts:
            minScore = min(minScore, self.value(gameState.generateSuccessor(ghostIndex, move),ghostIndex+1,depth,alpha,beta))
            if minScore<alpha:
                return minScore
            beta=min(beta,minScore)
        return minScore

    def maxValue(self, gameState,depth,alpha,beta):
        if (gameState.isLose()):
            return self.evaluationFunction(gameState)
        if(gameState.isWin()):
             return self.evaluationFunction(gameState)
        if(depth==0):
             return self.evaluationFunction(gameState)
        possiblePacmanMoves = gameState.getLegalActions(0)
        maxScore = -float('inf')
        for move in possiblePacmanMoves:
            maxScore = max(maxScore, self.value(gameState.generateSuccessor(0, move),1,depth,alpha,beta))
            if maxScore>beta:
                return maxScore
            alpha=max(alpha,maxScore)
        return maxScore

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getAction(self, gameState):
        possiblePacmanMoves = gameState.getLegalActions(0) # Get Possible Moves for root of the min max tree
        maxMove = (-float('inf'),None) # Best Move
        for move in possiblePacmanMoves:
            possibleBestMove = max(maxMove[0], self.minValue(gameState.generateSuccessor(0, move), 1,self.depth))
            if possibleBestMove!= maxMove[0]:
                maxMove=(possibleBestMove,move)
        return maxMove[1]

    def value(self,gameState,agentIndex,depth):
        if agentIndex==gameState.getNumAgents():
            depth-=1
            agentIndex=0
        if agentIndex==0:
            return self.maxValue(gameState, depth)
        else:
            return self.minValue(gameState, agentIndex,depth)

    def minValue(self, gameState,ghostIndex,depth):
        if (gameState.isLose()):
            return self.evaluationFunction(gameState)
        if(gameState.isWin()):
             return self.evaluationFunction(gameState)
        if(depth==0):
             return self.evaluationFunction(gameState)
        possibleMovesForGhosts= gameState.getLegalActions(ghostIndex)
        avgScore=[]
        for move in possibleMovesForGhosts:
            avgScore.append(self.value(gameState.generateSuccessor(ghostIndex, move),ghostIndex+1,depth))
        return sum(avgScore)/len(avgScore)

    def maxValue(self, gameState,depth):
        if (gameState.isLose()):
            return self.evaluationFunction(gameState)
        if(gameState.isWin()):
             return self.evaluationFunction(gameState)
        if(depth==0):
             return self.evaluationFunction(gameState)
        possiblePacmanMoves = gameState.getLegalActions(0)
        maxScore = -float('inf')
        for move in possiblePacmanMoves:
            maxScore = max(maxScore, self.value(gameState.generateSuccessor(0, move),1,depth))
        return maxScore



def betterEvaluationFunction(currentGameState):
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    foodPositions=currentGameState.getFood().asList()
    for ghostLocation in newGhostStates:
        if(ghostLocation.getPosition()==newPos and ghostState.scaredTimer is 0):
            return -float('inf')
	max=-float('inf')
	for foodLocation in foodPositions:
		xDistance=-1*abs(foodLocation[0]-newPos[0])
		yDistance=-1*abs(foodLocation[1]-newPos[1])
		if max<xDistance+yDistance:
			max=xDistance+yDistance
    if not foodPositions:
        return currentGameState.getScore()
    return currentGameState.getScore()+max

# Abbreviation
better = betterEvaluationFunction
