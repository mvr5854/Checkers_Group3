import numpy as np
import random
import math
import functools
cache = functools.lru_cache(10**6)

from io_helper import IOHelper, cell_to_coordinate, coordinate_to_cell


class MCT_Node:
    """Node in the Monte Carlo search tree, keeps track of the children states."""

    def __init__(self, parent=None, state=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, U=U, N=N)
        self.children = {}
        self.actions = None

def ucb(n, C=1.4):
    return np.inf if n.N == 0 else n.U / n.N + C * np.sqrt(np.log(n.parent.N) / n.N)

def monte_carlo_tree_search(game, state, N=300):
    def select(n):
        """select a leaf node in the tree"""
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n
    
    def expand(n):
        if not n.children and not game.is_terminal(n.state):
            if n.actions is None:
                n.actions = game.actions(n.state)
            n.children = {MCT_Node(state=game.result(n.state, action), parent=n): action
                for action in n.actions}
        return select(n)
    
    def simulate(game, state, max_depth=20):
        player = state.to_move
        for _ in range(max_depth):
            if game.is_terminal(state):
                break
            actions = game.actions(state)
            if not actions:
                break
            action = random.choice(actions)
            state = game.result(state, action)
        v = game.utility(state, player)
        return -v

    def backprop(n, utility):
        """passing the utility back to all parent nodes"""
        if utility > 0:
            n.U += utility
        # if utility == 0:
        #     n.U += 0.5
        n.N += 1
        if n.parent:
            backprop(n.parent, -utility)

    root = MCT_Node(state=state)

    for _ in range(N):
        leaf = select(root)
        child = expand(leaf)
        result = simulate(game, child.state)
        backprop(child, result)

    max_state = max(root.children, key=lambda p: p.N)

    return root.children.get(max_state)

def cache1(function):
    "Like lru_cache(None), but only considers the first argument of function."
    cache = {}
    def wrapped(x, *args):
        if x not in cache:
            cache[x] = function(x, *args)
        return cache[x]
    return wrapped

def minimax_search(game, state, depth=3, maximizing_player=True):
    def minimax(state, depth, alpha, beta, maximizing_player, player):
        if game.is_terminal(state) or depth == 0:
            return evaluate_state(state, player)

        if maximizing_player:
            max_eval = float('-inf')
            for move in game.actions(state):
                eval = minimax(game.result(state, move), depth-1, alpha, beta, False, player)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Prune
            return max_eval
        else:
            min_eval = float('inf')
            for move in game.actions(state):
                eval = minimax(game.result(state, move), depth-1, alpha, beta, True, player)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Prune
            return min_eval

    best_score = float('-inf')
    best_move = None
    for move in game.actions(state):
        score = minimax(game.result(state, move), depth, float('-inf'), float('inf'), maximizing_player, state.to_move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def piece_value(piece):
    val = 1.0
    # King bonus
    if piece.is_king:
        val += 1.5
    # Promotion potential (distance to becoming king)
    if piece.player == 'w':
        val += 0.2 * (7 - piece.cy)
    else:
        val += 0.2 * piece.cy
    # Mobility bonus: number of raw move options
    options = len(piece.available_moves())
    val += 0.1 * options
    # Edge safety bonus
    if piece.cx in (0, 7) or piece.cy in (0, 7):
        val += 0.2
    return val

def is_threatened(piece, state):
    y, x = piece.cy, piece.cx
    bd = state.grid
    for dy, dx in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        ay, ax = y + dy, x + dx
        jy, jx = y - dy, x - dx
        if 0 <= ay < 8 and 0 <= ax < 8 and 0 <= jy < 8 and 0 <= jx < 8:
            neigh = bd[ay][ax]
            if neigh and neigh.player != piece.player and bd[jy][jx] is None:
                return True
    return False

def evaluate_state(state, player):
    score = 0.0
    center = {(3, 3), (3, 4), (4, 3), (4, 4)}
    for row in state.grid:
        for p in row:
            if not p:
                continue
            val = piece_value(p)
            # Center control
            if (p.cy, p.cx) in center:
                val += 0.3
            # Threat penalty: if piece can be jumped next turn
            if is_threatened(p, state):
                val -= 0.5
            # Sum up with sign
            score += (1 if p.player == player else -1) * val
    return score

"""
def minimax_search(game, state, depth=3, maximizing_player=True):
    def minimax(state, depth, alpha, beta, maximizing_player, player):
        if game.is_terminal(state) or depth == 0:
            return evaluate_state(state, player)

        if maximizing_player:
            max_eval = float('-inf')
            for move in game.actions(state):
                eval = minimax(game.result(state, move), depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Prune
            return max_eval
        else:
            min_eval = float('inf')
            for move in game.actions(state):
                eval = minimax(game.result(state, move), depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Prune
            return min_eval

    best_score = float('-inf')
    best_move = None
    for move in game.actions(state):
        score = minimax(game.result(state, move), depth, float('-inf'), float('inf'), maximizing_player, state.to_move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


# Heuristic Evaluation Function
def evaluate_state(state, player):
    board = state.grid
    score = 0

    for row in board:
        for piece in row:
            if piece is not None:
                mult = 1 if piece.player == player else -1
                score += mult * piece_value(piece)

    return score


def piece_value(piece):
    val = 1

    # Heuristic 1: King bonus
    if piece.is_king:
        val += 1.5

    # Heuristic 2: Promotion potential
    if piece.player == "w":
        val += 0.2 * (7 - piece.cy)  # closer to becoming king
    elif piece.player == "b":
        val += 0.2 * piece.cy

    # Heuristic 3: Edge safety bonus
    if piece.cx == 0 or piece.cx == 7:
        val += 0.4

    return val
"""

def query_player(game, state):
    """Make a move by querying standard input."""
    available_moves = game.actions(state)
    available_moves = [coordinate_to_cell(move) for move in available_moves]

    print("current state:")
    game.display(state)
    io_helper = IOHelper(available_moves)
    io_helper.display_menu(max_per_line=3)
    move = None
    if game.actions(state):
        move_string = str(cell_to_coordinate(io_helper.read_user_input()))
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move
