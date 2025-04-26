import numpy as np
import random
import math

class MCT_Node:
    """Node in the Monte Carlo search tree, keeps track of the children states."""

    def __init__(self, parent=None, state=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, U=U, N=N)
        self.children = {}
        self.actions = None

def ucb(n, C=1.4):
    return np.inf if n.N == 0 else n.U / n.N + C * np.sqrt(np.log(n.parent.N) / n.N)

def monte_carlo_tree_search(game, state, N=200):
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

    def simulate(game, state, cutoff=cutoff_depth(np.inf), h=lambda s, p, g: 0):
        """simulate the utility of current state by random picking a step"""
        player  = state.to_move
        depth = 0
        while not game.is_terminal(state):
            if cutoff(game, state, depth):
                return -h(state, player, game)
            action = random.choice(list(game.actions(state)))
            state = game.result(state, action)
            depth+=1
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
        result = simulate(game, child.state, cutoff=cutoff_depth(20), h=heuristic_evaluation)
        backprop(child, result)

    max_state = max(root.children, key=lambda p: p.N)
    return root.children.get(max_state)

def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda game, state, depth: depth > d

def check_if_piece_can_be_jumped(piece, state):
    """
    Checks if the given 'piece' can be jumped by any opponent piece
    in the current 'state'.
    Returns True if threatened, False otherwise.
    """
    board = state.grid
    cy, cx = piece.cy, piece.cx
    opponent_player = state.players[1] if piece.player == state.players[0] else state.players[0]

    for dy in [-1, 1]:
        for dx in [-1, 1]:
            opp_y, opp_x = cy + dy, cx + dx
            land_y, land_x = cy - dy, cx - dx

            if not (0 <= opp_y < 8 and 0 <= opp_x < 8 and 0 <= land_y < 8 and 0 <= land_x < 8):
                continue

            opponent_piece = board[opp_y][opp_x]
            landing_spot = board[land_y][land_x]

            if opponent_piece is not None and \
               opponent_piece.player == opponent_player and \
               landing_spot is None:

                can_opponent_jump = False
                if opponent_piece.is_king:
                    can_opponent_jump = True
                elif opponent_player == state.players[0] and cy == opp_y + 1:
                     can_opponent_jump = True
                elif opponent_player == state.players[1] and cy == opp_y - 1:
                     can_opponent_jump = True

                if can_opponent_jump:
                    # If all conditions met, this piece is threatened
                    return True

    # If no threatening jump found after checking all directions
    return False

def heuristic_evaluation(state, player, game):
    """
    Evaluates the state for the given player.
    Higher values are better for the player.
    Includes penalty for threatened pieces.
    """
    opponent = [p for p in state.players if p != player][0]
    player0 = state.players[0]
    player1 = state.players[1]
    player0_promotion_row = 7
    player1_promotion_row = 0

    board = state.grid
    h = {player: 0.0, opponent: 0.0}

    king_weight = 1.5
    safe_piece_weight = 0.2 # Safety from edge/back row, not jump threats
    mobility_weight = 0.05
    jump_weight = 1.0 # Value of having a jump available
    promotion_potential_weight = 0.3
    threatened_penalty_weight = 1.2 # Penalty for being vulnerable to a jump

    for turn in [player, opponent]:
        pieces = 0
        kings = 0
        safe_pieces = 0
        total_simple_moves = 0
        total_jumps = 0
        total_promotion_potential = 0
        threatened_pieces = 0

        # Determine promotion row and direction for 'turn'
        if turn == player0:
            promotion_row = player0_promotion_row
        else: # turn == player1
            promotion_row = player1_promotion_row

        if turn not in state.pieces:
             continue # Skip if player has no pieces left

        for p in state.pieces[turn]:
            pieces += 1

            # Check if piece is threatened
            if check_if_piece_can_be_jumped(p, state):
                threatened_pieces += 1

            is_safe_edge_back = (p.cx == 0 or p.cx == 7)
            piece_jumps_list = game.get_jumps(board, p)
            num_piece_jumps = len(piece_jumps_list)
            total_jumps += num_piece_jumps
            num_piece_simple_moves = 0
            if num_piece_jumps == 0:
                potential_moves = p.available_moves()
                for move_candidate in potential_moves:
                    _, target_row, target_col = move_candidate
                    if 0 <= target_row < 8 and 0 <= target_col < 8 and board[target_row][target_col] is None:
                        if abs(p.cy - target_row) == 1 and abs(p.cx - target_col) == 1:
                             num_piece_simple_moves += 1
            total_simple_moves += num_piece_simple_moves

            if p.is_king:
                kings += 1
                # King on opponent's back row is safe
                if (turn == player0 and p.cy == player1_promotion_row) or \
                   (turn == player1 and p.cy == player0_promotion_row):
                   is_safe_edge_back = True
            else:
                # Promotion potential for non-kings
                dist_to_promotion = abs(p.cy - promotion_row)
                if dist_to_promotion > 0:
                    # Closer pieces get higher potential value
                    total_promotion_potential += (1.0 / dist_to_promotion)

            # Check if piece is on its own back row
            if (turn == player0 and p.cy == player0_promotion_row) or \
               (turn == player1 and p.cy == player1_promotion_row):
               is_safe_edge_back = True

            if is_safe_edge_back:
                safe_pieces += 1

        h[turn] = (
            pieces
            + kings * king_weight #
            + safe_pieces * safe_piece_weight # Safety from edges/back row
            + total_simple_moves * mobility_weight # Mobility bonus
            + total_jumps * jump_weight # Bonus for having jumps available
            + total_promotion_potential * promotion_potential_weight # Promotion potential
            - threatened_pieces * threatened_penalty_weight # Penalty for threatened pieces
        )

    h_player = h[player]
    h_opponent = h[opponent]
    total_h = h_player + h_opponent
    score_diff = h_player - h_opponent
    value = math.tanh(score_diff / 10.0)

    # Ensure value stays strictly within [-1, 1] bounds
    return max(-1.0, min(1.0, value))