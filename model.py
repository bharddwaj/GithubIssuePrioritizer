import tensorflow as tf
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import SGDClassifier,LogisticRegression
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from preprocessing import preprocess
def run(path):
	
	X_train, X_test, X_val,y_val, y_train, y_test = preprocess(path)
	clf = LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial')
	clf.fit(X_train,y_train)
	y_pred = clf.predict(X_val)
	return accuracy_score(y_val, y_pred)


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
	run("normalized-github-issues.csv")