"""
In search.py, you will implement generic search algorithms
"""

import util

UCS = "UCS"
DFS = "DFS"
BFS = "BFS"
A_STAR = "A_STAR"


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


class Node:
    def __init__(self,state,lastAction,path,cost=0):
        self.state = state
        self.lastAction = lastAction
        self.path = path
        self.cost = cost

    def getState(self):
        return self.state
    def getLastAction(self):
        return self.lastAction
    def getPath(self):
        return self.path
    def getCost(self):
        return self.cost


def generalSearch(problem, fringe, searchType, h = None):
    closed = []
    startNode = Node(problem.get_start_state(), None, [])
    if searchType == DFS or searchType == BFS:
        fringe.push(startNode)
    else:
        fringe.push(startNode, None)

    while not fringe.isEmpty():
        currentNode = fringe.pop()
        state = currentNode.getState()
        path = currentNode.getPath()
        cost = currentNode.getCost()
        if (problem.is_goal_state(state)):
            return path
        if state not in closed:
            successors = problem.get_successors(state)
            for s in successors:
                if s[0] not in closed:
                    if searchType == DFS or searchType == BFS:
                        newNode = Node(s[0], s[1], path + [s[1]])
                        fringe.push(newNode)
                    elif searchType == UCS:
                        newNode = Node(s[0], s[1], path + [s[1]], cost + s[2])
                        fringe.push(newNode, -newNode.getCost())
                    else:
                        #print(cost ,h(s[0],problem))
                        #print(h(state,problem),h(s[0],problem))
                        if(h(state,problem) > cost + h(s[0],problem)):
                            print("############################")
                        newNode = Node(s[0], s[1], path + [s[1]], cost + h(s[0],problem) + s[2])
                        fringe.push(newNode, -(newNode.getCost() + h(s[0],problem)))
            closed.append(state)
    return []


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    fringe = util.Stack()
    return generalSearch(problem, fringe, DFS)


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    fringe = util.Queue()
    return generalSearch(problem, fringe, BFS)


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    fringe = util.PriorityQueue()
    return generalSearch(problem, fringe, UCS)


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    fringe = util.PriorityQueue()
    return generalSearch(problem, fringe, A_STAR, heuristic)



# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
