import tensorflow as tf
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
def run(data):
	#features = [data['number_of_responses'],data['length_of_issue']]
	#the below two data fields have to be imported from the GitHub Issues dataset

	#label can be 0,1,2 
	# 0 = High Priority
	# 1 = Medium Priority
	# 2 = Low Priority
	number_of_responses = 3
	length_of_issue = 2
	label = 0

