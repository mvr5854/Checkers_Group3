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

def piece_value(state, piece):
    val = 1.0
    # King bonus
    if piece.is_king:
        val += 0.5
        
    # Promotion potential (distance to becoming king)
    if not piece.is_king:
        if piece.player == state.players[0]:
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

def is_threatened(state, piece):
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
            val = piece_value(state, p)
            # Center control
            if (p.cy, p.cx) in center:
                val += 0.3
            # Threat penalty: if piece can be jumped next turn
            if is_threatened(state, p):
                threat_cost = 1.0 + (0.5 if p.is_king else 0.0)
                val += (-threat_cost if p.player == player else +threat_cost)

            # Sum up with sign
            score += (1 if p.player == player else -1) * val
    return score