# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 19:23:14 2025

@author: wence
"""

import sys
sys.path.append(r'C:\Users\wence\Projects\AIMA')
from collections import defaultdict
from games4e import *
import copy
import math


class Board(defaultdict):
    """A board has the player to move, a cached utility value, 
    and a dict of {(x, y): player} entries, where player is dark_player or light_player."""
    empty = '.'
    off = '#'
    
    def __init__(self, width=8, height=8, to_move=None, **kwds):
        self.__dict__.update(width=width, height=height, to_move=to_move, **kwds)
        
    def new(self, changes: dict, **kwds) -> 'Board':
        "Given a dict of {(x, y): contents} changes, return a new Board with the changes."
        board = Board(width=self.width, height=self.height, to_move=self.to_move, **kwds)
        board.update(self)
        board.update(changes)
        return board

    def __missing__(self, loc):
        x, y = loc
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.empty
        else:
            return self.off
            
    def __hash__(self): 
        return hash(tuple(sorted(self.items()))) + hash(self.to_move)
    
    def __repr__(self):
        def row(x): return ' '.join(self[x, y] for y in range(self.width))
        return '\n'.join(map(row, range(self.height))) +  '\n'
    
    def copy(self):
        """Return a full copy of the board, including all attributes."""
        new_board = Board(width=self.width, height=self.height, to_move=self.to_move)
        new_board.update(self)
        new_board.__dict__.update(self.__dict__)
        return new_board

    
class Checkers(Game):
    """Play Checkers.
    dark_player plays first against light_player."""

    def __init__(self, h=8, v=8, dark_player='b', light_player='w'):
        dark_player = dark_player.lower()[0]
        light_player = light_player.lower()[0]
        self.h = h
        self.v = v
        self.board_history = {}
        board_ini = self.init_board(dark_player, light_player)
        self.initial = GameState(to_move=board_ini.dark_player, utility=0, board=board_ini, moves=[])
        self.initial.moves.extend(self.get_moves(self.initial))
        
        
    def get_moves(self, state):
        """Return a list of legal moves, including jumps when available."""
        
        def moves_from_pos(piece, direction, position):
            """Generate forward and backward moves for kings."""
            neighbors = lambda d, x, y: [(x + d, y + j) for j in (-1, 1)]
            forward_moves = neighbors(direction, *position)
            backward_moves = neighbors(-direction, *position) if is_king(piece) else []
            return forward_moves + backward_moves
    
        def is_king(piece):
            """Check if a piece is a king (represented by uppercase letters)."""
            return piece.isupper()

        jumps = []
        available_moves = []
        player = state.to_move
        direction = 1 if player == state.board.dark_player else -1
        board = state.board.copy()
        
        for from_pos, piece in board.items():
            if piece.lower() != player.lower():
                continue  # Ignore opponent pieces
            
            for to_pos in moves_from_pos(piece, direction, from_pos):
                if board[to_pos] not in [player, board.empty, board.off]:  # Opponent's piece detected
                    # Find the jump position
                    jump_x, jump_y = to_pos[0] + (to_pos[0] - from_pos[0]), to_pos[1] + (to_pos[1] - from_pos[1])
                    jump_pos = (jump_x, jump_y)
                    
                    if board[jump_pos] == board.empty:  # Ensure landing square is empty
                        jumps.append((from_pos, jump_pos, to_pos))  # Store move and captured piece
                
                elif board[to_pos] == board.empty:
                    available_moves.append((from_pos, to_pos))
        
        return jumps if jumps else available_moves  # Prioritize jumps over regular moves


    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves
    
    def result(self, state, move, update_counter=False):
        """Apply a move, update board state, and track draw conditions."""
        if move not in state.moves:
            return state  # Ignore illegal moves
        
        reset_capture = False
        increase_capture = False
        
        board = state.board.copy()
        prev_pos, new_pos = move[:2]  
        captured_pos = move[2] if len(move) > 2 else None  
    
        board[new_pos] = board[prev_pos]  # Place piece at new position
        board[prev_pos] = board.empty  # Remove piece from original position
    
        if captured_pos:
            board[captured_pos] = board.empty  # Remove captured piece
            reset_capture = True  # Reset the counter when a capture occurs
        else:
            increase_capture = True  # Increment if no capture
    
        # Check for king promotion
        if (state.to_move == board.dark_player and new_pos[0] == board.height - 1) or \
           (state.to_move == board.light_player and new_pos[0] == 0):
            board[new_pos] = board[new_pos].upper()  
            reset_capture = True  # Reset counter for king movement

        if update_counter and reset_capture:
            board.no_capture_count = 0
        elif update_counter and increase_capture:
            board.no_capture_count += 1
    
        # Determine if the player can continue jumping
        opponent = board.light_player if state.to_move == board.dark_player else board.dark_player
        moves = list(state.moves)
        moves.remove(move)
        player_moves = self.get_moves(GameState(to_move=state.to_move,
                         utility=self.compute_utility(board, move, state.to_move, update_counter=False),
                         board=board, moves=moves))
        opponent_moves = self.get_moves(GameState(to_move=opponent,
                         utility=self.compute_utility(board, move, opponent, update_counter=False),
                         board=board, moves=moves))
        next_to_move = state.to_move if captured_pos and any(len(m) > 2 and m[0] == new_pos for m in player_moves) else \
                       (board.light_player if state.to_move == board.dark_player else board.dark_player)
        new_moves = player_moves if next_to_move == state.to_move else opponent_moves
    
        return GameState(to_move=next_to_move,
                         utility=self.compute_utility(board, move, state.to_move, update_counter),
                         board=board, moves=new_moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 for draw."""
        return state.utility if player == state.board.dark_player else -state.utility

    def terminal_test(self, state, update_counter=False):
        """Check if the game is a win, a draw by repetition, or the 40-move rule."""
        
        # Win condition
        if state.utility != 0:
            return True  
    
        # 40-move rule
        if state.board.no_capture_count >= 40 and update_counter:
            if state.board.verbose:
                print("Draw by 40-move rule.")
            return True  
    
        # Threefold repetition rule
        if update_counter:
            board_tuple = tuple(sorted(state.board.items()))
            self.board_history[board_tuple] = self.board_history.get(board_tuple, 0) + 1
    
            if self.board_history[board_tuple] >= 3:
                if state.board.verbose:
                    print("Draw by threefold repetition.")
                return True  
    
        return False
    
    def display(self, state):
        board = state.board
        for x in range(self.v):
            for y in range(self.h):
                print(board.get((x, y), board.empty), end=' ')
            print()
            
    def compute_utility(self, board, move, player, update_counter=False):
        """Compute utility: 1 for win, -1 for loss, 0 for draw"""
        opponent = board.light_player if player == board.dark_player else board.dark_player
        util = {board.dark_player: 1, board.light_player: -1}
    
        # Count remaining pieces for both players
        player_pieces = sum(1 for piece in board.values() if piece.lower() == player.lower())
        opponent_pieces = sum(1 for piece in board.values() if piece.lower() == opponent.lower())
    
        # Win condition: If the opponent has no pieces left
        if opponent_pieces == 0:
            return util[player]  # Player wins
    
        # Draw conditions
        if board.no_capture_count >= 40 and update_counter:  # 40-move rule
            return 0  
    
        if not self.get_moves(GameState(to_move=opponent, board=board, utility=0, moves=[])) and update_counter:  
            return 0  # No legal moves → draw by stalemate
    
        return 0  # Game is still ongoing

    
    def init_board(self, dark_player='b', light_player='w'):
        dark_player = dark_player.lower()
        light_player = light_player.lower()
        board_dict = {}
        board_obj = Board(width=self.h, height=self.v, to_move=dark_player)
        for x in range(self.v):
            for y in range(self.h):
                piece = board_obj.empty
                if x%2 == 0 and y%2 != 0 or x%2 != 0 and y%2 == 0:
                    if x < 3:
                        piece = dark_player
                    elif x > 4:
                        piece = light_player
                board_dict[(x, y)] = piece
        board_obj = board_obj.new(board_dict, dark_player=dark_player, light_player=light_player, no_capture_count=0, verbose=True)
        
        return board_obj
    
    def play_game(self, *players):
        """Play a Checkers game with move logging if verbose is enabled."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                prev_pos, new_pos, *_ = move  # Extract move positions
                
                if state.board.verbose:
                    print('Player', state.to_move, 'move from:', prev_pos, 'to:', new_pos)
                
                state = self.result(state, move, update_counter=True)  # Apply the move
                
                if state.board.verbose:
                    print(state.board)  # Print board after move
                
                if self.terminal_test(state, update_counter=True):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


def cache1(function):
    "Like lru_cache(None), but only considers the first argument of function."
    cache = {}
    def wrapped(x, *args):
        if x not in cache:
            cache[x] = function(x, *args)
        return cache[x]
    return wrapped

def alphabeta_search_tt(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move
    infinity = math.inf

    @cache1
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    @cache1
    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity)


def alpha_beta_tt_player(game, state):
    return alphabeta_search_tt(state, game)


if __name__ == "__main__":

    g = Checkers()
    u = g.play_game(random_player, alpha_beta_cutoff_player)
    util = {1 : 'Dark_player', 0 : 'Draw', -1 : 'Light_player'}
    winner = util[u]
    print('Winner is', winner)