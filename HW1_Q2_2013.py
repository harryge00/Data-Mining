from __future__ import division
import itertools
import operator
from sys import argv 

# Read the data file
if argv[1]: 
    fileName = argv[1] 
else:
    fileName = "/Users/sa/courses/Winter12/CS246/workspace/cs246.chap2/input/p2/baskets.txt"

print "Reading from file: ", fileName

support = 99
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
                 if itemCounts[mappings.index(item)] > support]


print 'done. Processed %s lines.'%(transactions)


print 'Pass 2 (counting frequent pairs) .....'
   
# Get all candidate pairs (all combination pairs of frequent items). 
candidatePairs = {}
for pair in itertools.combinations(sorted(frequentItems),2):
    candidatePairs[pair] = 0   

# Get counts for all candidate pairs.
data = open(fileName,"r")

for basket in data:
    #print "\n",basket
    fitems  = sorted( [ mappings.index(item) for item in set(basket.split()) ] )
           
#    print fItems 
    # Generate pairs for them and update counts
    for pair in itertools.combinations(fitems,2):
        if pair in candidatePairs:
            count = candidatePairs[pair]
            count += 1
            candidatePairs[pair] = count

data.close()

# Get all frequent pairs
frequentPairs = sorted([k for k,v in candidatePairs.iteritems() if v > support])
#print frequentPairs

print 'done.'


print 'Pass 3 (counting frequent triples) ...'


# Generate candidate triples by frequentPairs JOIN frequentPairs
candidateTriples = {}
allCandidateTriples = []
for fcPair in frequentPairs:
    for jp in [joinPair for joinPair in frequentPairs \
              if joinPair[0] == fcPair[1]]:
#        print fcPair, jp
        allCandidateTriples.append( (fcPair[0],fcPair[1],jp[1]) )
  
# Prune non frequent candidate triples      
for candidate in allCandidateTriples:
    whatAboutIt = True
    for pair in itertools.combinations(candidate,2):
        if pair not in frequentPairs:
            whatAboutIt = False
            break
    if whatAboutIt:
        candidateTriples[candidate] = 0
        

# Get count for candidate triples 
data = open(fileName,"r")

for basket in data:
    items = sorted([mappings.index(item) for item in set(basket.split())])
    
    fPair = []
    for triple in itertools.combinations(items,3):
        if triple in candidateTriples:
            tripleCount = candidateTriples[triple] 
            tripleCount = tripleCount +1
            candidateTriples[triple] = tripleCount
 
data.close()

# Get frequent triples
frequentTriples = sorted ([k for k,v in candidateTriples.iteritems() if v > support])

print 'done.'


print 'Generating Rules for confidence ...'        

    
def confidence(I,J):
    # Calculate P(IJ)
    PIJ = 0
    
    IJ = set(I).union(set(J))
    
    if len(IJ) == 2:
        PIJ = candidatePairs[tuple(sorted(IJ))]
    elif len(IJ) == 3:
        PIJ = candidateTriples[tuple(sorted(IJ))]
    
    #Calculate P(I)
    PI = 0
    if len(I) == 1:
        PI = itemCounts[I[0]]
    elif len(I) == 2:
        PI = candidatePairs[tuple(sorted(I))]
    if PIJ > PI:
        print I, J, IJ
        print PIJ, PI, PIJ / PI
    
    return PIJ / PI
    
# Frequent pairs by confidence
pairRules = {}
for pair in frequentPairs:
    pairRules[pair]=confidence( (pair[0],),(pair[1],) )
    pairRules[(pair[1],pair[0])] = confidence( (pair[1],),(pair[0],) )


# Frequent triples by confidence
tripleRules = {}
for triple in frequentTriples:
    for pair in itertools.combinations(triple,2):
        item2 = tuple(set(triple).difference(set(pair)))
        tripleRules[(pair,item2)] = confidence(pair,item2)

print 'done.'

# Final o/p sort rules and get top 5 desc
cp = sorted(pairRules.iteritems(), key = operator.itemgetter(1))
cp.reverse()
cp5 = [ "%s-->%s  %s" % (mappings[rule[0][0]],mappings[rule[0][1]],rule[1])\
                                   for rule in cp[0:15] ]
print 'Top 15 pairs by confidence:'
print "\n".join(cp5)

ct = sorted(tripleRules.iteritems(), key = operator.itemgetter(1))
ct.reverse()
ct5 = [ "{%s,%s}-->%s  %s" % (mappings[rule[0][0][0]],   \
                              mappings[rule[0][0][1]], \
                              mappings[rule[0][1][0]], \
                              rule[1])\
                            for rule in ct[0:15] ]
print 'Top 15 triples by confidence:'
print "\n".join(ct5)

print 'Generating Rules for lift ...'

def lift(J,conf):
#    print J,type(J)
    if isinstance(J, tuple):
        suppJ = itemCounts[J[0]]
    else:
        suppJ = itemCounts[J]
        
    SJ = suppJ / transactions
    return conf / SJ
    
liftedPairRules = { k:lift(k[1],v) for k,v in pairRules.iteritems()}
lp = sorted(liftedPairRules.iteritems(), key = operator.itemgetter(1))
lp.reverse()
lp5 = [ "%s-->%s  %s" % (mappings[rule[0][0]],mappings[rule[0][1]],rule[1])\
                                   for rule in lp[0:15] ]  
print 'Top 15 pairs by lift:'
print "\n".join(lp5) 

liftedTripleRules = { k:lift(k[1],v) for k,v in tripleRules.iteritems()}
lt = sorted(liftedTripleRules.iteritems(), key = operator.itemgetter(1))
lt.reverse()

lt5 = [ "{%s,%s}-->%s  %s" % (mappings[rule[0][0][0]],   \
                              mappings[rule[0][0][1]], \
                              mappings[rule[0][1][0]], \
                              rule[1])\
                            for rule in lt[0:15] ]
print 'Top 15 triples by lift:'
print "\n".join(lt5)

print 'Generating Rules for conviction ...'
def conv(J,conf):
#    print J,type(J)
    if isinstance(J, tuple):
        suppJ = itemCounts[J[0]]
    else:
        suppJ = itemCounts[J]
        
    SJ = suppJ / transactions
    
    conv = float('inf')
    if not conf == 1: 
        conv = (1 - SJ)/(1 - conf)
    
    return conv
    
convictedPairRules = { k:conv(k[1],v) for k,v in pairRules.iteritems()}
convp = sorted(convictedPairRules.iteritems(), key = operator.itemgetter(1))
convp.reverse()
convp5 = [ "%s-->%s  %s" % (mappings[rule[0][0]],mappings[rule[0][1]],rule[1])\
                                   for rule in convp[0:15] ]  
print 'Top 15 pairs by conviction:'
print "\n".join(convp5)

convictedTripleRules = { k:conv(k[1],v) for k,v in tripleRules.iteritems()}
convt = sorted(convictedTripleRules.iteritems(), key = operator.itemgetter(1))
convt.reverse()

convt5 = [ "{%s,%s}-->%s  %s" % (mappings[rule[0][0][0]],   \
                              mappings[rule[0][0][1]], \
                              mappings[rule[0][1][0]], \
                              rule[1])\
                            for rule in convt[0:15] ]
print 'Top 15 triples by conviction:'
print "\n".join(convt5)

    