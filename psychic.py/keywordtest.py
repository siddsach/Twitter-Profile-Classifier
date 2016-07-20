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

ALLKEYS = STRONGKEYS + MEDIUMKEYS + WEAKKEYS

FILE = "EMPTY STRING"

KEYCOUNTSBIO = dict()
KEYCOUNTSHANDLE = dict()

EXCEL_BIO_INDEX = 0
EXCEL_HANDLE_INDEX = 0

def initial():
    dictionary = dict()
    for word in ALLKEYS:
        if word.lower() not in dictionary:
            dictionary[word] = 0
    return dictionary

#IMAGINE YOU HAD A READ CSV FILE THAT OUTPUTTED A LIST OF BIOS AND A LIST OF HANDLES

def read_CSV(filename):
    table = []
    with open("filename", 'rU') as csvfile:
        reader = csv.reader(csvfile,dialect=csv.excel_tab)
        for line in reader:
            example = line[0].split(",")
            table.append(example)
    return table

def output_lists(filename):
    table = read_CSV(filename)
    table.reverse(); table.pop(); table.reverse()
    biolist = []; handlelist = []
    for line in table:
        biolist.append(line[EXCEL_BIO_INDEX])
        handlelist.append(line[EXCEL_HANDLE_INDEX])
    return biolist, handlelist

BIOLIST = []
HANDLELIST = []

def counter(dictionary, list):
    for str in list:
        text = str.lower()
        for key in dictionary.keys():
            if re.search(key, text):
                dictionary[key] += 1
    return dictionary

if __name__ == '__main__':
    biolist, handlelist = reader("CSVNAME GOES HERE")
    Bio_result = counter(initial(), biolist)
    Handle_result = counter(initial(), handlelist)
    print("\n\n\n\nThese are the Bio Results\n")
    print(Bio_result)
    print("\n\n\n\nThese are the Handle Results\n")
    print(Handle_result)

