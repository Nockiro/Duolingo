import json
from lschallenge import DuolingoLearnSessionChallenge
from collections import namedtuple
from pprint import pprint

class DuolingoLearnSession(object):
    def __init__(self, jsonResponseData):
        self.learnSessionData = jsonResponseData
        self.learnSessionMetaData = self.learnSessionData["metadata"]
        self.learnSessionChallengeList = self.learnSessionData["challenges"]

        self.currentLanguage = self.learnSessionMetaData["language_string"]

    def getChallenge(self, index):
        challenge = DuolingoLearnSessionChallenge(self.learnSessionChallengeList[0])
        return challenge

    def getChallengeList(self):
        return self.learnSessionChallengeList


if __name__ == '__main__':
    #user = ls_user.User("DSA975012", "sprachassist")

    #pprint(user.getLanguage)
    ls = DuolingoLearnSession(json.loads(data.getData()))
    print("Frage 1:")
    pprint(ls.getChallenge(0).getSourcePrompt())
    print("Antwortmoeglichkeiten:")
    pprint(ls.getChallenge(0).getCorrectSolutions())