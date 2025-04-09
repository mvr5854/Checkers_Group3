import numpy as np
import random


class MCT_Node:
    """Node in the Monte Carlo search tree, keeps track of the children states."""

    def __init__(self, parent=None, state=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, U=U, N=N)
        self.children = {}
        self.actions = None

def ucb(n, C=1.4):
    return np.inf if n.N == 0 else n.U / n.N + C * np.sqrt(np.log(n.parent.N) / n.N)

def monte_carlo_tree_search(state, game, N=1000):
    def select(n):
        """select a leaf node in the tree"""
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n

    def expand(n):
        """expand the leaf node by adding all its children states"""
        if not n.children and not game.terminal_test(n.state):
            n.children = {MCT_Node(state=game.result(n.state, action), parent=n): action
                          for action in game.actions(n.state)}
        return select(n)

    def simulate(game, state):
        """simulate the utility of current state by random picking a step"""
        player = game.to_move(state)
        while not game.terminal_test(state):
            action = random.choice(list(game.actions(state)))
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

# Search algorithm: Minimax with Alpha-Beta Pruning
def minimax_search(game, state, depth=3, maximizing_player=True):
    def minimax(state, depth, alpha, beta, maximizing_player):
        if game.is_terminal(state) or depth == 0:
            return game.utility(state, state.to_move)

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

    # Choose the best move
    best_score = float('-inf')
    best_move = None
    for move in game.actions(state):
        score = minimax(game.result(state, move), depth, float('-inf'), float('inf'), maximizing_player)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def query_player(game, state):
    """Make a move by querying standard input."""
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    print("")
    move = None
    if game.actions(state):
        move_string = input('Your move? ')
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move
