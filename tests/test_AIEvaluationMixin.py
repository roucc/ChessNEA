"""
SimpleEvaluationMixin unit test
"""

from chess.AIEvaluationMixin import *
from chess import board
import unittest

class test_AIEvaluationMixin(unittest.TestCase):
    def test_init(self):
        pass

    def test_evaluate(self):
        e=AIEvaluationMixin("AI/chess5M.keras")
        b=board.Board("RNBQKBNR"
                   "PPPPPPPP"
                   "........"
                   "........"
                   "........"
                   "........"
                   "pppppppp"
                   "rnbqkbnr")
        self.assertTrue(-0.5 < e.evaluate(b) < 0.5)

        b=board.Board("..BQKBNR"
                   "..PPPPPP"
                   "........"
                   "........"
                   "........"
                   "........"
                   "pppppppp"
                   "rnbqkbnr")
        self.assertAlmostEqual(6.8,e.evaluate(b),delta=1)

        b=board.Board(".R..R.K."
                    ".....PP."
                    "P..B.NQP"
                    ".PPp...."
                    "....p..."
                    "..n..q.."
                    "pp...ppp"
                    ".r..r.k.")
        self.assertAlmostEqual(-3.5,e.evaluate(b),delta=1)
        
        b=board.Board("R.BQ.RK."
                    "PPP...PP"
                    "..N..N.."
                    ".b.P...."
                    "...p...."
                    "..nb.n.."
                    "ppp..ppp"
                    "r..q.rk.")
        self.assertAlmostEqual(4.3,e.evaluate(b),delta=1)
        
        b=board.Board("........"
                    "......K."
                    ".....P.."
                    ".....pP."
                    "........"
                    "...R...."
                    ".r......"
                    ".k......")
        self.assertAlmostEqual(-6.9,e.evaluate(b),delta=1)
        
        b=board.Board("........"
                    "........"
                    "...K...."
                    "...P...."
                    "...p.P.."
                    ".....p.."
                    ".....k.."
                    "........")
        self.assertAlmostEqual(5.4,e.evaluate(b),delta=6)

        b=board.Board(".R..QRK."
                    "PP....pp"
                    "..B..n.."
                    ".p.p...."
                    "....P..."
                    "..Nb.N.."
                    "pp...pp."
                    "r..q.rk.")
        self.assertAlmostEqual(3.2,e.evaluate(b),delta=1)

        b=board.Board("r..qk..r"
                    "pp..bp.."
                    ".n..pnp."
                    ".....p.."
                    ".PpP.P.."
                    "..N.BN.."
                    "P..Q..PP"
                    "R..R..K.")
        self.assertAlmostEqual(0,e.evaluate(b),delta=1)

        b=board.Board("R...k..."
                    ".P..pp.."
                    "...p...."
                    "..r....."
                    ".....P.."
                    "...P...."
                    "p....pPP"
                    ".....K..")
        print(e.evaluate(b))
        self.assertAlmostEqual(0,e.evaluate(b),delta=1)

        b=board.Board("....K..."
                    ".P......"
                    "....p..."
                    "....p.p."
                    "P......."
                    "..r....."
                    "..k..pp."
                    "........")
        print(e.evaluate(b))
        self.assertAlmostEqual(13.4,e.evaluate(b),delta=1)

        b=board.Board("....k..."
                    "....P..."
                    "p......P"
                    "..K....."
                    "........"
                    ".r......"
                    "......pp"
                    "........")
        print(e.evaluate(b))
        self.assertAlmostEqual(14,e.evaluate(b),delta=1)


if __name__ == '__main__':
    unittest.main()