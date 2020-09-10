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
    stack.push([[problem.getStartState(), 0]])
    output = []
    while stack.isEmpty() == False:
        current_stack = stack.pop()
        path = []
        for stack_item in current_stack:
            path.append(stack_item[0])
        current = current_stack[-1]

        if(problem.isGoalState(current[0])):
            print('found')
            for state in current_stack:
                output.append(state[1])
            break

        successors = problem.getSuccessors(current[0])
        for successor in successors:
            if successor[0] not in path:
                placeholder = current_stack.copy()
                placeholder.append(successor)
                stack.push(placeholder)
    # output.reverse()
    output = output[1:len(output)]
    return output

    # util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    queue = util.Queue()
    start_item = problem.getStartState()
    queue.push([[problem.getStartState(), 0]])

    visited = [start_item[0]]
    output = []

    while not queue.isEmpty():
        current_queue = queue.pop()
        current = current_queue[-1]
        if problem.isGoalState(current[0]):
            for state in current_queue:
                output.append(state[1])
            break

        for successor in problem.getSuccessors(current[0]):
            if successor[0] not in visited:
                placeholder = current_queue.copy()
                placeholder.append(successor)
                queue.push(placeholder)
                visited.append(successor[0])

    output = output[1:len(output)]
    return output


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    queue = util.PriorityQueue()
    start = problem.getStartState()
    prev = [start[0]]
    queue.push([[problem.getStartState(), "", 0]], 0)
    fin = []

    while not queue.isEmpty():
        current_queue = queue.pop()
        current = current_queue[-1]
        path = [c[0] for c in current_queue]
        # print("Current: ", current[0])
        # print("prev: ", prev)
        # print("Current: ", current)
        # for stack_item in current_stack:
        #     path.append(stack_item[0])
        # current = current_stack[-1]
        
        if problem.isGoalState(current[0]):
            fin = [x[1] for x in current_queue]
            break

        s = problem.getSuccessors(current[0])
        if len(s) > 0:
            for node in s:
                if node[0] not in prev:
                    # print("node: ", node)
                    ph = current_queue.copy()
                    next_cost = node[2] + current[2]
                    # print("next cost: ", next_cost)
                    ph.append([node[0], node[1], next_cost])
                    queue.push(ph, next_cost)
                    prev.append(node[0])
                elif node[0] in path:
                    print("node found in path: ", node[0])
                else: 
                    print("worthless node?: ", node)

    return fin[1:]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    queue = util.PriorityQueue()
    start_item = problem.getStartState()
    queue.push([[start_item, "", 0]],0)

    visited = {start_item: 0}
    output = []

    while not queue.isEmpty():
        current_queue = queue.pop()
        current = current_queue[-1]

        if current[0] not in visited or current[2] <= visited[current[0]]:
            if problem.isGoalState(current[0]):
                for state in current_queue:
                    output.append(state[1])
                break

            for successor in problem.getSuccessors(current[0]):
                if successor[0] not in visited or (current[2] + successor[2]+ heuristic(successor[0], problem)) < visited[successor[0]]:
                    updated_cost = current[2] + successor[2] + heuristic(successor[0], problem)
                    print(updated_cost)
                    visited[successor[0]] = updated_cost
                    updated_successor = (successor[0], successor[1], updated_cost)
                    placeholder = current_queue.copy()
                    placeholder.append(updated_successor)
                    queue.push(placeholder, updated_cost)

    output = output[1:len(output)]
    return output


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
