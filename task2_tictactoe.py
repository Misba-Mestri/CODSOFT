"""
╔══════════════════════════════════════════════════════════════╗
║         CODSOFT AI INTERNSHIP — TASK 2                       ║
║         Tic-Tac-Toe AI  (Minimax + Alpha-Beta Pruning)       ║
║         Author: Your Name | CodSoft AI Intern               ║
╚══════════════════════════════════════════════════════════════╝

WHAT IT DOES:
  Classic Tic-Tac-Toe where an AI plays against you.
  The AI uses the Minimax algorithm with Alpha-Beta Pruning —
  making it completely unbeatable. Your best outcome is a draw!

HOW TO PLAY:
  - The board positions are numbered 1–9 (like a numpad).
  - Enter a number to place your move.
  - You are X, AI is O.
"""

import math
import os

# ─────────────────────────────────────────────
#  BOARD UTILITIES
# ─────────────────────────────────────────────
def make_board():
    return [' '] * 9  # indices 0–8

def print_board(board):
    """Pretty-print the board with colors and position hints."""
    symbols = {' ': '\033[90m·\033[0m', 'X': '\033[94mX\033[0m', 'O': '\033[91mO\033[0m'}
    positions = [str(i + 1) for i in range(9)]

    def cell(i):
        return symbols[board[i]] if board[i] != ' ' else f'\033[90m{positions[i]}\033[0m'

    print()
    print(f"  {cell(0)} │ {cell(1)} │ {cell(2)}")
    print(" ───┼───┼───")
    print(f"  {cell(3)} │ {cell(4)} │ {cell(5)}")
    print(" ───┼───┼───")
    print(f"  {cell(6)} │ {cell(7)} │ {cell(8)}")
    print()

WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),  # rows
    (0,3,6), (1,4,7), (2,5,8),  # cols
    (0,4,8), (2,4,6)             # diagonals
]

def check_winner(board, player):
    return any(board[a] == board[b] == board[c] == player for a,b,c in WIN_LINES)

def is_draw(board):
    return ' ' not in board

def get_empty(board):
    return [i for i, v in enumerate(board) if v == ' ']

# ─────────────────────────────────────────────
#  MINIMAX WITH ALPHA-BETA PRUNING
# ─────────────────────────────────────────────
def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Minimax with Alpha-Beta Pruning.
    AI = O (maximizing), Human = X (minimizing).
    Returns a score: +10 = AI wins, -10 = Human wins, 0 = draw.
    """
    if check_winner(board, 'O'):
        return 10 - depth   # prefer faster wins
    if check_winner(board, 'X'):
        return depth - 10   # prefer slower losses
    if is_draw(board):
        return 0

    if is_maximizing:
        best = -math.inf
        for i in get_empty(board):
            board[i] = 'O'
            score = minimax(board, depth + 1, False, alpha, beta)
            board[i] = ' '
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break  # ✂️ Beta cut-off
        return best
    else:
        best = math.inf
        for i in get_empty(board):
            board[i] = 'X'
            score = minimax(board, depth + 1, True, alpha, beta)
            board[i] = ' '
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break  # ✂️ Alpha cut-off
        return best

def ai_move(board):
    """Choose the best move for AI (O)."""
    best_score = -math.inf
    best_move = None
    for i in get_empty(board):
        board[i] = 'O'
        score = minimax(board, 0, False, -math.inf, math.inf)
        board[i] = ' '
        if score > best_score:
            best_score = score
            best_move = i
    return best_move

# ─────────────────────────────────────────────
#  GAME LOOP
# ─────────────────────────────────────────────
def play_game():
    board = make_board()
    print("\n\033[1m🎮 Welcome to Tic-Tac-Toe AI!\033[0m")
    print("You are \033[94mX\033[0m  |  AI is \033[91mO\033[0m")
    print("Enter a position (1–9) to play.\n")
    print_board(board)

    # Let player choose who goes first
    choice = input("Do you want to go first? (y/n): ").strip().lower()
    human_turn = choice == 'y'

    while True:
        if human_turn:
            # Human move
            while True:
                try:
                    move = int(input("Your move (1–9): ")) - 1
                    if 0 <= move <= 8 and board[move] == ' ':
                        break
                    print("⚠️  Invalid move. Try again.")
                except ValueError:
                    print("⚠️  Please enter a number 1–9.")

            board[move] = 'X'
            print_board(board)

            if check_winner(board, 'X'):
                print("🎉 \033[94mYou win!\033[0m Incredible — you beat the AI!")
                break
        else:
            # AI move
            print("🤖 AI is thinking...")
            move = ai_move(board)
            board[move] = 'O'
            print(f"AI played position {move + 1}")
            print_board(board)

            if check_winner(board, 'O'):
                print("😈 \033[91mAI wins!\033[0m Better luck next time.")
                break

        if is_draw(board):
            print("🤝 It's a draw! The AI is hard to beat.")
            break

        human_turn = not human_turn

def main():
    print("=" * 55)
    print("   ❌⭕  Tic-Tac-Toe AI  — CodSoft Task 2")
    print("=" * 55)

    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != 'y':
            print("\nThanks for playing! 👋\n")
            break

if __name__ == "__main__":
    main()
