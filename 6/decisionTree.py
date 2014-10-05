import sys, math, re
import cPickle as pickle
import readARFF
import random

### takes as input a list of class labels. Returns a float
### indicating the entropy in this data.
### the form: [class1, class2, class3, ..., classn]
def entropy(data) :
    #you write this
    possibleclasses = set(data)
    r = 0.0
    for class1 in possibleclasses :
        c = data.count(class1)
        r -= float(c)/len(data)*math.log(float(c)/len(data),2)
    return r


### Compute remainder - this is the amount of entropy left in the data after
### we split on a particular attribute. Let's assume the input data is of
### the form:
###    [(value1, class1), (value2, class2), ..., (valuen, classn)]
def remainder(data) :
    possibleValues = set([item[0] for item in data])
    r = 0.0
    for value in possibleValues :
        c = len([item for item in data if item[0] == value])
        r += (float(c) / len(data) ) * entropy([item[1] for item in data if item[0] == value])
    return r


### selectAttribute: choose the index of the attribute in the current 
### dataset that minimizes the remainder. 
### data is in the form [[a1, a2, ..., c1], [b1,b2,...,c2], ... ]
### where the a's are attribute values and the c's are classifications.
### and attributes is a list [a1,a2,...,an] of corresponding attribute values
def selectAttribute(data, alist) :
    #you write this
    remainder_min = float("inf")
    for i in range(len( alist ) ):
        # print alist[i]
        temp = remainder( [(item[i], item[-1]) for item in data] )
        # print temp, alist[i]
        if temp < remainder_min:
            remainder_min = temp
            best_attribute = i
    # print alist[best_attribute], remainder_min,best_attribute

    return best_attribute

    
### a TreeNode is an object that has either:
### 1. An attribute to be tested and a set of children; one for each possible 
### value of the attribute.
### 2. A value (if it is a leaf in a tree)
class TreeNode :
    def __init__(self, attribute, value) :
        self.attribute = attribute
        self.value = value
        self.children = {}
        self.defaultValue = None

    def __repr__(self) :
        if self.attribute :
            return self.attribute
        else :
            return self.value

    ### a node with no children is a leaf
    def isLeaf(self) :
        return self.children == {}

    ### return the value for the given data
    ### the input will be:
    ### data - an object to classify - [v1, v2, ..., vn]
    ### attributes - the attribute dictionary
    def classify(self, data, attributes) :
        # you write this
        attrslist = readARFF.getAttrList(attributes)
        # if self.attribute:
        #     print self.attribute
        if self.value:
            # print self.value
            return self.value
        elif data[attrslist.index(self.attribute) ] in self.children:
            i = attrslist.index(self.attribute)
            return self.children[data[i]].classify(data, attributes)
        else:
            return self.defaultValue

    def printTree(self):
        if self.attribute:
            print self.attribute,self.children
            for i in self.children:
                if self.children[i].attribute:
                    self.children[i].printTree()
                    # pass

    def pickleTree(self):
        tr = open('treeroot', 'wb')
        pickle.dump(self, tr)
            

            

### a tree is simply a data structure composed of nodes (of type TreeNode).
### The root of the tree 
### is itself a node, so we don't need a separate 'Tree' class. We
### just need a function that takes in a dataset and our attribute dictionary,
### builds a tree, and returns the root node.
### makeTree is a recursive function. Our base case is that our
### dataset has entropy 0 - no further tests have to be made. There
### are two other degenerate base cases: when there is no more data to
### use, and when we have no data for a particular value. In this case
### we use either default value or majority value.
### The recursive step is to select the attribute that most increases
### the gain and split on that.


### assume: input looks like this:
### dataset: [[v1, v2, ..., vn, c1], [v1,v2, ..., c2] ... ]
### alist: [a1,a2,...,an]
### attributes: {0:{'outlook':['sunny','overcast','rainy']},1:...}
def makeTree(dataset, alist, attributes, defaultValue) :
    # you write; See assignment & notes for description of algorithm
    # if the dataset is empty
    if len(dataset) == 0:
        # print defaultValue
        return TreeNode(None, defaultValue)
    # if the dataset contains zero entropy, that is, all classes are the same.
    # that is, the entropy is zero
    elif entropy([item[-1] for item in dataset]) == 0:
        return TreeNode(None, dataset[0][-1])
    elif len(alist) == 0:
        return TreeNode(None, readARFF.computeZeroR(dataset))
    else:
        i = selectAttribute(dataset, alist)
        # print alist,alist[i], i
        # if alist[i] == 'age':
        #     print dataset
        #     print [item[-1] for item in dataset].count(dataset[0][-1]) , len(dataset)
        #     print [item[-1] for item in dataset].count(dataset[0][-1]) == len(dataset)
        current_Treenode = TreeNode(alist[i], None)
        current_Treenode.defaultValue = readARFF.computeZeroR(dataset)
        # print i
        # print dataset
        real_index = [j for j in range(len(attributes)) if attributes[j].keys() == [alist[i]]][0]
        # print dataset,attributes[real_index].keys()[0]
        del_attribute = attributes[real_index][alist[i]]
        
        for item in del_attribute:
            sub_data = [data[:i]+data[i+1:] for data in dataset if data[i] == item]
            # print [data[i] for data in dataset],item
            # print [data[i] for data in dataset].count(item)
            # print data[i][0] == item
            # print 'sub_data', sub_data, item
            # print sub_data,item
            # for eachdata in sub_data:
            #     del eachdata[i]
            current_Treenode.children[item] = makeTree(sub_data, alist[:i]+alist[i+1:], attributes, current_Treenode.defaultValue)
        return current_Treenode
            # print sub_data
            # print attributes,alist

def calc_precision_recall_accuracy(root, attrs, testdata):
    actual_class = {}
    predicted_class = {}
    correct_class = {}

    for i in testdata:
        a = root.classify(i, attrs)

        if i[-1] in actual_class:
            actual_class[i[-1]] += 1
        else:
            actual_class[i[-1]] = 1

        if a in predicted_class:
            predicted_class[a] += 1
        else:
            predicted_class[a] = 1
        
        if a == i[-1]:
            if i[-1] in correct_class:
                correct_class[i[-1]] += 1
            else:
                correct_class[i[-1]] = 1

    # print 'actual_class %s' %actual_class
    # print 'predicted_class %s' %predicted_class
    # print 'correct_class %s' %correct_class

    correct_num = 0
    precision = {}
    recall = {}

    for j in correct_class:
        recall[j] = float(correct_class[j]) / actual_class[j]
        precision[j] = float(correct_class[j]) / predicted_class[j]
        correct_num += correct_class[j]
    for k in actual_class:
        if k not in precision:
            precision[k] = 0
        if k not in recall:
            recall[k] = 0

    return precision, recall, correct_num

def calc_precision_recall_accuracy_zeroR(testdata):
    actual_class = {}
    predicted_class = {}
    correct_class = {}
    majority = readARFF.computeZeroR(testdata)
    for i in testdata:
        a = majority

        if i[-1] in actual_class:
            actual_class[i[-1]] += 1
        else:
            actual_class[i[-1]] = 1

        if a in predicted_class:
            predicted_class[a] += 1
        else:
            predicted_class[a] = 1
        
        if a == i[-1]:
            if i[-1] in correct_class:
                correct_class[i[-1]] += 1
            else:
                correct_class[i[-1]] = 1

    # print 'actual_class %s' %actual_class
    # print 'predicted_class %s' %predicted_class
    # print 'correct_class %s' %correct_class

    correct_num = 0
    precision = {}
    recall = {}

    for j in correct_class:
        recall[j] = float(correct_class[j]) / actual_class[j]
        precision[j] = float(correct_class[j]) / predicted_class[j]
        correct_num += correct_class[j]

    for k in actual_class:
        if k not in precision:
            precision[k] = 0
        if k not in recall:
            recall[k] = 0

    return precision, recall, correct_num

def calc_average(nfold, test_precision, test_recall, test_accuracy):
    test_precision_average = {}
    test_recall_average = {}
    test_accuracy_average = 0

    precision_num = {}
    recall_num = {}

    for l in range(nfold):
        for item in test_precision[l]:
            if item in test_precision_average:
                test_precision_average[item] += test_precision[l][item]
            else:
                test_precision_average[item] = test_precision[l][item]
            if item in precision_num:
                precision_num[item] += 1
            else:
                precision_num[item] = 1

        for item in test_recall[l]:
            if item in test_recall_average:
                test_recall_average[item] += test_recall[l][item]
            else:
                test_recall_average[item] = test_recall[l][item]
            if item in recall_num:
                recall_num[item] += 1
            else:
                recall_num[item] = 1
        test_accuracy_average += test_accuracy[l]

    for item in test_precision_average:
        test_precision_average[item] /= precision_num[item]
        test_recall_average[item] /= recall_num[item]
    test_accuracy_average /= nfold
    return test_precision_average, test_recall_average, test_accuracy_average


def print_pr_re(dict1):

    print '      ',['%s:%.2f%%' %(item,dict1[item]*100 ) for item in dict1]


def evaluation(nfold , attrs, data):
    train_precision = []
    train_recall = []
    train_accuracy = []

    test_precision = []
    test_recall = []
    test_accuracy = []

    for k in range(nfold):
        random.seed()
        random.shuffle(data)
        traindata = data[:len(data)/5*4]
        # print len(traindata)
        testdata = data[len(data)/5*4:]
        # print len(testdata)
        # print data[:len(data)/10]
        attrslist = readARFF.getAttrList(attrs)
        root = makeTree(traindata, attrslist, attrs, readARFF.computeZeroR(data))
        # print '####fold####',k
        # root.printTree()

        precision, recall, correct_num = calc_precision_recall_accuracy(root, attrs, testdata)
        test_precision.append(precision)
        test_recall.append(recall)
        test_accuracy.append(float(correct_num) / len(testdata))

        precision_train, recall_train, correct_num_train = calc_precision_recall_accuracy(root, attrs, traindata)
        train_precision.append(precision_train)
        train_recall.append(recall_train)
        train_accuracy.append(float(correct_num_train) / len(traindata))

    test_precision_average, test_recall_average, test_accuracy_average = calc_average(nfold, test_precision, test_recall, test_accuracy)
    train_precision_average, train_recall_average, train_accuracy_average = calc_average(nfold, train_precision, train_recall, train_accuracy)
    print '#####   The performance of decision tree   #####'
    print '     test_precision:' 
    print_pr_re(test_precision_average)
    print '     test_recall:' 
    print_pr_re(test_recall_average)
    print '     test_accuracy: %f%%' % (test_accuracy_average*100)
    print 
    print '     training_precision:'
    print_pr_re(train_precision_average)
    print '     training_recall:'
    print_pr_re(train_recall_average)
    print '     training_accuracy: %f%%' % (train_accuracy_average*100)

def evaluation_zeroR(nfold, data):
    train_precision = []
    train_recall = []
    train_accuracy = []

    test_precision = []
    test_recall = []
    test_accuracy = []

    for k in range(nfold):
        random.seed()
        random.shuffle(data)
        traindata = data[:len(data)/5*4]
        # print len(traindata)
        testdata = data[len(data)/5*4:]
        # print len(testdata)
        # print data[:len(data)/10]
        # print '####fold####',k
        # root.printTree()

        precision, recall, correct_num = calc_precision_recall_accuracy_zeroR(testdata)
        test_precision.append(precision)
        test_recall.append(recall)
        test_accuracy.append(float(correct_num) / len(testdata))

        precision_train, recall_train, correct_num_train = calc_precision_recall_accuracy_zeroR(traindata)
        train_precision.append(precision_train)
        train_recall.append(recall_train)
        train_accuracy.append(float(correct_num_train) / len(traindata))

    test_precision_average, test_recall_average, test_accuracy_average = calc_average(nfold, test_precision, test_recall, test_accuracy)
    train_precision_average, train_recall_average, train_accuracy_average = calc_average(nfold, train_precision, train_recall, train_accuracy)



    print '#####   The performance of zeroR   #####'
    print '     test_precision:' 
    print_pr_re(test_precision_average)
    print '     test_recall:' 
    print_pr_re(test_recall_average)
    print '     test_accuracy: %f%%' % (test_accuracy_average*100)
    print 
    print '     training_precision:'
    print_pr_re(train_precision_average)
    print '     training_recall:'
    print_pr_re(train_recall_average)
    print '     training_accuracy: %f%%' % (train_accuracy_average*100)


if __name__ == '__main__' :
    # for loading the existing data set pickle 
    # pickledata = open('pickledata','rb')
    # attrs = pickle.load(pickledata)
    # data = pickle.load(pickledata)

    # for loading the new data set
    # dataset = 'tennis.arff'
    # dataset = 'restaurant.arff'
    dataset = 'breast-cancer.arff'
    # dataset = 'nursery.arff'
    # dataset = 'lymphography.arff'

    
    attrs, data = readARFF.readArff(open(dataset))
    print '#####   %s dataset   #####' %dataset
# 
    # print len(data)
    # attrslist = readARFF.getAttrList(attrs)
    # root = makeTree(data, attrslist, attrs, readARFF.computeZeroR(data))
    # root.printTree()

    evaluation(5, attrs, data)
    evaluation_zeroR(5, data)






