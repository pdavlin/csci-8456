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
import random, util, sys

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
        newGhostPositions = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        gds = [manhattanDistance(newPos, gpos) for gpos in newGhostPositions]
        fps = [manhattanDistance(newPos, snack) for snack in newFood.asList()]
        
        #TODO: TELL PACMAN TO TAKE FOOD IF DISTANCE IS 0?
        # print("food distances: ", fps)
        if len(fps) == 0:
            return 1000 #+ successorGameState.getScore()
        else:
            gs = min(gds)
            fs = min(fps)
            # print("mgd: ", gs, " mfd: ", fs) 
            score = gs / (fs * 20)

        if action.strip() == 'Stop':
            score -= 100

        score += successorGameState.getScore()
        return score

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

        return self.max_value(gameState, 0)

    def max_value(self, state, d):
        # Return a score instead of action
        # Returning STOP or something similar broke the agent
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        # Get Pacman Actions
        legalActions = state.getLegalActions(0)

        # Lowest Possible score. Maybe there's a better way in Python to implement this
        best_score = -1 * sys.maxsize
        
        # Test all actions for pacman
        for a in legalActions:
            next_state = state.generateSuccessor(0, a)
            # Evaluate the ghost's scores beneath this max agent node
            score = self.min_value(next_state, d, 1)
            # Maintain the highest possible score for this node
            if score > best_score:
                best_score = score
                best_action = a

        if d > 0:
            # Mid-depth max agent, return score up the tree
            return best_score
        else:
            # Full d-depth tree explored, return action w/ best score
            return best_action

    def min_value(self, state, d, ghostNum):
        # Return score if game over
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        # Get legal actions for this ghost
        legalActions = state.getLegalActions(ghostNum)
        # Return worst case score for ghost
        best_score = sys.maxsize
        for a in legalActions:
            next_state = state.generateSuccessor(ghostNum, a)
            # if this is the last ghost
            if ghostNum == state.getNumAgents() - 1:
                # if this is the deepest node in the search tree, return score
                if d == (self.depth - 1):
                    score = self.evaluationFunction(next_state)
                # if middle depth, call another Max Agent
                else:
                    score = self.max_value(next_state, d+1)
            # not last ghost, call next min agent
            else:
                score = self.min_value(next_state, d, ghostNum+1)

            # Maintain min score
            if score < best_score:
                best_score = score

        return best_score


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.max_value(gameState, 0, -1 * sys.maxsize, sys.maxsize)

    def max_value(self, state, d, alpha, beta):
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        legalActions = state.getLegalActions(0)

        best_score = -1 * sys.maxsize
        
        for a in legalActions:
            next_state = state.generateSuccessor(0, a)
            score = self.min_value(next_state, d, 1, alpha, beta)
            if score > best_score:
                best_score = score
                best_action = a
                if best_score > beta:
                # print("best score >= passed beta")
                    return best_score
                if best_score > alpha:
                    alpha = best_score
            

        if d > 0:
            return best_score
        else:
            return best_action

    def min_value(self, state, d, ghostNum, alpha, beta):
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        legalActions = state.getLegalActions(ghostNum)
        best_score = sys.maxsize

        for a in legalActions:
            next_state = state.generateSuccessor(ghostNum, a)
            if ghostNum == state.getNumAgents() - 1:
                if d == (self.depth - 1):
                    score = self.evaluationFunction(next_state)
                else:
                    score = self.max_value(next_state, d+1, alpha, beta)
            else:
                score = self.min_value(next_state, d, ghostNum+1, alpha, beta)

            if score < best_score:
                best_score = score
                if best_score < alpha:
                    return best_score
                if best_score < beta:
                    beta = best_score
            

        return best_score

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
        return self.max_value(gameState, 0)

    def max_value(self, state, d):
        # Return a score instead of action
        # Returning STOP or something similar broke the agent
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        # Get Pacman Actions
        legalActions = state.getLegalActions(0)

        # Lowest Possible score. Maybe there's a better way in Python to implement this
        best_score = -1 * sys.maxsize
        
        # Test all actions for pacman
        for a in legalActions:
            next_state = state.generateSuccessor(0, a)
            # Evaluate the ghost's scores beneath this max agent node
            score = self.ex_value(next_state, d, 1)
            # Maintain the highest possible score for this node
            if score > best_score:
                best_score = score
                best_action = a

        if d > 0:
            # Mid-depth max agent, return score up the tree
            return best_score
        else:
            # Full d-depth tree explored, return action w/ best score
            return best_action

    def ex_value(self, state, d, ghostNum):
        # Return score if game over
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        # Get legal actions for this ghost
        legalActions = state.getLegalActions(ghostNum)
        # Return worst case score for ghost
        running_score = 0
        for a in legalActions:
            p = 1 / len(legalActions)
            next_state = state.generateSuccessor(ghostNum, a)
            # if this is the last ghost
            if ghostNum == state.getNumAgents() - 1:
                # if this is the deepest node in the search tree, return score
                if d == (self.depth - 1):
                    score = self.evaluationFunction(next_state)
                # if middle depth, call another Max Agent
                else:
                    score = self.max_value(next_state, d+1)
            # not last ghost, call next min agent
            else:
                score = self.ex_value(next_state, d, ghostNum+1)

            #maintain score:
            running_score += (score * p)

        return running_score

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Using practically the same function as the previous Eval, but I've tuned the ghost
    and food incentives. Frequently, pacman would stand still and wait until provoked by the ghost
    (the fastest changing part of the score value). To help normalize this, I multiplied the distance 
    to the closest ghost by .3. The current game score is also added to try and incentivise movement
    and early finishing instead of patience and safety
    """
    "*** YOUR CODE HERE ***"
    pacman_loc = currentGameState.getPacmanPosition()
    ghost_states = currentGameState.getGhostStates()
    ghost_locs = currentGameState.getGhostPositions()
    # scared_ghosts = currentGameState.get
    food_locs = currentGameState.getFood()
    food_list = food_locs.asList()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghost_states]
    fds = [manhattanDistance(pacman_loc, f) for f in food_list]
    gds = [manhattanDistance(pacman_loc, g) for g in ghost_locs]
    # print("ghost dists: ", gds)
    # print("food distances: ", fds)
    
    if fds == 0:
        return 1000
    else:
        closest_ghost = min(gds)
        closest_food = min(fds, default=1)
        # if len(fds) == 0:
        #     denom = 1
        # else:
        #     denom = len(fds)
        # avg_food = sum(fds) / denom
        score = currentGameState.getScore() + (0.3 * closest_ghost) / (closest_food * 10)
        # print("score: ", score)
        return score

# Abbreviation
better = betterEvaluationFunction
