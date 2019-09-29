from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from joblib import dump,load
import pandas as pd
from sklearn.model_selection import train_test_split

def preprocess(path):
    ''':data a string of the file name (in the same path)
    should return features and labels that we want for training and test'''
    data = pd.read_csv(path)
    X = data["time_difference","number_of_comments"]
    y = data["priority"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=1)

    return X_train, X_test, X_val,y_val, y_train, y_test
# TODO Fill this in with actual serialization and deserialization process
model = None
dump(model, 'models/model')
model = load('models/model')

print(model)
