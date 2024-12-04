import numpy as np
import fen_to_tensor
import tensorflow as tf
from tensorflow.keras import regularizers # type: ignore
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

def create_model():
    """
    Return a TensorFlow model for chess evaluation
    """
    input_layer = tf.keras.layers.Input(shape=(8, 8, 13))
    
    #convolutional block 1
    #correlates features in different places of the input producing 32x8x8 output layers
    x = tf.keras.layers.Conv2D(32, (5, 5), padding="same", kernel_regularizer=regularizers.l2(0.001))(input_layer)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)
    
    #convolutional block 2
    #correlate that into 64 higher level features 64x8x8
    x = tf.keras.layers.Conv2D(64, (3, 3), padding="same", kernel_regularizer=regularizers.l2(0.001))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)

    #residual connection
    residual = tf.keras.layers.Conv2D(64, (1, 1), padding="same")(input_layer)
    x = tf.keras.layers.Add()([x, residual])
    
    #convolutional block 3
    #correlate into higher level features still 128x8x8
    x = tf.keras.layers.Conv2D(128, (3, 3), padding="same", kernel_regularizer=regularizers.l2(0.001))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)
    
    #Global Average Pooling
    #collapse into 128 features
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    
    #dense layers
    #correlate the features
    x = tf.keras.layers.Dense(128, activation="relu", kernel_regularizer=regularizers.l2(0.001))(x)
    x = tf.keras.layers.Dropout(0.3)(x)  # Reduced dropout rate
    
    x = tf.keras.layers.Dense(64, activation="relu", kernel_regularizer=regularizers.l2(0.001))(x)
    x = tf.keras.layers.Dropout(0.3)(x)  # Reduced dropout rate
    
    #output layer
    #linear output layer to produce the evaluation in pawns directly
    output = tf.keras.layers.Dense(1, activation="linear")(x)
    
    #compile model
    model = tf.keras.models.Model(inputs=input_layer, outputs=output)
    #model.compile(optimizer="adam", loss="mean_squared_error")
    # Huber loss function is better at outliers which we have some of
    model.compile(optimizer="adam", loss=tf.keras.losses.Huber())
    
    return model


def train(size=1000000,epochs=50,batch_size=32):
    """
    Create and train the model on size items from the dataset
    """
    model=create_model()

    #create an image of the model architecture
    dot_img_file = 'model_architecture.png'
    tf.keras.utils.plot_model(model, to_file=dot_img_file, show_shapes=True)
    
    #reduce the learning rate if the validation loss plateaus
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.0001)

    #define the ModelCheckpoint callback to save the model as we progress
    save_model = tf.keras.callbacks.ModelCheckpoint(
        filepath='chess.keras',  # save model every epoch
        save_weights_only=False, # save the entire model (architecture + weights + optimizer state)
        save_freq='epoch',       # save every epoch
        verbose=1                # verbosity mode, 1 = progress bar
    )
    
    #training input
    x_train=np.empty((size,8,8,13))
    #desired output
    y_train=np.empty(size,dtype=np.float32)

    i=0
    positive = 0
    negative = 0
    for board_fen,eval in load_csv(dataset):
        # evaluation in pawns, not centi-pawns
        eval = float(eval) / 100

        # balance the number of positive and negative evaluations
        # to within 1%
        if eval > 0:
            if positive > 1.01*negative:
                continue
            positive += 1
        elif eval < 0:
            if negative > 1.01*positive:
                continue
            negative += 1

        x_train[i]=fen_to_tensor.fen_to_tensor(board_fen)
        y_train[i]=eval
        i+=1
        if i==size:
            break

    model.fit(x_train,
              y_train,
              epochs=epochs,
              batch_size=batch_size,
              validation_split=0.1,
              callbacks=[reduce_lr, save_model],
    )
    model.save("chess.keras")

if __name__ == "__main__":
    train()
