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


