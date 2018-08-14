import numpy as np
import pandas as pd
import json
from keras.utils import to_categorical



def decodePhred(x):
    return 1-10**(-x/10.0)


def encodePhred(x):
    out = -10 * np.log10(1.00000000001-x)
    out = out.astype(np.int64)
    out[out > 60] = 60
    out[out <= 0] = 1
    return out


def json2csv(file, debug=False, bow=False):
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
    
    max_seq_len = 0
    with open(file, "r+") as f:
        line = f.readline()
        kmers = 4
        if(bow):
            bw = generate_bag_of_words_list(kmers)
        
        i = 0
        while(line != ""):
            
            if(debug and i == 5000):
                break

            line_dict = json.loads(line)
            
            if(len(line_dict['sequence']) > max_seq_len):
                max_seq_len = len(line_dict['sequence'])
            
            if bow:
                current_bow = bag_of_words(line_dict['sequence'], kmers)
                
                for key in bw.keys():
                    bw[key].append(current_bow[key])
                
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
       
    df = pd.DataFrame(df_dict)
    df.score = df.score
    df.secondary_score = df.score 
    df.secondary_score_size = df.secondary_score_size
    df['mqp'] = decodePhred(df.mq)
    
    if(bow):
        df = df.join(pd.DataFrame(bw))
    
    return df


def get_orig_tsv(df):
    tsv_data = df.copy()
    return tsv_data.loc[:, ['correct', 'mq', 'aligner', 'read']]


def merge_orig_recal_tsv(orig_tsv, pred):
    recal = orig_tsv.copy()
    recal.loc[:, ['aligner']] = 'recal'
    recal.loc[:, ['mq']] = encodePhred(pred)
    return orig_tsv.append(recal, ignore_index=True)


def get_balanced_data(X, y, test_per=0.2):
    
    incorrect_amount = y[y == 0].correct.count()
    
    #if(incorrect_amount == 0):
    #    print("No incorrect class!!!!")
    #    exit()
        
    train_amount = int(incorrect_amount * (1 - test_per)) # per class
    test_amount = int(incorrect_amount * test_per )       # per class
    
    permu_index = np.random.permutation(y.shape[0])
    
    shuffled_X = X.iloc[permu_index, :]
    shuffled_y = y.iloc[permu_index]

    X_train_correct = shuffled_X[shuffled_y.correct == 1].iloc[:train_amount]
    y_train_correct = shuffled_y[shuffled_y.correct == 1].iloc[:train_amount]

    X_train_incorrect = shuffled_X[shuffled_y.correct == 0].iloc[:train_amount]
    y_train_incorrect = shuffled_y[shuffled_y.correct == 0].iloc[:train_amount]

    X_test_correct = shuffled_X[shuffled_y.correct == 1].iloc[train_amount:train_amount + test_amount]
    y_test_correct = shuffled_y[shuffled_y.correct == 1].iloc[train_amount:train_amount + test_amount]

    X_test_incorrect = shuffled_X[shuffled_y.correct == 0].iloc[train_amount:train_amount + test_amount]
    y_test_incorrect = shuffled_y[shuffled_y.correct == 0].iloc[train_amount:train_amount + test_amount]


    X_train = np.append(X_train_correct, X_train_incorrect, axis=0)
    X_test = np.append(X_test_correct, X_test_incorrect, axis=0)

    y_train = np.append(y_train_correct, y_train_incorrect)
    y_test = np.append(y_test_correct, y_test_incorrect)
    
    y_train = to_categorical(y_train, 2)
    y_test = to_categorical(y_test, 2)
    
    return X_train, y_train, X_test, y_test 
    
    
    
    
def get_train_data(train_file, debug=False, bow=False):  
    df, score_div = json2csv(train_file, debug, bow=bow)
    print(df)
    orig_tsv = get_orig_tsv(df)
    print(orig_tsv)
    X = df.drop(columns=['correct', 'mq'])
    y = df.loc[:, ['correct']]
    X_train, y_train, X_test, y_test = get_balanced_data(X, y, test_per=0.2)

    return X_train, y_train, X_test, y_test, orig_tsv, score_div


def get_test_data(test_file, score_div, bow=False):
    
    df, _ = json2csv(test_file, bow=bow)
    
    tsv_data = get_orig_tsv(df)

    X = df.drop(columns=['correct','mq'])
    labels = df.loc[:, ['correct']]
    labels = to_categorical(labels, 2)
    orig = decodePhred(df.mq.values)
    return X, labels, orig, tsv_data


def generate_bag_of_words(kmer):
    bw = dict()
    letters = ["A", "C", "G", "T"]
    
    for i in range(4**kmer):
        val = i
        s =""
        for j in range(kmer):
            l = int(val % 4)
            val /= 4
            s += letters[l]
        #print(s)
        bw[s] = 0
    return bw


def generate_bag_of_words_list(kmer):
    bw = dict()
    letters = ["A", "C", "G", "T"]
    
    for i in range(4**kmer):
        val = i
        s =""
        for j in range(kmer):
            l = int(val % 4)
            val /= 4
            s += letters[l]
        #print(s)
        bw[s] = list()
    return bw

    
def bag_of_words(seq, kmer):
    bw = generate_bag_of_words(kmer)
    
    for i in range(len(seq) - (kmer-1)):
        bw[seq[i:i+kmer]] += 1
    return bw


def output_tsv(df, pred):
    out_df = df.loc[:, ['correct', 'mq', 'aligner', 'read']]
    recal_df =  out_df.copy()
    recal_df.loc[:, 'aligner'] = 'recal'
    recal_df.loc[:, 'mq'] = pred
    
    return out_df.append(recal_df, ignore_index=True)


if __name__ == "__main__":
    
    train_file = "../data/train_gamcompare/json/compared_mapped100_sim100.json"
    test_file = "../data/test_gamcompare/json/tcompared_tmapped100_tsim100.json"
    X_train, y_train, X_val, y_val, orig_tsv, score_div = get_train_data(train_file, debug=False, bow=True)
    X_test, y_test, orig, test_orig_tsv = get_test_data(test_file, score_div, bow=True)
    
    print("Train Data")
    print(X_train, y_train)
    print("Validation Data")
    print(X_val, y_val)
    print("Test Data")
    print(X_test, y_test)
    test_pred = np.ones(orig_tsv.mq.shape) * 0.5555
    print(test_pred)
    print(y_test.shape)
    final_tsv = merge_orig_recal_tsv(orig_tsv, test_pred)
    print(final_tsv)
    #print(bag_of_words("ATGTGATAG", 3))