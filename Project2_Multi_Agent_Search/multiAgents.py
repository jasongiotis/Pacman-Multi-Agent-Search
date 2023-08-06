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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
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

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        "*** YOUR CODE HERE ***"

        food_distance=[manhattanDistance(food, newPos) for food in newFood.asList()] #manhatan distance for each food
        ghost_distance=[(manhattanDistance(ghost, newPos)) for ghost in childGameState.getGhostPositions()] #manhatan distance for each ghost

        if currentGameState.getPacmanPosition() == newPos: #dont want to loop around or stay still
            return (-(float("inf")))
        if min(ghost_distance)<1 : #dont fall into enemy while not immortal
            return (-(float("inf")))
        if len(food_distance)==0: # no more food means we win
            return ((float("inf")))
        #850 and 8000 are the best numbers i could find
        return ((850*len(food_distance)+8000*sum(food_distance))/(sum(food_distance)*len(food_distance)))



def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def max_move(gameState, depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth: #special cases
                return (self.evaluationFunction(gameState), None)
            Actions = gameState.getLegalActions(0)
            childval = [min_move(gameState.getNextState(0, action), 1, depth)[0] for action in Actions]
            move = Actions[childval.index(max(childval))] #finding the right move
            return (max(childval), move)  ## max value  and its move


        def min_move(gameState, agentID, depth):
            if  gameState.isWin() or gameState.isLose():  #special cases
                return (self.evaluationFunction(gameState), None)
            Actions = gameState.getLegalActions(agentID)
            if (agentID == gameState.getNumAgents() - 1):    #calling every agent
                childval=[(max_move(gameState.getNextState(agentID, action), depth + 1)[0]) for action in Actions]#max move for each child
            else:
                childval = [(min_move(gameState.getNextState(agentID, action),agentID+1, depth )[0]) for action in Actions]#mmin move for each child
            move = Actions[childval .index(min(childval))]  #finding the right move
            return (min(childval), move)         ## max value  and its move



        return max_move(gameState, 0)[1] ###starting from root and returning the actions

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def max_move(gameState, depth, a, b):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:   #special cases
                return (self.evaluationFunction(gameState), None)
            Actions = gameState.getLegalActions(0)
            result = -(float("inf"))
            childval=[]
            for action in Actions:
                childval .append(min_move(gameState.getNextState(0, action), 1, depth, a, b)[0])#min move for each child
                if result < max(childval):
                    result, move = max(childval), action
                if max(childval) > b:
                    move=action #pruning
                    break
                a = max(a, max(childval))
            return (result ,move)

        def min_move(gameState, agentID, depth, a, b):
            " Cases checking "
            if gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)
            Actions = gameState.getLegalActions(agentID)
            childval=[]
            move=None
            for action in Actions:
                if (agentID == gameState.getNumAgents() - 1):
                    childval.append(max_move(gameState.getNextState(agentID, action),  depth+1, a, b)[0]) #max move for each child
                else:
                    childval.append(min_move(gameState.getNextState(agentID, action), agentID + 1, depth, a, b)[0])
                if (min(childval) < a):
                    move=action
                    break
                b = min(b, min(childval))

            return (min(childval), move)

        return max_move(gameState, 0, -(float("inf")), float("inf"))[1]   ###starting from root and returning the actions
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def max_move(gameState, depth):
            if  gameState.isWin() or gameState.isLose() or depth == self.depth:  #special cases
                return (self.evaluationFunction(gameState), None)
            Actions = gameState.getLegalActions(0)
            childval = [expected_value(gameState.getNextState(0, action), 1, depth)[0] for action in Actions] # expected value for each child
            move = Actions[childval.index(max(childval))]
            return ( max(childval), move)

        def expected_value(gameState, agentID, depth):
            Actions = gameState.getLegalActions(agentID)
            if len(Actions) == 0: #no possible actions case
                return (self.evaluationFunction(gameState), None)
            move = None
            if (agentID == gameState.getNumAgents() - 1):
                childval = [(max_move(gameState.getNextState(agentID, action), depth + 1)[0]) for action in Actions] #max move for each child
            else:
                childval= [(expected_value(gameState.getNextState(agentID, action), agentID + 1, depth)[0]) for action in Actions] # expected value for each child
            result =sum(childval) / len(Actions)  #expected value

            return (result, move)

        return max_move(gameState, 0)[1]  ###starting from root and returning the actions
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    ##the func from q1 works fine
    ghost_distance = [(manhattanDistance(ghost, currentGameState.getPacmanPosition())) for ghost in currentGameState.getGhostPositions()]  # manhatan distance for each ghost
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")
    if min(ghost_distance) < 2 :  # dont fall into enemy
        return (-(float("inf")))
    foodDistList = [manhattanDistance(food, currentGameState.getPacmanPosition()) for food in currentGameState.getFood().asList()]  # manhatan distance for each food
    return ((850*len(foodDistList)+8000*sum(foodDistList))/(sum(foodDistList)*len(foodDistList)))
    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
