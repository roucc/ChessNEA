from stockfish import Stockfish
from pprint import pprint

from chess.board import Board
from chess.minimax import Minimax,MinimaxAI
from chess.alphabetapruning import AlphabetaPruning,AlphabetaPruningAI

stockfish_path=r"C:\Users\dougal\Documents\stockfish\stockfish-windows-x86-64.exe"
player=AlphabetaPruning


def play_game(my_depth,stockfish_elo,stats_dict):
    stockfish=Stockfish(stockfish_path)
    b=Board(chess960=False)

    stockfish.set_elo_rating(stockfish_elo)

    while True:
        status=b.winlossdraw()
        if status=="black win":
            stats_dict["stockfish win"]+=1
            break
        if status=="white win":
            stats_dict["me win"]+=1
            break
        if status=="draw":
            stats_dict["draw"]+=1
            break
        if b.turn==b.BLACK:
            move=stockfish.get_best_move()
            #print(f"stockfish best move {move}")
            # remove promoted piece from end
            if len(move) == 5:
                move = move[:4]
            assert len(move)==4, f"unkown move format {move}"
            # correcting algebraic notation for castling which is optimised for 960
            if move=="e1g1":
                move="e1h1"
            elif move=="e1c1":
                move="e1a1"
            elif move=="e8g8":
                move="e8h8"
            elif move=="e8c8":
                move="e8a8"
            src,dst=move[:2],move[2:]
        else:
            src,dst=player(b,my_depth).best_move()
            #print(f"our best move {src} {dst}")

        #print(f"we move {src} {dst}")
        b.move(src,dst)
        # correcting algebraic notation for castling which is optimised for 960
        move=src+dst
        if move=="e1h1":
            move="e1g1"
        elif move=="e1a1":
            move="e1c1"
        elif move=="e8h8":
            move="e8g8"
        elif move=="e8a8":
            move="e8c8"
        assert stockfish.is_move_correct(move), f"stockfish think we aint valid {move}"
        #print(f"stockfish moves {move}")
        stockfish.make_moves_from_current_position([move])
        
        b.display()
        # print(stockfish.get_board_visual())
        print(b.turn)
        print("---------------------------------------------------------------------")

def main():
    final_stats={}
    # for depth in [1,2,3]:
    for depth in [3]:
        # for level in [500,1000,1500,2000,2500]:
        for level in [500]:
            stats_dict={"stockfish win": 0, "me win": 0, "draw": 0, "errors": 0}
            while stats_dict["stockfish win"]+stats_dict["me win"]+stats_dict["draw"]<10:
            # while stats_dict["me win"]<1:
                try:
                    play_game(depth,level,stats_dict)
                except Exception as e:
                    print(f"Game failed with {repr(e)}")
                    stats_dict["errors"]+= 1
                pprint(stats_dict)
                print("======================================================================")
            final_stats[depth,level]=stats_dict
            stats_dict={"stockfish win": 0, "me win": 0, "draw": 0, "errors": 0}
    pprint(final_stats)


if __name__ == "__main__":
    main()
