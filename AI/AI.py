import numpy as np
import fen_to_tensor
import tensorflow as tf
import csv

# import data from csv
# example "7r/1p3k2/p1bPR3/5p2/2B2P1p/8/PP4P1/3K4 b - -",58
dataset="lichess_db_eval.csv"

def load_csv(data):
    """
    generator for reading lines out of large csv
    """
    with open(data,"r") as file:
        reader=csv.reader(file)
        for row in reader:
            board_fen,eval=row[0],row[1]
            yield (board_fen,eval)

size=100000

#training input
x_train=np.empty((size,8,8,13))
#desired output
y_train=np.empty(size,dtype=np.float32)

i=0
for board_fen,eval in load_csv(dataset):
    x_train[i]=fen_to_tensor.fen_to_tensor(board_fen)
    y_train[i]=float(eval)/100 #convert from centipawns to pawns
    i+=1
    if i==size:
        break

# model

def create_model():
    """
    return tensor flow model for chess evaluation
    """
    model=tf.keras.models.Sequential()
    #input
    model.add(tf.keras.layers.Input(shape=(8,8,13)))
    #convolution 1
    model.add(tf.keras.layers.Conv2D(32,(3,3),padding="same"))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Activation("relu"))
    #convolution 2
    model.add(tf.keras.layers.Conv2D(64,(3,3),padding="same"))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Activation("relu"))
    #flatten
    model.add(tf.keras.layers.Flatten())
    #dense 1
    model.add(tf.keras.layers.Dense(128,activation="relu"))
    model.add(tf.keras.layers.Dropout(0.5))
    #dense 2
    model.add(tf.keras.layers.Dense(64,activation="relu"))
    model.add(tf.keras.layers.Dropout(0.5))
    #output
    model.add(tf.keras.layers.Dense(1,activation="linear"))
    #compile
    model.compile(optimizer="adam",loss="mean_squared_error")
    return model

model=create_model()
#tf.keras.utils.plot_model(model,show_shapes=True)

model.fit(x_train,y_train,epochs=3,batch_size=32,validation_split=0.1)
model.save("chess.keras")