import numpy as np
import re
import csv
import sklearn
from sklearn import cross_validation, metrics, tree, neighbors, svm, ensemble, naive_bayes, discriminant_analysis


#Keyword categories
STRONGKEYS = ["Financ", "Alpha", "Stock", "equity", "RIA", "hedge","Fund", "securities"
              "Portfolio", "PM", "CFP", "Trade", "Invest", "CIO", "wall street", "forex"]
MEDIUMKEYS = ["OTC", "Fintech", "Asset","Advis", "Advis","Wealth","Manage", "capital", "Analyst", "Asset", "Option"]
WEAKKEYS = ["Board",  "Retail", "swing", "Chief", "executive", "business", "founder", "partner", "CEO", "president", "entrepeneur", "principal"]
INFLUENCERKEYS = ["social", "communications", "marketing", "media", "editor", "blog", "write", "author"]

ALLKEYS = STRONGKEYS + MEDIUMKEYS + WEAKKEYS + INFLUENCERKEYS

KEYDICT = dict()
for key in ALLKEYS:
    real = key.lower()
    KEYDICT[real] = 0
print(KEYDICT)

FILENAME = "TrainingList.csv"

#Indexes for CSV fields
HANDLE = 1
BIO = 2
FOLLOWER_COUNT = 7
FRIEND_COUNT = 8
INVESTOR = 0

#Indexes for output data fields
HANDLE_STRONG = 0
HANDLE_MEDIUM = 1
HANDLE_WEAK = 2
BIO_STRONG = 3
BIO_MEDIUM = 4
BIO_WEAK = 5
FOLLOWERS = 6
FRIENDS = 7

CLASSIFIERS = ["Tree Classifier","K-means Classifier","SVC Classifier","Centroid Classifier", "Random Forest Classifier",
                   "Ada Boost Classifier", "Linear Discrimant Analysis", "Quadratic Discriminant Analysis", "Naive Bayes"]

def findinst(string, keys):
    count = 0
    for word in keys:
        result = re.findall(word.lower(),string)
        count += len(result)
        KEYDICT[word.lower()] += len(result)
    return count

def read_CSV(filename):
    table = []
    with open(filename, 'rU') as csvfile:
        for line in csv.reader(csvfile,dialect=csv.excel_tab, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True):
            table.append(line)
    return table

def data_clean(table, consider):
    table.reverse(); table.pop(); table.reverse()
    #GET DATA IN TABLE INTO USABLE FORM
    data = []
    for line in range(len(table)):
        if table[line][HANDLE] == '' or table[line][BIO] == '' or table[line][FOLLOWER_COUNT] == '' or table[line][FRIEND_COUNT] =='':
            pass
        else:
            #determines whether or not we include influencer as separate category
            if consider:
                feature = float(table[line][INVESTOR])
            else:
                if float(table[line][INVESTOR]) != 3: feature = 1
                else: feature = 0
            current_row = []
            current_row.append(findinst(table[line][HANDLE].lower(), STRONGKEYS) + findinst(table[line][BIO].lower(), STRONGKEYS))
            current_row.append(findinst(table[line][HANDLE].lower(), MEDIUMKEYS) + findinst(table[line][BIO].lower(), MEDIUMKEYS))
            current_row.append(findinst(table[line][HANDLE].lower(), WEAKKEYS) + findinst(table[line][BIO].lower(), WEAKKEYS))
            current_row.append(findinst(table[line][HANDLE].lower(), INFLUENCERKEYS) + findinst(table[line][BIO].lower(), INFLUENCERKEYS))
            #current_row.append(float(table[line][FOLLOWER_COUNT]))
            #current_row.append(float(table[line][FRIEND_COUNT]))
            current_row.append(feature)
            data.append(current_row)

    #SPLIT DATA INTO FEATURES AND LABELS
    labels = []
    for row in data:
        labels.append(row.pop())

    #PARTITION DATA INTO TRAIN SET AND TEST SET
    x_train, x_test, y_train, y_test = cross_validation.train_test_split(data, labels, test_size = 0.5)

    return x_train, y_train, x_test, y_test

def willa_function(x):
    output_vect = []
    for line in x:
        a = 0
        for field in line:
            if field != 0:
                a = 1
        output_vect.append(a)
    return output_vect

def test_algorithms(x_train, y_train, x_test, y_test):

    trees = tree.DecisionTreeClassifier()
    kmeans = neighbors.KNeighborsClassifier()
    svc = svm.SVC()
    centroid = neighbors.NearestCentroid()
    forest = ensemble.RandomForestClassifier()
    ada = ensemble.AdaBoostClassifier()
    lda = discriminant_analysis.LinearDiscriminantAnalysis()
    qda = discriminant_analysis.QuadraticDiscriminantAnalysis()
    bae = naive_bayes.GaussianNB()

    classifiers = [trees,kmeans,svc,centroid, forest, ada, lda, qda, bae]

    for method in  range(len(CLASSIFIERS)):
        clf = classifiers[method]
        clf.fit(x_train,y_train)
        trainpredictions = clf.predict(x_train)
        testpredictions = clf.predict(x_test)
        print("\nThe {} test was {} % accurate on test data and {} % accurate on train data\n".format(CLASSIFIERS[method], 100*metrics.accuracy_score(y_test, testpredictions), 100*metrics.accuracy_score(y_train, trainpredictions)))

    print("The Willa Function was {} % on the test data\n\n".format(100*metrics.accuracy_score(y_test, willa_function(x_test))))

if __name__ == '__main__':
    table = read_CSV(FILENAME)
    x_train, y_train, x_test, y_test = data_clean(table, False)
    test_algorithms(x_train, y_train, x_test, y_test)
    print(KEYDICT)