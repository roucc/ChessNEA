from chess.SimpleEvaluationMixin import SimpleEvaluationMixin
from chess.AIEvaluationMixin import AIEvaluationMixin
from multiprocessing.pool import ThreadPool
import time

class AlphabetaPruningBase():
    """
    Base class for AlphabetaPruning
    """
    def __init__(self,board,depth):
        self.board=board
        self.depth=depth
        self.count=0
    
    def best_move(self):
        """
        returns best move at set depth
        """
        self.count=0
        start=time.time()
        eval=self.best_move_for_level(self.board,self.depth,-1000,1000)
        dt=time.time()-start
        print(f"Evaluations done: {self.count}, Best evaluation: {eval[0]}, Time taken: {round(dt,4)}")
        return eval[1]

    def best_move_for_level(self,board,depth,alpha,beta):
        """
        returns best move and evaluation, for current level and below until depth 0
        uses alpha-beta pruning to reduce searching, pseudo code wikipedia
        """
        if depth==0:
            self.count+=1
            return self.evaluate(board),None
        movelist=board.valid_move_src_dst(board.turn)
        movelist=self.sort_moves(board,movelist)
        bestmovelist=[]

        # multi threading experiment
        if False:
        # if depth==self.depth:
            with ThreadPool() as pool:
                def task(move):
                    """
                    uses a new thread for each sub tree of top level minimax tree
                    """
                    src,dst=move
                    copyboard=board.copy()
                    copyboard.move(src,dst)
                    eval,move=self.best_move_for_level(copyboard,depth-1,alpha,beta)
                    return eval,(src,dst)
                bestmovelist=list(pool.imap(task,movelist))
        else:         
            if board.turn==board.WHITE: #maximising player
                eval=-1000
                for src,dst in movelist:
                    copyboard=board.copy()
                    copyboard.move(src,dst)
                    eval,move=self.best_move_for_level(copyboard,depth-1,alpha,beta)
                    bestmovelist.append((eval,(src,dst)))
                    if eval>beta:
                        break #beta cut off
                    alpha=max(alpha,eval)
                    
            else: #minimising player
                eval=1000
                for src,dst in movelist:
                    copyboard=board.copy()
                    copyboard.move(src,dst)
                    eval,move=self.best_move_for_level(copyboard,depth-1,alpha,beta)
                    bestmovelist.append((eval,(src,dst)))
                    if eval<alpha:
                        break #alpha cut off
                    beta=min(beta,eval)
                
        bestmovelist.sort(reverse=board.turn==board.WHITE)
        if len(bestmovelist)==0:
            self.count+=1
            return self.evaluate(board),None
        return bestmovelist[0]
    
    def sort_moves(self,board,moves):
        """
        sort moves so takes are first to make alpha-beta pruning more efficient
        """
        notake=[]
        take=[]
        for src,dst in moves:
            if board.board[board.algebraic_to_pos(dst)]!=".":
                take.append((src,dst))
            else:
                notake.append((src,dst))
        return take+notake

class AlphabetaPruning(AlphabetaPruningBase,SimpleEvaluationMixin):
    def __init__(self,board,depth):
        AlphabetaPruningBase.__init__(self,board,depth)
        SimpleEvaluationMixin.__init__(self)

class AlphabetaPruningAI(AlphabetaPruningBase,AIEvaluationMixin):
    def __init__(self,board,depth):
        AlphabetaPruningBase.__init__(self,board,depth)
        AIEvaluationMixin.__init__(self,"AI/chess5M.keras")