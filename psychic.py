import numpy as np
import re
import csv
import sklearn

#Keyword categories
STRONGKEYS = ["Financ", "financ", "alpha", "Alpha", "trader", "Trader", "trading", "Trading", "stock", "Stock", "equity",
              "Equity", "Advis", "advis", "RIA", "Hedge", "hedge","Fund", "fund", "Wealth", "wealth", "AIM", "Portfolio",
              "portfolio", "CFP", "CPF", "Index", "index"]
MEDIUMKEYS = ["Asset", "asset", "Trade", "trade", "market", "Market", "capital", "Capital", "OTC", "executive", "Executive", "CEO", "Analyst", "analyst", "invest", "Invest",]
WEAKKEYS = ["Board", "board", "manage", "Manage", "Option", "option", "fintech", "Fintech", "retail", "Retail", "swing", "Swing", "chief", "Chief"]

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
    for word in STRONGKEYS:
        if re.search(word,string):
            return True
    return False

def findmedium(string):
    for word in MEDIUMKEYS:
        if re.search(word,string):
            return True
    return False

def findweak(string):
    for word in WEAKKEYS:
        if re.search(word,string):
            return True
    return False

def read_CSV(filename):
    table = []
    with open("filename", 'rU') as csvfile:
        reader = csv.reader(csvfile,dialect=csv.excel_tab)
        for line in reader:
            example = line[0].split(",")
            table.append(example)
    return table

def data_clean(table):

    #GET DATA IN TABLE INTO USABLE FORM
    data = []
    for line in range(len(table)):
        current_row = []
        if findstrong(data[HANDLE]): current_row.append(1);
        else: current_row.append(0)
        if findmedium(data[HANDLE]): current_row.append(1);
        else: current_row.append(0)
        if findweak(data[HANDLE]): current_row.append(1);
        else: current_row.append(0)
        if findstrong(data[BIO]): current_row.append(1);
        else: current_row.append(0)
        if findmedium(data[BIO]): current_row.append(1);
        else: current_row.append(0)
        if findweak(data[BIO]): current_row.append(1);
        else: current_row.append(0)
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