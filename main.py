import sys
from pathlib import Path
import csv
from copy import deepcopy
import DataPoint

# I included some python libraries that I used to implement this, but you don't
# have to use them if you don't want to! 

#********************************************************
# THIS FILE IS WHERE YOU SHOULD WRITE YOUR CODE 
#********************************************************

# I have created two functions for you to populate. 
# 
# One is main(), which calls translate_data(). The idea is that main() requires no context to run. It is called and figures out where to go get data to translate from your file system, formats into a data dictionary (see the comment below for the format) and then passes that data into translate_data(). You need to write the code to do this! 
#
# The other is translate_data(), which takes data in the form of a dictionary and then does all the actual interpretation of the data, creating a new output file. It also returns the data it parsed so that our tests work. You need to write the code to do this! 

# We could have just given you a single main() and let you do everything yourself in one place. We chose to do it this way instead to allow you to have two types of tests: unit tests and system tests. Unit tests will just call translate_data() and provide data that it created to test your code in a whole bunch of different ways, while the system tests call main() and test your ability to do the file handling component as well.


# This function takes a data dictionary (data_to_translate) and parses it in the following ways
#   - Orders by:
#       - All Cases with a variation of "Mac" Properties as a landlord are placed
#            ahead of cases with a different landlord.
#       - Both subsets of cases ("Mac" and non-"Mac") should be ordered in     
#            ascending order.
#   - Gender tags should be updated:
#       - Any tags marked as "Female" should be converted to say: "Female (she/her)"
#       - Any tags marked as "Male" should be converted to say: "Male (he/him)"
# This function should both write this data to an output file called: "outputs/output.csv" and return the list it wrote to the caller.
def translate_data( data_to_translate ):
    pass 
    


# The majority of the work should be done in translate data. This function should
# merely grab data out of the "inputs/input.csv" file from our package and convert
# it to a data_dictionary that translate_data() can use. 
# The format should be a list of dictionary entries, each formatted like:
    # { "Case Number", ____ }
    # { "Landlord", _______ }
    # { "Gender", _________ }
    # { "Issue", __________ }
def main():
    nonMacCases = {}
    macCases = {}
    with open('inputs/input.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            caseNumber = row[0]
            if (int(caseNumber) % 9 == 0):
                continue
            while (True):
                if (caseNumber in nonMacCases.keys() or caseNumber in macCases.keys()):
                    print("Error! Duplicate Case Detected! Case #:", caseNumber)
                    caseNumber += 'a'
                else:
                    break
            issues = row[1]
            complexName = row[2]
            tag = row[3]
            landlord = row[4]
            yesNo = row[5]
            comms = row[6]
            gender = row[7]
            location = row[8]
            caseData = DataPoint.DP(caseNumber, issues, complexName, tag, landlord, yesNo, comms, gender, location)
            if 'mac' in caseData.landlord.lstrip()[0:3].lower():
                macCases[caseNumber] = caseData
            else:
                nonMacCases[caseNumber] = caseData

    sortedMacCases = dict(sorted(macCases.items(), key=lambda item: int(''.join(filter(str.isdigit, item[0])))))
    sortedNonMacCases = dict(sorted(nonMacCases.items(), key=lambda item: int(''.join(filter(str.isdigit, item[0])))))
    
    with open('outputs/output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for caseNumber in sortedMacCases.keys():
            point = macCases[caseNumber]
            writer.writerow([
                ''.join([i for i in point.caseNumber if i.isdigit()]),
                point.issues,
                #point.complexName,
                #point.tag,
                point.gender,
                point.landlord,
                #point.yesNo,
                #point.comms,
                #point.location
            ])
        for caseNumber in sortedNonMacCases.keys():
            point = nonMacCases[caseNumber]
            writer.writerow([
                ''.join([i for i in point.caseNumber if i.isdigit()]),
                point.issues,
                #point.complexName,
                #point.tag,
                point.gender,
                point.landlord,
                #point.yesNo,
                #point.comms,
                #point.location
            ])

if __name__ == '__main__':
    main()