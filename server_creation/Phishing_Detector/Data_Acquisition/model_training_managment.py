import numpy as np
import pandas as pd
import sklearn.model_selection as skms
import tensorflow as tf
import tensorflowjs as tfjs


def open_model():
    """
    open and return model
    """
    return tfjs.converters.load_keras_model("Saved_Model\\model.json")

def save_model(model):
    """
    saves the retrained model in the required place
    """
    tfjs.converters.save_keras_model(model, "Saved_Model")


def process_training_data():
    """
    
    """
    pass


def train_model():
    """
    train the opened model and save it
    """
    model = open_model()
    data = process_training_data()
    if data == None:
        return False
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.05, patience=5)  # to prevent over fit
    model.fit(data.x_train, data.y_train, epochs=10, batch_size=100, validation_data=(data.x_val, data.y_val), verbose=1,
          callbacks=[early_stopping])
    save_model(model)
    return  True



