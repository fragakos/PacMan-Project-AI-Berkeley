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
        act, stepCost), where 'successor' is a successor to the current
        state, 'act' is the act required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfacts(self, acts):
        """
         acts: A list of acts to take

        This method returns the total cost of a particular sequence of acts.
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

def to_tuple(lst):
    return tuple(to_tuple(i) if isinstance(i, list) else i for i in lst)     

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of acts that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    if problem.isGoalState(problem.getStartState()):
        return []
    first_node = problem.getStartState()
    fr = util.Stack() # a list of nodes and acts (fr form frontier)
    fr.push(([], first_node))
    explored = set()
    acts = []
    while not fr.isEmpty():
        acts, this_node = fr.pop()
        if to_tuple(this_node) not in explored:
            explored.add(to_tuple(this_node))
            if problem.isGoalState(this_node):
                return acts
            for jump_node, act, cost in problem.getSuccessors(this_node):
                next_act = acts + [act]
                fr.push((next_act, jump_node))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    if problem.isGoalState(problem.getStartState()):
        return []
    first_node = problem.getStartState()
    q = util.Queue() # a list of nodes and acts
    q.push(([], first_node))
    explored = set()
    acts = []
    while not q.isEmpty():
        acts, this_node = q.pop()
        if to_tuple(this_node) not in explored:
            explored.add(to_tuple(this_node))
            if problem.isGoalState(this_node):
                return acts
            for jump_node, act, cost in problem.getSuccessors(this_node):
                next_act = acts + [act]
                q.push((next_act, jump_node))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    if problem.isGoalState(problem.getStartState()):
        return []
    first_node = problem.getStartState()
    pq = util.PriorityQueue() # a priority q which has a set containing (act to the node, the node, the cost) and the priority
    pq.push(([], first_node, 0), 0)
    explored = set()
    acts = []
    while not pq.isEmpty():
        acts, this_node, this_node_cost = pq.pop()
        if this_node not in explored:
            explored.add(this_node)
            if problem.isGoalState(this_node):
                return acts
            for jump_node, act, cost in problem.getSuccessors(this_node):
                next_act = acts + [act]
                priority = this_node_cost + cost
                pq.push((next_act, jump_node, priority),priority)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    if problem.isGoalState(problem.getStartState()):
        return []
    first_node = problem.getStartState()
    pq = util.PriorityQueue() # a priority q which has a set containing (the node,act to the node, the cost) and the priority
    pq.push((first_node, [], 0), 0)
    explored = set()
    acts = []
    while not pq.isEmpty():
        this_node, acts, this_node_cost = pq.pop()
        if to_tuple(this_node) not in explored:
            explored.add(to_tuple(this_node))
            if problem.isGoalState(this_node):
                return acts
            for jump_node, act, cost in problem.getSuccessors(this_node):
                next_act = acts + [act]
                ncost_jump_node = this_node_cost + cost
                priority_with_hrstc = ncost_jump_node + heuristic(jump_node,problem)
                pq.push((jump_node, next_act, ncost_jump_node),priority_with_hrstc)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
