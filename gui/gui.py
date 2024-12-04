import sys
import pygame
from chess import UI
from chess.minimax import Minimax,MinimaxAI
from chess.alphabetapruning import AlphabetaPruning,AlphabetaPruningAI
import time

class GUI:
    screen_width = 800
    screen_height = 600
    boardconstant = 0.85
    board_x=(screen_width-screen_height*boardconstant)/2
    board_y=screen_height*((1-boardconstant)/2)
    board_side=screen_height*boardconstant

    piecedict={
        "p":"gui/pawnw.png",
        "b":"gui/bishopw.png",
        "P":"gui/pawnb.png",
        "B":"gui/bishopb.png",
        "n":"gui/knightw.png",
        "N":"gui/knightb.png",
        "r":"gui/rookw.png",
        "R":"gui/rookb.png",
        "k":"gui/kingw.png",
        "K":"gui/kingb.png",
        "q":"gui/queenw.png",
        "Q":"gui/queenb.png"
    }

    pieceimages={}
    for key,file in piecedict.items():
        pieceimages[key]=pygame.image.load(file)
    
    def __init__(self):
        pygame.init()
        self.board=UI.Board(chess960=False)
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        pygame.display.set_caption("DOUGAL CHESS GUI")
        self.image_list=[]
        self.drag_pos=None
        self.square_list=[]
        self.valid_moves=[]
        self.font= pygame.font.SysFont("arialblack", 30)
        self.status=""
        self.players=[AlphabetaPruningAI,None] # [black,white]
        self.depth=2
        self.drag=False
        self.drag_image=None
        self.offset_x,self.offset_y=0,0
        self.run=True
    
    def main(self):
        """
        main loop, select menu then draws board and status then does player and non-player moves
        """
        self.players[1]=self.choose_player("White")
        self.players[0]=self.choose_player("Black")
        if self.players[1] is not None or self.players[0] is not None:
            self.depth=self.menu("Depth?",[
                ["Depth 1",1],
                ["Depth 2",2],
                ["Depth 3",3],
            ])
        chess960=self.menu("Chess 960?",[
            ["Yes",True],
            ["No",False]
        ])
        self.board=UI.Board(chess960=chess960)
        self.draw_board()
        pygame.display.flip()
        while self.run:
            player=self.players[self.board.turn]
            is_human = player is None
            self.src,self.dst = None,None
            self.event_handler(is_human)
            if not self.board.game_over():
                self.make_move(player, is_human)
            self.draw_board()
            if self.drag:
                self.screen.blit(self.drag_image[1],self.drag_image[0])
            self.draw_text(self.status,0.95,(255,0,0))
            pygame.display.flip()
            time.sleep(1/90) # runs at limited fps
        pygame.quit()
        sys.exit()

    def choose_player(self,colour):
        """
        displays menu options for the player
        """
        return self.menu(f"Choose {colour} Player",[
            ["Human",None],
            ["Computer no AI", AlphabetaPruning],
            ["Computer with AI", AlphabetaPruningAI]
        ])
    
    def menu(self,heading,options):
        """
        diplays menu for game options
        """
        rects=[]
        self.screen.fill((128,128,128))
        self.draw_text(heading,0.1,(0,0,0))
        i=0
        for option,value in options:
            i+=0.1
            text_rect=self.draw_text(option,0.2+i,(255,0,0))
            rects.append((text_rect,value))
        pygame.display.flip()
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run=False
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    for rect,value in rects:
                        if rect.collidepoint(event.pos):
                            return value

    def make_move(self, player, is_human):
        """
        makes either player move or engine move
        """
        if not is_human:
            m=player(self.board,self.depth)
            self.src,self.dst=m.best_move()
        if self.src is not None:
            try:
                self.board.move(self.src,self.dst)
                self.status=self.board.winlossdraw()
                self.board.display()
            except UI.ChessError as e:
                print(e)
            self.src,self.dst=None,None

    def event_handler(self, is_human):
        """
        handles mouse events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run=False
            elif is_human and event.type==pygame.MOUSEBUTTONDOWN:
                self.event_buttondown(event)
            elif is_human and event.type == pygame.MOUSEBUTTONUP:
                self.event_buttonup(event)
            elif is_human and event.type==pygame.MOUSEMOTION:
                self.event_mousemotion(event)

    def event_mousemotion(self, event):
        """
        handles mouse motion
        """
        if self.drag:
            self.drag_image[0].x=event.pos[0]-self.offset_x
            self.drag_image[0].y=event.pos[1]-self.offset_y

    def event_buttonup(self, event):
        """
        handles mouse button up
        """
        self.drag=False
        self.drag_image=None
        for rect,pos in self.square_list:
            if rect.collidepoint(event.pos) and self.drag_pos is not None:
                src_pos=self.drag_pos
                dst_pos=pos
                self.src=self.board.notation[src_pos]
                self.dst=self.board.notation[dst_pos]
        self.valid_moves=[]
        self.drag_pos=None

    def event_buttondown(self, event):
        """
        handles mouse button down
        """
        for rect,image,pos in self.image_list:
            if rect.collidepoint(event.pos):
                self.drag=True
                self.drag_image=(rect,image)
                self.offset_x=event.pos[0]-rect.x
                self.offset_y=event.pos[1]-rect.y
                self.drag_pos=pos
                if self.board.check_piece_color(self.board.board[pos])==self.board.turn:
                    self.valid_moves=self.board.piece_moves(self.board.notation[pos])
                else:
                    self.drag=False
                    self.drag_pos=None

    def draw_text(self,text,height_fraction,colour):
        """
        draws text to the screen at specificied height
        """
        text_surface = self.font.render(text, True, colour)  # Text, antialiasing, color (black)
        text_rect = text_surface.get_rect()
        # Set the position (x, y) of the text rectangle
        text_rect.center = (self.screen_width // 2, self.screen_height*height_fraction)  # Center the text
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_board(self):
        """
        draws the board onto the screen, flips screen if human black player
        """
        flip=False
        if self.players[self.board.turn] is None and self.board.turn==self.board.BLACK:
            flip=True
        elif self.players[0] is None and self.players[1] is not None:
            flip=True
        self.image_list=[]
        self.square_list=[]
        self.screen.fill((128,128,128))
        gridconstant=self.board_side/8
        black=True
        for x in range(8):
            black=not black
            for y in range(8):
                if flip:
                    x=7-x
                    y=7-y
                color=(92,64,51)
                if not black:
                    color=(255,255,255)
                rect=pygame.Rect(self.board_x+x*gridconstant,self.board_y+y*gridconstant,gridconstant,gridconstant)
                pygame.draw.rect(self.screen,color,rect)
                if flip:
                    pos=(7-x)+(7-y)*8
                else:
                    pos=x+y*8
                self.square_list.append((rect,pos))
                if pos in self.valid_moves:
                    highlight=pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
                    highlight.fill((100,100,0,200))
                    self.screen.blit(highlight,rect)
                i=self.board.board[pos]
                if pos!=self.drag_pos:
                    if i!=".":
                        self.screen.blit(self.pieceimages[i],(self.board_x+x*gridconstant,self.board_y+y*gridconstant))
                        self.image_list.append((rect,self.pieceimages[i],pos))
                if not flip:
                    black=not black

if __name__=="__main__":
    gui=GUI()
    gui.main()