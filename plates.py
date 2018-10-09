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
        wholeResults.sort(lambda x,y: cmp(x[1], y[1]))
        wholeResults.sort(lambda x,y: cmp(len(x[0]), len(y[0])))
        return wholeResults
    
    def alphabet_list(self, alpha):
        # Only interested in plates beginning with a word
        bRe = re.compile(r".*\b" + alpha + "([A-Z0-9]*)")
        beginResults = []
        for plateT in self.plates:
            bReM = bRe.match(plateT[0])
            if bReM:
                beginResults.append((plateT, bReM))
        # This sorts by the part after the searched for letter in the matching 
        # plate
        # so if the plate is "A35 II" - this sorts on the "35", if it is 
        # "45 AB" it is "B", if it is "A 1" it is ""
        # the sort order says that numbers are not as important as letters 
        # (so A11 will be after AA), then it is in alphabetic order, but if 
        # there is a tie - prefer it for the letter to be in the left part not 
        # the right part of the plate
        sortedResults = sorted(beginResults, key = lambda p: (p[1].groups()[0].isdigit(), p[1].groups()[0], p[1].start(1)))
        return [i[0] for i in sortedResults]
