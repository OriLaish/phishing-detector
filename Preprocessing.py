import numpy as np
import pandas as pd

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
    outputs = np.array(line[len(line)-1])
    inputsArray.append(inputs)
    outputsArray.append(outputs)


inputsMatrix = np.array(inputsArray)
outputsMatrix = np.array(outputsArray)
print(len(inputsArray))
print(len(outputsArray))

