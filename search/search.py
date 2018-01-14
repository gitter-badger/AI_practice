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

import util, sys
from node import Node
from util import *

# http://ai.berkeley.edu/project_overview.html
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
    return  [s, s, w, s, w, w, s, w]


def bsfOrDfs(fringe, problem):
    fringe.push(Node(problem.getStartState()))
    # Hash de estats expandits
    generated = {}

    while True:
        if fringe.isEmpty():
            print "No solution."
            sys.exit(-1)

        n = fringe.pop()
        # n passa a ser un nodo expandit
        generated[n.state] = []

        for s, a, c in problem.getSuccessors(n.state):
            ns = Node(s, n, a, c)
            if s not in generated.keys():
                if problem.isGoalState(ns.state):
                    print "Solution"
                    return ns.path()

                fringe.push(ns)
                generated[s] = []

def ucsFn(node, c, heuristic):
    return node.cost + c

def astarFn(node, c, heuristic):
    return max(node.cost + c + heuristic(s, problem), node.cost + heuristic(node.state, problem))

# For ucs heuristic won't have any efect
# fringe will be PriorityQueue for both
def ucsOrAStar(fn, heuristic, problem):
    generated = {}
    fringe = PriorityQueue()
    n = Node(problem.getStartState(),0)
    fringe.push(n, 0)
    generated[n.state] = [n, "F"]

    while True:
        if fringe.isEmpty():
            print "No solution."
            sys.exit(-1)

        n = fringe.pop()
        if generated[n.state][1] == "E": break

        if problem.isGoalState(n.state):
            return n.path()

        # n passa a ser un nodo expandit
        generated[n.state] = [n, "E"]

        for s, a, c in problem.getSuccessors(n.state):
            ns = Node(s, n, a, fn(n, c, heuristic))
            if s not in generated.keys():
                fringe.push(ns, ns.cost)
                generated[s] = [ns, "F"]
            elif generated[s][0].cost > ns.cost:
                fringe.push(ns, ns.cost)
                generated[s] = [ns, "F"]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    return bsfOrDfs(Stack(), problem)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Inicialitzar fringe
    return bsfOrDfs(Queue(), problem)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    ucsOrAStar(ucsFn, heuristic, problem)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    ucsOrAStar(astarFn, heuristic, problem)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
