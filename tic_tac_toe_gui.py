import tkinter as tk
from tkinter import messagebox
import random

SIZE = 3
PLAYER = 'O'   # You
AI      = 'X'  # Computer

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)

        self.board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]
        self.buttons = [[None for _ in range(SIZE)] for _ in range(SIZE)]

        # Top frame: status + new game
        top = tk.Frame(root, padx=10, pady=10)
        top.pack(fill="x")

        self.status = tk.Label(top, text="Your turn (O)", font=("Segoe UI", 12))
        self.status.pack(side="left")

        tk.Button(top, text="New Game", command=self.reset, font=("Segoe UI", 11)).pack(side="right")

        # Board
        board_frame = tk.Frame(root, padx=10, pady=10, bg="#0e1624")
        board_frame.pack()

        for r in range(SIZE):
            for c in range(SIZE):
                b = tk.Button(
                    board_frame,
                    text="",
                    font=("Segoe UI", 24, "bold"),
                    width=3,
                    height=1,
                    relief="raised",
                    bg="#122036",
                    fg="#00ffff",
                    activebackground="#183057",
                    activeforeground="#ff003c",
                    command=lambda rr=r, cc=c: self.handle_player_move(rr, cc)
                )
                b.grid(row=r, column=c, padx=6, pady=6)
                self.buttons[r][c] = b

    # ---------- Game flow ----------
    def handle_player_move(self, r, c):
        if self.board[r][c] != ' ' or self.game_over():
            return
        self.place(r, c, PLAYER)

        won, line = self.check_win(PLAYER)
        if won:
            self.highlight(line)
            self.end_game("You win! 🎉")
            return

        if self.is_full():
            self.end_game("Draw game.")
            return

        self.status.config(text="Computer thinking…")
        self.root.after(250, self.ai_move)  # small delay for UX

    def ai_move(self):
        r, c = self.best_ai_move()
        self.place(r, c, AI)

        won, line = self.check_win(AI)
        if won:
            self.highlight(line)
            self.end_game("Computer wins! 🤖")
            return

        if self.is_full():
            self.end_game("Draw game.")
            return

        self.status.config(text="Your turn (O)")

    def reset(self):
        self.board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]
        for r in range(SIZE):
            for c in range(SIZE):
                b = self.buttons[r][c]
                b.config(text="", state="normal", bg="#122036")
        self.status.config(text="Your turn (O)")

    def end_game(self, msg):
        # disable buttons
        for r in range(SIZE):
            for c in range(SIZE):
                self.buttons[r][c].config(state="disabled")
        self.status.config(text=msg)
        messagebox.showinfo("Game Over", msg)

    # ---------- Board helpers ----------
    def place(self, r, c, piece):
        self.board[r][c] = piece
        self.buttons[r][c].config(text=piece)

    def is_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def game_over(self):
        return self.check_win(PLAYER)[0] or self.check_win(AI)[0] or self.is_full()

    def highlight(self, line):
        for (r, c) in line:
            self.buttons[r][c].config(bg="#0a7")

    # ---------- Win check ----------
    def check_win(self, piece):
        # rows
        for r in range(SIZE):
            if all(self.board[r][c] == piece for c in range(SIZE)):
                return True, [(r, 0), (r, 1), (r, 2)]
        # cols
        for c in range(SIZE):
            if all(self.board[r][c] == piece for r in range(SIZE)):
                return True, [(0, c), (1, c), (2, c)]
        # diagonals
        if all(self.board[i][i] == piece for i in range(SIZE)):
            return True, [(0, 0), (1, 1), (2, 2)]
        if all(self.board[i][SIZE - 1 - i] == piece for i in range(SIZE)):
            return True, [(0, 2), (1, 1), (2, 0)]
        return False, []

    # ---------- Simple smart AI ----------
    def best_ai_move(self):
        # 1) If AI can win now, do it
        move = self.find_winning_move(AI)
        if move: return move

        # 2) If player can win next, block it
        move = self.find_winning_move(PLAYER)
        if move: return move

        # 3) Take center if free
        if self.board[1][1] == ' ':
            return (1, 1)

        # 4) Pick a corner if available
        corners = [(0,0),(0,2),(2,0),(2,2)]
        random.shuffle(corners)
        for r, c in corners:
            if self.board[r][c] == ' ':
                return (r, c)

        # 5) Fallback: any empty cell
        empties = [(r, c) for r in range(SIZE) for c in range(SIZE) if self.board[r][c] == ' ']
        return random.choice(empties)

    def find_winning_move(self, piece):
        # Try each empty cell; if placing piece there wins, take it
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == ' ':
                    self.board[r][c] = piece
                    win, _ = self.check_win(piece)
                    self.board[r][c] = ' '
                    if win:
                        return (r, c)
        return None

def main():
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
