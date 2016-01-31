from __future__ import division
import itertools
import operator
from sys import argv 

if argv[1]: 
    fileName = argv[1] 
else: 
	print "file name required"

print "Reading from file: ", fileName

support = 3
mappings = []
itemCounts = []  
transactions = 0  

print 'Pass 1 (counting frequent items) .....'

# Count all items
data = open(fileName,"r")
for basket in data:
    #print basket
    transactions += 1
    for item in set(basket.split()):
        #print item
        if item not in mappings:
            mappings.append(item)
            itemCounts.append(1)
        else:
            indexItem = mappings.index(item)
            counter = itemCounts[indexItem]
            counter += 1
            itemCounts[indexItem] = counter

data.close()

# Get frequent items
frequentItems = [mappings.index(item) for item in mappings \
                 if itemCounts[mappings.index(item)] >= support]
itemset1 = [mappings[index] for index in frequentItems]
print itemset1

support = 3
mappings = []
itemCounts = []  
transactions = 0  

print 'Pass 2 (counting frequent items) .....'

data = open(fileName,"r")
# Count all pairs
for basket in data:
	transactions += 1
	items = set(basket.split())
	for item in items:
		for anotherItem in items:
			if item != anotherItem and item in itemset1 and anotherItem in itemset1:
				if item < anotherItem:
					pair = [item, anotherItem]
				else:
					pair = [anotherItem, item]
				if pair not in mappings:
					mappings.append(pair)
					itemCounts.append(1)
				else:
					indexItem = mappings.index(pair)
					counter = itemCounts[indexItem]
					counter += 1
					itemCounts[indexItem] = counter

data.close()

# Get frequent items
itemset2 = [pair for pair in mappings if itemCounts[mappings.index(pair)] >= support]
print itemset2