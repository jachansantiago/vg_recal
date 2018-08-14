import keras
from keras.layers import Dense, Dropout, BatchNormalization
from keras.models import Sequential
import pandas as pd
import numpy as np


def shallow_model():
    input_layer = 5
    output_layer = 2 

    h_layer1 = 8
    dropout1 = 0.25

    h_layer2 = 8
    dropout2 = 0.5

    model = Sequential()

    model.add(Dense(h_layer1, activation='relu', input_shape=(input_layer, )))
    model.add(BatchNormalization())
    model.add(Dropout(dropout1))

    model.add(Dense(h_layer2, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(dropout2))

    model.add(Dense(output_layer, activation='softmax'))
    
    return model


def bow_model():
    input_layer = 262
    output_layer = 2 

    h_layer1 = 512
    dropout1 = 0.25

    h_layer2 = 256
    dropout2 = 0.5

    h_layer3 = 128
    dropout3 = 0.5

    model = Sequential()

    model.add(Dense(h_layer1, activation='relu', input_shape=(input_layer, )))
    model.add(BatchNormalization())
    model.add(Dropout(dropout1))

    model.add(Dense(h_layer2, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(dropout2))
    
    model.add(Dense(h_layer3, activation='relu', ))
    model.add(BatchNormalization())

    model.add(Dense(output_layer, activation='softmax'))

    return model
