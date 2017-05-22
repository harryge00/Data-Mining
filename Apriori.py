# FRO11987 ELE17451 ELE89019 SNA90258 GRO99222 
# GRO99222 GRO12298 FRO12685 ELE91550 SNA11465 ELE26917 ELE52966 FRO90334 SNA30755 ELE17451 FRO84225 SNA80192 
# ELE17451 GRO73461 DAI22896 SNA99873 FRO86643 
# ELE17451 ELE37798 FRO86643 GRO56989 ELE23393 SNA11465 
from itertools import combinations

SUPPORT_THRESHOLD=2
itemset=set()
transactionList=list()
count1={}
frequent_1items=set()
with open('browsing.txt', 'r') as f:
	for line in f:
		l =  line.strip().split(' ')
		transactionList.append(frozenset(l))
		for item in l:
			if item in count1:
				count1[item] += 1
			else:
				count1[item] = 1

# print transactionList
for item in count1:
	if count1[item] >= SUPPORT_THRESHOLD:
		print item, count1[item]
		frequent_1items.add(item)

# print(frequent_1items)

frequent_1items_combinationsList = list()
for x in combinations(frequent_1items, 2):
	frequent_1items_combinationsList.append(frozenset(x))


count2={}
# print(frequent_1items_combinationsList)

for item in frequent_1items_combinationsList:
	# print item
	for transaction in transactionList:
		if item.issubset(transaction):
			if item in count2:
				count2[item] += 1
			else:
				count2[item] = 1

print(count2)
res = sorted(count2.items(), key=operator.itemgetter(1))
print res[0:10]
print res[len(res)-5:len(res)]