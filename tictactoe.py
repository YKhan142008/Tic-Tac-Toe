from math import inf
import numpy as np

count = 0  # Number of recursive calls
transposition_table = {}

def main():
    board = create_board()
    print_board(board)
    
    player = input("Do you want to be X or O? ").strip().upper()
    while player not in ["X", "O"]:
        print("Invalid input. Please enter X or O.")
        player = input("Do you want to be X or O? ").strip().upper()
    
    opponent = "O" if player == "X" else "X"
    
    pvc = input("Would you like to play against a computer (Y or N)? ").strip().upper()
    while pvc not in ["Y", "N"]:
        pvc = input("Invalid input. Enter Y or N: ").strip().upper()

    if pvc == "N":
        player_versus_player(board, player, opponent)
    else:
        play_first = input("Do you want to play first (Y or N)? ").strip().upper()
        while play_first not in ["Y", "N"]:
            play_first = input("Invalid input. Enter Y or N: ").strip().upper()

        # Determine evaluation dictionary
        if play_first == "Y":
            eval_dict = {player: 1, opponent: -1}
            human_player, computer_player = player, opponent
        else:
            eval_dict = {opponent: 1, player: -1}
            human_player, computer_player = opponent, player

        player_versus_computer(board, eval_dict, human_player, computer_player)

# ========== Game Modes ==========

def player_versus_player(board, player, opponent):
    turn = 0
    while True:
        current_player = player if turn % 2 == 0 else opponent
        try:
            move = int(input(f"Enter your move {current_player} (1-9): "))
        except ValueError:
            print("Invalid input. Enter a number 1-9.")
            continue

        if move not in range(1, 10):
            print("Move must be between 1 and 9.")
            continue

        row, col = get_pos(move)
        if board[row, col] not in [str(i) for i in range(1, 10)]:
            print("That square is already taken.")
            continue

        play_move(row, col, board, current_player)
        print_board(board)

        winner = check_winner(board)
        if winner:
            print(f"{winner} wins!")
            break
        if check_draw(board):
            print("Draw!")
            break
        turn += 1

def player_versus_computer(board, eval_dict, human_player, computer_player):
    turn = 0
    while True:
        current_player = human_player if turn % 2 == 0 else computer_player

        if current_player == human_player:
            try:
                move = int(input(f"Enter your move {human_player} (1-9): "))
            except ValueError:
                print("Invalid input. Enter a number 1-9.")
                continue

            if move not in range(1, 10):
                print("Move must be between 1 and 9.")
                continue

            row, col = get_pos(move)
            if board[row, col] not in [str(i) for i in range(1, 10)]:
                print("That square is already taken.")
                continue

            play_move(row, col, board, human_player)
            print_board(board)

        else:
            print("Computer is thinking...")
            play_best_move(board, eval_dict, computer_player)
            print_board(board)

        winner = check_winner(board)
        if winner:
            if winner == human_player:
                print("You win!")
            else:
                print("Computer wins!")
            break

        if check_draw(board):
            print("Draw!")
            break

        turn += 1

# ========== Core Game Logic ==========

def create_board():
    return np.arange(1, 10).astype(str).reshape(3, 3)

def print_board(board):
    print()
    for i in range(3):
        print("     |     |     ")
        print(f"  {board[i, 0]}  |  {board[i, 1]}  |  {board[i, 2]}  ")
        print("     |     |     ")
        if i < 2:
            print("-" * 18)
    print()

def get_pos(index):
    return divmod(index - 1, 3)

def play_move(row, col, board, player):
    board[row, col] = player

def check_winner(board):
    for i in range(3):
        if np.all(board[i, :] == board[i, 0]):
            return board[i, 0]
        if np.all(board[:, i] == board[0, i]):
            return board[0, i]
    if np.all(np.diag(board) == board[1, 1]):
        return board[1, 1]
    if np.all(np.diag(np.fliplr(board)) == board[1, 1]):
        return board[1, 1]
    return None

def check_draw(board):
    return len(get_empty_squares(board)) == 0 and check_winner(board) is None

def get_empty_squares(board):
    return [(i, j) for i in range(3) for j in range(3)
            if board[i, j] in [str(n) for n in range(1, 10)]]

def order_moves(board, player):
    moves = get_empty_squares(board)
    ordered = []
    for move in moves:
        board_copy = np.copy(board)
        play_move(*move, board_copy, player)
        if check_winner(board_copy) == player:
            ordered.insert(0, move)
        else:
            ordered.append(move)
    return ordered

# ========== Minimax ==========

def minimaxAB(board, depth, alpha, beta, eval_dict, current_player):
    global count, transposition_table
    key = board.tobytes()

    if key in transposition_table:
        return transposition_table[key]

    winner = check_winner(board)
    if winner:
        return eval_dict[winner]
    if check_draw(board):
        return 0

    is_max = eval_dict[current_player] == 1
    players = list(eval_dict.keys())
    next_player = players[1] if current_player == players[0] else players[0]

    if is_max:
        max_eval = -inf
        for move in order_moves(board, current_player):
            board_copy = np.copy(board)
            play_move(*move, board_copy, current_player)
            eval_score = minimaxAB(board_copy, depth + 1, alpha, beta, eval_dict, next_player)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        transposition_table[key] = max_eval
        return max_eval
    else:
        min_eval = inf
        for move in order_moves(board, current_player):
            board_copy = np.copy(board)
            play_move(*move, board_copy, current_player)
            eval_score = minimaxAB(board_copy, depth + 1, alpha, beta, eval_dict, next_player)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        transposition_table[key] = min_eval
        return min_eval

def play_best_move(board, eval_dict, current_player):
    is_max = eval_dict[current_player] == 1
    best_score = -inf if is_max else inf
    best_move = None
    players = list(eval_dict.keys())
    next_player = players[1] if current_player == players[0] else players[0]

    for move in order_moves(board, current_player):
        board_copy = np.copy(board)
        play_move(*move, board_copy, current_player)
        score = minimaxAB(board_copy, 0, -inf, inf, eval_dict, next_player)

        if (is_max and score > best_score) or (not is_max and score < best_score):
            best_score = score
            best_move = move

    print(f"Computer chooses position {best_move[0] * 3 + best_move[1] + 1} (score: {best_score})")
    play_move(*best_move, board, current_player)

# ========== Run Game ==========

if __name__ == "__main__":
    main()
