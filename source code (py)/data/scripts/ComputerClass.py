import math

class Computer:
    # an algorithm which precalculates every possible move and evaluates the result
    # it is called recursively (again and again)
    def minimax(game_board: list, player_index: int, depth: int) -> int:
        from main import Game
        # evaluate the position if the current game is finished or depth is reached
        if Game.is_over(game_board) or depth == 0:
            return Game.evaluate(game_board)

        # making moves to calculate the possible result, then unding them
        evaluations = []
        for index in range(9):
            if game_board[index] == 0:
                # making move
                game_board[index] = player_index
                # calling algorithm again
                evaluations.append(Computer.minimax(game_board, player_index % 2 + 1, depth - 1))
                # unding move
                game_board[index] = 0

        # finally returning the best result
        return max(evaluations) if player_index == 1 else min(evaluations)  

    # getting the best move for the computer by using the minimax algorithm, returning a position
    def make_best_move(game_board: list, player_index: int, depth: int) -> int:
        # current best score and move are set to the worst case
        best_score = -math.inf if player_index == 1 else math.inf
        best_move = None
        # checking for every possible move all possible moves and evaluating them
        for index in range(9):
            if game_board[index] == 0:
                game_board[index] = player_index
                score = Computer.minimax(game_board, player_index % 2 + 1, depth)
                game_board[index] = 0
                # resetting best move if its better than the previous
                if player_index == 1:
                    if (score > best_score):
                        best_score = score
                        best_move = index
                else:
                    if (score < best_score):
                        best_score = score
                        best_move = index
        return best_move

    # converting the move from an index into x and y coordinates
    def make_move(board, depth) -> list:
        from main import Game
        move = Computer.make_best_move(board, 2, depth)
        for x in range(3):
            for y in range(3):
                if x + y * 3 == move:
                    pos_x = x
                    pos_y = y

        board = Game.make_move(board, (pos_x, pos_y), 2)
        return board