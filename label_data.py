import pandas as pd

high = ["high", "severe", "critical", "urgent", "highest", "top", "mvp", "emergency"]
medium = ["medium", "normal", "middle", "moderate", "med"]
low = ["low"]


def normalize_priority(label):
    if len([x for x in high if x in label]) > 0:
        return 1
    elif len([x for x in medium if x in label]) > 0:
        return 0
    elif len([x for x in low if x in label]) > 0:
        return -1
    else:
        return None


def normalize_data(data):
    data = data.copy()
    data['priority'] = data['priority'].map(normalize_priority)
    return data[data['priority'].notnull()]

def pivot_labels(data):
    data = data.copy()
    data['other_labels'] = data['other_labels'].str.split(',')
    data = data.explode('other_labels')
    data['other_labels'] = data['other_labels'].str.strip()
    data.drop(data['other_labels'] == '', axis=0)
    data['dummy'] = 1
    print(data.columns)
    print(data.shape)
    data = data.pivot_table(values='dummy',
                            columns=['other_labels'],
                            index=['issue_title', 'body', 'priority'])
    data.reset_index(level=data.index.names, inplace=True)
    return data


def main():
    data = pd.read_csv("github-issues.csv")
    normalized_data = normalize_data(data)
    normalized_label_data = pivot_labels(normalized_data)
    normalized_label_data.to_csv("normalized-github-issues.csv", index=False)


if __name__ == '__main__':
    main()
