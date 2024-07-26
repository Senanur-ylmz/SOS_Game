import random

# this class creates game board. Its default size is 5x5 with the letters 'S' in the corners.
class Board:
    def __init__(self):
        self.size = 5
        self.board = [[' ' for _ in range(self.size)]
                      for _ in range(self.size)]
        self.initialize_board()
    
    # bring the board to its initial state. There is the letter 'S' in the corners.
    def initialize_board(self):
        self.board[0][0] = self.board[0][4] = self.board[4][0] = self.board[4][4] = 'S'
    
    # prints the current state of the board on the screen.
    def display_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 9)
    
    # checks the specified row and column is a valid move.
    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == ' '

    # attempts to make a move to the specified row and column with the specified symbol.
    def make_move(self, row, col, symbol):
        if self.is_valid_move(row, col):
            self.board[row][col] = symbol
            return True
        return False
    
    # check if the board is full.
    def is_full(self):
        return all(all(cell != ' ' for cell in row) for row in self.board)


class Player:
    # each player has a name and score.
    def __init__(self, name):
        self.name = name
        self.score = 0


class HumanPlayer(Player):
    # allows a human player to make moves. It receives symbol and move information from the user.
    def make_move(self, board):
        symbol = input(
            f"{self.name}, enter your symbol ('S' or 'O'): ").upper()
        while symbol not in ['S', 'O']:
            print("Invalid symbol. Please enter 'S' or 'O'.")
            symbol = input(
                f"{self.name}, enter your symbol ('S' or 'O'): ").upper()

        while True:
            try:
                row = int(input(f"{self.name}, enter row (0-4): "))
                col = int(input(f"{self.name}, enter column (0-4): "))
                if board.make_move(row, col, symbol):
                    return row, col
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter integers for row and column.")


class AIPlayer(Player):
    # constructor method of AI player class. It has features such as depth, heuristic function and name.
    def __init__(self, depth=4, heuristic=None, name="AI"):
        super().__init__(name)
        self.depth = depth
        self.heuristic = heuristic if heuristic else self.h1

    # AI player make a move. This method use Minimax algorithm.
    def make_move(self, board):
        # generate all valid moves
        valid_moves = [(i, j) for i in range(board.size)
                    for j in range(board.size) if board.is_valid_move(i, j)]

        # evaluate each move
        scores = []
        for move in valid_moves:
            row, col = move
            board.make_move(row, col, 'S')  # try 'S'
            score_s = self.minimax(board, self.depth, float(
                '-inf'), float('inf'), False, 'S')[0]
            board.board[row][col] = ' '  # undo the move

            board.make_move(row, col, 'O')  # try 'O'
            score_o = self.minimax(board, self.depth, float(
                '-inf'), float('inf'), False, 'O')[0]
            board.board[row][col] = ' '  # undo the move

            # choose symbol that gives the higher score
            if score_s > score_o:
                symbol = 'S'
                score = score_s
            else:
                symbol = 'O'
                score = score_o

            scores.append((score, symbol, move))

        # sort moves by their scores
        scores.sort(reverse=True)

        # choose one of top moves randomly
        top_scores = [score for score in scores if score[0] == scores[0][0]]
        _, symbol, move = random.choice(top_scores)

        # make the chosen move
        row, col = move
        board.make_move(row, col, symbol)
        return row, col

    # heuristic 1
    @staticmethod
    def h1(board):
        # count the number of 'SOS' sequences
        count = 0
        for i in range(board.size):
            for j in range(board.size):
                # check for vertical 'SOS'
                if i + 2 < board.size and board.board[i][j] == board.board[i + 2][j] == 'S' and board.board[i + 1][j] == 'O':
                    count += 1
                # check for horizontal 'SOS'
                if j + 2 < board.size and board.board[i][j] == board.board[i][j + 2] == 'S' and board.board[i][j + 1] == 'O':
                    count += 1
                # check for diagonal 'SOS'
                if i + 2 < board.size and j + 2 < board.size and (
                        board.board[i][j] == board.board[i + 2][j + 2] == 'S' and board.board[i + 1][j + 1] == 'O' or
                        i == 0 and board.board[i][j] == board.board[i +
                                                                    2][j + 2] == 'S' and board.board[i + 1][j + 1] == 'O'
                ):
                    count += 1
                # check for reverse diagonal 'SOS'
                if i - 2 >= 0 and j + 2 < board.size and board.board[i][j] == board.board[i - 2][j + 2] == 'S' and board.board[i - 1][j + 1] == 'O':
                    count += 1

        return count

    # heuristic 2
    @staticmethod
    def h2(board):
        # count number of 'SOS' sequences and penalize for each 'O' symbol on board.
        count = AIPlayer.h1(board)
        for row in board.board:
            count -= row.count('O')
        return count

    #  finds the best move with the minimax algorithm.
    def minimax(self, board, depth, alpha, beta, maximizing_player, symbol):
        if depth == 0 or board.is_full():
            # return empty move when game is over.
            return self.heuristic(board), (0, 0)

        valid_moves = [(i, j) for i in range(board.size)
                    for j in range(board.size) if board.is_valid_move(i, j)]

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in valid_moves:
                row, col = move
                board.make_move(row, col, symbol)
                eval = self.minimax(board, depth - 1, alpha,
                                    beta, False, symbol)[0]
                board.board[row][col] = ' '  # undo the move
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval, best_move if best_move is not None else (0, 0)
        else:
            min_eval = float('inf')
            best_move = None
            for move in valid_moves:
                row, col = move
                board.make_move(row, col, 'O' if symbol == 'S' else 'S')
                eval = self.minimax(board, depth - 1, alpha,
                                    beta, True, symbol)[0]
                board.board[row][col] = ' '  # undo the move
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval, best_move if best_move is not None else (0, 0)


# starts the game and controls the flow of the game.
def play_game(player1, player2):
    board = Board()
    current_player = player1

    while True:
        board.display_board()
        row, col = current_player.make_move(board)

        sos_count = AIPlayer.h1(board)
        if sos_count > (player1.score + player2.score):
            board.display_board()
            player_added_score = sos_count - (player1.score + player2.score)
            print(
                f"{current_player.name} ({'S' if current_player == player1 else 'O'}) scores {player_added_score} point(s)!")
            current_player.score += player_added_score
        
        print("Score:")
        print(f"{player1.name}: {player1.score}")
        print(f"{player2.name}: {player2.score}")

        if board.is_full():
            board.display_board()
            if player1.score > player2.score:
                print(f"{player1.name} Wins!")
                break
            elif player2.score > player1.score:
                print(f"{player2.name} Wins!")
                break
            else:
                print("It's a draw!")
                break


        current_player = player2 if current_player == player1 else player1

# selects the game mode and starts the game.
def main():
    while True:
        print("Select Game Mode:")
        print("1. Human vs Human")
        print("2. Human vs AI")
        print("3. AI vs AI")

        choice = input("Enter the number of your choice (1-3): ")

        if choice == '1':
            player1_name = input("Enter name for Player 1: ")
            player2_name = input("Enter name for Player 2: ")
            play_game(HumanPlayer(player1_name), HumanPlayer(player2_name))
        elif choice == '2':
            while True:
                player_name = input("Enter name for Player: ")
                choice_mod = input("Enter the mode that you play (Easy or Hard): ")
                if choice_mod.lower() == 'easy':
                    play_game(HumanPlayer(player_name), AIPlayer(
                        heuristic=AIPlayer.h1, name="AI"))
                    break
                elif choice_mod.lower() == 'hard':
                    play_game(HumanPlayer("Player"), AIPlayer(heuristic=AIPlayer.h2, name="AI"))
                    break
                else:
                    print("Invalid mode. Please enter 'Easy' or 'Hard'.")
        elif choice == '3':
            player1 = AIPlayer(heuristic=AIPlayer.h1, name="AI1")
            player2 = AIPlayer(heuristic=AIPlayer.h2, name="AI2")
            play_game(player1, player2)
        else:
            print("Invalid choice. Exiting.")
            break

        restart = input("Do you want to play again? (yes/no): ").lower()
        if restart != 'yes':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
