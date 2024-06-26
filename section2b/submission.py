
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
#################################################
# file to edit: notebook.ipynb͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁

import time
from isolation import Board

# Credits if any͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
# 1)͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
# 2)͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
# 3)͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁

class OpenMoveEvalFn:
    def score(self, game, my_player=None):
        """Score the current game state
        Evaluation function that outputs a score equal to how many
        moves are open for AI player on the board minus how many moves
        are open for Opponent's player on the board.

        Note:
            If you think of better evaluation function, do it in CustomEvalFn below.

            Args
                game (Board): The board and game state.
                my_player (Player object): This specifies which player you are.

            Returns:
                float: The current state's score. MyMoves-OppMoves.

            """

        # TODO: finish this function!͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
        #print(len(game.get_player_moves(my_player)))
        #print(len(game.get_opponent_moves(my_player)))

        #return len(game.get_player_moves(my_player)) - len(game.get_opponent_moves(my_player)) #Current

        player_moves = len(game.get_player_moves(my_player))
        opponent_moves = len(game.get_opponent_moves(my_player))

        threshold = (player_moves + opponent_moves) / 72

        if threshold < 0.25:
            return (player_moves * 2) - opponent_moves
        else:
            return player_moves - (2 * opponent_moves)

        #raise NotImplementedError

######################################################################
########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
######## IF YOU WANT TO CALL OR TEST IT CREATE A NEW CELL ############͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
######################################################################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
################ END OF LOCAL TEST CODE SECTION ######################͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁

class CustomPlayer:
    # TODO: finish this class!͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
    """Player that chooses a move using your evaluation function
    and a minimax algorithm with alpha-beta pruning.
    You must finish and test this player to make sure it properly
    uses minimax and alpha-beta to return a good move."""

    def __init__(self, search_depth=4, eval_fn=OpenMoveEvalFn()):
        """Initializes your player.

        if you find yourself with a superior eval function, update the default
        value of `eval_fn` to `CustomEvalFn()`

        Args:
            search_depth (int): The depth to which your agent will search
            eval_fn (function): Evaluation function used by your agent
        """
        self.eval_fn = eval_fn
        self.search_depth = search_depth

    def move(self, game, time_left):
        """Called to determine one move by your agent

        Note:
            1. Do NOT change the name of this 'move' function. We are going to call
            this function directly.
            2. Call alphabeta instead of minimax once implemented.
        Args:
            game (Board): The board and game state.
            time_left (function): Used to determine time left before timeout

        Returns:
            tuple: (int,int): Your best move
        """
        #best_move, utility = minimax(self, game, time_left, depth=self.search_depth)
        print("Time before :", time_left())

        # Iterative deepening
        max_depth = 24
        best_moves = []
        for depth in range(1, max_depth + 1):
            best_move, utility = alphabeta(self, game, time_left, depth = self.search_depth - self.search_depth + depth)
            best_moves.append(best_move)
            print("Move: ", best_moves, " Depth: ", self.search_depth - self.search_depth + depth)
            print("Best Moves at -1: ", best_moves[-1])

            if best_moves[-1] == (-1,-1):
                print(time_left())
                return best_moves[-2]

        print("Time after :", time_left())
        return best_move

    def utility(self, game, my_turn):
        """You can handle special cases here (e.g. endgame)"""

        return self.eval_fn.score(game, self)



###################################################################
########## DON'T WRITE ANY CODE OUTSIDE THE CLASS! ################͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
###### IF YOU WANT TO CALL OR TEST IT CREATE A NEW CELL ###########͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
###################################################################


def minimax(player, game, time_left, depth, my_turn=True):
    """Implementation of the minimax algorithm.
    Args:
        player (CustomPlayer): This is the instantiation of CustomPlayer()
            that represents your agent. It is used to call anything you
            need from the CustomPlayer class (the utility() method, for example,
            or any class variables that belong to CustomPlayer()).
        game (Board): A board and game state.
        time_left (function): Used to determine time left before timeout
        depth: Used to track how deep you are in the search tree
        my_turn (bool): True if you are computing scores during your turn.

    Returns:
        (tuple, int): best_move, val
    """
    #print("Time at beginning: ", time_left)
    #Base Case:
    #if depth is reached or game is over (e.g., no more active moves for one player)
    if depth == 0:
        return (None, player.utility(game, my_turn))
    #return score of current position

    #Recursive Call
    if my_turn:
        best_cost = -1000
        best_move = None
        #print("Time at depth ",depth,": ", game.time_left())
        for move in game.get_active_moves():
            _, eval = minimax(player, game.forecast_move(move)[0], time_left, depth - 1, my_turn = False)
            if eval > best_cost:
                best_cost = eval
                best_move = move
        return (best_move, best_cost)

    else:
        best_cost = 1000
        best_move = None
        #print("Time at depth ",depth,": ", time_left)
        for move in game.get_active_moves():
            _, eval = minimax(player, game.forecast_move(move)[0], time_left, depth - 1, my_turn = True)
            if eval < best_cost:
                best_cost = eval
                best_move = move
        return (best_move, best_cost)

    #raise NotImplementedError


######################################################################
########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
######## IF YOU WANT TO CALL OR TEST IT CREATE A NEW CELL ############͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
######################################################################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
################ END OF LOCAL TEST CODE SECTION ######################͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁

def alphabeta(player, game, time_left, depth, alpha=float("-inf"), beta=float("inf"), my_turn=True):
    """Implementation of the alphabeta algorithm.

    Args:
        player (CustomPlayer): This is the instantiation of CustomPlayer()
            that represents your agent. It is used to call anything you need
            from the CustomPlayer class (the utility() method, for example,
            or any class variables that belong to CustomPlayer())
        game (Board): A board and game state.
        time_left (function): Used to determine time left before timeout
        depth: Used to track how deep you are in the search tree
        alpha (float): Alpha value for pruning
        beta (float): Beta value for pruning
        my_turn (bool): True if you are computing scores during your turn.

    Returns:
        (tuple, int): best_move, val
    """

    if depth == 0 or len(game.get_active_moves()) == 0:
        return (None, player.utility(game, my_turn))

    if time_left() < 30: #Was 60 at 95pt submission
        print(time_left())
        return (-1,-1), -100

    if my_turn:
        best_score, best_move = float("-inf"), None
        for move in game.get_active_moves():
            _, eval = alphabeta(player, game.forecast_move(move)[0], time_left, depth - 1, alpha, beta, my_turn = False)
            if eval == -100:
                return (-1,-1), -100
            if eval > best_score:
                best_score = eval
                best_move = move
            alpha = max(eval, alpha)
            if beta <= alpha:
                break
        return (best_move, best_score)

    else:
        best_score, best_move = float("inf"), None
        for move in game.get_active_moves():
            _, eval = alphabeta(player, game.forecast_move(move)[0], time_left, depth - 1, alpha, beta, my_turn = True)
            if eval < best_score:
                best_score = eval
                best_move = move
            beta = min(eval, beta)
            if beta <= alpha:
                break
        return (best_move, best_score)

    raise NotImplementedError


######################################################################
########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
######## IF YOU WANT TO CALL OR TEST IT CREATE A NEW CELL ############͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
######################################################################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
#tests.minimaxTest(CustomPlayer, minimax)#tests.name_of_the_test #you can uncomment this line to run your test͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
################ END OF LOCAL TEST CODE SECTION ######################͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁

class CustomEvalFn:
    def __init__(self):
        pass

    def score(self, game, my_player=None):
        """Score the current game state.

        Custom evaluation function that acts however you think it should. This
        is not required but highly encouraged if you want to build the best
        AI possible.

        Args:
            game (Board): The board and game state.
            my_player (Player object): This specifies which player you are.

        Returns:
            float: The current state's score, based on your own heuristic.
        """

        # TODO: finish this function!͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
        raise NotImplementedError

######################################################################
############ DON'T WRITE ANY CODE OUTSIDE THE CLASS! #################͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
######## IF YOU WANT TO CALL OR TEST IT CREATE A NEW CELL ############͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
######################################################################