import pandas as pd
import numpy as np
from fp_growth import find_frequent_itemsets
import operator
import random

#---------------------------------------------------------------------------------
# Initial Background

minsup = 5000
feature = 5

attack_table = ["Normal", "Reconnaissance", "Backdoor", "DoS", "Exploits", "Analysis", "Fuzzers", "Worms", "Shellcode", "Generic"]

fNormal = {}
fReconnaissance = {}
fBackdoor = {}
fDoS = {}
fExploits = {}
fAnalysis = {}
fFuzzers = {}
fWorms = {}
fShellcode = {}
fGeneric = {}
fAbnormal = {}

attack_feature = {"Normal": fNormal, "Reconnaissance": fReconnaissance, "Backdoor": fBackdoor, "DoS": fDoS, "Exploits": fExploits, "Analysis": fAnalysis, "Fuzzers": fFuzzers, "Worms": fWorms, "Shellcode": fShellcode, "Generic": fGeneric, "Abnormal": fAbnormal}

old_raw_train_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")
print(old_raw_train_data.shape)
raw_train_data = pd.DataFrame(index = old_raw_train_data.index, columns = old_raw_train_data.columns)
#print(old_raw_train_data.ix[1000])

for feature in old_raw_train_data.columns:
	#print(feature + " " + old_raw_train_data[feature])
	if feature != "attack_cat":
		raw_train_data[feature] = feature + " " + old_raw_train_data[feature]
	else:
		raw_train_data[feature] = old_raw_train_data[feature]
#print(raw_train_data.ix[1000])
#---------------------------------------------------------------------------------
# Discretize value map to category feature name

category = {}
for feature in raw_train_data.columns:
	#print(feature)
	for item in raw_train_data[feature].values:
		if item not in category:
			category[item] = feature
#---------------------------------------------------------------------------------
# Sampling

sample_num = int(raw_train_data.shape[0] * 0.1)
print sample_num
train_data = raw_train_data.loc[random.sample(list(raw_train_data.index), sample_num)]
#train_data = raw_train_data.sample(frac=0.2, replace=True)
#---------------------------------------------------------------------------------
# Compute Frequent pattern

transactions = []

for label in attack_table:
	print(label)
	temp = train_data[train_data["attack_cat"]==label]
	data = temp.drop(['attack_cat'], axis=1)
	print(data.shape)
	np_data = data.as_matrix()
	transactions = np_data.tolist()

	minsup = data.shape[0]
	#if label == "Normal":
		#minsup = int(minsup * 9 / 10)
		#print("Normal:" + str(minsup))
	if minsup < 500:
		minsup = 500
	#print(minsup)
	if label == "Generic":
		minsup = 3000
	
	#minsup = int(minsup * 9 / 10)	

	label_item = {}
	new_itemset = []
	count = 0
	num = 0
	maxsup = 0

	for itemset, sup in find_frequent_itemsets(transactions, minsup, True):
		count = count + 1
		trans_item = []
		for token in itemset:
			trans_item.append(category[token])
		str_itemset = ','.join(trans_item)
		label_item[str_itemset] = sup
		if sup > maxsup:
			maxsup = sup
	new_itemset = sorted(label_item.items(), key=operator.itemgetter(1), reverse=True)
	
	max_rule = []

	for rule in new_itemset:
		if int(rule[1]) == maxsup:
			print rule
			num = num + 1
			max_rule.append(rule[0])
		elif num < 10:
			print rule
			num = num + 1
			max_rule.append(rule[0])
#---------------------------------------------------------------------------------
# Count Feature's numbers

	for token in max_rule:
		for take_feature in token.split(","):
			#print(take_feature)
			if take_feature not in attack_feature[label]:
				attack_feature[label][take_feature] = 0
			else:
				attack_feature[label][take_feature] = int(attack_feature[label][take_feature]) + 1
			if label != "Normal":
				if take_feature not in attack_feature["Abnormal"]:
					attack_feature["Abnormal"][take_feature] = 0
				else:
					attack_feature["Abnormal"][take_feature] = int(attack_feature["Abnormal"][take_feature]) + 1
	print(attack_feature[label])
	print("Count " + str(count))

print(attack_feature)

for print_rule in attack_feature:
	print("")
	print(print_rule)
	choose_feature = sorted(attack_feature[print_rule].items(), key=operator.itemgetter(1), reverse=True)
	print(choose_feature)
#---------------------------------------------------------------------------------
# Print Results

print("")
normal_feature = attack_feature["Normal"].keys()
abnormal_feature = attack_feature["Abnormal"].keys()
print(normal_feature)
print(abnormal_feature)

print("Union")
print(list(set(normal_feature).union(set(abnormal_feature))))

print("Difference")
print("normal")
print(list(set(normal_feature).difference(set(abnormal_feature))))
print("abnormal")
print(list(set(abnormal_feature).difference(set(normal_feature))))

print("And")
print(list((set(normal_feature)&(set(abnormal_feature)))))
