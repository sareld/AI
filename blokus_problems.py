from board import Board
from search import SearchProblem, ucs, a_star_search, bfs,dfs
import util
import numpy as np


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.actions = []
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        shape = state.state.shape
        return state.state[0, 0] != -1 and \
               state.state[0, shape[1]-1] != -1 and \
               state.state[shape[0]-1, 0] != -1 and \
               state.state[shape[0]-1, shape[1]-1] != -1

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return sum([action.piece.get_num_tiles() for action in actions])


def manhattan_distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(bx - ax) + abs(by - ay)



def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    boardState = state.state
    row,col = boardState.shape
    coordinates = np.argwhere(boardState != -1)
    corners = np.array([[0,col-1],
                        [row-1,0],
                        [row-1,col-1]])
    freeCorners = []
    for cor in corners:
        if boardState[tuple(cor)] == -1:
            freeCorners.append(cor)

    if coordinates.size != 0:
        if len(freeCorners) != 0:
            minDist = np.sum([manhattan_distance(coordinates[0], corn) for corn in freeCorners])
            for c in coordinates[1:]:
                distSum = np.sum([manhattan_distance(c, corn) for corn in freeCorners])
                minDist = min(minDist,distSum)

            return minDist
        else:
            return 0
    else:
        return 0


def blokus_corners_heuristic1(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    boardState = state.state
    row,col = boardState.shape
    coordinates = np.argwhere(boardState != -1)
    corners = np.array([[0,col-1],
                        [row-1,0],
                        [row-1,col-1]])
    freeCorners = []
    distSum = 0

    for corner in corners:
        if boardState[tuple(corner)] == -1:
            freeCorners.append(corner)

    for corner in freeCorners:
        if len(coordinates) != 0:
            distSum += np.min([manhattan_distance(corner, c) for c in coordinates])

    # if coordinates.size != 0:
    #     if len(freeCorners) != 0:
    #         # minDist = np.sum([manhattan_distance(coordinates[0], corn) for corn in freeCorners])
    #
    #         for corn in freeCorners:
    #             distSum += np.min([manhattan_distance(corn, c) for c in coordinates])
    #             # minDist = min(minDist,distSum)
    #
    #         # for c in coordinates[1:]:
    #         #     distSum = np.sum([manhattan_distance(c, corn) for corn in freeCorners])
    #         #     minDist = min(minDist,distSum)
    #
    #         return distSum
    #     else:
    #         return 0
    # else:
    #     return 0
    return distSum


def blokus_corners_heuristic2(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    boardState = state.state
    row, col = boardState.shape
    coordinates = np.argwhere(boardState != -1)
    corners = np.array([[0, col - 1],
                        [row - 1, 0],
                        [row - 1, col - 1]])
    freeCorners = []
    distSum = 0

    for cor in corners:
        if boardState[tuple(cor)] == -1:
            freeCorners.append(cor)

    if coordinates.size != 0:
        if len(freeCorners) != 0:
            minDist = np.min([manhattan_distance(coordinates[0], corn) for corn in freeCorners])
            for c in coordinates[1:]:
                distSum += np.min([manhattan_distance(c, corn) for corn in freeCorners])
                minDist = min(minDist, distSum)

            return minDist
        else:
            return 0
    else:
        return 0

class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.startingPoint = starting_point
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.actions = []

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        for target in self.targets:
            if state.state[tuple(target)] == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return sum([action.piece.get_num_tiles() for action in actions])


def blokus_cover_heuristic(state, problem):
    boardState = state.state
    coordinates = np.argwhere(boardState != -1)
    targets = np.array(problem.targets)

    freetargets = []
    for cor in targets:
        if boardState[tuple(cor)] == -1:
            freetargets.append(cor)

    if coordinates.size != 0:
        if len(freetargets) != 0:
            minDist = np.average([manhattan_distance(coordinates[0], corn) for corn in freetargets])
            for c in coordinates[1:]:
                distMin = np.average([manhattan_distance(c, corn) for corn in freetargets])
                minDist = min(minDist, distMin)
            return minDist
        else:
            return 0
    else:
        return 0


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.startingPoint = starting_point

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board


    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board.__copy__()
        backtrace = []

        while ....

            actions = set of actions that covers the closets uncovered target location
            add actions to backtrace

        return backtrace
        """
        current_state = self.board.__copy__()
        backtrace = []

        sortedTargets = sorted(self.targets)

        problem = BlokusCoverProblem(current_state.board_w, current_state.board_h,
                                     current_state.piece_list, self.startingPoint)
        for target in sortedTargets:
            problem.targets = [target]
            actions = a_star_search(problem, blokus_cover_heuristic)
            # actions = ucs(problem)
            problem.actions.extend(actions)
            if len(actions) == 0:
                print(str(target) +" no actions")
            else:
                print(str(target) + " actions")
            for action in actions:
                problem.board.add_move(0, action)
            backtrace.extend(actions)
            self.expanded += problem.expanded
        return backtrace


class MiniContestSearch:
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
