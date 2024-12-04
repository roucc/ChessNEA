#suppress tensorflow messages
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from AI.fen_to_tensor import fen_to_tensor
import tensorflow as tf
import numpy as np

class AIEvaluationMixin:
    """
    AI evaluation
    """
    def __init__(self,model):
        self.model=tf.keras.models.load_model(model)
        #model=tf.keras.models.load_model("chess7500000.keras")

    @tf.function
    def infer(self,x):
        """
        speed up model inference
        """
        return self.model(x)

    def evaluate(self,b):
        """
        returns number representing favour of board
        """
        winlossdraw=b.winlossdraw()
        if winlossdraw=="white win":
            return 1000
        elif winlossdraw=="black win":
            return -1000
        elif winlossdraw=="draw":
            return 0
        fen=b.board_to_fen()
        input_tensor=fen_to_tensor(fen)
        input_tensor=np.expand_dims(input_tensor, axis=0) # model expects batch
        # batching experiment
        # copies=1
        # input_tensor=np.tile(input_tensor,(copies,1,1,1))
        eval=self.infer(input_tensor)
        eval=float(eval[0][0])
        return eval
