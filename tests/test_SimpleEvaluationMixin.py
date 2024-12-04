"""
SimpleEvaluationMixin unit test
"""

from chess.SimpleEvaluationMixin import *
from chess import board
import unittest

class test_SimpleEvaluationMixin(unittest.TestCase):
    def test_init(self):
        pass

    def test_evaluate(self):
        e=SimpleEvaluationMixin()
        b=board.Board("k......K"
                "........"
                "........"
                "........"
                "........"
                "........"
                "........"
                "........")
        self.assertEqual(0,e.evaluate(b))
        b=board.Board("....r..K"
                "....r..."
                "........"
                "........"
                "........"
                "........"
                "........"
                "k.......")
        b.turn=b.BLACK
        self.assertEqual(1000,e.evaluate(b))
        b=board.Board(".......K"
                "........"
                "........"
                "........"
                "........"
                "........"
                "..R....."
                "k.R.....")
        self.assertEqual(-1000,e.evaluate(b))
        b=board.Board("........"
                "...R...."
                ".R......"
                "....k..."
                "......R."
                ".....R.."
                "........"
                "K.......")
        self.assertEqual(0,e.evaluate(b))
        b=board.Board("RNBQKBNR"
                "PPPPPPPP"
                "........"
                "....R..."
                "........"
                "........"
                "pppp.ppp"
                "rnbqkbnr")
        self.assertEqual(-6,e.evaluate(b))

if __name__ == '__main__':
    unittest.main()