import cProfile
from chess import board
from chess.alphabetapruning import *

b=board.Board()
a=AlphabetaPruning(b,2)
cProfile.run("a.best_move()")