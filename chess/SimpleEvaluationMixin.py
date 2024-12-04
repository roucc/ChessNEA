class SimpleEvaluationMixin:
    """
    Simple evaluation based on Claude Shannon's evaluation
    """
    def evaluate(self,b):
        """
        returns number representing favour of board
        """
        winlossdraw=b.winlossdraw()
        if winlossdraw=="white win":
            return 1000
        elif winlossdraw=="black win":
            return -1000
        elif winlossdraw=="draw":
            return 0
        #find number of each pieces
        piecedict={}
        for i in range(64):
            piece=b.board[i]
            piecedict.setdefault(piece,0)
            piecedict[piece]+=1
        #return evaluation
        eval=200*(piecedict.get("k",0)-piecedict.get("K",0))+9*(piecedict.get("q",0)-piecedict.get("Q",0))+5*(piecedict.get("r",0)-piecedict.get("R",0))+3*(piecedict.get("b",0)-piecedict.get("b",0) + piecedict.get("n",0)-piecedict.get("N",0))+(piecedict.get("p",0)-piecedict.get("P",0))
        return eval