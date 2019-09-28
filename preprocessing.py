from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from joblib import dump,load

# TODO Fill this in with actual serialization and deserialization process
model = None
dump(model, 'models/model')
model = load('models/model')

print(model)
