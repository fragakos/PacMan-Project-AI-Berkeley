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
points_taken = -500
weight = 75
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

        "*** YOUR CODE HERE ***"
        ghost_distances = []
        for single_ghost in newGhostStates:
            ghost_distances.append(manhattanDistance(newPos, single_ghost.getPosition()))
        ghost_to_avoid = min(ghost_distances)
        if ghost_to_avoid == 0:
            r_distance = points_taken
        else:
            r_distance = ghost_to_avoid

        food_distances = []
        food_list = newFood.asList()
        food_to_eat = 0
        for food in food_list:
            food_distances.append(manhattanDistance(newPos,food))
        if len(food_distances) > 0:
            food_to_eat = -min(food_distances)
        total_points = (r_distance + 2*food_to_eat) - weight*len(food_list)
        return total_points

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
        Returns a list of legal actions for an agentminimum
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimum(gameState, depth, ghost_agend):
            acts=gameState.getLegalActions(ghost_agend)
            if len(acts) == 0:
                return(self.evaluationFunction(gameState), None)

            largest=float("inf")  
            for single_act in acts:
                if(ghost_agend == gameState.getNumAgents() -1):
                    min_from_max_function=maximum(gameState.generateSuccessor(ghost_agend, single_act),depth + 1)
                else:
                    min_from_max_function = minimum(gameState.generateSuccessor(ghost_agend, single_act), depth, ghost_agend+1)
                if(min_from_max_function[0] < largest):
                    largest = min_from_max_function[0]
                    next_act = single_act

            return(largest, next_act)


        def maximum(gameState,depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return(self.evaluationFunction(gameState), None)

            acts=gameState.getLegalActions(0)
            if len(acts) == 0:
                return(self.evaluationFunction(gameState), None)
                
            ghost_agend = 1
            smallest=float("-inf")
            for single_act in acts:
                max_from_min_function = minimum(gameState.generateSuccessor(0, single_act),depth, ghost_agend) #minimum "plays" for the ghosts
                if(max_from_min_function[0] > smallest):
                    smallest = max_from_min_function[0]
                    next_act = single_act

            return(smallest, next_act)

        what_actions_to_take = maximum(gameState, 0)[1]
        return what_actions_to_take   

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minimum(gameState, depth, ghost_agend, alpha, beta):
            acts=gameState.getLegalActions(ghost_agend)
            if len(acts) == 0:
                return(self.evaluationFunction(gameState), None)

            largest=float("inf")  
            for single_act in acts:
                if(ghost_agend == gameState.getNumAgents() - 1):
                    min_from_max_function=maximum(gameState.generateSuccessor(ghost_agend, single_act),depth + 1, alpha, beta)
                else:
                    min_from_max_function = minimum(gameState.generateSuccessor(ghost_agend, single_act), depth, ghost_agend+1, alpha, beta)
                if(min_from_max_function[0] < largest):
                    largest = min_from_max_function[0]
                    next_act = single_act
                if(alpha <= largest):
                    beta = min(beta, largest)
                else:
                    return(largest, single_act)
                        
            return(largest, next_act)

        def maximum(gameState,depth, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return(self.evaluationFunction(gameState), None)

            acts=gameState.getLegalActions(0)
            if len(acts) == 0:
                return(self.evaluationFunction(gameState), None)
                
            ghost_agend = 1
            smallest=float("-inf")
            for single_act in acts:
                max_from_min_function = minimum(gameState.generateSuccessor(0, single_act), depth, ghost_agend, alpha, beta) #minimum "plays" for the ghosts
                if(max_from_min_function[0] > smallest):
                    smallest = max_from_min_function[0]
                    next_act = single_act
                if(beta >= smallest):
                   alpha = max(alpha,smallest)
                else:   
                    return (smallest,single_act)

            return(smallest, next_act)
    
        alpha = float("-inf")
        beta = float("inf")
        what_actions_to_take = maximum(gameState, 0, alpha, beta)[1]
        return what_actions_to_take

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
        def maximum(gameState,depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return(self.evaluationFunction(gameState), None)

            acts=gameState.getLegalActions(0)
            if len(acts) == 0:
                return(self.evaluationFunction(gameState), None)
                
            ghost_agend = 1
            smallest=float("-inf")
            for single_act in acts:
                max_from_exp_function = expected_max(gameState.generateSuccessor(0, single_act),depth, ghost_agend) #expected value
                if(max_from_exp_function[0] > smallest):
                    smallest = max_from_exp_function[0]
                    next_act = single_act

            return(smallest, next_act)

        def expected_max(gameState, depth, ghost_agend):
            acts = gameState.getLegalActions(ghost_agend)
            if len(acts) == 0:
                return(self.evaluationFunction(gameState), None)

            largest = 0
            for single_act in acts:
                if(ghost_agend == gameState.getNumAgents() - 1):
                    next_max = maximum(gameState.generateSuccessor(ghost_agend,single_act), depth + 1)
                else:
                    next_max = expected_max(gameState.generateSuccessor(ghost_agend,single_act), depth, ghost_agend + 1)
                expectation=next_max[0]
                largest = largest + expectation
            return(largest,None) 

        what_actions_to_take = maximum(gameState, 0)[1]
        return what_actions_to_take      

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacman_position = list(currentGameState.getPacmanPosition())
    food_list = currentGameState.getFood().asList()
    caps=currentGameState.getCapsules()
    alive_ghosts = []
    eatable_ghosts = []
    for single_ghost in currentGameState.getGhostStates():
        if single_ghost.scaredTimer:
            eatable_ghosts.append(single_ghost)
        else:
           alive_ghosts.append(single_ghost)

    food_distances = []
    for food in food_list:
        food_distances.append(manhattanDistance(pacman_position, food))
    if len(food_distances) == 0:
        closest_food = 0
    else:
        closest_food = min(food_distances) 

    eatable_ghosts_distances = []
    alive_ghosts_distances = []
    for single_ghost in alive_ghosts:
        eatable_ghosts_distances.append(manhattanDistance(pacman_position,single_ghost.getPosition()))

    for single_ghost in alive_ghosts:
        eatable_ghosts_distances.append(manhattanDistance(pacman_position,single_ghost.getPosition()))

    alive_ghosts = -1
    eatable_ghosts = -1
    if len(alive_ghosts_distances) > 0:
        alive_ghosts = min(alive_ghosts_distances)
    if len(eatable_ghosts_distances) > 0:
        eatable_ghosts = min(eatable_ghosts_distances)

    return currentGameState.getScore() - (15*len(caps) + 5*len(food_list) + (1/3)*closest_food + 2*eatable_ghosts + 2*(alive_ghosts^(-1)))

# Abbreviation
better = betterEvaluationFunction
