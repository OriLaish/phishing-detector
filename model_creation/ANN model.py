import numpy as np
import pandas as pd
import sklearn.model_selection as skms
import tensorflow as tf

NUM_OF_FEATURES = 30

# ###### Data Processing ###### #

# extracting data from file
data = pd.read_csv("CSVDataSet.csv")

# updating the Result column for training
data.rename(columns={'Result': 'Class'}, inplace=True)
data['Class'] = data['Class'].map({-1: 0, 1: 1})

# splitting features from classes(results)
x_data = data.iloc[0: -1, 0: NUM_OF_FEATURES]  # feature data
y_data = data.iloc[0: -1, NUM_OF_FEATURES]  # result data

# splitting data to training, validation & testing
x_temp, x_test, y_temp, y_test = skms.train_test_split(x_data, y_data, test_size=0.09, random_state=18)
x_train, x_val, y_train, y_val = skms.train_test_split(x_temp, y_temp, test_size=0.1, random_state=27)


# ###### Creating ANN model ###### #
HIDDEN_LAYER_SIZE = 100

model = tf.keras.Sequential([
    tf.keras.layers.Input(NUM_OF_FEATURES),  # inputs layer
    tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 1st hidden layer
    tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 2st hidden layer
    tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 3st hidden layer
    tf.keras.layers.Dense(1, activation='sigmoid')  # output layer
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=20, batch_size=80, validation_data=(x_val, y_val), verbose=1)

