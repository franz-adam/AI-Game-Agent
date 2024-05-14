#!/usr/bin/env python
# coding: utf-8

# # Challenge the machine
# 
# Play a game of isolation against 3 levels of my AI agents. For all levels, I restricted the 'thinking' period to at most 5 seconds. However, with each level the underlying algorithm changes and the AI agent becomes stronger. Should you be able to defeat Level 3, send me a screenshot and I will share my secret evaluation function with you!
# 
# 1. Click any open field to make the first move.
# 2. Wait at most five seconds for the AI to respond with a move
# 
# 
#   
#   ## Good luck!
#   
#   ---

# In[4]:


# Following two lines make sure anything imported from .py scripts͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁 
# is automatically reloaded if edited & saved (e.g. local unit tests or players)͏󠄂͏️͏󠄌͏󠄎͏󠄎͏󠄊͏󠄁
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
from board_viz import ReplayGame, InteractiveGame
from isolation import Board
from test_players import RandomPlayer
import player_submission_tests as tests
from test_players import HumanPlayer


# In[5]:


import time
from isolation import Board
import random


# In[6]:


class OpenMoveEvalFn:
    def score(self, game, my_player=None):
        player_moves = len(game.get_player_moves(my_player))
        opponent_moves = len(game.get_opponent_moves(my_player))

        threshold = (player_moves + opponent_moves) / 72
        
        if threshold < 0.25:
            return (player_moves * 2) - opponent_moves
        else: 
            return player_moves - (2 * opponent_moves)


# In[7]:


class OpenMoveEvalFn1:
    def score(self, game, my_player=None):
        return len(game.get_player_moves(my_player)) - len(game.get_opponent_moves(my_player))


# In[8]:


class CustomPlayer:

    def __init__(self, search_depth=10, eval_fn=OpenMoveEvalFn()):
        self.eval_fn = eval_fn
        self.search_depth = search_depth
    
    def move(self, game, time_left):   
        # Iterative deepening
        max_depth = 30
        best_moves = []
        for depth in range(1, max_depth + 1):     
            best_move, utility = alphabeta(self, game, time_left, depth = depth)
            best_moves.append(best_move)
    
            if best_moves[-1] == (-1,-1):
                return best_moves[-2]
                
        return best_move

    def utility(self, game, my_turn):
        
        return self.eval_fn.score(game, self)


# In[18]:


class CustomPlayer1:

    def __init__(self, search_depth=5, eval_fn=OpenMoveEvalFn1()):
        self.eval_fn = eval_fn
        self.search_depth = search_depth
    
    def move(self, game, time_left):
        best_move, utility = minimax(self, game, time_left, depth=self.search_depth)
        return best_move

    def utility(self, game, my_turn):
        return self.eval_fn.score(game, self)


# In[1]:


class CustomPlayer2:

    def __init__(self, search_depth=5, eval_fn=OpenMoveEvalFn1()):
        self.eval_fn = eval_fn
        self.search_depth = search_depth
    
    def move(self, game, time_left):
        best_move, utility = alphabeta2(self, game, time_left, depth = self.search_depth)
        return best_move

    def utility(self, game, my_turn):
        return self.eval_fn.score(game, self)


# In[16]:


def minimax(player, game, time_left, depth, my_turn=True):
    #if depth is reached or game is over (e.g., no more active moves for one player)
    if depth == 0:
        return (None, player.utility(game, my_turn))

    if time_left() < 30: #Was 60 at 95pt submission 
        return game.get_active_moves()[0]
        
    #Recursive Call
    if my_turn:
        best_cost = -1000
        best_move = None
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


# In[12]:


def alphabeta(player, game, time_left, depth, alpha=float("-inf"), beta=float("inf"), my_turn=True):

    if depth == 0 or len(game.get_active_moves()) == 0:
        return (None, player.utility(game, my_turn))

    if time_left() < 30: #Was 60 at 95pt submission 
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


# In[31]:


def alphabeta2(player, game, time_left, depth, alpha=float("-inf"), beta=float("inf"), my_turn=True):

    if depth == 0 or len(game.get_active_moves()) == 0:
        return (None, player.utility(game, my_turn))

    if time_left() < 30: #Was 60 at 95pt submission 
        return game.get_active_moves()[0]
    
    if my_turn:
        best_score, best_move = float("-inf"), None
        for move in game.get_active_moves():
            _, eval = alphabeta2(player, game.forecast_move(move)[0], time_left, depth - 1, alpha, beta, my_turn = False)
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
            _, eval = alphabeta2(player, game.forecast_move(move)[0], time_left, depth - 1, alpha, beta, my_turn = True)
            if eval < best_score:
                best_score = eval
                best_move = move
            beta = min(eval, beta)
            if beta <= alpha:
                break
        return (best_move, best_score)
        
    raise NotImplementedError


# ## Level 1
# ### Minimax algorithm with Max Tree Depth = 4

# In[27]:


ig1 = InteractiveGame(CustomPlayer1(), show_legal_moves=True)


# ---
#   ## Level 2 
#   ### AlphaBeta pruning with Max Tree Depth = 6

# In[36]:


ig2 = InteractiveGame(CustomPlayer2(), show_legal_moves=True)


# ---
#   ### Level 3
#   ### Iterative Deepening + Alphabeta pruning + optimized evaluation function

# In[30]:


ig3 = InteractiveGame(CustomPlayer(), show_legal_moves=True)


# In[ ]:




