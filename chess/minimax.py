from chess.SimpleEvaluationMixin import SimpleEvaluationMixin
from chess.AIEvaluationMixin import AIEvaluationMixin

class MinimaxBase():
    """
    Base class for minimax
    """
    def __init__(self,board,depth):
        self.board=board
        self.depth=depth
    
    def best_move(self):
        """
        returns best move at set depth
        """
        return self.best_move_for_level(self.board,self.depth)[1]

    def best_move_for_level(self,board,depth):
        """
        returns best move and evaluation, for current level and below until depth 0
        """
        movelist=board.valid_move_src_dst(board.turn)
        bestmovelist=[]
        for src,dst in movelist:
            copyboard=board.copy()
            copyboard.move(src,dst)
            if depth<=1:
                eval=self.evaluate(copyboard)
            else:
                eval,move=self.best_move_for_level(copyboard,depth-1)
            bestmovelist.append((eval,(src,dst)))
        # reverse if turn is white, sorts lowest first by default, lowest is best evaluation for black
        # maximises for white, minimises for black
        bestmovelist.sort(reverse=board.turn==board.WHITE)
        return bestmovelist[0]

class Minimax(MinimaxBase,SimpleEvaluationMixin):
    def __init__(self,board,depth):
        MinimaxBase.__init__(self,board,depth)
        SimpleEvaluationMixin.__init__(self)

class MinimaxAI(MinimaxBase,AIEvaluationMixin):
    def __init__(self,board,depth):
        MinimaxBase.__init__(self,board,depth)
        AIEvaluationMixin.__init__(self,"AI/chess5M.keras")
