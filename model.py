import tensorflow as tf
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC 
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from preprocessing import preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import numpy as np
def train(path):
	
	X_train, X_test, X_val,y_val, y_train, y_test = preprocess(path)
	clf = LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial')
	#clf = LinearSVC()
	clf.fit(X_train,y_train)
	y_pred = clf.predict(X_val)
	val_accuracy = accuracy_score(y_val, y_pred)
	y_pred = clf.predict(X_test)
	test_accuracy = accuracy_score(y_test, y_pred)

	filename = 'LogisticRegression.sav'
	pickle.dump(clf, open(filename, 'wb'))
	return [val_accuracy,test_accuracy]

def run_logistic_model(data):
	'''Didn't have this working for the hackathon'''
	''':data is a list of strings '''
	loaded_model = pickle.load(open('models/LogisticRegression.sav', 'rb'))
	
	
	tf1 = pickle.load(open("models/vectorizer.pickle", 'rb'))
	# Create new tfidfVectorizer with old vocabulary
	tfidf3 = TfidfVectorizer(stop_words="english",vocabulary = tf1.vocabulary_)
	transformed_data = tfidf3.fit_transform(data)
	return loaded_model.predict(transformed_data)

def run_neural_network(data):
	'''Didn't have this working for the hackathon'''
	''':data is a list of strings '''
	''' 0 = medium 1 = high 2 = medium priorities'''
	loaded_model = tf.keras.models.load_model('models/sequential_32_Dropout.h5')
	
	
	tf1 = pickle.load(open("models/vectorizer.pickle", 'rb'))
	# Create new tfidfVectorizer with old vocabulary
	tfidf3 = TfidfVectorizer(stop_words="english",vocabulary = tf1.vocabulary_)
	transformed_data = tfidf3.fit_transform(data)
	count = 0
	prediction = tf.convert_to_tensor(loaded_model.predict(transformed_data))
	print(prediction)
	return tf.math.argmax(prediction)
	

	

def train_neural_network(path):
	'''Didn't have this working for the hackathon'''
	X_train, X_test, X_val,y_val, y_train, y_test = preprocess(path)
	def change(x):
		if x == -1:
			return 2
		if x == 0:
			return 0
		if x == 1:
			return 1
	print(type(y_train))
	#neural network doesn't allow - numbers in labels so changed all -1 to 2
	y_train = np.asarray(list(map(change,y_train)))
	y_test = np.asarray(list(map(change,y_test)))
	y_val = np.asarray(list(map(change,y_val)))
	
	model = tf.keras.models.Sequential([
		tf.keras.Input(shape=(35400)), 
		tf.keras.layers.Dense(32, activation='relu'),
		tf.keras.layers.Dropout(0.2),
		tf.keras.layers.Dense(3, activation='softmax')
	])

	model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
	model.fit(X_train,y_train, validation_data=(X_val, y_val),epochs = 6)
	evaluation = model.evaluate(X_test,y_test)
	accuracy = evaluation[1]
	model.save('sequential_32_Dropout.h5')
	return accuracy



if __name__ == "__main__":
	#print(train("normalized-github-issues.csv"))
	#print(train_neural_network("normalized-github-issues.csv"))
	print(run_neural_network(["A few issues while demonstrating Manager to my grandpa on his old iPad."]))
	print(run_logistic_model(["A few issues while demonstrating Manager to my grandpa on his old iPad."]))