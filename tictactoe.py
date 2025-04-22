import random 
from math import inf
import numpy as np


count = 0 #Represents the number of recurssive calls used by the minimax function
player = input("Do you want to be x or o: ").upper() #Determines the player who starts
opponent = "O" if player == "X" else "X"
eval_dict = {player: 1, opponent: -1} #Assigns an eval value if the player/opponent wins

def main():
    ... 


#Initialise board 
def create_board():
    return np.arange(1, 10).astype(str).reshape(3,3)

board = create_board()

#Pretty Print
def print_board(board):
    board_lines = " " * 5 + "|" + " "*5 + "|" + " "*5  
    for i in range(np.size(board, 0)):
        print(board_lines)
        print(f'  {board[i, 0]}  |  {board[i, 1]}  |  {board[i, 2]}   ')
        print(board_lines)
        if i < np.size(board, 0) - 1:
            print("-"* 18)


def play_move(row, col, board, player):
    if board[row, col] in [str(i) for i in range(1, 10)]:  board[row, col] = player 



#Check win conditions 
def check_winner(board):
    #Check horizontal and vertical winner
    for i in range(3):
        if np.all(board[i, :] == board[i, 0]):
            return board[i, 0]
        if np.all(board[:, i] == board[0, i]):
            return board[0, i]
    
    #Diagonal winner 
    if np.all(np.diag(board) == board[1, 1]):
        return board[1,1]
    if np.all(np.diag(np.fliplr(board)) == board[1, 1]):
        return board[1, 1]
    
    return None

def get_empty_squares(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i, j] in [str(i) for i in range(1, 10)]:
                moves.append((i, j))
    return moves

def order_moves(board, player):
    moves = get_empty_squares(board)
    ordered_moves = []

    for move in moves:
        board_copy = np.copy(board)
        play_move(move[0], move[1], board_copy, player)

        if check_winner(board_copy) == player:
            # Winning move, add to the front
            ordered_moves.insert(0, move)
            
        else:
            # Non-winning move, add to the back
            ordered_moves.append(move)

    return ordered_moves

        

def check_draw(board):
   if len(get_empty_squares(board)) == 0 and not check_winner(board):
       return True 
   return False


def minimax(board, depth, is_maximizer):
    global count 
    winner  = check_winner(board)
    if winner:
        count += 1
        return eval_dict[winner] * (10 - depth)
    
    if check_draw(board):
        count += 1
        return 0
    
    if is_maximizer:
        max_eval = -inf
        for move in get_empty_squares(board):
            board_copy = np.copy(board)
            play_move(move[0], move[1], board_copy, player)
            eval = minimax(board_copy, depth + 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = inf
        for move in get_empty_squares(board):
            board_copy = np.copy(board)
            play_move(move[0], move[1], board_copy, opponent)
            eval = minimax(board_copy, depth + 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


transposition_table = {}

def minimaxAB(board, depth, alpha, beta, is_maximizer):
    global count, transposition_table
    count += 1  # Increment count for each recursion

    key = board.tobytes()

    if key in transposition_table:
        return transposition_table[key]

    winner = check_winner(board)
    if winner:
        return eval_dict[winner]
    
    if check_draw(board):
        return 0
    
    if is_maximizer:
        max_eval = -inf
        for move in get_empty_squares(board):
            board_copy = np.copy(board)
            play_move(move[0], move[1], board_copy, player)
            eval = minimaxAB(board_copy, depth + 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        transposition_table[key] = max_eval
        return max_eval
    else:
        min_eval = inf
        for move in get_empty_squares(board):
            board_copy = np.copy(board)
            play_move(move[0], move[1], board_copy, opponent)
            eval = minimaxAB(board_copy, depth + 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        transposition_table[key] = min_eval
        return min_eval


print(count, minimaxAB(board, 0, -inf, inf, True))