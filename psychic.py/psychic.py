import numpy as np
import re
import csv
import sklearn

#Keyword categories
STRONGKEYS = ["Financ", "Alpha", "Trader", "Trading", "Stock", "equity", "Advis", "RIA", "hedge","Fund", "Wealth","Portfolio",
              "portfolio", "CFP", "Trade", "Invest", "Asset", ]
MEDIUMKEYS = ["capital", "OTC", "executive", "CEO", "Analyst", "Fintech"]
WEAKKEYS = ["Board", "Manage", "Option", "Retail", "swing", "Chief"]

ALLKEYS = STRONGKEYS + MEDIUMKEYS + WEAKKEYS

KEYDICT = dict()
for key in ALLKEYS:
    real = key.lower()
    KEYDICT[real] = 0


FILENAME = "BLAHBLAHBLAH.csv"

#Indexes for CSV fields
HANDLE = 0
BIO = 1
FOLLOWER_COUNT = 2
FRIEND_COUNT = 3
INVESTOR = 4

#Indexes for output data fields
HANDLE_STRONG = 0
HANDLE_MEDIUM = 1
HANDLE_WEAK = 2
BIO_STRONG = 3
BIO_MEDIUM = 4
BIO_WEAK = 5
FOLLOWERS = 6
FRIENDS = 7

def findstrong(string):
    count = 0
    for word in STRONGKEYS:
        result = re.findall(word,string)
        count += len(result)
        KEYDICT[word] += len(result)
    return count

def findmedium(string):
    count = 0
    for word in MEDIUMKEYS:
        result = re.findall(word,string)
        count += len(result)
        KEYDICT[word] += len(result)
    return count

def findweak(string):
    count = 0
    for word in WEAKKEYS:
        result = re.findall(word,string)
        count += len(result)
        KEYDICT[word] += len(result)
    return count

def read_CSV(filename):
    table = []
    with open("filename", 'rU') as csvfile:
        for line in csv.reader(csvfile,dialect=csv.excel_tab, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True):
            table.append(line)
    return table

def data_clean(table):

    #GET DATA IN TABLE INTO USABLE FORM
    data = []
    for line in range(len(table)):
        current_row = []
        current_row.append(findstrong((line[HANDLE]).lower()))
        current_row.append(findmedium(line[HANDLE].lower()))
        current_row.append(findweak(line[HANDLE].lower()))
        current_row.append(findstrong(line[BIO].lower()))
        current_row.append(findmedium(line[BIO].lower()))
        current_row.append(findweak(line[BIO].lower()))
        current_row.append(data[FOLLOWER_COUNT])
        current_row.append(data[FRIEND_COUNT])
        current_row.append(data[INVESTOR])
        data.append(current_row)

    #SPLIT DATA INTO FEATURES AND LABELS
    labels = []
    for row in data:
        labels.append(row.pop())

    #PARTITION DATA INTO TRAIN SET AND TEST SET
    x_train, y_train, x_test, y_test = sklearn.cross_validation.train_test_split(data, labels, test_size = 0.25)

    return x_train, y_train, x_test, y_test

def test_algorithms(x_train, y_train, x_test, y_test):

    treeclassifier = sklearn.tree.DecisionTreeClassifier()
    kmeansclassifier = sklearn.neighbors.KNeighborsClassifier()
    svclassifier = sklearn.svm.SVC()
    centroidclassifier = sklearn.neighbors.NearestCentroid()

    classifiers = [treeclassifier,kmeansclassifier,svclassifier,centroidclassifier]
    classifiernames = ["treeclassifier","kmeansclassifier","svclassifier","centroidclassifier"]
    classifiernames.reverse()
    for method in  range(len(classifiers)):
        clf = classifiers(method)
        clf.fit(x_train,y_train)
        predictions = clf.predict(x_test)
        print("\n\nThe {} test was {} % accurate\n\n".format(classifiernames.pop(),sklearn.metrics.accuracy_score(y_test, predictions)))

if __name__ == '__main__':
    table = read_CSV(FILENAME)
    x_train, y_train, x_test, y_test = data_clean(table)
    test_algorithms(x_train, y_train, x_test, y_test)
    print(KEYDICT)