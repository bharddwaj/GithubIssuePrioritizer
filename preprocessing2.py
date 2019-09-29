import pandas as pd

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
def preprocess(data):
    ''':data a string of the file name (in the same path)
    should return features and labels that we want for training and test'''
    data = pd.read_csv(data)
    data = data.sample(frac=1).reset_index(drop=True)
    training_features = []
    training_labels = []

    testing_features = []
    testing_labels = []
    for index, row in data.iterrows():
        if index < int(.60 * data.shape[0]):
            training_features.append((data['number_of_comments'][index],data['time difference'][index]))
            training_labels.append(data['labels'][index])
        else:
            testing_features.append((data['number_of_comments'][index],data['time difference'][index]))
            testing_labels.append(data['labels'][index])
    validation_features = training_features[int(.9*len(training_features)):]
    validation_labels = training_labels[int(.9*len(training_features)):]
    return [training_features, training_labels, validation_features, validation_labels,testing_features, testing_labels]