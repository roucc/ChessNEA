"""
This is the implemenation of the Chess Board
"""

import random

class ChessError(ValueError):
    """
    This is a superclass for all chess errors, differentiates them from ValueErrors
    """

class EmptySquareError(ChessError):
    pass

class InvalidAlgebraicNotationError(ChessError):
    pass

class OutsideBoardError(ChessError):
    pass

class InvalidMoveError(ChessError):
    pass

class InvalidColorError(ChessError):
    pass

class Board:
    """
    This class represents a chess board and knows how to calculate valid moves
    """
    notation=["a8","b8","c8","d8","e8","f8","g8","h8",
              "a7","b7","c7","d7","e7","f7","g7","h7",
              "a6","b6","c6","d6","e6","f6","g6","h6",
              "a5","b5","c5","d5","e5","f5","g5","h5",
              "a4","b4","c4","d4","e4","f4","g4","h4",
              "a3","b3","c3","d3","e3","f3","g3","h3",
              "a2","b2","c2","d2","e2","f2","g2","h2",
              "a1","b1","c1","d1","e1","f1","g1","h1",]
    reverse_notation = {}
    for i, square in enumerate(notation):
        reverse_notation[square]=i
    
    #creates "slots" for class variables decreasing memory usage and increasing speed
    #if changed, change copy method to include change
    __slots__="board","turn","move_count","states","enpassant_check","unmoved","valid_moves_cache"
    
    startposition=("RNBQKBNR"
                   "PPPPPPPP"
                   "........"
                   "........"
                   "........"
                   "........"
                   "pppppppp"
                   "rnbqkbnr")

    valid_pieces={"p","P","n","N","b","B","r","R","q","Q","k","K","."}
    BLACK=0
    WHITE=1

    def __init__(self, startboard=None,turn=WHITE,chess960=False):
        if startboard is None:
            startboard=Board.startposition
            if chess960:
                startboard=Board.randomize960()
        self.board=[" "]*64
        assert len(startboard) == 64
        for i,piece in enumerate(startboard):
            assert piece in self.valid_pieces
            self.board[i]=piece
        self.turn=turn
        self.move_count=0
        self.states=[]
        self.enpassant_check=[]
        self.unmoved={0,7,4,56,63,60} # unmoved castles and kings positions
        if chess960:
            self.unmoved={self.find_piece("R")[0],self.find_piece("R")[1],self.find_piece("K")[0],self.find_piece("r")[0],self.find_piece("r")[1],self.find_piece("k")[0]}
        self.clear_caches()
    
    @staticmethod
    def randomize960():
        """
        randomize for backrows for chess 960
        """
        startposition=Board.startposition
        rows=[startposition[i:i+8] for i in range(0,len(startposition),8)]
        randomizedposition=[]
        randomrow=""
        for row_i,row in enumerate(rows):
            if row_i == 0:
                row="".join(random.sample(row,len(row)))
                randomrow=row
            if row_i==7:
                row=randomrow.lower()
            randomizedposition.append(row)
        startposition=("".join(randomizedposition))
        if Board.valid960(startposition):
            return startposition
        else:
            return Board.randomize960()

    @staticmethod  
    def valid960(startposition):
        """
        validates if random boards obey chess 960 rules
        """
        top_row=[startposition[i:i+8] for i in range(0,len(startposition),8)][0]
        bishops_pos=[i for i,piece in enumerate(top_row) if piece=="B"]
        if len(bishops_pos)==2 and bishops_pos[0]%2==bishops_pos[1]%2:
            return False
        king_pos=top_row.index("K")
        rooks_pos=[i for i,piece in enumerate(top_row) if piece=="R"]
        if len(rooks_pos)==2 and not(rooks_pos[0]<king_pos<rooks_pos[1]):
            return False
        return True
    
    def clear_caches(self):
        """
        clear caches after board state changes
        """
        self.valid_moves_cache={}
    
    def display(self):
        """
        Display the board in simple textual format with row and column numbers
        """
        for i,piece in enumerate(self.board):
            if i%8==0:
                print(f"{8-(i//8)}   ",end="")
            print(piece+" ",end="")
            if i%8==7:
                print()
        print()
        print("    a b c d e f g h")
        print(self.winlossdraw())
    
    def algebraic_to_pos(self,algebraic):
        """
        Convert algebraic notation to board position
        """
        try:
            pos=self.reverse_notation[algebraic]
        except KeyError:
            raise InvalidAlgebraicNotationError(f"Not valid algebraic notation: {algebraic}")
        return pos

    def is_valid(self,src,dst):
        """
        Check if a move is valid from source (src) to destination (dst) in algebraic format
        """
        # redo this function so move calls it and it returns true or false?
        src_pos=self.algebraic_to_pos(src)
        dst_pos=self.algebraic_to_pos(dst)
        piece=self.board[src_pos]
        if piece == ".":
            raise EmptySquareError("cannot move from an empty square")
        if piece not in self.valid_pieces:
            raise InvalidAlgebraicNotationError("Not valid piece notation")
    
    def check_piece_color(self,piece):
        """
        Check the colour of piece, returns WHITE, BLACK, None if neither.
        """
        if piece in "pnbrqk":
            return self.WHITE
        if piece in "PNBRQK":
            return self.BLACK
        if piece == ".":
            return None
    
    def move_pos(self,pos,dx,dy):
        """
        This takes the position and moves it by dx and dy, returns -1 if outside board
        """
        x=pos%8
        y=pos//8
        x+=dx
        y+=dy
        dst_pos=x+y*8
        if x>7 or x<0 or y>7 or y<0:
            return None
        return dst_pos
    
    def move_okay(self,dst,turn=None):
        """
        Checks if a destination of a move is valid.
        """
        if dst is None:
            return False
        piece=self.board[dst]
        colour=self.check_piece_color(piece)
        if turn is None:    
            if colour == self.turn:
                return False
        else:
            if colour==turn:
                return False
        return True

    def take_okay(self,dst,turn):
        """
        Checks if a piece is eligible to be taken
        """
        if dst is None:
            return False
        piece=self.board[dst]
        if piece == ".":
            return False
        return self.move_okay(dst,turn=turn) and self.check_piece_color(piece)!=turn

    def pawn(self,src,turn):
        """"
        Moves for a pawn, src and dst as pos
        """
        if turn == self.WHITE:
            dy=-1
        else:
            dy=1
        valid_moves=[]
        #move one step
        dst=self.move_pos(src,0,dy)
        #pawns can only move into a free space
        if self.move_okay(dst,turn=turn) and self.board[dst]==".":
            valid_moves.append(dst)
        #two steps, can't move over pieces
        dst=self.move_pos(src,0,2*dy)
        if self.move_okay(dst,turn=turn) and self.board[dst]=="." and self.board[src+(dy*8)]==".":
            #pawns can only move twice if on home row
            if turn==self.BLACK and src//8==1:
                valid_moves.append(dst)
            elif turn==self.WHITE and src//8==6:
                valid_moves.append(dst)
        #diagonal take up and right
        dst=self.move_pos(src,1,dy)
        if self.take_okay(dst,turn):
            valid_moves.append(dst)
        #diagonal take up and left
        dst=self.move_pos(src,-1,dy)
        if self.take_okay(dst,turn):
            valid_moves.append(dst)
        #enpassant
        if src in self.enpassant_check:
            valid_moves.append(self.enpassant_check[2])
        return valid_moves
    
    def knight(self,src,turn):
        """
        Moves for a knight
        """
        valid_moves=[]
        #different possible vector directions it can move, see diagram
        directions=[(1,2),(-1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,1),(-2,-1)]
        for x,y in directions:
            dst=self.move_pos(src,x,y)
            if self.move_okay(dst,turn):
                valid_moves.append(dst)
        return valid_moves
    
    def linear_move(self,src,dx,dy,turn):
        """"
        Moves where the piece can move as far as it wants: bishop, queen, rook
        """
        dst=src
        valid_moves=[]
        while True:
            dst=self.move_pos(dst,dx,dy)
            if self.move_okay(dst,turn=turn):
                valid_moves.append(dst)
            if dst==None:
                break
            if self.board[dst]!=".":
                break
        return valid_moves

    def bishop(self,src,turn):
        """
        Moves for bishop
        """
        #up and down is different on each colour
        if turn == self.WHITE:
            dy=-1
        else:
            dy=1
        valid_moves=[]
        #up right
        valid_moves.extend(self.linear_move(src,1,dy,turn))
        #up left
        valid_moves.extend(self.linear_move(src,-1,dy,turn))
        #down right
        valid_moves.extend(self.linear_move(src,1,-dy,turn))
        #down left
        valid_moves.extend(self.linear_move(src,-1,-dy,turn))
        return valid_moves
    
    def rook(self,src,turn):
        """
        Moves for a rook
        """
        if turn == self.WHITE:
            dy=-1
        else:
            dy=1
        valid_moves=[]
        #up
        valid_moves.extend(self.linear_move(src,1,0,turn))
        #right
        valid_moves.extend(self.linear_move(src,0,dy,turn))
        #down
        valid_moves.extend(self.linear_move(src,-1,0,turn))
        #left
        valid_moves.extend(self.linear_move(src,0,-dy,turn))
        return valid_moves
    
    def queen(self,src,turn):
        """
        Moves for a queen, equivalent to bishop and rook
        """
        valid_moves=[]
        #diagonals
        valid_moves.extend(self.bishop(src,turn))
        #straights
        valid_moves.extend(self.rook(src,turn))
        return valid_moves
    
    def find_rooks(self,king_pos):
        """
        finds rooks [left,right] compared to king
        """
        rooks=[None,None]
        if self.turn==self.WHITE:
            for i in range(56,64):
                if self.board[i]=="r":
                    rooks[0 if i<king_pos else 1]=i
        else:
            for i in range(8):
                if self.board[i]=="R":
                    rooks[0 if i<king_pos else 1]=i
        return rooks
    
    def king(self,src,turn,checkcheck=True):
        """
        Moves for a king
        """
        valid_moves=[]
        #8 directions, only move 1 space:
        directions=[(1,0),(0,1),(1,1),(-1,0),(-1,1),(0,-1),(1,-1),(-1,-1)]
        for x,y in directions:
            dst=self.move_pos(src,x,y)
            if self.move_okay(dst,turn=turn) and (checkcheck==False or self.is_check(dst,turn)==False):
                valid_moves.append(dst)
        def is_okay(src):
            """
            checks if square is blank and king wouldn't be in check if moved there
            """
            return self.board[src]=="." and (checkcheck==False or not self.is_check(src,turn))
        #960 castling: a-side castle king to c-file rook to d-file, h-side castle king to g-file rook to f-file
        if src in self.unmoved and (checkcheck==False or self.is_check(src)==False):
            left_rook,right_rook=self.find_rooks(src)
            #a-side
            if left_rook is not None and left_rook in self.unmoved and all(is_okay(i) for i in range(left_rook+1,src)):
                valid_moves.append(left_rook)
            #h-side
            if right_rook is not None and right_rook in self.unmoved and all(is_okay(i) for i in range(src+1,right_rook)):
                valid_moves.append(right_rook)
        for move in valid_moves:
            if checkcheck==True and self.is_check(move,turn):
                valid_moves.remove(move)
        return valid_moves
    
    def piece_moves(self,src,checkcheck=True,turn=None):
        """
        Takes an algebraic src, finds the colour and the piece and runs the function for it.
        """
        src=self.algebraic_to_pos(src)
        piece = self.board[src]
        valid_moves=[]
        if turn is None:
            turn=self.check_piece_color(piece)
        if piece == "p" or piece == "P":
            valid_moves=self.pawn(src,turn)
        elif piece == "b" or piece == "B":
            valid_moves=self.bishop(src,turn)
        elif piece == "n" or piece == "N":
            valid_moves=self.knight(src,turn)
        elif piece == "r" or piece == "R":
            valid_moves=self.rook(src,turn)
        elif piece == "q" or piece == "Q":
            valid_moves=self.queen(src,turn)
        elif piece == "k" or piece == "K":
            valid_moves=self.king(src,turn,checkcheck=checkcheck)
        else:
            raise EmptySquareError("src not a piece")
        if checkcheck:
            valid_moves=[move for move in valid_moves if self.is_move_out_of_check(src,move)]
        return valid_moves
        
    
    def all_valid_moves(self,turn,checkcheck=True):
        """
        Iterate through all the number srcs and find run piece_moves for each
        """
        #get valid moves from cache if possible
        cache_key=(turn,checkcheck,tuple(self.board),tuple(self.enpassant_check),frozenset(self.unmoved))
        cached_valid_moves=self.valid_moves_cache.get(cache_key)
        if cached_valid_moves is not None:
            return cached_valid_moves
        valid_moves=[]
        for i in self.notation:
            if self.check_piece_color(self.board[self.algebraic_to_pos(i)])!=turn:
                continue
            try:
                new_moves=self.piece_moves(i,checkcheck=checkcheck,turn=turn)
                valid_moves.extend(new_moves)
            except EmptySquareError as e:
                print(e)
        self.valid_moves_cache[cache_key]=valid_moves # cache valid moves
        return valid_moves
    
    def total_moves(self):
        """
        Count how many total moves there are for the board for current side
        """
        return len(self.all_valid_moves(self.turn))
        
    def move(self,src,dst):
        """
        Moves a piece from src to dst (in algebraic), and returns updated board, appends old board to states
        """
        pos_dst=self.algebraic_to_pos(dst)
        pos_src=self.algebraic_to_pos(src)
        piece = self.board[pos_src]
        if self.board[pos_src] == ".":
            raise InvalidMoveError(f"No piece at {src}")
        if not(pos_dst in self.piece_moves(src)):
            raise InvalidMoveError(f"Invalid move from {src} to {dst}")
        if self.check_piece_color(piece)!=self.turn:
            raise InvalidMoveError("Wrong colour piece")
        # checked for all errors now we can change the state of board
        castle=False
        if piece in ["k","K"]:
            if pos_src in self.unmoved and pos_dst in self.unmoved:
                castle=True
                self.board[pos_src],self.board[pos_dst]=".","."
                if piece=="k":
                    #a-side
                    if pos_dst<pos_src:
                        self.board[58],self.board[59]="k","r"
                    #h-side
                    else:
                        self.board[62],self.board[61]="k","r"
                else:
                    if pos_dst<pos_src:
                        self.board[2],self.board[3]="K","R"
                    #h-side
                    else:
                        self.board[6],self.board[5]="K","R"  
        self.unmoved.discard(pos_src)
        self.move_count+=1
        self.states.append(self.board[:]) # copy the board state as a new object
        if piece=="p" or piece=="P":
            self.enpassant(pos_dst)
        if len(self.enpassant_check)>0 and self.enpassant_check[2]==pos_dst:
            if piece=="p":
                self.board[pos_dst+8]="."
            elif piece=="P":
                self.board[pos_dst-8]="."
        if not castle:
            self.board[pos_src]="."
            self.board[pos_dst]=piece
        self.promotion(piece,pos_dst)
        #print(self.winlossdraw())
        self.turn=1-self.turn

    def is_check(self,king_pos,color=None):
        """
        Checks if the king is in check, returns Boolean, king_pos number postion, if no color specified (to be confirmed)
        has to find out color from pos, if king not at pos and not specified color then error
        """
        #finds colour thats being checked
        if color is None:
            if self.check_piece_color(self.board[king_pos]) == self.WHITE:
                check_turn=self.BLACK
            elif self.check_piece_color(self.board[king_pos]) is None:
                raise EmptySquareError(f"no king on specified king_pos: {king_pos} and no color specified")
            else:
                check_turn=self.WHITE
        elif color is not None:
            if color==self.WHITE:
                check_turn=self.BLACK
            elif color==self.BLACK:
                check_turn=self.WHITE
            else:
                raise InvalidColorError(f"Not valid color specified: {color}")
        #check if in check, uses copy of board to see if moved will it be in check
        copy=self.copy()
        if check_turn==self.WHITE:
            copy.board[king_pos]="K"
        else:
            copy.board[king_pos]="k"
        if king_pos in copy.all_valid_moves(check_turn,checkcheck=False):
            return True
        return False
    
    def find_piece_index(self, pos):
        """
        finds index of piece on board given pos, pos in algebraic, returns None if not found.
        """
        return self.reverse_notation.get(pos)
    
    def find_piece(self,piece):
        """
        finds a piece on the board, if multiple returns list, piece is in letter form
        """
        return [i for i in range(64) if self.board[i]==piece]

    def is_stalemate(self,king_pos):
        """
        Check if stalemate for current, returns boolean, current color is the one to be checked
        """
        if self.total_moves()==0 and self.is_check(king_pos)==False:
            return True
        return False
    
    def is_checkmate(self,king_pos):
        """
        Check if checkmate for current pos, returns boolean, current color is the one to be checked,
        """
        #king has no moves AND other pieces have no VALID moves -> total_moves=0
        return self.total_moves()==0 and self.is_check(king_pos)

    def is_75_move_rule(self):
        """
        Checks for 75 move rule, returns boolean
        """
        #75 move rule, 150th move game stops
        if self.move_count==150:
            return True
        return False
    
    def is_threefold_repetition(self):
        """
        Checks for threefold repetition, forces draw, returns boolean
        """
        repcount=1
        for state in self.states:
            if state==self.board:
                repcount+=1
            if repcount>=3:
                return True
        return False
    
    def contains(self,pos,piece):
        """
        if a specific position contains a specific piece, pos as number piece as string
        """
        if pos is None:
            return False
        if self.board[pos]==piece:
            return True
        return False

    def enpassant(self,pos):
        """
        checks either side of a pawn thats moved up 2 for opposite color pawns
        if so stores opposite color pawn positions and valid move
        """
        opp1=self.move_pos(pos,1,0)
        opp2=self.move_pos(pos,-1,0) # adjacent squares
        self.enpassant_check=[]
        if self.turn==self.WHITE:
            if self.contains(opp1,"P") or self.contains(opp2,"P"):
                self.enpassant_check=[opp1,opp2,pos+8]
        elif self.turn==self.BLACK:
            if self.contains(opp1,"p") or self.contains(opp2,"p"):
                self.enpassant_check=[opp1,opp2,pos-8]
    
    def promotion(self,piece,dst):
        """
        if pawn on opposite end becomes queen for simplicity
        """
        if piece=="p" and dst//8==0:
            self.board[dst]="q"
        if piece=="P" and dst//8==7:
            self.board[dst]="Q"
    
    def winlossdraw(self):
        """
        runs all functions related to win/loss/draw, returns state in string
        """
        if self.turn==self.BLACK:
            king_pos=self.find_piece("K")[0]
            if self.is_checkmate(king_pos):
                return "white win"
            elif self.is_stalemate(king_pos):
                return "draw"
            elif self.is_75_move_rule():
                return "draw"
            elif self.is_threefold_repetition():
                return "draw"
            elif self.is_check(king_pos):
                return "black in check"
        else:
            king_pos=self.find_piece("k")[0]
            if self.is_checkmate(king_pos):
                return "black win"
            elif self.is_stalemate(king_pos):
                return "draw"
            elif self.is_75_move_rule():
                return "draw"
            elif self.is_threefold_repetition():
                return "draw"
            elif self.is_check(king_pos):
                return "white in check"
        return ""
    
    def game_over(self):
        """
        checks if game is over
        """
        return self.winlossdraw() in ["white win", "draw", "black win"]
    
    def copy(self):
        """
        return deep copy of this board without using copy.deepcopy as it's slow
        """
        copy=Board.__new__(Board) # makes uninitialised board
        #shallow copy class variables
        copy.board=self.board[:]
        copy.turn=self.turn
        copy.move_count=self.move_count
        copy.states=self.states[:]
        copy.enpassant_check=self.enpassant_check[:]
        copy.unmoved=self.unmoved.copy()
        copy.clear_caches()
        return copy
    
    def is_move_out_of_check(self,src,dst):
        """
        does move on copy of board and sees if still in check
        """
        board=self.copy()
        board.board[src],board.board[dst]=".",board.board[src]
        if board.turn==board.BLACK:
            king_pos=board.find_piece("K")[0]
        else:
            king_pos=board.find_piece("k")[0]
        return not board.is_check(king_pos)
    
    def valid_move_src_dst(self,turn,checkcheck=True):
        srcdstlist=[]
        for i in self.notation:
            if self.check_piece_color(self.board[self.algebraic_to_pos(i)])!=turn:
                continue
            try:
                new_moves=self.piece_moves(i,checkcheck=checkcheck,turn=turn)
                for move in new_moves:
                    srcdstlist.append((i,self.notation[move]))
            except EmptySquareError as e:
                print(e)
        return srcdstlist
    
    def board_to_fen(self):
        """
        takes current board and returns it in fen notation
        """
        fen=""
        for row in [self.board[i:i+8] for i in range(0, len(self.board), 8)]:
            space_count=0
            for char in row:
                if char==".":
                    space_count+=1
                else:
                    if space_count>0:
                        fen+=str(space_count)
                        space_count=0
                    if char in ["P","R","B","N","K","Q"]: # colours are other way round
                        fen+=char.lower()
                    else:
                        fen+=char.upper()
            if space_count>0:
                fen+=str(space_count)
            fen+="/"
        #add turn
        fen = fen[:-1]
        if self.turn==self.WHITE:
            fen+=" w"
        else:
            fen+=" b"
        return fen