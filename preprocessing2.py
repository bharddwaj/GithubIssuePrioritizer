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
    