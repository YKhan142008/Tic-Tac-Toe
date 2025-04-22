import random 
import numpy as np

eval_dict = {"X": 1, "O": -1} #Assigns an eval value if the player/opponent wins

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


def play_move(row, col, player):
    global board
    board[row, col] = player


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


play_move(0, 2, "X")
play_move(1, 1, "X")
play_move(2, 1, "X")
print(check_winner(board))