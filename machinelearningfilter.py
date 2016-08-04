import re
import csv
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

def data_clean(table, consider, training):
    table.reverse(); table.pop(); table.reverse()
    #GET DATA IN TABLE INTO USABLE FORM
    data = []
    for line in range(len(table)):
        if table[line][HANDLE] == '' or table[line][BIO] == '':
            pass
        else:
            #determines whether or not we include influencer as separate category
            if training:
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
            if training:
                current_row.append(feature)
            data.append(current_row)

    #SPLIT DATA INTO FEATURES AND LABELS
    labels = []
    for row in data:
        labels.append(row.pop())

    #PARTITION DATA INTO TRAIN SET AND TEST SET

    return data, labels


def model(train_data, train_labels):
    clf = ensemble.RandomForestClassifier()
    clf.fit(train_data, train_labels)
    return clf

def applymodel(classifier, usernames, bios):
    table = []
    for i in len(usernames):
        table.append([])
        table[i].append(usernames[i])
        table[i].append(bios[i])

    x = data_clean(table, True, False)

    return classifier.predict(x)

def execute(usernames, bios):
    table = read_CSV(FILENAME)
    data, labels = data_clean(table, True, True)
    classifier = model(data,labels)
    return applymodel(classifier, usernames, bios)

def filter(usernames, bios, influencers = True):
    results = execute(usernames,bios)
    good = []
    for i in range(len(usernames)):
        if influencers:
            if not results[i] == 3:
                good.append(usernames[i])
        else:
            if results[i] == 1:
                good.append(usernames[i])
    return good
