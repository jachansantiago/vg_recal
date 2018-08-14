
# coding: utf-8

# In[9]:


import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import keras
from keras.layers import Dense, Dropout, BatchNormalization
from keras.models import Sequential
from sklearn.metrics import brier_score_loss, accuracy_score

def decodePhed(x):
    return 1-10**(-x/10.0)

def encodePhed(x):
    return -10 * np.log10(x)


# In[10]:


train_file_placeholder = "data/train_gamcompare/json/compared_mapped{}_sim{}.json"
test_file_placeholder = "data/test_gamcompare/json/tcompared_tmapped{}_tsim{}.json"
model_file_placeholder = "models/model_len{}.h5"
tsv_file_placeholder = "tsv/tcompared_tmapped{}_tsim{}.tsv"


# In[11]:


def json2csv(file):
    df_dict = {
        'correct': list(),
        'mq': list(),
        'score': list(),
        'secondary_score' : list(),
        'secondary_score_size':list(),
        'identity': list(),
        'aligner' : list(),
        'read': list()
    }
    with open(file, "r+") as f:
        line = f.readline()
        #line_dict = json.loads(line) 
        i = 0
        while(line != ""):
            line_dict = json.loads(line)
            if 'correctly_mapped' in line_dict:
                df_dict['correct'].append(1)
            else:
                df_dict['correct'].append(0)
                
            if 'mapping_quality' in line_dict:
                df_dict['mq'].append(line_dict['mapping_quality'])
            else:
                df_dict['mq'].append(0)
            
            if 'score' in line_dict:
                df_dict['score'].append(line_dict['score'])
            else:
                df_dict['score'].append(0)
                
            if 'identity' in line_dict:
                df_dict['identity'].append(line_dict['identity'])
            else:
                df_dict['identity'].append(0)
                
            if 'secondary_score' in line_dict:
                df_dict['secondary_score'].append(line_dict['secondary_score'][0])
                df_dict['secondary_score_size'].append(len(line_dict['secondary_score']))
            else:
                df_dict['secondary_score'].append(0)
                df_dict['secondary_score_size'].append(0)
            
            df_dict['aligner'].append('orig')
            df_dict['read'].append(line_dict['name'])
            
            line = f.readline()
            i += 1
        print(i)

    return pd.DataFrame(df_dict)


# In[12]:


def get_train_data(train_file):  
    df = json2csv(train_file)
    ndf = df.copy()

    ndf['mq'] = df.mq/60.0
    ndf['score'] = df.score/df.score.max()
    ndf['secondary_score'] = df.secondary_score/df.secondary_score.max()
    ndf['secondary_score_size'] = df.secondary_score_size/df.secondary_score_size.max()

    incorrect_amount = ndf[ndf.correct == 0]['correct'].count()
    incorrect_amount

    train_incorrect_amount = int(incorrect_amount * 0.8)
    test_incorrect_amount = int(incorrect_amount * 0.2)
    train_incorrect_amount,test_incorrect_amount

    X = ndf.iloc[:, 1:6]
    y = ndf.iloc[:, :1]

    permu_index = np.random.permutation(X.shape[0])

    X = X.iloc[permu_index, :]
    y = y.iloc[permu_index]

    X_train_correct = X[y.correct == 1].iloc[:train_incorrect_amount]
    y_train_correct = y[y.correct == 1].iloc[:train_incorrect_amount]

    X_train_incorrect = X[y.correct == 0].iloc[:train_incorrect_amount]
    y_train_incorrect = y[y.correct == 0].iloc[:train_incorrect_amount]

    X_test_correct = X[y.correct == 1].iloc[train_incorrect_amount:train_incorrect_amount+test_incorrect_amount]
    y_test_correct = y[y.correct == 1].iloc[train_incorrect_amount:train_incorrect_amount+test_incorrect_amount]

    X_test_incorrect = X[y.correct == 0].iloc[train_incorrect_amount:train_incorrect_amount+test_incorrect_amount]
    y_test_incorrect = y[y.correct == 0].iloc[train_incorrect_amount:train_incorrect_amount+test_incorrect_amount]


    X_train = np.append(X_train_correct, X_train_incorrect, axis=0)
    X_test = np.append(X_test_correct, X_test_incorrect, axis=0)

    y_train = np.append(y_train_correct, y_train_incorrect)
    y_test = np.append(y_test_correct, y_test_incorrect)

    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)

    y_train_class = np.zeros((2*train_incorrect_amount, 2))
    y_train_class[(y_train==1), : ] = [1, 0]
    y_train_class[(y_train==0), :] = [0, 1]

    y_test_class = np.zeros((2 * test_incorrect_amount, 2))

    y_test_class[(y_test == 1), : ] = [1, 0]
    y_test_class[(y_test == 0), :] = [0, 1]

    return X_train, y_train_class, X_test, y_test_class


# In[17]:


def get_test_data(test_file):
    
    df = json2csv(train_file)
    ndf = df.copy()
    ndf['mq'] = df.mq/60.0
    ndf['score'] = df.score/df.score.max()
    ndf['secondary_score'] = df.secondary_score/df.secondary_score.max()
    ndf['secondary_score_size'] = df.secondary_score_size/df.secondary_score_size.max()
    
    X = ndf.iloc[:, 1:6]
    labels = ndf.correct.values
    orig = decodePhed(df.mq.values)
    tsv_data = df.copy()
    tsv_data = tsv_data.drop(['score', 'secondary_score', 'identity', 'secondary_score_size'], axis=1)
    return X, labels, orig, tsv_data


# #### Neural Network HyperParameters

# In[14]:


def get_model():
    input_layer = 5
    output_layer = 2 

    h_layer1 = 8
    dropout1 = 0.25

    h_layer2 = 16
    dropout2 = 0.5

    h_layer3 = 16
    dropout3 = 0.5

    h_layer4 = 8
    dropout4 = 0.5

    model = Sequential()

    model.add(Dense(h_layer1, activation='relu', input_shape=(input_layer, )))
    model.add(BatchNormalization())
    model.add(Dropout(dropout1))

    model.add(Dense(h_layer2, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(dropout2))

    model.add(Dense(h_layer3, activation='relu'))
    model.add(Dropout(dropout3))

    model.add(Dense(h_layer4, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(dropout4))

    model.add(Dense(output_layer, activation='softmax'))
    return model


# In[23]:


df_dict = {
    'len' : list(),
    'orig_brier_score' : list(),
    'nn_brier_score' : list(),
    'nn_accuracy': list(),
    'orig_accuracy':list(),
    'nn_pos_accuracy':list(),
    'orig_pos_accuracy' : list(),
    'nn_neg_accuracy':list(),
    'orig_neg_accuracy' : list(),
    'train_file' : list(),
    'test_file': list(),
    'model_file': list()
}

for i in range(210, 260, 10):
    train_file = train_file_placeholder.format(i, i)
    test_file = test_file_placeholder.format(i, i)
    model_file = model_file_placeholder.format(i)
    tsv_file = tsv_file_placeholder.format(i, i)
    print("Loading Train Data...")
    X_train, y_train, X_test, y_test = get_train_data(train_file)
    print("Loading Test Data...")
    X, labels, orig, orig_tsv_data = get_test_data(test_file)
    recal_tsv_data = orig_tsv_data.copy()

    model = get_model()

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(X_train, y_train, batch_size=128, epochs=30, 
              verbose=1, validation_data=(X_test, y_test), shuffle=True)

    model.save(model_file)

    print("Predicting...")
    y_pred = model.predict(X)
    nn_pred = y_pred[:, 0]
    
    recal_tsv_data.loc[:,'mq'] = encodePhed(y_pred[:, 1])
    recal_tsv_data.loc[:,'aligner'] = 'recal'
    orig_tsv_data = orig_tsv_data.append(recal_tsv_data , ignore_index=True)
    orig_tsv_data.to_csv(tsv_file)
    
    
    nn_brier_score = brier_score_loss(labels, nn_pred)
    orig_brier_score = brier_score_loss(labels, orig)

    nn_pred_class = nn_pred.copy()
    nn_pred_class[nn_pred >= 0.5] = 1
    nn_pred_class[nn_pred < 0.5] = 0

    nn_acc = accuracy_score(labels, nn_pred_class)

    orig_class = orig.copy()
    orig_class[orig >= 0.5] = 1
    orig_class[orig < 0.5] = 0

    orig_acc = accuracy_score(labels, orig_class)

    nn_pos_acc = accuracy_score(labels[labels == 1], nn_pred_class[labels == 1])
    orig_pos_acc = accuracy_score(labels[labels == 1], orig_class[labels == 1])

    nn_neg_acc = accuracy_score(labels[labels == 0], nn_pred_class[labels == 0])
    orig_neg_acc = accuracy_score(labels[labels == 0], orig_class[labels == 0])
    
    df_dict['len'].append(i)
    df_dict['orig_brier_score'].append(orig_brier_score)
    df_dict['nn_brier_score'].append(nn_brier_score)
    df_dict['nn_accuracy'].append(nn_acc)
    df_dict['orig_accuracy'].append(orig_acc)
    df_dict['nn_pos_accuracy'].append( nn_pos_acc)
    df_dict['orig_pos_accuracy'].append(orig_pos_acc)
    df_dict['nn_neg_accuracy'].append(nn_neg_acc)
    df_dict['orig_neg_accuracy'].append(orig_neg_acc)
    df_dict['train_file'].append(train_file)
    df_dict['test_file'].append(test_file)
    df_dict['model_file'].append(model_file)
    
    

model_stats = pd.DataFrame(df_dict)
model_stats.to_csv('model_stats.csv')

