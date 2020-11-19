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
    line = np.array(line.split(','))
    line = list(map(lambda x: (int(x) + 1) / 2, line))
    inputs = np.array(line[:-1])
    outputs = np.array(line[len(line) - 1])
    inputsArray.append(inputs)
    outputsArray.append(outputs)

# Put all of the inputs and outputs into a matrix
inputsMatrix = np.array(inputsArray)
outputsMatrix = np.array(outputsArray)


TrainingData = { "inputs": inputsMatrix[:9000], "outputs": outputsMatrix[:9000] }
ValidationData = { "inputs": inputsMatrix[9000:10000], "outputs": outputsMatrix[9000:10000] }
TestData = { "inputs": inputsMatrix[10000:], "outputs": outputsMatrix[10000:] }

#  Divide the data to Training data \ Validation data \ Test data.
TrainingData["inputs"] = tf.data.Dataset.from_tensor_slices(TrainingData["inputs"]).shuffle(1000).batch(100)
TrainingData["outputs"] = tf.data.Dataset.from_tensor_slices(TrainingData["outputs"]).shuffle(1000).batch(100)
TrainingData["data"] = tf.data.Dataset.zip((TrainingData["inputs"], TrainingData["outputs"]))


ValidationData["inputs"] = tf.data.Dataset.from_tensor_slices(ValidationData["inputs"]).batch(len(ValidationData["inputs"]))
ValidationData["outputs"] = tf.data.Dataset.from_tensor_slices(ValidationData["outputs"]).batch(len(ValidationData["outputs"]))
ValidationData["data"] = tf.data.Dataset.zip((ValidationData["inputs"], ValidationData["outputs"]))

TestData["inputs"] = tf.data.Dataset.from_tensor_slices(TestData["inputs"]).batch(len(TestData["inputs"]))
TestData["outputs"] = tf.data.Dataset.from_tensor_slices(TestData["outputs"]).batch(len(TestData["outputs"]))

# #### Create the ANN model #### #
INPUTS = 0
OUTPUTS = 1
input_size = 30
output_size = 1

hidden_layer_size = 15

model = tf.keras.Sequential([

    tf.keras.layers.Dense(input_size),  # input layer
    tf.keras.layers.Dense(hidden_layer_size, activation='relu'),  # 1st hidden layer
    tf.keras.layers.Dense(hidden_layer_size, activation='relu'),  # 2nd hidden layer
    tf.keras.layers.Dense(hidden_layer_size, activation='relu'),  # 3nd hidden layer
    tf.keras.layers.Dense(hidden_layer_size, activation='relu'),  # 4nd hidden layer
    tf.keras.layers.Dense(output_size, activation='sigmoid')  # output layer
])

# choosing optimizer and loss function
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


# #### Training the model (unfinished) #### #
NUM_EPOCHS = 10
model.fit(TrainingData["data"], epochs=NUM_EPOCHS, validation_data=ValidationData["data"], verbose=1)

