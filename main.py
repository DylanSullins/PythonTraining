import sys
from pathlib import Path
import csv
from copy import deepcopy

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
#       - NOTE: Mac cases are determined by the string "mac" appearing anywhere
#               in the landlord field, regardless of whether it is a Mac Properties 
#               case or not. This is intentional to follow testing requirements.
#   - Gender tags should be updated:
#       - Any tags marked as "Female" should be converted to say: "Female (she/her)"
#       - Any tags marked as "Male" should be converted to say: "Male (he/him)"
# This function should both write this data to an output file called: "outputs/output.csv" and return the list it wrote to the caller.
def translate_data( data_to_translate ):
    data_to_translate = sorted(data_to_translate, key = lambda i: int(i["Case Number"]))
    macCases = []
    nonMacCases = []
    for i in data_to_translate:
        if int(i["Case Number"]) % 9 == 0:
            continue
        gender = i["Gender"]
        i["Gender"] = "Female (she/her)" if (gender.strip().lower() == "female") else "Male (he/him)" if (gender.strip().lower() == "male") else gender
        # if 'mac' in i["Landlord"].lstrip()[0:3].lower():
        # Uncomment the above line and comment the below line to restrict to Mac Properties
        if 'mac' in i["Landlord"].lower():
            macCases.append(i)
        else:
            nonMacCases.append(i)
    data_to_translate = []
    for i in macCases:
        data_to_translate.append(i)
    for i in nonMacCases:
        data_to_translate.append(i)

    with open('outputs/output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in data_to_translate:
            writer.writerow([
                i["Case Number"],
                i["Issues"],
                i["Gender"],
                i["Landlord"]
            ])
    return data_to_translate
        
    
def read_data():
    allCases = []
    with open('inputs/input.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            allCases.append(
                {
                    "Case Number": row[0],
                    "Issues": row[1],
                    "Landlord": row[4],
                    "Gender": row[7]
                }
            )
    return allCases

# The majority of the work should be done in translate data. This function should
# merely grab data out of the "inputs/input.csv" file from our package and convert
# it to a data_dictionary that translate_data() can use. 
# The format should be a list of dictionary entries, each formatted like:
    # { "Case Number", ____ }
    # { "Landlord", _______ }
    # { "Gender", _________ }
    # { "Issue", __________ }
def main():
    allCases = read_data()
    allCases = translate_data(allCases)

if __name__ == '__main__':
    main()