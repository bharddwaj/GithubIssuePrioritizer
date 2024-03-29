from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from joblib import dump,load
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from pandas import DataFrame
import pickle
def preprocess(path):
    ''':data a string of the file name (in the same path)
    should return features and labels that we want for training and test'''
    #-1 low, 0 medium, 1 high
    data = pd.read_csv(path)
    tfidf =  TfidfVectorizer(stop_words="english")
    tfidf2 =  TfidfVectorizer(stop_words="english")
    X = [tfidf.fit_transform(data["issue_title"]),tfidf2.fit_transform(data["body"])]
    with open('models/vectorizer.pickle', 'wb') as fin:
        pickle.dump(tfidf2, fin)
    y = data["priority"]
    # new_x = []
    # for i in range(len(X[0])):
    #     new_x.append((X[0][i],X[1][i]))
    new_x = DataFrame.from_records(X)
    #print(f"{X[1][0]}")
    X_train, X_test, y_train, y_test = train_test_split(X[1], y, test_size=0.4, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.3, random_state=1)

    return X_train, X_test, X_val,y_val, y_train, y_test

