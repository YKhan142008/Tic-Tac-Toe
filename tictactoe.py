import random 
import numpy as np 

def main():
    ... 


#Initialise board 
def create_board():
    return np.arange(1, 10).reshape(3,3)

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

print_board(board)