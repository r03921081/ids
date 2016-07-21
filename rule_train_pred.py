import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer as dv
from sklearn.cross_validation import train_test_split
from sklearn import linear_model

feature = ["dload", "is_sm_ips_ports", "synack", "sttl"]

raw_train_data = pd.read_csv("unsw/UNSW_NB15_training-set.csv", delimiter=',', encoding="utf-8-sig")

train_data = pd.DataFrame(index = raw_train_data.index, columns = feature)

for item in feature:
	train_data[item] = raw_train_data[item]

train_target = raw_train_data['label']

feature_train_data = train_data.as_matrix()
feature_train_target = train_target.as_matrix()

# NaiveBayes
model = GaussianNB()
model.fit(feature_train_data, feature_train_target)
print(model)

expected = feature_train_target
predicted = model.predict(feature_train_data)

print("NaiveBayes GaussianNB")
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))


true_positive = 0
false_positive = 0
true_negative = 0
false_negative = 0

for i in range(len(expected)):
	if expected[i] == 0 and predicted[i] == 0:
		true_positive = true_positive + 1
	elif expected[i] == 1 and predicted[i] == 0:
		false_positive = false_positive + 1
	elif expected[i] == 1 and predicted[i] == 1:
		true_negative = true_negative + 1
	else: # if expected[i] == 0 && predicted[i] == 1
		false_negative = false_negative + 1

print("")
print("Truth Table")
print(str(true_positive) + "\t" + str(false_positive))
print(str(false_negative) + "\t" + str(true_negative))
print("")

prediction_mother = true_positive + false_positive
#print(prediction_mother)
#print(true_positive)
prediction = float(true_positive) / float(prediction_mother)
print prediction

recall = float(true_positive) / (true_positive + false_negative)
print recall

predict_normal = 0
predict_abnormal = 0

for i in range(len(predicted)):
	if predicted[i] == 0:
		predict_normal = predict_normal + 1
	else:
		predict_abnormal = predict_abnormal + 1
print("")
print("Predict Normal Data: " + str(predict_normal))
print("Predict Anomaly Data: " + str(predict_abnormal))
#-----------------------------------------------------------------------------
second_index = []
for i in range(len(predicted)):
	if predicted[i] == 1: # Into next term
		second_index.append(i) # index
#print second_index

raw_discretize_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")

second_discretize_data = raw_discretize_data.ix[second_index]
second_data = raw_train_data.ix[second_index]

print ("Second Round Data: " + str(len(second_index)))
print ("Second Round %: " + str(float(len(second_index))/raw_train_data.shape[0]))
print second_discretize_data.shape
print second_data.shape

second_discretize_data.to_csv("unsw/UNSW_Discretize_Second_Turn.csv", sep=',', encoding='utf-8-sig')
second_data.to_csv("unsw/UNSW_Training_Second_Turn.csv", sep=',', encoding='utf-8-sig')

#-----------------------------------------------------------------------------
