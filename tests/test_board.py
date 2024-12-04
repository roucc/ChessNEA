"""
Unit Test for Board class
"""

import unittest
from chess.board import *

class TestBoard(unittest.TestCase):
    def test_init(self):
        b=Board()
        for i,piece in enumerate(Board.startposition):
            self.assertEqual(b.board[i], piece)

    def test_algebraic_to_pos(self):
        b=Board()
        self.assertEqual(0,b.algebraic_to_pos("a8"))
        self.assertEqual(20,b.algebraic_to_pos("e6"))
        self.assertRaises(InvalidAlgebraicNotationError,b.algebraic_to_pos,"k8")

    def test_is_valid(self):
        b=Board()
        self.assertRaises(EmptySquareError,b.is_valid,"e6","e7")
        self.assertRaises(InvalidAlgebraicNotationError,b.is_valid,"k7","e4")
        self.assertRaises(InvalidAlgebraicNotationError,b.is_valid,"e4","k7")
    
    def test_check_piece_color(self):
        b=Board()
        self.assertEqual(1,b.check_piece_color("p"))
        self.assertEqual(0,b.check_piece_color("P"))
        self.assertEqual(None,b.check_piece_color("."))
    
    def test_move_pos(self):
        b=Board()
        self.assertEqual(7,b.move_pos(0,7,0))
        self.assertEqual(None,b.move_pos(0,-1,-1))
    
    def test_take_okay(self):
        b=Board()
        self.assertEqual(True,b.take_okay(10,b.WHITE))
        self.assertEqual(True,b.take_okay(51,b.BLACK))
        self.assertEqual(False,b.take_okay(35,b.WHITE))
        self.assertEqual(False,b.take_okay(None,b.WHITE))

    def test_pawn(self):
        b=Board()
        self.assertEqual([41,33],b.pawn(49,b.WHITE))
        self.assertEqual([19,27],b.pawn(11,b.BLACK))
        b=Board("RNBQKBNR"
                   "PPPPPP.P"
                   "...p..P."
                   "........"
                   "........"
                   "..p....."
                   "pp..pppp"
                   "rnbqkbnr")
        self.assertEqual([12,10],b.pawn(19,b.WHITE))
        self.assertEqual([34],b.pawn(42,b.WHITE))
        self.assertEqual(".",b.board[50])
        self.assertEqual([],b.pawn(11,b.BLACK))
        self.assertEqual([30],b.pawn(22,b.BLACK))

    def test_knight(self):
        b=Board()
        self.assertEqual([43,41],b.knight(58,b.turn))
        b=Board("........"
                "....N..."
                "........"
                "...n.N.."
                "........"
                "........"
                "........"
                "........")
        self.assertEqual([44, 42, 37, 21, 12, 10, 33, 17],b.knight(27,b.turn))
        b.turn=b.BLACK
        self.assertEqual([27, 22, 6, 18, 2],b.knight(12,b.turn))
    
    def test_linear_move(self):
        b=Board("........"
                "........"
                "........"
                "........"
                "...P...."
                "........"
                "........"
                "b.......")
        self.assertEqual([49,42,35],b.linear_move(56,1,-1,b.turn))

    def test_bishop(self):
        b=Board("........"
                "........"
                "........"
                "........"
                "...P...."
                "........"
                "...b...."
                "........")
        self.assertEqual([44, 37, 30, 23, 42, 33, 24, 60, 58],b.bishop(51,b.WHITE))
    
    def test_rook(self):
        b=Board("........"
                "........"
                "........"
                "........"
                "...P...."
                "........"
                "...r...."
                "........")
        self.assertEqual([52, 53, 54, 55, 43, 35, 50, 49, 48, 59],b.rook(51,b.WHITE))
    
    def test_queen(self):
        b=Board("........"
                "........"
                "........"
                "........"
                "...P...."
                "........"
                "...q...."
                "........")
        self.assertEqual([44, 37, 30, 23, 42, 33, 24, 60, 58,52, 53, 54, 55, 43, 35, 50, 49, 48, 59],b.queen(51,b.WHITE))
    
    def test_king(self):
        b=Board("........"
                "........"
                "........"
                "........"
                "........"
                "........"
                "...k...."
                "........")
        self.assertEqual([52, 59, 60, 50, 58, 43, 44, 42],b.king(51,b.WHITE))
        b=Board("........"
                "........"
                "........"
                "........"
                "....R..."
                "........"
                "...k...."
                "........")
        self.assertEqual([59, 50, 58, 43, 42],b.king(51,b.WHITE))
        self.assertRaises(InvalidMoveError,b.move,"d2","e2")
        b=Board("........"
                "........"
                "........"
                "........"
                "........"
                "........"
                "...K...."
                "........")
        b.turn=b.BLACK
        self.assertEqual([52, 59, 60, 50, 58, 43, 44, 42],b.king(51,b.BLACK))
        b=Board("........"
                "........"
                "........"
                "........"
                "....r..."
                "........"
                "...K...."
                "........")
        b.turn=b.BLACK
        self.assertEqual([59, 50, 58, 43, 42],b.king(51,b.BLACK))
        self.assertRaises(InvalidMoveError,b.move,"d2","e2")
        b=Board("........"
                "........"
                "...Kp..."
                "........"
                "..p.r..."
                "........"
                "........"
                "........")
        b.turn=b.BLACK
        self.assertRaises(InvalidMoveError,b.move,"d6","e6")
        self.assertRaises(InvalidMoveError,b.move,"d6","d5")
        b=Board("....K..."
                "...p...."
                "........"
                "........"
                "........"
                "........"
                "........"
                "...q....")
        b.turn=b.BLACK
        self.assertRaises(InvalidMoveError,b.move,"e8","d7")
        
    
    def test_piece_moves(self):
        b=Board(".......K"
                "........"
                "........"
                "........"
                "...P...."
                "........"
                "........"
                "b......k")
        self.assertEqual([49,42,35],b.piece_moves("a1"))
        self.assertEqual([43],b.piece_moves("d4"))
        self.assertRaises(EmptySquareError,b.piece_moves,"b2")
    
    def test_all_valid_moves(self):
        b=Board(".......K"
                "........"
                "........"
                "........"
                "...P...."
                "........"
                "........"
                "b......k")
        self.assertEqual([49, 42, 35, 62, 55, 54],b.all_valid_moves(b.WHITE))
        self.assertEqual([15, 6, 14, 43],b.all_valid_moves(b.BLACK))
    
    def test_total_moves(self):
        b=Board()
        self.assertEqual(20,b.total_moves())

    def test_move(self):
        b=Board()
        b.move("a2","a4")
        self.assertEqual(list("RNBQKBNR"
                   "PPPPPPPP"
                   "........"
                   "........"
                   "p......."
                   "........"
                   ".ppppppp"
                   "rnbqkbnr"), b.board)
        self.assertRaises(InvalidMoveError,b.move,"a2","a4")
        self.assertRaises(InvalidMoveError,b.move,"h2","h5")
    
    def test_is_check(self):
        b=Board("....K..."
                "........"
                "........"
                "K...q..."
                "........"
                "........"
                "..Q....."
                "....k...")
        self.assertEqual(True,b.is_check(24))
        self.assertEqual(False,b.is_check(60))
        self.assertEqual(True,b.is_check(12,b.BLACK))
        self.assertEqual(False,b.is_check(11,b.BLACK))
        self.assertEqual(True,b.is_check(58,b.WHITE))
        self.assertEqual(True,b.is_check(4))
        self.assertRaises(EmptySquareError,b.is_check,56)
        b=Board("RNBQKBNR"
                "PPPPPPPP"
                "........"
                "....R..."
                "........"
                "........"
                "pppp.ppp"
                "rnbqkbnr")
        self.assertEqual(True,b.is_check(60))
        self.assertEqual(False,b.is_checkmate(60))
        b=Board()
        b.move("b1","c3")
        self.assertEqual(False,b.is_check(4))
        b.move("b8","c6")
        self.assertEqual(False,b.is_check(60))
        b.move("c3","b5")
        self.assertEqual(False,b.is_check(4))
        b.move("c6","b4")
        self.assertEqual(False,b.is_check(60))
        self.assertEqual([27, 20, 4, 16, 0],b.knight(10,b.turn))
        b.move("b5","c7")
        self.assertEqual(True,b.is_check(4))
        #b.move("b4","c2")
        #self.assertEqual(True,b.is_check(60))

    
    def test_find_piece_index(self):
        b=Board()
        self.assertEqual(60,b.find_piece_index("e1"))

    def test_find_piece(self):
        b=Board()
        self.assertEqual([60],b.find_piece("k"))
        self.assertEqual([8,9,10,11,12,13,14,15],b.find_piece("P"))
    
    def test_is_stalemate(self):
        b=Board("........"
                "...R...."
                ".R......"
                "....k..."
                "......R."
                ".....R.."
                "........"
                "........")
        self.assertEqual(True,b.is_stalemate(28))
        self.assertEqual(True,b.game_over())
        b=Board()
        b.turn=b.BLACK
        self.assertEqual(False,b.is_stalemate(4))
    
    def test_is_checkmate(self):
        b=Board("....r..K"
                "....r..."
                "........"
                "........"
                "........"
                "........"
                "........"
                "........")
        b.turn=b.BLACK
        self.assertEqual(True,b.is_checkmate(7))
        b=Board("RNB.KBNR"
                "PPPP.PPP"
                "....P..."
                "........"
                "......pQ"
                ".....p.."
                "ppppp..p"
                "rnbqkbnr")
        b.turn=b.WHITE
        self.assertEqual(0,len(b.all_valid_moves(b.turn,True)))
        b.turn=b.WHITE # checks if current side is checkmate
        self.assertEqual(True,b.is_checkmate(60))
        b=Board()
        self.assertEqual(False,b.is_checkmate(4))
        b=Board("....R..k"
                "....R..."
                "........"
                "........"
                "........"
                "........"
                "........"
                "........")
        self.assertEqual(True,b.is_checkmate(7))
        self.assertEqual(True,b.game_over())
        
    
    def test_is_75_move_rule(self):
        b=Board()
        b.move_count=149
        self.assertEqual(False,b.is_75_move_rule())
        b.move("a2","a4")
        self.assertEqual(True,b.is_75_move_rule())
    
    def test_is_threefold_repetition(self):
        b=Board("k......K"
                "........"
                "........"
                "........"
                "........"
                "........"
                "........"
                "........")
        b.move("a8","a7")
        self.assertEqual(False,b.is_threefold_repetition())
        b.turn=b.WHITE
        b.move("a7","a8")
        self.assertEqual(False,b.is_threefold_repetition())
        b.turn=b.WHITE
        b.move("a8","a7")
        self.assertEqual(False,b.is_threefold_repetition())
        b.turn=b.WHITE
        b.move("a7","a8")
        self.assertEqual(True,b.is_threefold_repetition())
    
    def test_enpassant(self):
        b=Board()
        b.move("a2","a3")
        b.move("e7","e5")
        b.move("a3","a4")
        b.move("e5","e4")
        b.piece_moves("d2")
        b.move("d2","d4")
        b.piece_moves("e4")
        self.assertEqual([36, 34, 43],b.enpassant_check)
        self.assertEqual([44,43],b.piece_moves("e4"))
        self.assertEqual([44,43],b.pawn(36,b.BLACK))
        self.assertEqual(b.board[35],"p")
        b.move("e4","d3")
        b=Board("RNB.KBNR"
                ".P......"
                "........"
                "........"
                "........"
                "........"
                "........"
                "rnbqkbnr")
        b.move("a1","a7")
        self.assertRaises(InvalidMoveError,b.move,"b7","a6")
    
    def test_castle(self):
        b=Board("R...K..R"
                "........"
                "........"
                "........"
                "........"
                "........"
                "p......."
                "r...kq..")
        b.move("e1","a1")
        self.assertEqual(False,b.is_check(58,b.WHITE))
        self.assertEqual(b.board[59],"r")
        self.assertEqual(b.board[58],"k")
        self.assertRaises(InvalidMoveError,b.move,"e8","h8")
        b.turn=b.WHITE
        b.move("f1","e2")
        self.assertEqual(True,b.is_check(4))
        self.assertRaises(InvalidMoveError,b.move,"e8","h8")
        b.turn=b.WHITE
        b.move("e2","d2")
        b.move("e8","h8")

    def test_winlossdraw(self):
        b=Board()
        self.assertEqual("",b.winlossdraw())
        b=Board("......k."
                "........"
                "........"
                "........"
                "...q...."
                "........"
                "........"
                "...K....")
        b.turn=b.BLACK
        self.assertEqual("black in check",b.winlossdraw()) # you are 'checking' the opposition
        b=Board("........"
                "...R...."
                ".R......"
                "....k..."
                "......R."
                ".....R.."
                "........"
                "K.......")
        self.assertEqual("draw",b.winlossdraw())
        b=Board("RNB.KBNR"
                "PPPP.PPP"
                "....P..."
                "........"
                "......pQ"
                ".....p.."
                "ppppp..p"
                "rnbqkbnr")
        self.assertEqual("black win",b.winlossdraw())
        b=Board("..RK.RBB"
                "P.PP.PPP"
                "..P....."
                "...N.P.."
                "........"
                "........"
                ".Q..pppp"
                "nk.Nnrbb")
        self.assertEqual("black win",b.winlossdraw())
        b=Board("RNBQKBNR"
                ".PPP.qPP"
                "........"
                "P...P..."
                "..b.p..."
                "........"
                "pppp.ppp"
                "rnb.k.nr")
        b.turn=b.BLACK
        self.assertEqual("white win",b.winlossdraw())
        b=Board("RNBQKBNR"
                ".PPP.PPP"
                "P......."
                "....P..q"
                "..b.p..."
                "........"
                "pppp.ppp"
                "rnb.k.nr")
        b.turn=b.BLACK
        b.move("a6","a5")
        b.move("h5","f7")
        self.assertEqual("white win",b.winlossdraw())

    def test_is_move_out_of_check(self):
        b=Board("...K...."
                "........"
                "........"
                "...QQ..."
                "........"
                "........"
                "...r...."
                "...k....")
        self.assertRaises(InvalidMoveError,b.move,"d1","e1")
        self.assertRaises(InvalidMoveError,b.move,"d2","e2")
    
    def test_valid_move_src_dst(self):
        b=Board("K......."
                "........"
                "........"
                "........"
                "....p..."
                "........"
                "........"
                "k.......")
        self.assertEqual([('e4', 'e5'),('a1', 'b1'), ('a1', 'a2'), ('a1', 'b2')],b.valid_move_src_dst(b.turn))
        self.assertEqual([('a8', 'b8'), ('a8', 'a7'), ('a8', 'b7')],b.valid_move_src_dst(1-b.turn))
    
    def test_fen_to_board(self):
        b=Board()
        self.assertEqual("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w",b.board_to_fen())
        b=Board("RNB.KBNR"
                "PPPP.PPP"
                "....P..."
                "........"
                "......pQ"
                ".....p.."
                "ppppp..p"
                "rnbqkbnr")
        b.turn=b.BLACK
        self.assertEqual("rnb1kbnr/pppp1ppp/4p3/8/6Pq/5P2/PPPPP2P/RNBQKBNR b",b.board_to_fen())
    
if __name__ == '__main__':
    unittest.main()