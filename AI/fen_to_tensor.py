import numpy as np

# "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

pieces={"r":0,"n":1,"b":2,"q":3,"k":4,"p":5,"R":6,"N":7,"B":8,"Q":9,"K":10,"P":11}

def fen_to_tensor(fen):
    """
    converts fen board notation to tensor of board and turn colour
    """
    board,turn,*_=fen.split() # ignore all except board and turn (simplicity)
    board_tensor = np.zeros((8,8,12))
    rows=board.split("/")
    for row_i,row in enumerate(rows):
        col_i=0
        for char in row:
            if char.isdigit():
                col_i+=int(char)
            else:
                piece=pieces[char]
                board_tensor[row_i,col_i,piece]=1 # add to tensor
                col_i+=1
    if turn=="w":
        turn_tensor=np.ones((8,8,1))
    else:
        turn_tensor=np.zeros((8,8,1))
    return np.concatenate([board_tensor,turn_tensor],axis=2) # axis 2 makes 8x8x12 into 8x8x13
        
#print(fen_to_tensor("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))