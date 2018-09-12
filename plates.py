import csv
import random
import re

CSV_FLDR = 'csv'
ALPHA_RE = re.compile(r"[A-Z]+")

class Plates():

    def __init__(self, dealers):
        self.dealers = dealers
        self.plates = []
        for (dealer, vat_status) in dealers:
            with open (CSV_FLDR + "/" + dealer + ".csv", 'rb') as csvFile:
                reader = csv.reader(csvFile)
                for [plate, price] in reader:
                    plateT = (plate, price, dealer, vat_status)
                    self.plates.append(plateT)
    
    def match_plate(self, matchString):
        # First try and find up to three letters in the search string
        # Want to match on letters only, if letters are provided, ignoring
        # any other letters after the first 3
        # If no letters provided match on the whole search string
        alphaMatches = ALPHA_RE.match(matchString)
        if alphaMatches:
            refinedMatch = alphaMatches.group(0)[:3]
        else:
            refinedMatch = matchString

        wholeRe = re.compile(r".*\b" + refinedMatch + "\\b")
        wholeResults = []
        for plateT in self.plates:
            if wholeRe.match(plateT[0]):
                wholeResults.append(plateT)
        return wholeResults
    
    def alphabet_list(self, alpha):
        # Only interested in plates beginning with a word
        beginRe = re.compile(r".*\b" + alpha)
        wholeRe = re.compile(r".*\b" + alpha + "\\b")
        beginResults, wholeResults = [], []
        for plateT in self.plates:
            if wholeRe.match(plateT[0]):
                wholeResults.append(plateT)
            elif beginRe.match(plateT[0]):
                beginResults.append(plateT)
        wholeResults.sort(lambda x,y: cmp(len(x[0]), len(y[0])))
        beginResults.sort(lambda x,y: cmp(len(x[0]), len(y[0])))
        return wholeResults + beginResults


