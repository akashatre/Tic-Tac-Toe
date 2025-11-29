#!/usr/bin/env python3
"""
Tic-Tac-Toe (2 Player) — Tkinter
Single-file, click-to-play game for two human players.
Run: python tictactoe_two_player.py
"""
import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe (2 Player)")
        self.root.resizable(False, False)

        # Game state
        self.board = [None] * 9  # 0..8
        self.current_player = 'X'  # X starts
        self.move_history = []
        self.game_over = False
        self.round_starting_player = 'X'

        # Scoreboard
        self.score = {'X': 0, 'O': 0, 'Draws': 0}

        # UI setup
        self.status_var = tk.StringVar()
        self.status_var.set("Player X's turn")

        self._build_ui()

    def _build_ui(self):
        # Status label
        status_frame = tk.Frame(self.root)
        status_frame.pack(padx=10, pady=(10, 0), fill='x')
        status_label = tk.Label(status_frame, textvariable=self.status_var, font=('Segoe UI', 12, 'bold'))
        status_label.pack()

        # Grid buttons
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(padx=10, pady=10)

        self.buttons = []
        for r in range(3):
            for c in range(3):
                idx = r * 3 + c
                btn = tk.Button(
                    grid_frame,
                    text="",
                    width=6,
                    height=3,
                    font=('Segoe UI', 20, 'bold'),
                    command=lambda i=idx: self.on_cell_click(i)
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons.append(btn)

        # Control buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(padx=10, pady=(0, 10), fill='x')

        self.undo_btn = tk.Button(control_frame, text="Undo", command=self.undo_move)
        self.undo_btn.pack(side='left', padx=5)

        new_round_btn = tk.Button(control_frame, text="New Round", command=self.new_round)
        new_round_btn.pack(side='left', padx=5)

        reset_score_btn = tk.Button(control_frame, text="Reset Score", command=self.reset_score)
        reset_score_btn.pack(side='left', padx=5)

        # Scoreboard
        score_frame = tk.Frame(self.root)
        score_frame.pack(padx=10, pady=(0, 10), fill='x')

        self.score_var = tk.StringVar()
        self._update_score_label()
        score_label = tk.Label(score_frame, textvariable=self.score_var, font=('Segoe UI', 10))
        score_label.pack()

    def on_cell_click(self, idx):
        if self.game_over:
            return
        if self.board[idx] is not None:
            return

        # Make move
        self.board[idx] = self.current_player
        self.buttons[idx].config(text=self.current_player)
        self.move_history.append(idx)

        # Check game state
        winner, combo = self._check_winner()
        if winner:
            self.game_over = True
            self._highlight_winner(combo)
            self.score[winner] += 1
            self._update_score_label()
            self.status_var.set(f"Player {winner} wins! Click 'New Round' to play again.")
            return

        if all(cell is not None for cell in self.board):
            self.game_over = True
            self.score['Draws'] += 1
            self._update_score_label()
            self.status_var.set("It's a draw! Click 'New Round' to play again.")
            return

        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.status_var.set(f"Player {self.current_player}'s turn")

    def undo_move(self):
        if not self.move_history or self.game_over:
            return
        last_idx = self.move_history.pop()
        self.board[last_idx] = None
        self.buttons[last_idx].config(text="", bg=self.root.cget('bg'))
        # Switch player back
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.status_var.set(f"Player {self.current_player}'s turn (after undo)")

    def new_round(self):
        # Clear board
        self.board = [None] * 9
        for btn in self.buttons:
            btn.config(text="", bg=self.root.cget('bg'))
        self.move_history.clear()
        self.game_over = False
        # Alternate starting player each round
        self.round_starting_player = 'O' if self.round_starting_player == 'X' else 'X'
        self.current_player = self.round_starting_player
        self.status_var.set(f"New round! Player {self.current_player} starts")

    def reset_score(self):
        if messagebox.askyesno("Reset Score", "Reset the scoreboard? This won't affect the current round."):
            self.score = {'X': 0, 'O': 0, 'Draws': 0}
            self._update_score_label()

    def _update_score_label(self):
        self.score_var.set(f"Score — X: {self.score['X']} | O: {self.score['O']} | Draws: {self.score['Draws']}")

    def _check_winner(self):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for a, b, c in wins:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a], (a, b, c)
        return None, None

    def _highlight_winner(self, combo):
        if combo:
            for i in combo:
                self.buttons[i].config(bg="#90EE90")  # light green

def main():
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
