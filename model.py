import tensorflow as tf
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import SGDClassifier,LogisticRegression
from sklearn.svm import LinearSVC 
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from preprocessing import preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
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

def run(data):
	loaded_model = pickle.load(open('LogisticRegression.sav', 'rb'))
	tfidf3 = TfidfVectorizer(stop_words="english")
	with open('vectorizer.pickle', 'r') as f:
	 	vectorizer = pickle.load(f)
	 	data = vectorizer.transform(data)
	return loaded_model.predict(data)
	

def run2(path):
	model = tf.keras.models.Sequential([
		tf.keras.layers.Flatten(input_shape=(28, 28)), #need to change input size
		tf.keras.layers.Dense(128, activation='relu'),
		tf.keras.layers.Dropout(0.2),
		tf.keras.layers.Dense(10, activation='softmax')
	])

	model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
	X_train, X_test, X_val,y_val, y_train, y_test = preprocess(path)
	model.fit(X_train,y_train, validation_data=(X_val, y_val))
	accuracy = model.evaluate(X_test,y_test)
	return accuracy



if __name__ == "__main__":
	print(train("normalized-github-issues.csv"))
	#print(run("whatever blah blah We are taking this very seriously"))