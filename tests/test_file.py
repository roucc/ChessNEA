from AI import fen_to_tensor

#print(fen_to_tensor.fen_to_tensor("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))

import numpy as np
import tensorflow as tf
from chess.board import *
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # suppress everything except errors

b=Board("RNBQKBNR"
        "PPPPPPPP"
        "........"
        "........"
        "........"
        "........"
        "pppppppp"
        "rnbqkbnr")
model=tf.keras.models.load_model("AI/chess5M.keras")
def eval(b):
    fen=b.board_to_fen()
    #print(fen)
    input_tensor=fen_to_tensor.fen_to_tensor(fen)
    #print(input_tensor)
    input_tensor=np.expand_dims(input_tensor, axis=0) # model expects batch
    eval=model.predict(input_tensor,verbose=0)
    print(eval[0][0])
    return eval[0][0]
eval(b)
b=Board("....K..."
        "....Q..."
        "........"
        "........"
        "........"
        "........"
        "pppppppp"
        "rnbqkbnr")
eval(b)
b=Board("RNBQKBNR"
        "PPPPPPPP"
        "........"
        "........"
        "........"
        "........"
        "pppppppp"
        "....k...")
eval(b)
b=Board("RNBQKBNR"
        "PPPPPPPP"
        "........"
        "........"
        "........"
        "........"
        "pppp.ppp"
        "....k...")
eval(b)
b=Board("RNBQKBNR"
        ".PPPPPPP"
        "........"
        "P......."
        "....p..."
        "........"
        "pppp.ppp"
        "rnbqkbnr")
eval(b)
b=Board("RNBQKBNR"
        "PPPP.PPP"
        "........"
        "....p..."
        "....p..."
        "........"
        "pppp.ppp"
        "rnbqkbnr")
eval(b)
