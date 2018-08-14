import pandas as pd
from models import *
from keras.utils import to_categorical
from keras.models import load_model
from load_data import *
from sklearn.metrics import brier_score_loss

print("Loading Train data")
test_df = pd.read_csv("big_bow_df_test.csv")

y_test = to_categorical(test_df['correct'].values)

print("Praparing X_train data")
X_test = test_df.drop(['correct','aligner', 'read', 'mq'], axis=1).values

model = load_model("bow_model_sz_robust.h5")

y_pred = model.predict(X_test)


print("Brier Score orig: {}".format(brier_score_loss(test_df['correct'].values, test_df['mqp'].values)))
print("Brier Score model: {}".format(brier_score_loss(test_df['correct'].values, y_pred[:, 1])))
tsv = output_tsv(test_df, encodePhred(y_pred[:, 1]))

tsv.to_csv("output.tsv", index=False, sep='\t')
