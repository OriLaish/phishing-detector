import numpy as np
import tensorflow as tf
from tensorflow.contrib.tensor_forest.python import tensor_forest

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

# Create the Random forest model

