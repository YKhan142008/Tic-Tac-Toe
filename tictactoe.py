import random
import re 
from math import inf
import numpy as np


count = 0 #Represents the number of recurssive calls used by the minimax function


def main():
    board = create_board()
    print_board(board)
    player = input("Do you want to be x or o: ").strip().upper()
    
    while True:
        if player == "O" or player == "X":
            pvc = input("Would you like to play against a computer (Y or N) ").strip().upper()
            if pvc in ["Y", "N"]:
                break 
            continue
            
        else:
            print("You must enter x or o")
            player = input("Do you want to be x or o: ").strip().upper()
        
        
    
    opponent = "O" if player == "X" else "X"
    eval_dict = {player: 1, opponent: -1} #Assigns an eval value if the player/opponent wins
    if pvc == "N":
        player_versus_player(board, player, opponent)
    else:
        return


def player_versus_player(board, player, opponent):
    turn = 0
    while True:
        current_player = players_turn(player, opponent, turn)
        try:
            move = int(input(f"Enter the number you want to play {current_player}: "))
        except ValueError:
            print(f"Index must be a number.")
        
        if move not in range(1, 10):
            print("Index must be in range (1-9)")
        
        row, col = get_pos(move)
        play_move(row, col, board, current_player)
        print_board(board)
        turn += 1

        if check_winner(board) == player:
            print(f"{player} wins!")
            break 
        elif check_winner(board) == opponent:
            print(f"{opponent} wins!")
            break
        
        elif len(get_empty_squares(board)) == 0:
            print("Draw!")
            break



def players_turn(player, opponent, turn):
    return player if turn % 2 == 0 else opponent

def get_pos(index):
    return divmod(index - 1, 3)

    

#Initialise board 
def create_board():
    return np.arange(1, 10).astype(str).reshape(3,3)


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


transposition_table = {}

def minimaxAB(board, depth, alpha, beta, eval_dict, current_player):
    global count, transposition_table

    key = board.tobytes()

    if key in transposition_table:
        return transposition_table[key]

    winner = check_winner(board)
    if winner:
        count += 1
        return eval_dict[winner]
    
    if check_draw(board):
        count += 1
        return 0
    
    is_maximizer = eval_dict[current_player] == 1
    players = list(eval_dict.keys())
    next_player = players[1] if current_player == players[0] else players[1]

    if is_maximizer:
        max_eval = -inf
        for move in order_moves(board, current_player):
            board_copy = np.copy(board)
            play_move(move[0], move[1], board_copy, current_player)
            eval = minimaxAB(board_copy, depth + 1, alpha, beta, next_player)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        transposition_table[key] = max_eval
        return max_eval
    else:
        min_eval = inf
        for move in order_moves(board, current_player):
            board_copy = np.copy(board)
            play_move(move[0], move[1], board_copy, current_player)
            eval = minimaxAB(board_copy, depth + 1, alpha, beta, next_player)
            min_eval = min(min_eval, eval)
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        transposition_table[key] = min_eval
        return min_eval


def play_best_move(board, eval_dict, current_player):
    is_maximizer = eval_dict[current_player] == 1
    best_score = -inf if is_maximizer else inf
    best_move = None
    players = list(eval_dict.keys())

    for move in order_moves(board, current_player):
        board_copy = np.copy(board)
        play_move(move[0], move[1], board_copy, current_player)

        next_player = players[1] if current_player == players[0] else players[0]
        score = minimaxAB(board_copy, 0, -inf, inf, next_player) 

        if (is_maximizer and score > best_score) or (not is_maximizer and score < best_score):
            best_score = score
            best_move = move
    
    print(f"Best score for {current_player}: {best_score}")
    play_move(best_move[0], best_move[1], board, current_player)



if __name__ == "__main__":
    main()