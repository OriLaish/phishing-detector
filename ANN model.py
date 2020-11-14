import numpy as np
import tensorflow as tf


# #### Processing the data #### #


file = (open('TrainingDataset.arff'))
lines = file.read().split('\n')
inputs = []
outputs = []
inputsArray = []
outputsArray = []
for line in lines:
    dataByLines = lines[0]
    line = np.array(dataByLines.split(','))
    line = list(map(int, line))
    inputs = np.array(line[:-1])
    outputs = np.array(line[len(line) - 1])
    inputsArray.append(inputs)
    outputsArray.append(outputs)

# Put all of the inputs and outputs into a matrix
inputsMatrix = np.array(inputsArray)
outputsMatrix = np.array(outputsArray)

batchInputs = tf.data.Dataset.from_tensor_slices(inputsMatrix).batch(100)
batchOutputs = tf.data.Dataset.from_tensor_slices(outputsMatrix).batch(100)



TrainingData = []
ValidationData = []
TestData = []

#  Divide the data to Training data \ Validation data \ Test data.
TrainingData.append(inputsMatrix[:9000])
TrainingData.append(outputsMatrix[:9000])

ValidationData.append(inputsMatrix[9000:10000])
ValidationData.append(outputsMatrix[9000:10000])

TestData.append(inputsMatrix[10000:])
TestData.append(outputsMatrix[10000:])

# #### Create the ANN model #### #
INPUTS = 0
OUTPUTS = 1
input_size = 30
output_size = 1

hidden_layer_size = 10

model = tf.keras.Sequential([

    tf.keras.layers.Dense(input_size),  # input layer
    tf.keras.layers.Dense(hidden_layer_size, activation='relu'),  # 1st hidden layer
    tf.keras.layers.Dense(hidden_layer_size, activation='relu'),  # 2nd hidden layer
    tf.keras.layers.Dense(output_size, activation='softmax')  # output layer
])

# choosing optimizer and loss function
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accurasy'])


# #### Training the model (unfinished) #### #
NUM_EPOCHS = 6
model.fit(TrainingData, epochs=NUM_EPOCHS, validation_data=(ValidationData[INPUTS],ValidationData[OUTPUTS]), verbose=2)