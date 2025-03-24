class DP:
    def __init__(self, caseNumber,issues, complexName, tag, landlord, yesNo, comms, gender, location):
        self.caseNumber = caseNumber
        self.issues = issues
        self.complexName = complexName
        self.tag = tag
        self.landlord = landlord
        self.yesNo = yesNo
        self.comms = comms
        self.gender = DP.ProcessGender(gender)
        self.location = location

    def ProcessGender(gender):
        processedGender = "Female (she/her)" if (gender.strip().lower() == "female") else "Male (he/him)" if (gender.strip().lower() == "male") else gender
        return processedGender

    def __str__(self):
        return str(self.caseNumber) + ' ' + self.gender