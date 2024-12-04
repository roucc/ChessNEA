"""
Implementation of UI
"""

from chess.board import *

class UI:
    """
    This class defines ways of displaying the board to the user
    """
    def __init__(self):
        self.board=Board()
    
    def player_input(self,input=input):
        src=input("Original position of piece:")
        dst=input("Destination of piece:")
        return src,dst

    def simple_display(self):
        self.board.display()

    def main_loop(self):
        """
        Runs the game loop
        """
        while not self.board.game_over():
            self.simple_display()
            okay=False
            while not okay:
                src,dst=self.player_input()
                try:
                    self.board.move(src,dst)
                    okay=True
                except ChessError as e:
                    print(e.__class__.__name__,e)
        self.simple_display()

if __name__=="__main__":
    a=UI()
    a.main_loop()