"""
Minimax unit test
"""

from chess.minimax import *
from chess import board
import unittest

class test_minimax(unittest.TestCase):
    def test_init(self):
        pass

    def test_best_move_white(self):
        b=board.Board("k......K"
                "........"
                "........"
                "........"
                ".p..p..."
                "........"
                "...P...."
                "..p.....")
        # m=Minimax(b,1)
        m=MinimaxAI(b,1)

        self.assertEqual(("c1","d2"),m.best_move())
        b=board.Board("k......K"
                "........"
                "........"
                "...P...."
                "....n..."
                "P......."
                ".p......"
                "........")
        #move differs depending on evaluation
        # m=Minimax(b,2)
        # self.assertEqual(('e4', 'g5'),m.best_move())

        m=MinimaxAI(b,2)
        # depth 2 works, sees its about to be taken
        self.assertEqual(('e4', 'f6'),m.best_move())
        b=board.Board(".......K"
                "........"
                "....r..."
                "...r...."
                "........"
                "........"
                "........"
                "...k....")
        # m=Minimax(b,3)
        m=MinimaxAI(b,3)
        #mate in 2
        self.assertEqual(("e6","e7"),m.best_move())
    
    def test_best_move_black(self):
        b=board.Board("k......K"
                "........"
                "........"
                "........"
                ".p..p..."
                "........"
                "...P...."
                "..p.....")
        b.turn=b.BLACK

        #move differs depending on evaluation
        # m=Minimax(b,1)
        # self.assertEqual(('d2', 'c1'),m.best_move())

        m=MinimaxAI(b,1)
        self.assertEqual(('d2', 'd1'),m.best_move())

        b=board.Board("k......K"
                "........"
                ".P......"
                "p......."
                "....N..."
                "...p...."
                "........"
                "........")
        b.turn=b.BLACK
        #move differs depending on evaluation
        # m=Minimax(b,2)
        # self.assertEqual(('e4', 'c3'),m.best_move())

        m=MinimaxAI(b,2)
        # depth 2 works, sees its about to be taken
        self.assertEqual(('b6', 'a5'),m.best_move())
        b=board.Board(".......K"
                "........"
                "........"
                "........"
                "........"
                "....RR.."
                "........"
                "k.......")
        b.turn=b.BLACK
        # m=Minimax(b,3)
        m=MinimaxAI(b,3)

        #mate in 2
        self.assertEqual(('e3', 'e2'),m.best_move())
        

if __name__ == '__main__':
    unittest.main()