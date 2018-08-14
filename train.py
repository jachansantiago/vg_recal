from load_data import *
from models import *
import datetime
import os

def time_log():
    dformat = "%Y-%b-%d_%I:%M"
    return datetime.datetime.now().strftime(dformat)

TRAIN_DIR = 'sims/train_gamcompare/json/'
TEST_DIR = 'sims/test_gamcompare/json/'
train_files = os.listdir(TRAIN_DIR)
test_files = os.listdir(TEST_DIR)

test_tsv_file_placeholder = "sims/stats/test/{}.tsv"
train_tsv_file_placeholder = "sims/stats/train/{}.tsv"
model_file_placeholder = "sims/models/{}__model_{}.h5"

sorted(train_files)
sorted(test_files)
i = 70 
for train_f, test_f in zip(train_files, test_files):
    
    train_tsv_file = train_tsv_file_placeholder.format(train_f[:-5])
    test_tsv_file = test_tsv_file_placeholder.format(test_f[:-5])
    model_file = model_file_placeholder.format(time_log(), train_f[:-5])
    print("Loading Training Data... from {}".format(os.path.join(TRAIN_DIR, train_f)))
    X_train, y_train, X_val, y_val, _ , score_div = get_train_data(os.path.join(TRAIN_DIR, train_f))
    X_train_t, y_train_t, train_orig_tsv, train_orig_tsv = get_test_data(os.path.join(TRAIN_DIR, train_f), score_div)
    print("Loading Testing Data... from {}".format(os.path.join(TEST_DIR, test_f)))
    X_test, y_test, orig, test_orig_tsv = get_test_data(os.path.join(TEST_DIR, test_f), score_div)
    
    model = shallow_model()
    
    model.compile(loss='categorical_crossentropy', optimizer='SGD', metrics=['accuracy'])

    model.fit(X_train, y_train, batch_size=128, epochs=30, 
              verbose=1, validation_data=(X_val, y_val), shuffle=True)
    model.save(model_file)
    print("Predicting Train...")
    y_pred_t = model.predict(X_train_t)
    
    final_train_tsv = merge_orig_recal_tsv(train_orig_tsv, y_pred_t[:, 1])
    print("Saving stats in {}".format(train_tsv_file))
    final_train_tsv.to_csv(train_tsv_file, sep='\t', index=False)
    
    print("Predicting Test...")
    y_pred = model.predict(X_test)
    
    final_test_tsv = merge_orig_recal_tsv(test_orig_tsv, y_pred[:, 1])
    print("Saving stats in {}".format(test_tsv_file))
    final_test_tsv.to_csv(test_tsv_file, sep='\t', index=False)
    
    i += 10