# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 23:35:31 2025

@author: wence
"""

import tkinter as tk
from tkinter import messagebox
from games4e import *
import random
from checkers import Checkers  # Import your Checkers game class

# Dictionary mapping player choices to functions in games4e
players = {
    "Human": None,
    "Random": random_player,
    "Alpha-Beta": alpha_beta_player,
    "Alpha-Beta Cutoff": alpha_beta_cutoff_player,
    "ExpectiMinMax": expect_min_max_player,
    "Monte Carlo Tree Search": mcts_player
}

class CheckersGUI:
    """A GUI interface for playing Checkers with AI and Human options."""
    
    def __init__(self, master):
        self.master = master
        self.master.title("Checkers Game")

        # Game initialization
        self.game = Checkers()
        self.state = self.game.initial
        self.selected_piece = None
        self.valid_moves = []
        
        # Default players (Human vs AI)
        self.player1 = None
        self.player2 = alpha_beta_cutoff_player

        # Player selection UI
        self.create_player_selection()
        
        # Board UI
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()
        self.buttons = {}
        self.create_board()

    def create_player_selection(self):
        """Create dropdowns to select players before starting the game."""
        frame = tk.Frame(self.master)
        frame.pack()

        tk.Label(frame, text="Player 1 (Dark - B)").grid(row=0, column=0)
        self.p1_choice = tk.StringVar(value="Human")
        self.p1_menu = tk.OptionMenu(frame, self.p1_choice, *players.keys())
        self.p1_menu.grid(row=0, column=1)

        tk.Label(frame, text="Player 2 (Light - W)").grid(row=1, column=0)
        self.p2_choice = tk.StringVar(value="Alpha-Beta Cutoff")
        self.p2_menu = tk.OptionMenu(frame, self.p2_choice, *players.keys())
        self.p2_menu.grid(row=1, column=1)

        start_button = tk.Button(frame, text="Start Game", command=self.start_game)
        start_button.grid(row=2, column=0, columnspan=2)

    def start_game(self):
        """Set players and start the game."""
        self.player1 = players[self.p1_choice.get()]
        self.player2 = players[self.p2_choice.get()]
        self.state = self.game.initial  # Reset the game
        self.update_board()

        # If Player 1 is AI, start AI move
        self.run_ai_turn()

    def create_board(self):
        """Create a Tkinter grid for the checkers board."""
        for x in range(8):
            for y in range(8):
                color = "white" if (x + y) % 2 == 0 else "gray"
                btn = tk.Button(self.board_frame, bg=color, width=5, height=2,
                                command=lambda x=x, y=y: self.on_click(x, y))
                btn.grid(row=x, column=y)
                self.buttons[(x, y)] = btn

    def on_click(self, x, y):
        """Handle user clicks to make a move."""
        if self.get_current_player() is not None:  # AI turn, ignore clicks
            return

        piece = self.state.board.get((x, y))
        if self.selected_piece is None:
            if piece.lower() == self.state.to_move.lower():
                self.selected_piece = (x, y)
                self.valid_moves = [move for move in self.state.moves if move[0] == (x, y)]
                self.highlight_moves()
        else:
            move = next((m for m in self.valid_moves if m[1] == (x, y)), None)
            if move:
                self.state = self.game.result(self.state, move, update_counter=True)
                self.update_board()
                self.clear_selection()
                self.check_game_status()
                self.run_ai_turn()  # AI makes the next move if needed
            else:
                self.clear_selection()  # Invalid move, reset

    def highlight_moves(self):
        """Highlight possible moves for selected piece."""
        for _, (tx, ty), *_ in self.valid_moves:
            self.buttons[(tx, ty)].config(bg="lightgreen")

    def clear_selection(self):
        """Reset selection and clear move highlights."""
        for _, btn in self.buttons.items():
            btn.config(bg="white" if (btn.grid_info()["row"] + btn.grid_info()["column"]) % 2 == 0 else "gray")
        self.selected_piece = None
        self.valid_moves = []
        
    def update_board(self):
        """Update the GUI board to reflect the current game state."""
        for (x, y), btn in self.buttons.items():
            piece = self.state.board.get((x, y), '.')
            if piece == '.':
                btn.config(text='')  # Empty square
            else:
                color = "black" if piece.lower() == 'b' else "white"  # Dark pieces are black, Light pieces are white
                font_style = ("Arial", 9, "bold") if piece.isupper() else ("Arial", 9, "normal")  # Bold for kings
                btn.config(text=piece, fg=color, font=font_style)

    def check_game_status(self):
        """Check if the game has ended and show the winner."""
        if self.game.terminal_test(self.state, update_counter=False):
            self.display_winner()

    def display_winner(self):
        """Display the winner in a message box."""
        winner_util = self.game.utility(self.state, self.state.to_move)
        winner = "Dark Player (B)" if winner_util == 1 else "Light Player (W)" if winner_util == -1 else "Draw"
        messagebox.showinfo("Game Over", f"Winner: {winner}")
        for btn in self.buttons.values():
            btn.config(state=tk.DISABLED)

    def get_current_player(self):
        """Return the function of the current player (AI) or None if Human."""
        return self.player1 if self.state.to_move == self.game.initial.board.dark_player else self.player2

    def run_ai_turn(self):
        """If the current player is an AI, execute their move automatically."""
        ai_player = self.get_current_player()
        if ai_player:
            self.master.after(1000, self.ai_move)  # Delay AI move slightly

    def ai_move(self):
        """AI selects and plays a move."""
        if self.game.terminal_test(self.state, update_counter=False):  # Stop AI if game over
            return
    
        ai_player = self.get_current_player()
        if ai_player:
            move = ai_player(self.game, self.state)
            self.state = self.game.result(self.state, move, update_counter=True)
            self.update_board()
            self.check_game_status()
    
            if not self.game.terminal_test(self.state, update_counter=False):  # Ensure game is still running
                self.run_ai_turn()  # Continue AI moves if needed


# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    gui = CheckersGUI(root)
    root.mainloop()
