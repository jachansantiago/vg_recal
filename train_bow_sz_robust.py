import pandas as pd
from models import *
from keras.utils import to_categorical

print("Loading Train data")
train_df = pd.read_csv("big_bow_df.csv")

y_train = to_categorical(train_df['correct'].values)

print("Praparing X_train data")
X_train = train_df.drop(['correct','aligner', 'read', 'mq'], axis=1).values

model = bow_model()

model.compile(loss='categorical_crossentropy', optimizer='SGD', metrics=['accuracy'])

model.fit(X_train, y_train, batch_size=256, epochs=1, verbose=1, shuffle=True, validation_split=0.2)

model.save("bow_model_sz_robust.h5")