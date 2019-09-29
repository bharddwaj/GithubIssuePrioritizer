import tensorflow as tf
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import SGDClassifier,LogisticRegression
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from preprocessing import preprocess
def run(path):
	#features = [data['number_of_responses'],data['length_of_issue']]
	#the below two data fields have to be imported from the GitHub Issues dataset

	#label can be 0,1,2 
	# 0 = High Priority
	# 1 = Medium Priority
	# 2 = Low Priority
	number_of_responses = 3
	length_of_issue = 2
	label = 0
	X_train, X_test, X_val,y_val, y_train, y_test = preprocess(path)
	clf = LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial')
	clf.fit(X_train,y_train)
	y_pred = clf.predict(X_val)
	accuracy_score(y_val, y_pred)


