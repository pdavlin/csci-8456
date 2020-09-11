# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import copy


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    stack = util.Stack()
    stack.push([problem.getStartState(), []])
    visited = set()
    fin = []

    while not stack.isEmpty():
        current = stack.pop()
        xy = current[0]
        path = current[1]

        if xy not in visited:
            visited.add(xy)

            if problem.isGoalState(xy):
                return path
            
            for node in problem.getSuccessors(xy):
                nxy = node[0]
                npath = node[1]
                if nxy not in visited:
                    stack.push([node[0], path + [npath]])

    return fin


def breadthFirstSearch(problem):
    queue = util.Queue()
    queue.push([problem.getStartState(), []])
    visited = set()
    fin = []

    while not queue.isEmpty():
        current = queue.pop()
        xy = current[0]
        path = current[1]

        if xy not in visited:
            visited.add(xy)

            if problem.isGoalState(xy):
                return path
            
            for node in problem.getSuccessors(xy):
                nxy = node[0]
                npath = node[1]
                if nxy not in visited:
                    queue.push([node[0], path + [npath]])

    return fin


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    queue = util.PriorityQueue()
    queue.push([problem.getStartState(), [], 0], 0)
    visited = set()
    fin = []

    while not queue.isEmpty():
        current = queue.pop()
        xy = current[0]
        path = current[1]
        cost = current[2]

        if xy not in visited:
            visited.add(xy)

            if problem.isGoalState(xy):
                return path
            
            for node in problem.getSuccessors(xy):
                nxy = node[0]
                npath = node[1]
                npriority = node[2]
                if nxy not in visited:
                    queue.push([node[0], path + [npath], npriority + cost], npriority + cost)

    return fin


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node of least total cost first."""
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    queue = util.PriorityQueue()
    start_state = problem.getStartState()
    start_heuristic = heuristic(start_state, problem)
    queue.push([start_state, [], 0, start_heuristic], 0)
    visited = set()
    fin = []

    while not queue.isEmpty():
        current = queue.pop()
        xy = current[0]
        path = current[1]
        cost = current[2]
        xyh = current[3]
        newh = heuristic(xy, problem)

        if xy not in visited or xyh < heuristic(xy, problem):
            visited.add(xy)

            if problem.isGoalState(xy):
                return path
            
            for node in problem.getSuccessors(xy):
                nxy = node[0]
                npath = node[1]
                npriority = node[2]
                heuristic_value = heuristic(node[0], problem)

                sum_cost = npriority + cost + heuristic_value
                if nxy not in visited:
                    queue.push([node[0], path + [npath], npriority + cost, heuristic_value], sum_cost)

    return fin


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
