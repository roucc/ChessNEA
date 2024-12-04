"""
Test that the model evaluates to something like the training data
"""

import csv
from AI.fen_to_tensor import fen_to_tensor
import tensorflow as tf
import numpy as np

# import data from csv
# example "7r/1p3k2/p1bPR3/5p2/2B2P1p/8/PP4P1/3K4 b - -",58
dataset="AI/lichess_db_eval.csv"

def load_csv(data):
    """
    generator for reading lines out of large csv
    """
    with open(data,"r") as file:
        reader=csv.reader(file)
        for row in reader:
            board_fen,eval=row[0],row[1]
            yield (board_fen,eval)


def main():
    """
    Test the model against the test data
    """
    model=tf.keras.models.load_model("AI/chess5M.keras")

    size = 100
    i=0
    for board_fen,eval in load_csv(dataset):
        board_tensor=fen_to_tensor(board_fen)
        expected_eval=float(eval)/100 #convert from centipawns to pawns

        input_tensor=np.expand_dims(board_tensor, axis=0) # model expects batch
        eval = model.predict(input_tensor,verbose=0)[0][0]
        print(f"{eval:6.3f} {expected_eval:6.3f} {board_fen}")
        i+=1
        if i==size:
            break
    
if __name__ == "__main__":
    main()
