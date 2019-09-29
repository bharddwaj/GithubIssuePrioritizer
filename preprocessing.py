from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from joblib import dump,load
import pandas as pd
from sklearn.model_selection import train_test_split
keywords = ["priority","bug","enhancement","high","medium","low"]
def filter_priority_labels(keywords):
    ''':keywords list of possible labels
        this function keeps the rows that have the possible labels'''
    data = pd.read_csv("githubIssues.csv")
    names = data['labels']
    indices = []
    def check_for_keywords(x):
        if str(x).lower() == "nan":
            return False
        try:
            for i in range(len(keywords)):
                #print(f"keywords: {keywords[i]}")
                if keywords[i] in x:
                    return True
            return False
        except:
            #print(f"error x: {x}")
            pass
    count = 0
    for i in names:
        if check_for_keywords(i):
            indices.append(count)
        count += 1

    for index, row in data.iterrows():
        if not index in indices:
            data = data.drop(index)
    return data

#print(len(indices))
#print(len(data))

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
