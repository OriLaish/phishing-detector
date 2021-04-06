import numpy as np
import pandas as pd
import sklearn.model_selection as skms
import tensorflow as tf
import tensorflowjs as tfjs
import tensorflow.keras.backend as K

NUM_OF_FEATURES = 30


def get_f1(y_true, y_pred): #taken from old keras source code
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

# ###### Data Processing ###### #

# extracting data from file
data = pd.read_csv("CSVDataSet.csv")

# updating the Result column for training
data.rename(columns={'Result': 'Class'}, inplace=True)
data['Class'] = data['Class'].map({-1: 0, 1: 1})

# removing data of unfounded extension data
list_of_unfounded_features = ['SSLfinal_State', 'Domain_registeration_length', 'Submitting_to_email', 'Abnormal_URL',
                              'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'age_of_domain', 'DNSRecord',
                              'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page', 'Statistical_report']

data = data = data.drop(columns=list_of_unfounded_features)  # removing data
NUM_OF_FEATURES -= len(list_of_unfounded_features)  # updating dimension size

# splitting features from classes(results)
x_data = data.iloc[0: -1, 0: NUM_OF_FEATURES]  # feature data
y_data = data.iloc[0: -1, NUM_OF_FEATURES]  # result data

# splitting data to training, validation & testing
x_temp, x_test, y_temp, y_test = skms.train_test_split(x_data, y_data, test_size=0.09, random_state=18)
x_train, x_val, y_train, y_val = skms.train_test_split(x_temp, y_temp, test_size=0.1, random_state=27)

# ###### Creating ANN model ###### #
HIDDEN_LAYER_SIZE = 50

model = tf.keras.Sequential([
    tf.keras.layers.Input(NUM_OF_FEATURES),  # inputs layer
    tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 1st hidden layer
    tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 2st hidden layer
    tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 3st hidden layer
    tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 3st hidden layer
    tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 3st hidden layer
    tf.keras.layers.Dense(1, activation='sigmoid')  # output layer
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', get_f1])
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.05, patience=5)  # to prevent over fit

model.fit(x_train, y_train, epochs=10, batch_size=100, validation_data=(x_val, y_val), verbose=1,
          callbacks=[early_stopping])

tfjs.converters.save_keras_model(model, "savedModel")


