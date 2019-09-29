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
    data['priority'] = data['priority'].map(normalize_priority)
    return data[data['priority'].notnull()]


def main():
    if __name__ == '__main__':
        data = pd.read_csv("github-issues.csv")
        normalized_data = normalize_data(data)
        normalized_data.to_csv("normalized-github-issues.csv")


main()
