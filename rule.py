import pandas as pd
import numpy as np
from fp_growth import find_frequent_itemsets

minsup = 5000
feature = 5

attack_table = ["Normal", "Reconnaissance", "Backdoor", "DoS", "Exploits", "Analysis", "Fuzzers", "Worms", "Shellcode", "Generic"]

raw_train_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")
#print(raw_train_data.columns)
print(raw_train_data.shape)

category = {}
for feature in raw_train_data.columns:
	#print(feature)
	for item in raw_train_data[feature].values:
		if item not in category:
			category[item] = feature
#print(category)

train_data = raw_train_data.sample(frac=0.1, replace=True)
#print(train_data)
transactions = []

label_item = {}

for label in attack_table:
	print(label)
	temp = train_data[train_data["attack_cat"]==label]
	data = temp.drop(['attack_cat'], axis=1)
	print(data.shape)
	np_data = data.as_matrix()
	transactions = np_data.tolist()

	minsup = data.shape[0]
	if minsup < 500:
		minsup = 500
	#print(minsup)

	count = 0
	for itemset, sup in find_frequent_itemsets(transactions, minsup, True):
		label_item[itemset] = sup
		new_itemset = sorted(label_item.items(), key=operator.itemgetter(1), reverse=True)
		for i in range(10):
			print(new_itemset[i])
		#print(itemset)
		#print("ItemSet Length " + str(len(itemset)))
		#if len(itemset) == feature:
		#	new_itemset = []
		#	count = count + 1
		#	for item in itemset:
		#		print(item)
		#		new_itemset.append(category[item])
		#	print(new_itemset)
	print("Count " + str(count))
