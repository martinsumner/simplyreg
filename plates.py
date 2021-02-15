import csv
import random
import re
from os import listdir
from os.path import isfile, join

FILE_RE = re.compile(r"([A-Za-z0-9]+)_(NOVAT|PLUSVAT)_([0-9]+)\.(csv|CSV)")
ALPHA_RE = re.compile(r"[A-Z]+")

class Plates():

    def __init__(self, dealerFolder):
        folderListing = listdir(dealerFolder)
        onlyfiles = [f for f in folderListing if isfile(join(dealerFolder, f))]
        dealerList = []
        for dealerFile in onlyfiles:
            dealerMatch = FILE_RE.match(dealerFile)
            if dealerMatch and len(dealerMatch.groups()) == 4:
                if dealerMatch.groups()[1] == 'PLUSVAT':
                    addVat = True
                else:
                    addVat = False
                
                dealer = dealerMatch.groups()[0]
                markup = dealerMatch.groups()[2]
                dealerList.append((dealerFile, dealer, addVat, markup))
            else:
                print("Unable to load dealerFile" + repr(dealerFile))

        self.plates = []
        self.load_plates(dealerList, dealerFolder)
        print(repr(len(self.plates)) + " plates loaded from " + repr(len(onlyfiles)) + " dealer files")
        
    
    def load_plates(self, dealerList, dealerFolder):
        duplicateCheck = dict()
        for (dealerFile, dealer, addVat, markup) in dealerList:
            with open (join(dealerFolder, dealerFile), 'rb') as csvFile:
                reader = csv.reader(csvFile)
                for line in reader:
                    if len(line) == 2:
                        [plate, price] = line
                        platePrice = int(float(price.replace(',', '')) + float(markup))
                        plateT = (platePrice, addVat, dealer, dealerFile)
                        if plate in duplicateCheck:
                            logTxt = ("Ignoring duplicate plate ", " from dealer ", " duplicate found in ")
                            (dupPlatePrice, dupAddVat, dupDealer, dupDealerFile) = duplicateCheck[plate]
                            if platePrice > dupPlatePrice:
                                duplicateCheck[plate] = plateT
                                print(logTxt[0] + repr(plate) + logTxt[1] + repr(dupDealerFile) + logTxt[2] + repr(dealerFile))
                            else:
                                duplicateCheck[plate] = (dupPlatePrice, dupAddVat, dupDealer, dupDealerFile)
                                print(logTxt[0] + repr(plate) + logTxt[1] + repr(dealerFile) + logTxt[2] + repr(dupDealerFile))
                        else:
                            duplicateCheck[plate] = plateT
                    else:
                        logTxt = ("Cannot read line ", " of incorrect length for dealerFile ")
                        print(logTxt[0] + repr(line) + logTxt[1] + repr(dealerFile))
        for plate in duplicateCheck:
            (platePrice, addVat, dealer, dealerFile) = duplicateCheck[plate]
            self.plates.append((plate, repr(platePrice), repr(addVat), dealer))


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
